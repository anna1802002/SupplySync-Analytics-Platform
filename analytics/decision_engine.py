from pathlib import Path

import pandas as pd
from ortools.linear_solver import pywraplp
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA


RAW_PATH = Path("data/raw/orders.csv")
OUT_PATH = Path("data/processed/reorder_recommendations.csv")


def build_demand_forecast() -> pd.DataFrame:
    orders = pd.read_csv(RAW_PATH, parse_dates=["order_date"])
    daily = (
        orders.groupby(["sku_id", "order_date"], as_index=False)["qty_ordered"]
        .sum()
        .rename(columns={"sku_id": "unique_id", "order_date": "ds", "qty_ordered": "y"})
    )

    sf = StatsForecast(models=[AutoARIMA(season_length=7)], freq="D")
    fcst = sf.forecast(df=daily, h=14).rename(columns={"AutoARIMA": "forecast_qty"})
    return fcst


def optimize_reorder(forecast_df: pd.DataFrame) -> pd.DataFrame:
    # Simple linear program: minimize stockout penalty while capping total buy quantity.
    latest = forecast_df.groupby("unique_id", as_index=False)["forecast_qty"].mean()
    latest["target_qty"] = latest["forecast_qty"].clip(lower=0).round().astype(int)

    solver = pywraplp.Solver.CreateSolver("GLOP")
    decision_vars = {}
    for _, row in latest.iterrows():
        sku = row["unique_id"]
        decision_vars[sku] = solver.NumVar(0.0, float(row["target_qty"] * 2), f"buy_{sku}")

    solver.Add(sum(decision_vars.values()) <= float(latest["target_qty"].sum() * 1.1))
    solver.Minimize(
        sum((float(row["target_qty"]) - decision_vars[row["unique_id"]]) for _, row in latest.iterrows())
    )
    solver.Solve()

    latest["recommended_reorder_qty"] = latest["unique_id"].map(lambda s: round(decision_vars[s].solution_value()))
    return latest.rename(columns={"unique_id": "sku_id"})[
        ["sku_id", "forecast_qty", "target_qty", "recommended_reorder_qty"]
    ]


if __name__ == "__main__":
    forecast = build_demand_forecast()
    recommendations = optimize_reorder(forecast)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    recommendations.to_csv(OUT_PATH, index=False)
    print(f"Saved recommendations to {OUT_PATH}")

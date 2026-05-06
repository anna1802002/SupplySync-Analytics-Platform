from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROC = Path("data/processed")
OUT = Path("artifacts/kpi_scorecard.json")


def _safe_mean(path: Path, column: str) -> float | None:
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if column not in df.columns or df.empty:
        return None
    return float(df[column].mean())


def build_scorecard() -> dict:
    fill_rate = _safe_mean(PROC / "fill_rate.csv", "fill_rate")
    stockout = _safe_mean(PROC / "stockout_rate.csv", "stockout_rate")
    turnover = _safe_mean(PROC / "inventory_turnover.csv", "inventory_turnover")

    score = 0.0
    checks = {}
    if fill_rate is not None:
        checks["fill_rate_ok"] = fill_rate >= 0.9
        score += 35 if checks["fill_rate_ok"] else 15
    if stockout is not None:
        checks["stockout_ok"] = stockout <= 0.1
        score += 35 if checks["stockout_ok"] else 15
    if turnover is not None:
        checks["turnover_ok"] = turnover >= 1.0
        score += 30 if checks["turnover_ok"] else 10

    return {
        "kpis": {
            "avg_fill_rate": fill_rate,
            "avg_stockout_rate": stockout,
            "avg_inventory_turnover": turnover,
        },
        "checks": checks,
        "score_out_of_100": round(score, 2),
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = build_scorecard()
    OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()

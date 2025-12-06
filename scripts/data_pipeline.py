import pandas as pd
import numpy as np
from pathlib import Path

# Paths
RAW = Path("data/raw")
PROC = Path("data/processed")
PROC.mkdir(parents=True, exist_ok=True)

# Load data
inventory = pd.read_csv(RAW / "inventory.csv", parse_dates=["date"])
orders = pd.read_csv(RAW / "orders.csv", parse_dates=["order_date"])
shipments = pd.read_csv(RAW / "shipments.csv", parse_dates=["ship_date", "delivery_date"])

# ---------------- CLEANING ----------------
# remove duplicates
inventory.drop_duplicates(inplace=True)
orders.drop_duplicates(subset=["order_id"], inplace=True)
shipments.drop_duplicates(subset=["shipment_id"], inplace=True)

# sanity check: no negative qty or prices
orders = orders[orders["qty_ordered"] > 0]
orders = orders[orders["unit_price"] > 0]

# handle missing warehouse/category if any
for df in [inventory, orders, shipments]:
    df.fillna({"warehouse_id": "UNKNOWN", "category": "Unassigned"}, inplace=True)

# ---------------- INTEGRATION ----------------
# merge orders & shipments
merged = pd.merge(orders, shipments, on=["order_id", "sku_id", "warehouse_id", "region"], how="left")
merged["revenue"] = merged["qty_shipped"] * merged["unit_price"]
merged["order_to_delivery_days"] = (merged["delivery_date"] - merged["order_date"]).dt.days

# ---------------- KPI CALCULATIONS ----------------
# Inventory Turnover per SKU per warehouse
inv_turnover = (
    merged.groupby(["warehouse_id", "sku_id"])
    .agg({"revenue": "sum"})
    .reset_index()
    .merge(
        inventory.groupby(["warehouse_id", "sku_id"])
        .agg({"on_hand": "mean"})
        .reset_index(),
        on=["warehouse_id", "sku_id"],
        how="left",
    )
)
inv_turnover["inventory_turnover"] = inv_turnover["revenue"] / (inv_turnover["on_hand"] * np.mean(orders["unit_price"]))
inv_turnover.to_csv(PROC / "inventory_turnover.csv", index=False)

# Stockout Rate (days with backorder > 0)
stockout_rate = (
    inventory.assign(stockout=(inventory["backorder"] > 0).astype(int))
    .groupby(["warehouse_id", "sku_id"])
    .agg(stockout_days=("stockout", "sum"), total_days=("date", "nunique"))
    .reset_index()
)
stockout_rate["stockout_rate"] = stockout_rate["stockout_days"] / stockout_rate["total_days"]
stockout_rate.to_csv(PROC / "stockout_rate.csv", index=False)

# Lead Time Variance per SKU
lead_time_var = (
    shipments.groupby(["warehouse_id", "sku_id"])
    .agg(mean_lead_time=("lead_time_days", "mean"), lead_time_variance=("lead_time_days", "std"))
    .reset_index()
)
lead_time_var.to_csv(PROC / "lead_time_variance.csv", index=False)

# Fill Rate = shipped_qty / ordered_qty
fill_rate = (
    merged.groupby(["warehouse_id", "sku_id"])
    .agg(total_ordered=("qty_ordered", "sum"), total_shipped=("qty_shipped", "sum"))
    .reset_index()
)
fill_rate["fill_rate"] = fill_rate["total_shipped"] / fill_rate["total_ordered"]
fill_rate.to_csv(PROC / "fill_rate.csv", index=False)

# Combined summary
summary = inv_turnover[["warehouse_id", "sku_id", "inventory_turnover"]].merge(
    stockout_rate[["warehouse_id", "sku_id", "stockout_rate"]], on=["warehouse_id", "sku_id"], how="left"
)
summary = summary.merge(lead_time_var, on=["warehouse_id", "sku_id"], how="left")
summary = summary.merge(fill_rate[["warehouse_id", "sku_id", "fill_rate"]], on=["warehouse_id", "sku_id"], how="left")
summary.to_csv(PROC / "supply_chain_summary.csv", index=False)

print("✅ Data cleaning & KPI files saved to data/processed/")

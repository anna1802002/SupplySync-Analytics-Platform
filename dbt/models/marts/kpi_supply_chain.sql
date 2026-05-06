with summary as (
    select *
    from read_csv_auto('../../data/processed/supply_chain_summary.csv', header=true)
),
fill_rate as (
    select *
    from read_csv_auto('../../data/processed/fill_rate.csv', header=true)
),
lead_time as (
    select *
    from read_csv_auto('../../data/processed/lead_time_variance.csv', header=true)
),
stockout as (
    select *
    from read_csv_auto('../../data/processed/stockout_rate.csv', header=true)
)
select
    s.warehouse_id,
    s.sku_id,
    s.inventory_turnover,
    s.stockout_rate,
    s.mean_lead_time,
    s.lead_time_variance,
    f.fill_rate
from summary s
left join fill_rate f
    on s.warehouse_id = f.warehouse_id
    and s.sku_id = f.sku_id
left join lead_time l
    on s.warehouse_id = l.warehouse_id
    and s.sku_id = l.sku_id
left join stockout so
    on s.warehouse_id = so.warehouse_id
    and s.sku_id = so.sku_id

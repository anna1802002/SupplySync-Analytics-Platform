import os
import subprocess
from pathlib import Path

from dagster import Definitions, ScheduleDefinition, job, op


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_DIR = PROJECT_ROOT / "dbt"
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "data_pipeline.py"


@op
def run_python_kpi_pipeline() -> None:
    subprocess.run(["python", str(SCRIPT_PATH)], check=True)


@op
def run_dbt_build() -> None:
    env = os.environ.copy()
    env.setdefault("DBT_PROFILES_DIR", str(DBT_DIR))
    subprocess.run(["dbt", "build", "--project-dir", str(DBT_DIR)], check=True, env=env)


@job
def supplysync_daily_job():
    run_dbt_build(run_python_kpi_pipeline())


daily_schedule = ScheduleDefinition(
    job=supplysync_daily_job,
    cron_schedule="0 7 * * *",
)


defs = Definitions(
    jobs=[supplysync_daily_job],
    schedules=[daily_schedule],
)

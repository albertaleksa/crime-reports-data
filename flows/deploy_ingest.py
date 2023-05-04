import argparse
import json

from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment, run_deployment
from ingest import parent_flow


def deploy(name: str, params: dict, **kwargs):
    cron_value = kwargs.get("cron", None)

    if cron_value is None:
        subflow_name = name
    else:
        subflow_name = f"schedule-{name}"
    deployment = Deployment.build_from_flow(
        flow=parent_flow,
        name=subflow_name,
        work_queue_name="default",
        schedule=CronSchedule(cron=f"{cron_value}") if cron_value else None,
        parameters=params,
    )
    deployment.apply()

    if cron_value is None:
        run_deployment(name=f"parent-flow/{subflow_name}", timeout=10)


def main(args):
    name = args.name
    params = json.loads(args.params)
    cron = args.cron

    deploy(name, params, cron=cron)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to GCS')
    parser.add_argument('--name', required=True, help='Flow name')
    parser.add_argument('--params', required=True, help='Flow parameters')
    parser.add_argument('--cron', required=False, help='Set schedule to run the command')

    args = parser.parse_args()
    main(args)

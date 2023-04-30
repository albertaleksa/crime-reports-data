import argparse
from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment, run_deployment
from ingest import parent_flow

def deploy(name: str, **kwargs):
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
    )
    deployment.apply()

    if cron_value is None:
        run_deployment(name=f"parent-flow/{subflow_name}", timeout=10)


def main(args):
    name = args.name
    cron = args.cron

    deploy(name, cron=cron)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to GCS')
    parser.add_argument('--name', required=True, help='Flow name')
    parser.add_argument('--cron', required=False, help='Set schedule to run the command')

    args = parser.parse_args()
    main(args)

from typing import OrderedDict
import subprocess
import requests
import concurrent.futures
from datetime import datetime, date, timedelta
from dateutil import parser
import json


def run(command):
    proc = subprocess.run(command, capture_output=True, text=True)
    try:
        proc.check_returncode()  # raise exception on nonz-ero return code
    except subprocess.CalledProcessError as e:
        print(f"\n---- STDERR ----\n{proc.stderr}")
        print(f"\n---- STDOUT ----\n{proc.stdout}")
        raise e

    return proc


def get_files_by_date(date):
    files_cmd = [
        "aws",
        "s3api",
        "list-objects-v2",
        "--bucket",
        "dl-batch-logs",
        "--query",
        f"Contents[?LastModified>=`{date}`]",
        "--output",
        "json",
        "--no-paginate",
    ]
    return run(files_cmd)


def get_exit_code(url):
    return requests.get(url, timeout=10).content


def create_log(logs, log_times, log_date, key, val):
    parent_dict = logs
    date_dict = parent_dict.setdefault(log_date, {})
    log_dict = date_dict.setdefault(key, {})

    log_dict["exit_code"] = val
    log_dict["time"] = log_times[key]
    log_dict["stdout_url"] = (
        "https://dl-batch-logs.s3.eu-west-2.amazonaws.com/"
        + f"{log_date}/{key}/stdout.log"
    )
    log_dict["stderr_url"] = (
        "https://dl-batch-logs.s3.eu-west-2.amazonaws.com/"
        + f"{log_date}/{key}/stderr.log"
    )


def order_logs(logs):
    logs = OrderedDict(sorted(logs.items(), reverse=True))
    for date, log_items in logs.items():
        logs[date] = OrderedDict(
            sorted(log_items.items(), key=lambda x: x[1]["time"], reverse=True)
        )

    return logs


def get_log_statuses():
    logs = {}
    two_weeks_ago = str(date.today() - timedelta(days=14))
    output = get_files_by_date(two_weeks_ago)
    json_output = json.loads(output.stdout)
    log_times = {}
    for log in json_output:
        log_times["/".join(log["Key"].split("/")[-3:-1])] = datetime.fromisoformat(
            log["LastModified"]
        ).time()

    return_code_urls = [
        "https://dl-batch-logs.s3.eu-west-2.amazonaws.com/{}".format(item["Key"])
        for item in json_output
        if item["Key"].endswith("exit_code.log")
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url = {
            executor.submit(get_exit_code, url): url for url in return_code_urls
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                exit_code = int(data.decode("utf-8"))
                log_date = url.split("/")[-4]
                key = "/".join(url.split("/")[-3:-1])
                create_log(logs, log_times, log_date, key, exit_code)
            except Exception as exc:
                print("%r generated an exception: %s" % (url, exc))
    logs = order_logs(logs)

    return logs

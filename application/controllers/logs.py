from typing import DefaultDict, OrderedDict
import boto3
import time
from datetime import datetime


client = boto3.client('logs')

def get_errored_runs():
    last_thirty_epoch = int(time.time() - 3600*24*30)
    logGroupName = '/aws/batch/job'
    filterPattern = 'make Error'
    logStreamNamePrefix="dl-batch-def"

    response = client.filter_log_events(
        logGroupName=logGroupName,
        logStreamNamePrefix=logStreamNamePrefix,
        startTime=last_thirty_epoch,
        filterPattern=filterPattern
    )

    events = response['events']

    while 'nextToken' in response.keys():
        currentToken = response['nextToken']
        
        response = client.filter_log_events(
                    logGroupName = logGroupName,
                    logStreamNamePrefix=logStreamNamePrefix,
                    nextToken = currentToken,
                    startTime=last_thirty_epoch,
                    filterPattern=filterPattern
                )

        events = events + response['events']


    logs = {}
    for item in events:
        if item["logStreamName"] in logs:
            logs[item["logStreamName"]]["events"].append(item)
        else:
            logs[item["logStreamName"]] = {
                "events" : [item],
                "time" : item["timestamp"]
            }
    logs = OrderedDict(sorted(logs.items(), key=lambda x: x[1]['time'], reverse=True))
    return logs

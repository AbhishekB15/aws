import csv

import time

import traceback

from datetime import datetime, timedelta

import boto3

import os

 

start_time_str = os.environ['START_TIME']

end_time_str = os.environ['END_TIME']

cloudwatch_query = os.environ['CLOUDWATCH_QUERY']

time_delta = float(os.environ['TIMEDELTA'])

 

print(f'Query is: {cloudwatch_query}')

 

def process_results(starttime, endtime):

    try:

        cw_client = boto3.client('logs')

 

        # select your interval, according to which you want to divide your time interval into

        interval = timedelta(minutes=time_delta)

 

        count = 0

        with open('query' + '_results.csv', mode='a') as file:

            writer = csv.writer(file)

           periods = []

            writer.writerow(['name'])

            period_start = starttime

            while period_start < endtime:

                period_end = min(period_start + interval, endtime)

                print(period_end)

                periods.append((period_start, period_end))

                logs = get_logs_for_query(cw_client, "", period_start, period_end)

                logs = logs['results']

                for log in logs:

                    print(log)

                    writer.writerow([log[0]['value']+','+log[1]['value']])

                    count = count+1

                period_start = period_end

        print(count)

 

    except Exception as e:

        print("Something went wrong with account: ")

        print("Error: " + str(e))

        traceback.print_exc()

 

def get_logs_for_query(logs_client, query_str, start_time, end_time):

    response = logs_client.start_query(logGroupName='/aws/containerinsights/<EKS-CLUSTER-NAME>/application',

                                      startTime=int(start_time.timestamp()),

                                      endTime=int(end_time.timestamp()),

                                      queryString=cloudwatch_query,

                                      limit=10000

                                      )

    print(response)

    query_id = response['queryId']

    final_response = None

 

    while final_response is None or final_response['status'] == 'Running':

        print('Waiting for query to complete ...')

        time.sleep(1)

        final_response = logs_client.get_query_results(

            queryId=query_id

        )

    print(final_response)

    return final_response

 

def main():

    # start and endtime of the log insights query that you want to divide into smaller intervals

    # NOTE: Please provide the time in UTC timezone

    starttime = datetime.fromisoformat(start_time_str)

    endtime = datetime.fromisoformat(end_time_str)

    process_results(starttime, endtime)

 

if _name_ == '_main_':

    main()
# Python script for fetching cloudwatch logs bypassing the 10k limit

There is a limitation in AWS CloudWatch for fetching 10K records from a single query execution.

This script will help in fetching logs greater than 10K records. You need to specify the timedelta in minutes for fetching the logs in chunks.

This script is testing for EKS log group and can be used for other log groups as well.
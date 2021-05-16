import os
import json
import boto3

s3 = boto3.client('s3', 'eu-central-1')

def get_current():
    response = s3.get_object(
        Bucket=os.environ['BUCKET'],
        Key=os.environ['BASE_PATH'] + 'current.json'
    )
    data = json.loads(response['Body'].read().decode('utf-8'))
    return data

def upload(data):
    s3.put_object(
        Body=json.dumps(data),
        Bucket=os.environ['BUCKET'],
        Key=os.environ['BASE_PATH'] + 'current.json'
    )



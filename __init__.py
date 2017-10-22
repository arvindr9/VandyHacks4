import boto3
import os

ml_client_connection = boto3.client(
    'machinelearning',
    aws_access_key_id = 'YOUR_AWS_ACCESS_KEY',
    aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY',
    region_name = 'us-east-1'
)

import boto3

def get_sqs_from_settings():
    return boto3.client('sqs'),boto3.resource('sqs')

from_settings = get_sqs_from_settings




# response = boto3.client('sqs').send_message(
#     QueueUrl='https://sqs.cn-north-1.amazonaws.com.cn/006685339268/spy-ctrip-price',
#     MessageBody='string',
# )

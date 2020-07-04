import json
import boto3
import ast
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    city_data = event['Records'][0]['s3']['object']['key']
    
    s3_client = boto3.client('s3')
    
    json_data = s3_client.get_object(Bucket=bucket,Key=city_data)
    
    jsonFileReader = json_data['Body'].read()
    
    json_city = jsonFileReader.decode('utf-8')
    
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    
    print('Inserting data in the table')
    
    table = dynamodb.Table('covid19citydata')
    
    dic = ast.literal_eval(json_city)
    
    for i in dic:
        try:
            resp = table.put_item(Item=i)
            print(resp)
        except ClientError as e:
            print(' Skipped due to exception ', e.response['Error']['Code'])
            print(' Reason ', e.response['Error']['Message'])
    
    
    return {
        'body': "done"
    }
import os
import json
import boto3
import datetime
from elasticsearch import Elasticsearch
from dynamodb_json import json_util as dynamo_json

es = Elasticsearch([os.environ['ES_DOMAIN']])
dynamodb = boto3.client('dynamodb')


"""
   Adds user request to the DB, return fail  
"""
def submitProfile(event, context):
    event_body = json.loads(event['body'])
    dynamo_item = dynamo_json.dumps({
            'username': event_body['username'],
            'selected_type': event_body['selected_type'],
            'requested_at': str(datetime.datetime.now())
        })

    try:
        res = dynamodb.put_item(
                TableName=os.environ['DYNAMO_TABLE_NAME'],
                Item=json.loads(dynamo_item),
                ConditionExpression='attribute_not_exists(username)'
                )
    except Exception as e: # V2: enhance cancel for different response
        print(e)
        response = {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "message": "Something went wrong on our end"    
            })
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "message": "Profile successfully updated"    
            })
        }
    
    return response



"""
    Get user profile based on Id
"""
def getProfile(event, context):
    req_username = event['queryStringParameters']['username']

    try:
        res_dynamo = dynamodb.get_item(
            TableName=os.environ['DYNAMO_TABLE_NAME'],
            Key={
                    'username': {
                        'S': req_username
                    }
                }
            )

        res_body = dynamo_json.loads(res_dynamo['Item'])
    except Exception as e:
        print(e)
        response = {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "message": "Something went wrong on our end"    
            })
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(res_body)
        }

    return response


"""
    Trigger ElasticSearch to find result
"""
def searchForProfile(event, context):
    req_username = json.loads(event['body'])

    try:
        es_body = {
            "query": {
                "match_all": {} # TODO: update search
            }    
        }
        res = es.search(index="garuda_hacks_2020", body=es_body)

        res_body = []
        for hit in res['hits']['hits']:
            res_body.append(hit["_source"])
    except Exception as e:
        print(e)
        response = {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "message": "Something went wrong on our end"    
            })
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(res_body)
        }

    return response

import json
import boto3
import datetime

dynamodb = boto3.client('dynamodb')


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response



"""
   Adds user request to the DB, return fail  
"""
def submitProfile(event, context):
    event_body = json.loads(event['body'])
    dynamo_item = {
        'username': {
            'S': event_body['username']
        },
        'selected_type': {
            'SS': event_body['selected_type']
        },
        'posts': {
            'L': []    
        },
        'requested_at': {
            'S': str(datetime.datetime.now())
        }
    }

    """
        Potential new fields:
            location (as mapping)
            tags (from ML)
    """

    try:
        res = dynamodb.put_item(
                table_name='', # TODO: add table name
                Item=dynamo_item,
                ConditionExpression='attribute_not_exists(username)'
                )
    except: # TODO: enhance cancel for different response
        response = {
            "statusCode": 502,
            "body": {
                "message": "Something went wrong on our end"    
            }
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    
    return response



"""
    Get user profile based on Id
"""
def getProfile(event, context):
    # TODO: potentially we do query call instead
    req_username = json.loads(event['body'])

    try:
        res_dynamo = dynamodb.get_item(
            table_name='', # TODO: add table name
            key={
                    'username': {
                        'S': req_username
                    }
                }
            )
        # TODO: convert to response
        res_body = {
            'username': '',
            'selected_type': [],
            'posts': []
        }
    except:
        response = {
            "statusCode": 502,
            "body": {
                "message": "Something went wrong on our end"    
            }
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(res_body)
        }

    return response


"""
    Trigger ElasticSearch to find result
"""
def searchForProfile(event, context):
    # TODO: potentially we do query call instead
    req_username = json.loads(event['body'])

    # TODO: call ES to query for result.

    response = {
        "statusCode": 200,
        "body": json.dumps({})
    }

    return response

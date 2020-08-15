import json
import boto3
import os
from elasticsearch import Elasticsearch
from inscrawler import InsCrawler
from inscrawler.settings import settings
from dynamodb_json import json_util as dynamo_json

ins_crawler = InsCrawler()
dynamodb = boto3.client('dynamodb')
es = Elasticsearch([os.environ['ES_DOMAIN']])


"""
    Triggered when DynamoHook exist and crawl website
"""
def crawlUserProfile(event, context):
    event_details = json.loads(json.dumps(event['Records'][0]['dynamodb']))
    
    converted_table = dynamo_json.loads(event_details['NewImage'])
    username = converted_table['username']
    
    crawled_username = ins_crawler.get_user_profile(username)
    setattr(settings, "fetch_details", True)
    crawled_media = ins_crawler.get_user_posts(username, number=1)

    captions = [] # timestamp is missing from crawl
    locations = []

    for post in crawled_media:
        captions.append({
            "postid": post['key'].split('/')[-2],
            "text": post['description']
        })

        if post.get("location") and post["location"] not in locations:
            locations.append(post["location"])

    payload = {
        "username": username,
        "selected_type": converted_table['selected_type'],
        "name": crawled_username['name'],
        "desc": crawled_username['desc'],
        "posts": captions,
        "locations": locations
    }

    # Ideally we want this as another lambda to maintain single responsibility
    # but no time to mess with AWS permissions
    updateDataResource(payload)

    return {
        "message": "success"    
    }


"""
    Update resources with data
"""
def updateDataResource(payload):

    dynamo_req = dynamo_json.dumps(payload)

    res_dynamo = dynamodb.put_item(
            #TableName=os.environ['DYNAMO_TABLE_NAME'],
            TableName='garuda_hacks_2020_table',
            Item=json.loads(dynamo_req)
            )

    res_es = es.index(index="garuda_hacks_2020", 
                      id=payload['username'],
                      body=payload)

    _generateSiteMapXML(payload)

    return {
        "message": "success"    
    }


"""
    Ideally we create an XML and upload it to CDN.
    but since we are using bubble.io (free), capability is not available

    another option would be updating database and have a job that would generate new xml.
"""
def _generateSiteMapXML(payload):
    # V2: complete function (https://pymotw.com/2/xml/etree/ElementTree/create.html)
    """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
            xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
            
            <url>
                <loc>OUR_WEBSITE_URL/username</loc>
                <lastmod>todays_date</lastmod>
            </url>
        
        </urlset>
    """
    print("do nothing for now")
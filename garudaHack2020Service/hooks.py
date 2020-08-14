import json
import boto3
from xml.dom import minidom
from elasticsearch import Elasticsearch
from inscrawler import InsCrawler
from inscrawler.settings import settings

ins_crawler = InsCrawler()
dynamodb = boto3.client('dynamodb')
es = Elasticsearch(['HOST'])

"""
    Triggered when DynamoHook exist and crawl website
"""
def crawlUserProfile(event, context):
    event_details = json.loads(json.dumps(event['Records'][0]['dynamodb']))

    username = event_details['NewImage']['username']['S']
    
    crawled_username = ins_crawler.get_user_profile(username)
    setattr(settings, "fetch_details", True)
    crawled_media = ins_crawler.get_user_posts(username, number=10)

    caption = [] # timestamp is missing from crawl
    locations = []

    for post in crawled_media:
        captions.append({
            "postid": post['key'].split('/')[-2],
            "text": post['description']
        })

        if post["location"] and post["location"] not in locations:
            locations.append(post["location"])

    payload = {
        "name": crawled_username['name'],
        "desc": crawled_username['desc'],
        "posts": captions,
        "locations": locations
    }

    return {
        "message": "success"    
    }


"""
    Update resources with data
"""
def updateDataResource(event, context):

    res_dynamo = dynamodb.update_item(
            table_name=os.environ['DYNAMO_TABLE_NAME'],
            key={
                    'username': {
                        'S': req_username
                    }
                },
            AttributeUpdates={} # TODO: convert event to attribute update
            )

    res_es = es.index(index="test-index", 
                      id=1, # get from event
                      body=doc) # generate from doc

    _generateSiteMapXML(payload)

    return {
        "message": "success"    
    }


def _generateSiteMapXML(payload):
    # TODO: complete function (https://pymotw.com/2/xml/etree/ElementTree/create.html)
    root = minidom.Document()

    xml = root.create('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" ' +
                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + 
                    'xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 ' +
                    'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"></urlset>')

    """
        sitemap.root()
                    .ele('url')
                        .ele('loc').txt('http://customkicks.nabilsutjipto.me/artist/' + profile.username).up()
                        .ele('lastmod').txt(new Date().toISOString()).up()
                    .up()
    """
    print("nothing")
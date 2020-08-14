"""
    Triggered when DynamoHook exist and crawl website
"""
def crawlUserProfile(event, context):
    return {
        "message": "success"    
    }


"""
    Triggered when a page is crawled and update
    dynamo + post to ES
"""
def crawlUserProfile(event, context):
    return {
        "message": "success"    
    }
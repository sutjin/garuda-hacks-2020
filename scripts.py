"""
    This file reserved for scripts to automate creations
"""
import os
from elasticsearch import Elasticsearch


def generateESIndex():
    es = Elasticsearch([os.environ['ES_DOMAIN']])

    # we are doing a plain creation for now
    # ideally we optimized mapping based on ES types
    es.indices.create(index='garuda_hacks_2020')


if __name__ == "__main__":
    generateESIndex()
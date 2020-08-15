"""
    This file reserved for scripts to automate creations
"""
import os
from elasticsearch import Elasticsearch


def generateESIndex():
    es = Elasticsearch(['https://9dhfzwk724:49bt6kh1nt@custom-kicks-sandbox-1191858573.us-west-2.bonsaisearch.net:443'])

    # we are doing a plain creation for now
    # ideally we optimized mapping based on ES types
    es.indices.create(index='garuda_hacks_2020')


if __name__ == "__main__":
    generateESIndex()
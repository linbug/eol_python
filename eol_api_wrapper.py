from urllib.request import urlopen
from io import BytesIO
import json
import random
from PIL import Image
import os
import pickle
import re
import math
import time

class API(object):
    '''Basic methods for searching API and pinging'''

    @staticmethod
    def _get_url(url):
        '''get json page data using a specified eol API url'''
        response = urlopen(url)
        data = str(response.read().decode('utf-8'))
        page = json.loads(data)
        return page

    @staticmethod
    def _bool_converter(string):
        _bool_dict = {True: 'true', False:'false'}
        return _bool_dict[string]

    @staticmethod
    def ping():
        '''Check whether the API is working'''
        url = "http://eol.org/api/ping/1.0.json"
        ping = API._get_url(url)
        return ping['response']['message']

    def __repr__(self):
        return("SOMESTUFF")

class Page(object):
    '''Takes an EOL identifier and returns a dictionary of information about that page.
    Use kwargs to set other attributes'''

    def __init__(self, id, images = 2, videos = 0, sounds = 0, \
                maps = 0, text = 2, iucn = False, subjects = 'overview', \
                licences = 'all', details = True, common_names = True, \
                synonyms = True, references = True, vetted = 0):


        attributes = [id, images, videos, sounds, maps, text, API._bool_converter(iucn),\
                         subjects, licences, _bool_converter[details], API._bool_converter(common_names), API._bool_converter(synonyms),\
                          API._bool_converter(references), vetted]

        ##Do a bunch of checks here to make sure the inputs are in the right format

        # attributes = {"id":id, "images":images, "videos":videos, "sounds":sounds, "maps":maps, "text":text, "iucn":iucn_converter[iucn],\
        #                  "subjects": subjects, "licences": licences, "details": details, "common_names": common_names, "synonyms": synonyms,\
        #                   references, \
        #                 vetted, format}
        self.id = id

        url = (
            "http://eol.org/api/pages/1.0/{0}.json?images={1}&videos={2}&sounds={3}"
            "&maps={4}&text={5}&iucn={6}&subjects={7}&licenses={8}&details={9}&common_names={10}"
            "&synonyms={11}&references={12}&vetted={13}&cache_ttl=".format(*attributes)
            )

        page = API._get_url(url)

        self.scientific_name = page["scientificName"]
        self.richness_score = page["richness_score"]
        self.synonyms = page["synonyms"]
        self.common_names = page["vernacularNames"]
        self.references = page["references"]
        self.taxon_concepts = page["taxonConcepts"]
        self.data_objects = page["dataObjects"]

class Search(object):
    '''Searches the EOL database with the string you supply'''

    def __init__(self, q, page = 1, exact = False, filter_by_taxon_concept_id = '', filter_by_hierarchy_entry_id = '',
        filter_by_string = '', cache_ttl = ''):


        attributes = [q,page,API._bool_converter(exact),filter_by_taxon_concept_id, filter_by_hierarchy_entry_id, filter_by_string,cache_ttl ]
        ##Do checks


        url = (
            "http://eol.org/api/search/1.0.json?q={0}&page={1}&exact={2}&filter_by_taxon_concept_id={3}"
            "&filter_by_hierarchy_entry_id={4}&filter_by_string={5}&cache_ttl={6}".format(*attributes))

        search = API._get_url(url)

        self.q = q
        self.total_results = search["totalResults"]
        self.startIndex = search["startIndex"]
        self.items_per_page = search["itemsPerPage"]

        if page!= 'all':
            print("getting just 30 items")
            self.results = search["results"]
            self.first = search["first"]
            self.self = search["self"]
            self.last = search["last"]
            try:
                self.next = search["next"]
            except KeyError:
                pass
        else:
            self.results = []
            for page in range(1,math.ceil(self.total_results/30)+1):
                print("pinging page {}".format(page))
                attributes = [q,page,API._bool_converter(exact),filter_by_taxon_concept_id, filter_by_hierarchy_entry_id, filter_by_string,cache_ttl ]
                url = (
                "http://eol.org/api/search/1.0.json?q={0}&page={1}&exact={2}&filter_by_taxon_concept_id={3}"
                "&filter_by_hierarchy_entry_id={4}&filter_by_string={5}&cache_ttl={6}".format(*attributes))

                search = API._get_url(url)
                # try:
                self.results+=search["results"]
                # self.previous = search["previous"]
                self.first = search["first"]
                # self.self = search["self"]
                self.last = search["last"]
                # except Exception:
                #     print("You got an exception!"   )

class Collections(object):
    '''Returns all metadata about the collection and the items it contains'''

    def __init__(self, id, page = 1, per_page = 50, filter = 'none', sort_by='recently_added', sort_field='', cache_ttl=''):

        attributes = [id,page,per_page,filter, sort_by, sort_field, cache_ttl]
        url = ("http://eol.org/api/collections/1.0/{}.json?page={}&per_page={}&filter={}&sort_by={}&sort_field={}&cache_ttl={}".format(*attributes))
        collection = API._get_url(url)
        self.name = collection["name"]
        self.description = collection["description"]
        self.created = collection["created"]
        self.modified = collection["modified"]
        self.total_items = collection["total_items"]
        self.item_types = collection["item_types"]
        self.collection_items = collection["collection_items"]

class DataObjects(object):
    '''Given the identifier for a data object this API will return all metadata about the object as submitted to EOL by the contributing content partner'''

        def __init__(self, id, cache_ttl=''):
            attributes = [id, cache_ttl]

            url = "http://eol.org/api/data_objects/1.0/{}.json?cache_ttl={}".format(*attributes)
            data_object = API._get_url(url)
            self.identifier = id
            self.scientific_name = data_object["scientificName"]
            self.exemplar = data_object["exemplar"]
            self.richness_score = data_object["richness_score"]
            self.synonyms = data_object["synonyms"]
            self.data_objects = data_object["dataObjects"]
            self.references = data_object["references"]















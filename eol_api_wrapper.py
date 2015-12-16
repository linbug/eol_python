from urllib.request import urlopen
from io import BytesIO
import json
import random
from PIL import Image
import os
import pickle
import re

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
    def __bool_converter(string):
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
        attributes
        url = (
            "http://eol.org/api/pages/1.0/{0}.json?images={1}&videos={2}&sounds={3}"
            "&maps={4}&text={5}&iucn={6}&subjects={7}&licenses={8}&details={9}&common_names={10}"
            "&synonyms={11}&references={12}&vetted={13}&cache_ttl=".format(*attributes))

        page = API._get_url(url)

        self.scientific_name = page["scientificName"]
        self.richness_score = 86.9941
        self.synonyms = page["synonyms"]
        self.common_names = page["vernacularNames"]
        self.references = page["references"]
        self.taxon_concepts = page["taxonConcepts"]
        self.data_objects = page["dataObjects"]

class Search(object):
    '''Searches the EOL database with the string you supply'''

    def __init__(self, q, page = 1, exact = False, filter_by_taxon_concept_id = '', filter_by_hierarchy_entry_id = '',
        filter_by_string = '', cache_ttl = ''):

        attributes = [q,page,exact,filter_by_taxon_concept_id]
        ##Do checks

        url = (
            "http://eol.org/api/search/1.0.json?q=Ursus&page=1&exact=false&filter_by_taxon_concept_id="
            "&filter_by_hierarchy_entry_id=&filter_by_string=&cache_ttl=".format()
            )



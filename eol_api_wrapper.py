from urllib.request import urlopen
import json
import math

class API(object):
    '''Methods for accessing the API'''

    def __init__(self,key=''):
        self.key = key
        '''Api instance constructor

        Parameters
        ---------
        key: Optional argument which adds your API key to all API calls made from this object '''

    @staticmethod
    def _get_url(url):
        '''Get json page data using a specified eol API url'''
        response = urlopen(url)
        data = str(response.read().decode('utf-8'))
        page = json.loads(data)
        return page

    @staticmethod
    def _bool_converter(string):
        '''Convert Python bools to the correct format'''
        _bool_dict = {True: 'true', False:'false'}
        return _bool_dict[string]

    @staticmethod
    def ping():
        '''Check whether the API is working'''
        url = "http://eol.org/api/ping/1.0.json"
        ping = API._get_url(url)
        return ping['response']['message']

    def Page(self, id, images = 2, videos = 0, sounds = 0, \
                maps = 0, text = 2, iucn = False, subjects = 'overview', \
                licences = 'all', details = True, common_names = True, \
                synonyms = True, references = True, vetted = 0):
        '''
         Takes an EOL page identifier and returns the scientific name for that page, and optionally
         returns information about common names, media (text, images and videos), and references to the
         hierarchies which recognize the taxon described on the page.

        Parameters
        ---------
        Parameters can be found here: http://eol.org/api/docs/pages
        id is the only required argument; the rest are optional
        Booleans are entered in Pythonic form (e.g. False, rather than 'false')

        Example
        ------
        >>> api = API()
        >>> page = api.Page(1045608)
        >>> page.scientific_name
        'Apis mellifera Linnaeus 1758'

        '''
        return Page(id, images, videos, sounds, maps, text, iucn, subjects, licences, details, common_names, synonyms, references, vetted, self.key)

    def Search(self, q, page = 1, exact = False, filter_by_taxon_concept_id = '', filter_by_hierarchy_entry_id = '',\
                filter_by_string = '', cache_ttl = ''):
        '''
         Search the EOL API with a string.

        Parameters
        ---------
        Parameters can be found here: http://eol.org/api/docs/search
        The search string is the only required argument; the rest are optional.
        An optional page='all' argument has been added to allow you to retrieve all
        of the appended results pages for a given search.
        Booleans are entered in Pythonic form (e.g. False, rather than 'false').

        Example
        ------
        >>> api = API()
        >>> search = api.Search('Ursus')
        Retrieving page 1
        >>> search.q
        'Ursus'

        '''
        return Search(q, page, exact, filter_by_taxon_concept_id, filter_by_hierarchy_entry_id ,filter_by_string, cache_ttl, self.key)

    def Collection(self, id, page = 1, per_page = 50, filter = 'none', sort_by='recently_added', sort_field='', cache_ttl=''):

        '''
        Given the identifier for a collection this API will return all metadata about the collection and the items it contains.

        Parameters
        ---------
        Parameters can be found here: http://eol.org/api/docs/collections
        The collection id is the only required argument; the rest are optional
        Booleans are entered in Pythonic form (e.g. False, rather than 'false')

        Example
        ------
        >>> api = API()
        >>> collection = api.Collection(176)
        >>> collection.name
        'EOL Group on Flickr'

        '''
        return Collection(id,page,per_page,filter, sort_by, sort_field, cache_ttl, self.key)


    def DataObject(self, id, cache_ttl = ''):

        '''
        Given the identifier for a data object this API will return all metadata about the object as
        submitted to EOL by the contributing content partner.

        Parameters
        ---------
        Parameters can be found here: http://eol.org/api/docs/data_objects
        The id is the only required argument; cache ttl is optional

        Example
        ------
        >>> api = API()
        >>> dataobject = api.DataObject(30073527)
        >>> dataobject.scientific_name
        'Apis mellifera Linnaeus 1758'

        '''
        return DataObject(id, cache_ttl, self.key)

    def Hierachy_entries(self,id, common_names = False, synonyms = False, cache_ttl=''):

        '''
        The Encyclopedia of Life does not have a singular taxonomic hierarchy upon which it creates its pages.
        Rather EOL indexes many hierarchies and compares them against each other.
        As a result any EOL page may relate to several nodes from various hierarchies.
        This API gives access to a single hierarchy and its internal relationships.

        Parameters
        ---------
        Parameters can be found here: http://eol.org/api/docs/hierarchy_entries
        The id is the only required argument; the rest are optional
        Booleans are entered in Pythonic form (e.g. False, rather than 'false')

        Example
        ------
        >>> api = API()
        >>> hierachy = api.Hierachy_entries(63220654)
        >>> hierachy.scientific_name
        'Dubosquellidae'

        '''

        return Hierachy_entries(id, common_names, synonyms, cache_ttl, self.key)

    def __repr__(self):
        return '<%s (key = %s)>' % (
    self.__class__.__name__, self.key
    )

class Page(object):
    '''
    Takes an EOL identifier and returns a dictionary of information about that page.
    Use kwargs to set other attributes
    '''

    def __init__(self, id, images = 2, videos = 0, sounds = 0, \
                maps = 0, text = 2, iucn = False, subjects = 'overview', \
                licences = 'all', details = True, common_names = True, \
                synonyms = True, references = True, vetted = 0, key=''):


        attributes = [id, images, videos, sounds, maps, text, API._bool_converter(iucn),\
                         subjects, licences, API._bool_converter(details), API._bool_converter(common_names), API._bool_converter(synonyms),\
                          API._bool_converter(references), vetted, key]

        self.id = id
        self.key = key

        url = (
            "http://eol.org/api/pages/1.0/{0}.json?images={1}&videos={2}&sounds={3}"
            "&maps={4}&text={5}&iucn={6}&subjects={7}&licenses={8}&details={9}&common_names={10}"
            "&synonyms={11}&references={12}&vetted={13}&cache_ttl=&key={14}".format(*attributes)
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
        filter_by_string = '', cache_ttl = '', key=''):

        if not isinstance(page, int) and page!='all':
            raise ValueError('Not a valid page number')

        attributes = [q,page,API._bool_converter(exact),filter_by_taxon_concept_id, filter_by_hierarchy_entry_id, filter_by_string, cache_ttl, key]

        url = (
            "http://eol.org/api/search/1.0.json?q={0}&page={1}&exact={2}&filter_by_taxon_concept_id={3}"
            "&filter_by_hierarchy_entry_id={4}&filter_by_string={5}&cache_ttl={6}&key={7}".format(*attributes))
        search = API._get_url(url)
        self.q = q
        self.total_results = search["totalResults"]
        self.startIndex = search["startIndex"]
        self.items_per_page = search["itemsPerPage"]

        if page == 'all':
            self.key = key
            self.results = []
            self.total_pages = math.ceil(self.total_results/30)
            for page in range(1,self.total_pages+1):
                print("Retrieving page {} of {}".format(page,self.total_pages))
                attributes = [q,page,API._bool_converter(exact),filter_by_taxon_concept_id, filter_by_hierarchy_entry_id, filter_by_string,cache_ttl,key ]
                url = (
                "http://eol.org/api/search/1.0.json?q={0}&page={1}&exact={2}&filter_by_taxon_concept_id={3}"
                "&filter_by_hierarchy_entry_id={4}&filter_by_string={5}&cache_ttl={6}&key={7}".format(*attributes))
                search = API._get_url(url)
                self.results+=search["results"]
                self.first = search["first"]
                self.last = search["last"]
        else:
            print("Retrieving page {}".format(page))
            self.key = key
            self.results = search["results"]
            self.first = search["first"]
            self.self = search["self"]
            self.last = search["last"]
            try:
                self.next = search["next"]
            except KeyError:
                pass

class Collection(object):
    '''Returns all metadata about the collection and the items it contains'''

    def __init__(self, id, page = 1, per_page = 50, filter = 'none', sort_by='recently_added', sort_field='', cache_ttl='', key = ''):

        attributes = [id,page,per_page,filter, sort_by, sort_field, cache_ttl, key]
        self.key = key
        url = ("http://eol.org/api/collections/1.0/{}.json?page={}&per_page={}&filter={}&sort_by={}&sort_field={}&cache_ttl={}&key={}".format(*attributes))
        collection = API._get_url(url)
        self.name = collection["name"]
        self.description = collection["description"]
        self.created = collection["created"]
        self.modified = collection["modified"]
        self.total_items = collection["total_items"]
        self.item_types = collection["item_types"]
        self.collection_items = collection["collection_items"]

class DataObject(object):
    '''Given the identifier for a data object this API will return all metadata about the object as submitted to EOL by the contributing content partner'''

    def __init__(self, id, cache_ttl = '', key = ''):
        attributes = [id, cache_ttl, key]
        self.key = key
        url = "http://eol.org/api/data_objects/1.0/{}.json?cache_ttl={}&key={}".format(*attributes)
        data_object = API._get_url(url)
        self.identifier = id
        self.scientific_name = data_object["scientificName"]
        self.exemplar = data_object["exemplar"]
        self.richness_score = data_object["richness_score"]
        self.synonyms = data_object["synonyms"]
        self.data_objects = data_object["dataObjects"]
        self.references = data_object["references"]

class Hierachy_entries(object):

    def __init__(self,id, common_names = False, synonyms = False, cache_ttl='', key = ''):
        attributes = [id, API._bool_converter(common_names), API._bool_converter(synonyms), cache_ttl, key]
        url = "http://eol.org/api/hierarchy_entries/1.0/{}.json?common_names={}&synonyms={}&cache_ttl={}&key={}".format(*attributes)
        hierachy = API._get_url(url)
        self.key = key
        self.id = id
        self.source_identifier = hierachy["sourceIdentifier"]
        self.taxon_id = hierachy["taxonID"]
        self.parent_name_usage_id = hierachy["parentNameUsageID"]
        self.taxon_concept_id = hierachy["taxonConceptID"]
        self.scientific_name = hierachy["scientificName"]
        self.taxon_rank = hierachy["taxonRank"]
        self.source = hierachy["source"]
        self.name_according_to = hierachy["nameAccordingTo"]
        self.vernacularNames = hierachy["vernacularNames"]

if __name__ == '__main__':
    #run doctests
    import doctest
    doctest.testmod()















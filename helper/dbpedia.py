import os
from SPARQLWrapper import SPARQLWrapper, JSON


DBPEDIA_COMMONS = 'http://commons.dbpedia.org/sparql'
METADATA = {
    'url': 'http://dbpedia.org/ontology/fileURL'
    'lat': 'http://www.w3.org/2003/01/geo/wgs84_pos#lat'
    'file_format': 'http://purl.org/dc/terms/format'
    'description': 'http://commons.dbpedia.org/property/archiveTitle'
}


def fetch_uris(keywords, amount):
    """
    Query the DBpedia SPARQL endpoint to fetch amount names of images that
    contain at least one of keywords in their description.
    """
    try:
        data = query_uris(keywords, amount)
        filenames = parse_uris(data)
        return list(filenames)
    except:
        print('Could not get filesnames for keyword', keywords)

def query_uris(keywords, amount):
    keywords = '|'.join(keywords)
    keywords = r'(^|\\W)(' + keywords + r')(\\W|$)'
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dbpc: <http://dbpedia.org/ontology/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT ?s WHERE {{
                ?s ?p ?keyword; rdf:type foaf:Image
                FILTER regex(str(?keyword), "{keywords}", "i")
                FILTER (?p = <http://www.w3.org/2000/01/rdf-schema#label>)
            }} LIMIT {amount}""".format(**locals())
    result = execute_query(query)
    return result

def parse_uris(json):
    for result in json['results']['bindings']:
        yield result['s']['value']

def fetch_metadata(uri):
    print('Download metadata', uri)
    filename = get_filename(uri) + '.meta'
    resource = '<{}>'.format(filename)
    # Download all properties from the global METADATA dictionary
    metadata = fetch_properties(resource, METADATA.values())
    return metadata

def fetch_properties(resource, properties):
    try:
        json = query_properties(resource)
        properties = parse_properties(json, properties)
        return properties
    except:
        print('Error retrieving resource', resource)

def query_properties(resource):
    query = """SELECT DISTINCT ?s ?p ?o WHERE {{
            ?s ?p ?o
            FILTER (?s = {resource}) }}""".format(**locals())
    result = execute_query(query)
    return result

def parse_properties(json, predicates):
    properties = {}
    for predicate in predicates:
        properties[predicate] = ''
    for result in json['results']['bindings']:
        value = result['p']['value']
        for predicate in predicates:
            if value == predicate:
                properties[predicate] = result['o']['value']
    return properties

def execute_query(query):
    sparql = SPARQLWrapper(DBPEDIA_COMMONS)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(300)  # Does this mean 5 seconds?
    data = sparql.query().convert()
    return data

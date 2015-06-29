import os
from SPARQLWrapper import SPARQLWrapper, JSON
from .download import get_filename


METADATA = {
    'url':         'http://dbpedia.org/ontology/fileURL',
    'extension':   'http://dbpedia.org/ontology/fileExtension',
    'title':       'http://dbpedia.org/ontology/title',
    'description': 'http://commons.dbpedia.org/property/description',
    'lat':         'http://www.w3.org/2003/01/geo/wgs84_pos#lat',
    'long':        'http://www.w3.org/2003/01/geo/wgs84_pos#long',
}


def fetch_uris_from_metadata(keywords, amount):
    """
    Query DBpedia for image uris where one of the keywords is found in the
    'label' tag.
    """
    ontology = '<http://www.w3.org/2000/01/rdf-schema#label>'
    uris = query_uris_from_keywords(ontology, keywords, amount)
    return uris

def fetch_uris_from_articles(keywords, amount):
    """
    Query DBpedia for image uris where one of the keywords is found in the
    the name of an article using the image.
    """
    ontology = '<http://dbpedia.org/ontology/galleryItem>'
    uris = query_uris_from_keywords(ontology, keywords, amount)
    return uris

def fetch_metadata(uri):
    resource = '<{}>'.format(uri)
    # Download all properties from the global METADATA dictionary
    metadata = fetch_properties(resource, list(METADATA.values()))
    if not metadata:
        return None
    # Use simple key names
    for key, value in METADATA.items():
        if value in metadata:
            metadata[key] = metadata.pop(value)
    return metadata

def fetch_properties(resource, properties):
    try:
        data = query_properties(resource)
        properties = parse_properties(data, properties)
        return properties
    except:
        print('Error retrieving', resource.strip('<>'))

def query_uris_from_keywords(ontology, keywords, amount):
    print('Query image URIs for:' , ','.join(keywords))
    assert isinstance(ontology, str)
    keywords = '|'.join(keywords)
    keywords = r'(^|\\W)(' + keywords + r')(\\W|$)'
    filters = [
        '?uri {} ?object; rdf:type foaf:Image'.format(ontology),
        'FILTER regex(str(?object), "{}", "i")'.format(keywords)
    ]
    results = query_uris(filters, amount)
    uris = parse_uris(results)
    return list(uris)

def query_uris(filters, amount=5000):
    """
    Query DBpedia for image uris where all of the SPARQL filter rules apply.
    """
    filters = '\n'.join(filters)
    query = 'SELECT DISTINCT ?uri WHERE {{ {filters} }} LIMIT {amount}'.format(**locals())
    result = execute_query(query)
    return result

def query_properties(resource):
    query = """SELECT DISTINCT ?subject ?predicate ?object WHERE {{
            ?subject ?predicate ?object
            FILTER (?subject = {resource}) }}""".format(**locals())
    result = execute_query(query)
    return result

def parse_uris(json):
    for result in json['results']['bindings']:
        yield result['uri']['value']

def parse_properties(data, predicates):
    properties = {x: '' for x in predicates}
    for result in data['results']['bindings']:
        predicate = result['predicate']['value']
        if predicate in predicates:
            properties[predicate] = result['object']['value']
    return properties

def execute_query(query):
    sparql = SPARQLWrapper('http://commons.dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(300)  # 5 minutes
    data = sparql.query().convert()
    return data

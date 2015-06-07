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
        print('Could not get filenames for keyword', keywords)

def query_uris(keywords, amount):
    print('Query images for', ','.join(keywords))
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

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def fetch_metadata(uri):
    print('Fetch metadata:', remove_prefix(os.path.basename(uri), 'File:'))
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
    #try:
        data = query_properties(resource)
        properties = parse_properties(data, properties)
        return properties
    #except:
    #    print('Error retrieving', resource.strip('<>'))

def query_properties(resource):
    query = """SELECT DISTINCT ?s ?p ?o WHERE {{
            ?s ?p ?o
            FILTER (?s = {resource}) }}""".format(**locals())
    result = execute_query(query)
    return result

def parse_properties(data, predicates):
    #print(data)
    properties = {x: '' for x in predicates}
    for result in data['results']['bindings']:
        predicate = result['p']['value']
        if predicate in predicates:
            properties[predicate] = result['o']['value']
    return properties

def execute_query(query):
    sparql = SPARQLWrapper('http://commons.dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(300)  # TODO: Does this mean 5 seconds?
    data = sparql.query().convert()
    return data

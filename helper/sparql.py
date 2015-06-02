import constants
from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA_COMMONS = 'http://commons.dbpedia.org/sparql'
FILE_URL = 'http://dbpedia.org/ontology/fileURL'
TIMEOUT = 300 #seconds

def to_resource_uri(filename):
    return '<' + filename + '>'

def execute_query(query):
    sparql = SPARQLWrapper(DBPEDIA_COMMONS)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(TIMEOUT)
    print('\n' + query + '\n')
    data = sparql.query().convert()
    return data

def query_filenames(keywords, number):
    regex = r'(^|\\W)(' + '|'.join(keywords) + r')(\\W|$)'
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dbpc: <http://dbpedia.org/ontology/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT ?s WHERE {{
                ?s ?p ?keyword; rdf:type foaf:Image
                FILTER regex(str(?keyword), "{regex}", "i")
                FILTER (?p = <http://www.w3.org/2000/01/rdf-schema#label>)
            }} LIMIT {number}""".format(**locals())
    result = execute_query(query)
    return result

def parse_filenames(json):
    filenames = []
    for result in json['results']['bindings']:
        filename = result['s']['value']
        filenames.append(filename)
    return filenames

def get_filenames(keywords, number):
    try:
        json = query_filenames(keywords, number)
        filenames = parse_filenames(json)
        print('Result set size:', len(filenames))
        return filenames
    except:
        print('Could not get filesnames for keywords:', keywords)
        return False

def query_resource(resource):
    query = """SELECT DISTINCT ?s ?p ?o WHERE {{
            ?s ?p ?o
            FILTER (?s = {resource}) }}""".format(**locals())
    result = execute_query(query)
    return result

def parse_resource(json, predicates):
    properties = {}
    for predicate in predicates:
        properties[predicate] = ''
    for result in json['results']['bindings']:
        value = result['p']['value']
        for predicate in predicates:
            if value == predicate:
                properties[predicate] = result['o']['value']
    return properties

def get_resource(resource, properties):
    try:
        json = query_resource(resource)
        properties = parse_resource(json, properties)
        print('Result set size:', len(properties))
        return properties
    except:
        print('Could not get resource:', resource)
        return False

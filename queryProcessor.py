from processor import Processor
from sqlite3 import connect
from pandas import read_sql, read_sql_query

from pandas.io.json import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON


class QueryProcessor(Processor):
    def __init__(self):
        super().__init__()

    def getEntityById(self, entityId: str):
        # return data frame for a specific identifier
        # reading data from sqlite or blazegraph
        # for json do we need to wrap the .. for RDF triplestore??

        if self.dbPathOrUrl:  # dummy condition
            with connect(self.dbPathOrUrl) as con:
                query = """
                SELECT * FROM EntitiesWithMetadata
                FULL OUTER JOIN Annotations ON EntitiesWithMetadata.metadata_internal_id = Annotations.annotation_targets
                FULL OUTER JOIN Images ON Annotations.annotation_bodies = Images.images_internal_id
                FULL OUTER JOIN Creators ON EntitiesWithMetadata.creator = Creators.creator_internal_id
                WHERE EntitiesWithMetadata.id = ? OR Annotations.annotation_ids = ? OR Images.image_ids = ?
                """
                cursor = con.cursor()
                cursor.execute(query, (entityId, entityId, entityId))
                df = read_sql_query(query, con, params=(entityId, entityId, entityId))
                # df = read_sql(query, con)
                return df
        else:
            endpoint = self.getDbPathOrUrl()
            query = (
                """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX p1: <https://github.com/datasci2023/datascience/res/>
            PREFIX p2: <https://github.com/datasci2023/datascience/attr/>
            SELECT ?id ?items ?type ?label 
            WHERE {
                ?literal_id a \""""
                + entityId
                + """\" .
                ?id p2:id ?literal_id;
                    rdf:type ?type ;
                    rdfs:label ?label .
                OPTIONAL { ?id p2:items ?items}
            }
            """
            )
            sparql = SPARQLWrapper(endpoint)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            result = sparql.query().convert()
            return json_normalize(result)  # ???

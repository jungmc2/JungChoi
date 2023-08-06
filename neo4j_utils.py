from neo4j import GraphDatabase
import pandas as pd 


def return_universities():
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j" 
    neo4j_pw = "123456yoyo" 
    database_name = "academicworld"
    uri_with_database = f"{neo4j_uri}/db/{database_name}"
    
    driver = GraphDatabase.driver(uri_with_database, auth=(neo4j_user, neo4j_pw))
    session = driver.session(database=database_name)
    
    query = f"""MATCH (i:INSTITUTE)-[a:AFFILIATION_WITH]-(f:FACULTY)-[pd:PUBLISH]-(p:PUBLICATION)
            WITH p.year as year, count(*) as count_of_publications, i.name as name
            WHERE year >= 2000 AND year <= 2020
            RETURN distinct name
            """
    
    response = list(session.run(query))
    df = pd.DataFrame([dict(record) for record in response])
    universities_neo = df.squeeze().tolist()
    session.close()
    
    return universities_neo

def widget5_helper(college):
    uri = "bolt://localhost:7687"
    neo4j_user = "neo4j" 
    neo4j_pw = "123456yoyo" 
    database_name = "academicworld"
    uri_with_database = f"{uri}/db/{database_name}"
    
    driver = GraphDatabase.driver(uri_with_database, auth=(neo4j_user, neo4j_pw))
    session = driver.session(database=database_name)
    query = f"""MATCH (i:INSTITUTE)-[a:AFFILIATION_WITH]-(f:FACULTY)-[pd:PUBLISH]-(p:PUBLICATION)
            WITH p.year as year, count(*) as count_of_publications, i.name as name
            WHERE name = '{college}'
            RETURN year, count_of_publications
            ORDER BY year
            """
    
    response = list(session.run(query))
    df = pd.DataFrame([dict(record) for record in response])
    session.close()

    return df

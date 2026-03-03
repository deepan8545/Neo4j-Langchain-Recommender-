import pandas as pd
from neo4j import GraphDatabase
from utils import load_env, require_env

DATASET_PATH = "dataset/neo4j_langchain_project_dataset.csv"

def main():
    load_env()

    uri = require_env("NEO4J_URI")
    user = require_env("NEO4J_USERNAME")
    pwd = require_env("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    df = pd.read_csv(DATASET_PATH)

    rows = []
    for _, r in df.iterrows():
        rows.append({
            "user_id": r["user_id"],
            "product_name": r["product_name"],
            "rating": int(r["rating (1-5)"]),
            "discount": int(r["discount_purchase (0/1)"])
        })

    with driver.session() as session:
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE p.name IS UNIQUE;")

        query = '''
        UNWIND $rows AS row
        MERGE (u:User {user_id: row.user_id})
        MERGE (p:Product {name: row.product_name})
        MERGE (u)-[r:PURCHASED]->(p)
        SET r.rating = toInteger(row.rating),
            r.discount_purchase = toInteger(row.discount)
        '''

        session.run(query, {"rows": rows})

    driver.close()
    print("Dataset loaded successfully.")

if __name__ == "__main__":
    main()

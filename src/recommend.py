import argparse
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from utils import load_env, require_env
from cypher import RECOMMEND_QUERY, SIMILAR_USERS_QUERY

def main(user_id: str):
    load_env()

    graph = Neo4jGraph(
        url=require_env("NEO4J_URI"),
        username=require_env("NEO4J_USERNAME"),
        password=require_env("NEO4J_PASSWORD"),
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    recs = graph.query(RECOMMEND_QUERY, params={"user": user_id})
    sims = graph.query(SIMILAR_USERS_QUERY, params={"user": user_id})

    prompt = f'''
You are an assistant explaining graph-based recommendations.

Target user: {user_id}

Similar users:
{sims}

Recommended products:
{recs}

Return:
1) Bullet list of recommendations
2) Short explanation using support + rating signals
'''

    explanation = llm.invoke(prompt).content
    print(explanation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    args = parser.parse_args()
    main(args.user)

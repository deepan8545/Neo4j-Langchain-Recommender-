RECOMMEND_QUERY = '''
MATCH (u:User {user_id:$user})-[:PURCHASED]->(p:Product)
WITH u, collect(p) AS already

MATCH (u)-[:PURCHASED]->(:Product)<-[:PURCHASED]-(other:User)-[r:PURCHASED]->(rec:Product)
WHERE NOT rec IN already
WITH rec, avg(r.rating) AS avg_rating, count(*) AS support
ORDER BY support DESC, avg_rating DESC
LIMIT 5
RETURN rec.name AS product, support, round(avg_rating*10)/10 AS avg_rating;
'''

SIMILAR_USERS_QUERY = '''
MATCH (u:User {user_id:$user})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:User)
WHERE other <> u
WITH other, count(p) AS overlap
ORDER BY overlap DESC
LIMIT 10
RETURN other.user_id AS similar_user, overlap;
'''

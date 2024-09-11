from neo4j import GraphDatabase

# Neo4j数据库连接
uri = "bolt://localhost:7687"  # 根据你的Neo4j设置更改
username = "neo4j"  # 根据你的Neo4j设置更改
password = "password"  # 根据你的Neo4j设置更改

# 创建Neo4j驱动程序
driver = GraphDatabase.driver(uri, auth=(username, password))

def batch_load(session, filename, query, description, batch_size=5000):
    load_query = f"""
        CALL {{
            LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
            {query}
        }} IN TRANSACTIONS OF {batch_size} ROWS
    """
    print(f"Starting batch load for {description}")
    session.run(load_query)
    print(f"Finished batch load for {description}")

# 批量插入电影数据
movie_query = """
    MERGE (m:Movie {tconst: row.tconst})
    SET m.primaryTitle = row.primaryTitle, m.startYear = toInteger(row.startYear)
"""
# 批量插入评分数据
grade_query = """
    MATCH (m:Movie {tconst: row.tconst})
    SET m.averageRating = toFloat(row.averageRating), m.numVotes = toInteger(row.numVotes)
"""
# 批量插入演员数据
actor_query = """
    MERGE (a:Actor {nconst: row.nconst})
    SET a.primaryName = row.primaryName
    MERGE (m:Movie {tconst: row.tconst})
    MERGE (a)-[:ACTED_IN]->(m)
"""
# 批量插入导演数据
director_query = """
    MERGE (d:Director {nconst: row.nconst})
    SET d.primaryName = row.primaryName
    MERGE (m:Movie {tconst: row.tconst})
    MERGE (d)-[:DIRECTED]->(m)
"""
# 批量插入用户评分数据
user_rating_query = """
    MERGE (u:User {userID: row.userID})
    MERGE (m:Movie {tconst: row.tconst})
    MERGE (u)-[:RATED {rating: toInteger(row.rating), reviewDate: row.reviewDate}]->(m)
"""
# 批量插入类型数据
genre_query = """
    MATCH (m:Movie {tconst: row.tconst})
    MERGE (g:Genre {name: row.genre})
    MERGE (m)-[:HAS_GENRE]->(g)
"""

# 执行批量插入
with driver.session() as session:
    # 插入电影数据
    batch_load(session, 'filtered_high_quality_movies.csv', movie_query, "movies")

    # 插入评分数据
    batch_load(session, 'filtered_high_quality_grades.csv', grade_query, "grades")

    # 插入演员数据
    batch_load(session, 'filtered_high_quality_cast.csv', actor_query, "cast")

    # 插入导演数据
    batch_load(session, 'filtered_high_quality_directors.csv', director_query, "directors")

    # 插入用户评分数据
    batch_load(session, 'filtered_high_quality_user_ratings.csv', user_rating_query, "user ratings")

    # 插入类型数据
    genre_load_query = """
        CALL {
            LOAD CSV WITH HEADERS FROM 'file:///filtered_high_quality_genres.csv' AS row
            UNWIND split(row.genres, ',') AS genre
            MATCH (m:Movie {tconst: row.tconst})
            MERGE (g:Genre {name: genre})
            MERGE (m)-[:HAS_GENRE]->(g)
        } IN TRANSACTIONS OF 5000 ROWS
    """
    print("Starting batch load for genres")
    session.run(genre_load_query)
    print("Finished batch load for genres")

driver.close()

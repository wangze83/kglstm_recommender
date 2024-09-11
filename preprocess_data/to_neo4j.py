from neo4j import GraphDatabase

# Neo4j 数据库连接信息
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# 定义批量加载函数
def batch_load(session, filename, query):
    load_query = f"""
        CALL {{
            LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
            {query}
        }} IN TRANSACTIONS of 5000 ROWS
    """
    session.run(load_query)

# 加载电影节点的查询
def create_movie_node():
    return """
        MERGE (m:Movie {tconst: row.tconst})
        ON CREATE SET m.primaryTitle = row.primaryTitle
    """

# 加载导演关系的查询
def create_director_relationship():
    return """
        MATCH (m:Movie {tconst: row.tconst})
        MERGE (d:Director {primaryName: row.primaryName})
        CREATE (m)-[:DIRECTED_BY]->(d)
    """

# 加载演员关系的查询
def create_cast_relationship():
    return """
        MATCH (m:Movie {tconst: row.tconst})
        MERGE (p:Person {primaryName: row.primaryName})
        CREATE (m)-[:HAS_CAST]->(p)
    """

# 加载评分关系的查询
def create_rating_relationship():
    return """
        MATCH (m:Movie {tconst: row.tconst})
        CREATE (r:Rating {averageRating: toFloat(row.averageRating), numVotes: toInteger(row.numVotes)})
        CREATE (m)-[:HAS_RATING]->(r)
    """

# 加载电影类型关系的查询
def create_genre_relationship():
    return """
        MATCH (m:Movie {tconst: row.tconst})
        WITH m, split(row.genres, ',') AS genres
        UNWIND genres AS genre
        MERGE (g:Genre {name: genre})
        CREATE (m)-[:HAS_GENRE]->(g)
    """

# 加载用户评分关系的查询
def create_user_rating_relationship():
    return """
        MERGE (u:User {userID: row.userID})
        MATCH (m:Movie {tconst: row.tconst})
        CREATE (u)-[:RATED {rating: toInteger(row.rating), reviewDate: row.reviewDate}]->(m)
    """

# 主函数：加载数据
def load_data():
    with driver.session() as session:
        # 清空数据库
        session.run("MATCH ()-[r]->() DELETE r")
        session.run("MATCH (n) DETACH DELETE n")

        # 加载电影节点
        print("start Movie")
        batch_load(session, "out_movies.csv", create_movie_node())

        # 加载导演关系
        print("start Director")
        batch_load(session, "out_directors.csv", create_director_relationship())

        # 加载演员关系
        print("start Cast")
        batch_load(session, "out_cast.csv", create_cast_relationship())

        # 加载评分关系
        print("start Rating")
        batch_load(session, "out_grade.csv", create_rating_relationship())

        # 加载电影类型关系
        print("start Genre")
        batch_load(session, "out_genre.csv", create_genre_relationship())

        # 加载用户评分关系
        print("start User Rating")
        batch_load(session, "user_ratings.csv", create_user_rating_relationship())

# 执行加载数据函数
load_data()

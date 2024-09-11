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

# 加载用户节点的查询
def create_user_node():
    return """
        MERGE (u:User {userID: row.userID})
    """

# 加载用户评分关系的查询
def create_rating_relationship():
    return """
        MATCH (u:User {userID: row.userID}), (m:Movie {tconst: row.tconst})
        MERGE (u)-[r:RATED {rating: toFloat(row.rating), reviewDate: row.reviewDate}]->(m)
    """

# 主函数：加载数据
def load_user_data():
    with driver.session() as session:
        # 加载用户节点
        print("start User")
        batch_load(session, "user_rating_filtered.csv", create_user_node())

        # 加载用户评分关系
        print("start Rating Relationship")
        batch_load(session, "user_rating_filtered.csv", create_rating_relationship())

# 执行加载数据函数
load_user_data()

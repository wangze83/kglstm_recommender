from neo4j import GraphDatabase

class MovieDatabase:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, file_path):
        with self.driver.session() as session:
            session.write_transaction(self._load_data, file_path)

    @staticmethod
    def _load_data(tx, file_path):
        query = """
        LOAD CSV WITH HEADERS FROM $file_path AS row
        MATCH (m:Movie {tconst: row.tconst})
        SET m.startYear = toInteger(row.startYear)
        RETURN m
        """
        tx.run(query, file_path=file_path)

if __name__ == "__main__":
    # 替换为你的Neo4j数据库的连接信息
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"

    # CSV文件路径，确保文件位于Neo4j的import目录中，或者提供绝对路径
    file_path = "file:///add_year_out_movies.csv"

    db = MovieDatabase(uri, user, password)
    try:
        db.load_data(file_path)
        print("Data loaded successfully.")
    finally:
        db.close()

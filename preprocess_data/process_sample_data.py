import pandas as pd

# 定义中间文件和输出文件目录
input_dir = "./data_out"
output_dir = "./data_out"

# 读取中间文件，跳过重复表头
movies = pd.read_csv(f"{input_dir}/movies_filtered.csv", sep='\t', low_memory=False)
directors_temp = pd.read_csv(f"{input_dir}/directors_filtered.csv", sep='\t', low_memory=False)
cast_temp = pd.read_csv(f"{input_dir}/cast_filtered.csv", sep='\t', low_memory=False)
ratings = pd.read_csv(f"{input_dir}/ratings_filtered.csv", sep='\t', low_memory=False)
names = pd.read_csv(f"{input_dir}/names_filtered.csv", sep='\t', low_memory=False)

# 手动设置列名
movies.columns = ["tconst", "primaryTitle", "genres"]
directors_temp.columns = ["tconst", "nconst"]
cast_temp.columns = ["tconst", "nconst"]
ratings.columns = ["tconst", "averageRating", "numVotes"]
names.columns = ["nconst", "primaryName"]

# 过滤抽样
sample_fraction = 0.08
movies_sampled = movies.sample(frac=sample_fraction, random_state=42)

# 合并导演信息
directors = directors_temp.merge(names, left_on='nconst', right_on='nconst', how='left')
directors = directors[['tconst', 'primaryName']]
directors = directors[directors['tconst'].isin(movies_sampled['tconst'])]

# 合并演员信息
cast = cast_temp.merge(names, left_on='nconst', right_on='nconst', how='left')
cast = cast[['tconst', 'primaryName']]
cast = cast[cast['tconst'].isin(movies_sampled['tconst'])]

# 处理电影评分信息
ratings_sampled = ratings[ratings['tconst'].isin(movies_sampled['tconst'])]

# 处理电影类型信息
genres_sampled = movies_sampled[['tconst', 'genres']]

# 检查并删除重复表头
def remove_duplicate_header(df):
    if df.columns.tolist() == df.iloc[0].tolist():
        df = df[1:]
    return df

movies_sampled = remove_duplicate_header(movies_sampled)
directors = remove_duplicate_header(directors)
cast = remove_duplicate_header(cast)
ratings_sampled = remove_duplicate_header(ratings_sampled)
genres_sampled = remove_duplicate_header(genres_sampled)

if movies_sampled.empty or directors.empty or cast.empty or ratings_sampled.empty or genres_sampled.empty:
    print("Error: One or more sampled datasets are empty.")
    exit()

# 保存为CSV以供Neo4j使用
movies_sampled.to_csv(f"{output_dir}/out_movies.csv", index=False)
directors.to_csv(f"{output_dir}/out_directors.csv", index=False)
cast.to_csv(f"{output_dir}/out_cast.csv", index=False)
ratings_sampled.to_csv(f"{output_dir}/out_grade.csv", index=False)
genres_sampled.to_csv(f"{output_dir}/out_genre.csv", index=False)

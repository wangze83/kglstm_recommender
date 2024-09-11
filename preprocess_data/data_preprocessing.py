import pandas as pd
import os

# 确保输出目录存在
output_dir = "./data_out"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取IMDB数据
basics = pd.read_csv("../datasets/title.basics.tsv.gz", sep='\t', na_values="\\N", low_memory=False)
ratings = pd.read_csv("../datasets/title.ratings.tsv.gz", sep='\t', na_values="\\N")
crew = pd.read_csv("../datasets/title.crew.tsv.gz", sep='\t', na_values="\\N")
principals = pd.read_csv("../datasets/title.principals.tsv.gz", sep='\t', na_values="\\N")
names = pd.read_csv("../datasets/name.basics.tsv.gz", sep='\t', na_values="\\N")

# 过滤出电影类型数据
movies = basics[basics['titleType'] == 'movie']

# 过滤掉startYear为空或为\N的数据
movies = movies[movies['startYear'].notna()]

# 获取movies的tconst列表
movie_tconsts = set(movies['tconst'])

# 合并ratings数据
movies = movies.merge(ratings, on='tconst', how='left')

# 处理导演信息，并剔除不在movie_tconsts中的数据
directors = crew[['tconst', 'directors']].dropna()
directors = directors[directors['tconst'].isin(movie_tconsts)]
directors = directors.set_index('tconst')['directors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='nconst')
directors = directors.merge(names[['nconst', 'primaryName']], on='nconst', how='left')

# 处理演员信息，并剔除不在movie_tconsts中的数据
cast = principals[principals['category'].str.contains("actor|actress", na=False)]
cast = cast[cast['tconst'].isin(movie_tconsts)]
cast = cast[['tconst', 'nconst']].dropna()
cast = cast.merge(names[['nconst', 'primaryName']], on='nconst', how='left')

# 提取电影评分信息，并剔除不在movie_tconsts中的数据
ratings = ratings[ratings['tconst'].isin(movie_tconsts)]

# 提取电影类型信息，并剔除不在movie_tconsts中的数据
genres = movies[['tconst', 'genres']].dropna()

# 将 startYear 转换为整数以去除 .0 后缀
movies['startYear'] = movies['startYear'].astype(int)

# 保存为CSV以供Neo4j使用
movies[['tconst', 'primaryTitle', 'startYear']].to_csv(os.path.join(output_dir, "out_movies.csv"), index=False)
directors.to_csv(os.path.join(output_dir, "out_directors.csv"), index=False)
cast.to_csv(os.path.join(output_dir, "out_cast.csv"), index=False)
ratings.to_csv(os.path.join(output_dir, "out_grade.csv"), index=False)
genres.to_csv(os.path.join(output_dir, "out_genre.csv"), index=False)

import pandas as pd

# 设置采样比例或数量
sample_fraction = 0.01  # 采样比例
sample_n = 1000  # 采样数量

# 读取IMDB数据
basics = pd.read_csv("../datasets/title.basics.tsv.gz", sep='\t', na_values="\\N", low_memory=False)
ratings = pd.read_csv("../datasets/title.ratings.tsv.gz", sep='\t', na_values="\\N")
crew = pd.read_csv("../datasets/title.crew.tsv.gz", sep='\t', na_values="\\N")
# principals = pd.read_csv("../datasets/title.principals.tsv.gz", sep='\t', na_values="\\N")
names = pd.read_csv("../datasets/name.basics.tsv.gz", sep='\t', na_values="\\N")

# 过滤出电影类型数据
movies = basics[basics['titleType'] == 'movie']

# 合并ratings数据
movies = movies.merge(ratings, on='tconst', how='left')

# 抽取代表性数据样本
movies_sample = movies.sample(n=sample_n)

# 处理导演信息
directors = crew[['tconst', 'directors']].dropna()
directors = directors[directors['directors'].notna()]
directors = directors['directors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).to_frame('nconst').reset_index()
directors = directors.merge(names[['nconst', 'primaryName']], on='nconst', how='left')

# # 只保留与样本电影相关的导演信息
directors_sample = directors[directors['tconst'].isin(movies_sample['tconst'])]
#
# # 处理演员信息
# cast = principals[principals['category'].str.contains("actor|actress")]
# cast = cast[['tconst', 'nconst']].dropna()
# cast = cast.merge(names[['nconst', 'primaryName']], on='nconst', how='left')
#
# # 只保留与样本电影相关的演员信息
# cast_sample = cast[cast['tconst'].isin(movies_sample['tconst'])]
#
# # 提取电影评分信息
# ratings_sample = ratings[ratings['tconst'].isin(movies_sample['tconst'])]
#
# # 提取电影类型信息
# genres_sample = movies_sample[['tconst', 'genres']].dropna()

# 保存为CSV以供Neo4j使用
# movies_sample[['tconst', 'primaryTitle']].to_csv("./sampling_data_out/sample_movies.csv", index=False)
directors_sample.to_csv("./sampling_data_out/sample_directors.csv", index=False)
# cast_sample.to_csv("./sampling_data_out/sample_cast.csv", index=False)
# ratings_sample.to_csv("./sampling_data_out/sample_grade.csv", index=False)
# genres_sample.to_csv("./sampling_data_out/sample_genre.csv", index=False)

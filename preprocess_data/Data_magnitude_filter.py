import pandas as pd

# 读取数据
movies = pd.read_csv("./data_out/filtered_out_movies.csv")
grades = pd.read_csv("./data_out/filtered_out_grade.csv")
cast = pd.read_csv("./data_out/filtered_out_cast.csv")
directors = pd.read_csv("./data_out/filtered_out_directors.csv")
user_ratings = pd.read_csv("./data_out/filtered_user_rating_temp.csv")
genres = pd.read_csv("./data_out/filtered_out_genre.csv")

# 设定最低评分和最低评价次数阈值
min_rating = 4.5
min_votes = 500

# 过滤优质电影
high_quality_movies = grades[(grades['averageRating'] >= min_rating) & (grades['numVotes'] >= min_votes)]

# 获取高质量电影的 tconst 列表
high_quality_tconst = set(high_quality_movies['tconst'])

# 统计高质量电影的数量
num_high_quality_movies = len(high_quality_tconst)
# print(f"Number of high-quality movies: {num_high_quality_movies}")

# 获取高质量电影的详细信息
filtered_movies = movies[movies['tconst'].isin(high_quality_tconst)]

# 打印高质量电影的数量
# print(f"Number of high-quality movie records: {len(filtered_movies)}")

# 设定重要演员和导演的阈值，比如出现在多少部高评分电影中
cast_min_appearances = 5
director_min_appearances = 1

# 统计演员和导演的出现次数
cast_counts = cast['nconst'].value_counts()
director_counts = directors['nconst'].value_counts()

# 过滤重要演员和导演
important_cast = cast_counts[cast_counts >= cast_min_appearances].index
important_directors = director_counts[director_counts >= director_min_appearances].index

# 统计重要演员和导演的数量
num_important_cast = len(important_cast)
num_important_directors = len(important_directors)
# print(f"Number of important cast members: {num_important_cast}")
# print(f"Number of important directors: {num_important_directors}")

# 保留重要演员和导演的数据
filtered_cast = cast[cast['nconst'].isin(important_cast)]
filtered_directors = directors[directors['nconst'].isin(important_directors)]

# 打印重要演员和导演的记录数量
# print(f"Number of important cast records: {len(filtered_cast)}")
# print(f"Number of important director records: {len(filtered_directors)}")

# 去除user_ratings_user_counts中为1的数据
user_ratings_user_counts = user_ratings['userID'].value_counts().reset_index()
user_ratings_user_counts.columns = ['userID', 'count']
user_ratings_user_counts = user_ratings_user_counts[user_ratings_user_counts['count'] > 3]

# 过滤user_ratings中userID出现次数大于1的记录
filtered_user_ratings = user_ratings[user_ratings['userID'].isin(user_ratings_user_counts['userID'])]

# 去除user_ratings_tconst_counts中为1的数据
user_ratings_tconst_counts = user_ratings['tconst'].value_counts().reset_index()
user_ratings_tconst_counts.columns = ['tconst', 'count']
user_ratings_tconst_counts = user_ratings_tconst_counts[user_ratings_tconst_counts['count'] > 1]

# 过滤user_ratings中tconst出现次数大于1的记录
filtered_user_ratings = filtered_user_ratings[filtered_user_ratings['tconst'].isin(user_ratings_tconst_counts['tconst'])]

# 过滤 genres 数据
filtered_genres = genres[genres['tconst'].isin(high_quality_tconst)]
filtered_grades = grades[grades['tconst'].isin(high_quality_tconst)]

# 获取所有文件中共有的 tconst
common_tconst = set(filtered_movies['tconst']) & set(filtered_cast['tconst']) & set(filtered_user_ratings['tconst']) & set(filtered_genres['tconst']) & set(filtered_grades['tconst']) & set(filtered_directors['tconst'])

# 保留共有 tconst 的数据
filtered_movies = filtered_movies[filtered_movies['tconst'].isin(common_tconst)]
filtered_cast = filtered_cast[filtered_cast['tconst'].isin(common_tconst)]
filtered_user_ratings = filtered_user_ratings[filtered_user_ratings['tconst'].isin(common_tconst)]
filtered_genres = filtered_genres[filtered_genres['tconst'].isin(common_tconst)]
filtered_grades = high_quality_movies[high_quality_movies['tconst'].isin(common_tconst)]
filtered_directors = filtered_directors[filtered_directors['tconst'].isin(common_tconst)]

# 输出每个数据类型的数量
print(f"Number of final filtered movies: {len(filtered_movies)}")
print(f"Number of final filtered cast records: {len(filtered_cast)}")
print(f"Number of final filtered user ratings: {len(filtered_user_ratings)}")
print(f"Number of final filtered genres: {len(filtered_genres)}")
print(f"Number of final filtered grades: {len(filtered_grades)}")
print(f"Number of final filtered directors: {len(filtered_directors)}")

# 保存过滤后的数据
filtered_movies.to_csv("./data_out/filtered_high_quality_movies.csv", index=False)
filtered_cast.to_csv("./data_out/filtered_high_quality_cast.csv", index=False)
filtered_user_ratings.to_csv("./data_out/filtered_high_quality_user_ratings.csv", index=False)
filtered_directors.to_csv("./data_out/filtered_high_quality_directors.csv", index=False)
filtered_genres.to_csv("./data_out/filtered_high_quality_genres.csv", index=False)
filtered_grades.to_csv("./data_out/filtered_high_quality_grades.csv", index=False)
filtered_directors.to_csv("./data_out/filtered_high_quality_directors.csv", index=False)

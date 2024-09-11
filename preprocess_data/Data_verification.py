import pandas as pd

# 读取过滤后的数据
movies = pd.read_csv("./data_out/filtered_high_quality_movies.csv")
grades = pd.read_csv("./data_out/filtered_high_quality_grades.csv")
cast = pd.read_csv("./data_out/filtered_high_quality_cast.csv")
directors = pd.read_csv("./data_out/filtered_high_quality_directors.csv")
user_ratings = pd.read_csv("./data_out/filtered_high_quality_user_ratings.csv")
genres = pd.read_csv("./data_out/filtered_high_quality_genres.csv")

# 检查数据集中是否所有 tconst 都存在于所有文件中
movie_tconst_set = set(movies['tconst'])
grade_tconst_set = set(grades['tconst'])
cast_tconst_set = set(cast['tconst'])
director_tconst_set = set(directors['tconst'])
user_ratings_tconst_set = set(user_ratings['tconst'])
genre_tconst_set = set(genres['tconst'])

all_tconst_sets = [movie_tconst_set, grade_tconst_set, cast_tconst_set, director_tconst_set, user_ratings_tconst_set, genre_tconst_set]

# 计算交集
common_tconst = set.intersection(*all_tconst_sets)

# 打印检查结果
print(f"Number of common tconst across all datasets: {len(common_tconst)}")
print(f"Difference between movie tconst and common tconst: {len(movie_tconst_set - common_tconst)}")
print(f"Difference between grade tconst and common tconst: {len(grade_tconst_set - common_tconst)}")
print(f"Difference between cast tconst and common tconst: {len(cast_tconst_set - common_tconst)}")
print(f"Difference between director tconst and common tconst: {len(director_tconst_set - common_tconst)}")
print(f"Difference between user ratings tconst and common tconst: {len(user_ratings_tconst_set - common_tconst)}")
print(f"Difference between genre tconst and common tconst: {len(genre_tconst_set - common_tconst)}")

# 检查 cast 和 directors 中的 nconst 是否与 high-quality movies 的 tconst 一致
cast_movie_tconst_set = set(cast['tconst'])
director_movie_tconst_set = set(directors['tconst'])

print(f"Difference between cast movie tconst and movie tconst: {len(cast_movie_tconst_set - movie_tconst_set)}")
print(f"Difference between director movie tconst and movie tconst: {len(director_movie_tconst_set - movie_tconst_set)}")

# 检查 user_ratings 中的 userID 出现的次数
user_ratings_user_counts = user_ratings['userID'].value_counts()
print(f"Number of unique users in user ratings: {len(user_ratings_user_counts)}")

# 检查 user_ratings 中的 tconst 出现的次数
user_ratings_tconst_counts = user_ratings['tconst'].value_counts()
print(f"Number of unique movies in user ratings: {len(user_ratings_tconst_counts)}")

# 打印一些样本数据以检查数据完整性
print("Sample of filtered_movies:")
print(movies.head())
print("Sample of filtered_grades:")
print(grades.head())
print("Sample of filtered_cast:")
print(cast.head())
print("Sample of filtered_directors:")
print(directors.head())
print("Sample of filtered_user_ratings:")
print(user_ratings.head())
print("Sample of filtered_genres:")
print(genres.head())

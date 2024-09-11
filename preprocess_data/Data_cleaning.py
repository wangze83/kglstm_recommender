import pandas as pd

output_dir = "./data_out/"

# 读取数据
movies = pd.read_csv(output_dir+"out_movies.csv")
cast = pd.read_csv(output_dir+"out_cast.csv")
directors = pd.read_csv(output_dir+"out_directors.csv")
genres = pd.read_csv(output_dir+"out_genre.csv")
grades = pd.read_csv(output_dir+"out_grade.csv")
user_ratings = pd.read_csv(output_dir+"user_rating_temp.csv")

# 获取所有tconst集合
tconst_movies = set(movies['tconst'])
tconst_cast = set(cast['tconst'])
tconst_directors = set(directors['tconst'])
tconst_genres = set(genres['tconst'])
tconst_grades = set(grades['tconst'])
tconst_user_ratings = set(user_ratings['tconst'])

# 找到在所有文件中都存在的tconst
valid_tconst = tconst_movies & tconst_cast & tconst_directors & tconst_genres & tconst_grades & tconst_user_ratings

# 过滤数据
filtered_movies = movies[movies['tconst'].isin(valid_tconst)]
filtered_cast = cast[cast['tconst'].isin(valid_tconst)]
filtered_directors = directors[directors['tconst'].isin(valid_tconst)]
filtered_genres = genres[genres['tconst'].isin(valid_tconst)]
filtered_grades = grades[grades['tconst'].isin(valid_tconst)]
filtered_user_ratings = user_ratings[user_ratings['tconst'].isin(valid_tconst)]

# 保存过滤后的数据
filtered_movies.to_csv(output_dir+"filtered_out_movies.csv", index=False)
filtered_cast.to_csv(output_dir+"filtered_out_cast.csv", index=False)
filtered_directors.to_csv(output_dir+"filtered_out_directors.csv", index=False)
filtered_genres.to_csv(output_dir+"filtered_out_genre.csv", index=False)
filtered_grades.to_csv(output_dir+"filtered_out_grade.csv", index=False)
filtered_user_ratings.to_csv(output_dir+"filtered_user_rating_temp.csv", index=False)

print("过滤后的数据已保存至对应的CSV文件")

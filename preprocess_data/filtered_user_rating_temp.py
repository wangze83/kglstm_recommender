import pandas as pd

# 读取数据
user_ratings = pd.read_csv("../datasets/user_rating_temp.csv")

# 提取 reviewDate 中的年份并添加为新列
user_ratings['year'] = pd.to_datetime(user_ratings['reviewDate'], errors='coerce').dt.year

# 计算每个用户对每部电影的评价次数
rating_counts = user_ratings.groupby(['userID', 'tconst']).size().reset_index(name='count')

# 过滤掉评价次数不超过两次的数据
filtered_ratings = user_ratings.merge(rating_counts, on=['userID', 'tconst'])
filtered_ratings = filtered_ratings[filtered_ratings['count'] > 1]

# 删除辅助列 'count'
filtered_ratings = filtered_ratings.drop(columns=['count'])

# 只保留原始列加上年份列
filtered_ratings = filtered_ratings[['userID', 'tconst', 'rating', 'year']]

# 保存过滤后的数据
filtered_ratings.to_csv("./data_out/filtered_user_rating_temp.csv", index=False)

print("过滤后的数据已保存至 filtered_user_rating_temp.csv")

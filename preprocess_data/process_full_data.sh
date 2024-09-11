#!/bin/bash

# 定义数据集目录
DATASET_DIR="../datasets"

# 创建输出目录
mkdir -p data_out

# 过滤出电影类型数据
zcat "$DATASET_DIR/title.basics.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 == "movie") print $1, $3}' > data_out/out_movies.csv

# 处理导演信息
zcat "$DATASET_DIR/title.crew.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 != "\\N") print $1, $2}' | \
awk -F'\t' 'BEGIN {OFS="\t"} {split($2, directors, ","); for (i in directors) print $1, directors[i]}' > data_out/directors_temp.csv

# 合并导演姓名
zcat "$DATASET_DIR/name.basics.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2}' > data_out/names.csv
join -t $'\t' -1 2 -2 1 <(sort -k2 data_out/directors_temp.csv) <(sort -k1 data_out/names.csv) | \
awk -F'\t' 'BEGIN {OFS="\t"} {print $2, $3, $1}' > data_out/out_directors.csv

# 处理演员信息
zcat "$DATASET_DIR/title.principals.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $4 ~ /actor|actress/) print $1, $2}' | \
join -t $'\t' -1 2 -2 1 -o 1.1,1.2,2.2 <(sort -k2 data_out/names.csv) - | \
sort -k1,1 -k2,2 > data_out/out_cast.csv

# 提取电影评分信息
zcat "$DATASET_DIR/title.ratings.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2, $3}' > data_out/out_grade.csv

# 提取电影类型信息
awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 != "\\N") print $1, $2}' data_out/out_movies.csv > data_out/out_genre.csv

# 清理临时文件
rm data_out/directors_temp.csv
rm data_out/names.csv

echo "数据处理完成，生成了以下文件："
echo "1. out_movies.csv"
echo "2. out_directors.csv"
echo "3. out_cast.csv"
echo "4. out_grade.csv"
echo "5. out_genre.csv"

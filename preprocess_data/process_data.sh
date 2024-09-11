#!/bin/bash

# 定义数据集目录
DATASET_DIR="../datasets"
OUTPUT_DIR="./data_out"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 过滤出电影类型数据，包含 genres 字段
gunzip -c "$DATASET_DIR/title.basics.tsv.gz" | \
awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 == "movie") {if ($9 != "\\N") print $1, $3, $9}}' > "$OUTPUT_DIR/movies_temp.csv"

# 处理导演信息
gunzip -c "$DATASET_DIR/title.crew.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 != "\\N") print $1, $2}' | \
awk -F'\t' 'BEGIN {OFS="\t"} {split($2, directors, ","); for (i in directors) print $1, directors[i]}' > "$OUTPUT_DIR/directors_temp.csv"

# 处理演员信息
gunzip -c "$DATASET_DIR/title.principals.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $4 ~ /actor|actress/) print $1, $3}' > "$OUTPUT_DIR/cast_temp.csv"

# 提取电影评分信息
gunzip -c "$DATASET_DIR/title.ratings.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2, $3}' > "$OUTPUT_DIR/ratings_temp.csv"

# 提取演员和导演姓名
gunzip -c "$DATASET_DIR/name.basics.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2}' > "$OUTPUT_DIR/names_temp.csv"

echo "Shell部分处理完成，生成了中间文件："
echo "1. movies_temp.csv"
echo "2. directors_temp.csv"
echo "3. cast_temp.csv"
echo "4. ratings_temp.csv"
echo "5. names_temp.csv"

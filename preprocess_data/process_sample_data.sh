#!/bin/bash

# 定义数据集目录
DATASET_DIR="../datasets"
OUTPUT_DIR="./sampling_data_out"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 定义抽样比例
SAMPLE_FRACTION=0.01

# 过滤出电影类型数据并抽样
gunzip -c "$DATASET_DIR/title.basics.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 == "movie") print $1, $3}' | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/out_movies.csv"

# 处理导演信息并抽样
gunzip -c "$DATASET_DIR/title.crew.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 != "\\N") print $1, $2}' | \
awk -F'\t' 'BEGIN {OFS="\t"} {split($2, directors, ","); for (i in directors) print $1, directors[i]}' | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/directors_temp.csv"

# 合并导演姓名并抽样
gunzip -c "$DATASET_DIR/name.basics.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2}' > "$OUTPUT_DIR/names.csv"
join -t $'\t' -1 2 -2 1 <(sort -k2 "$OUTPUT_DIR/directors_temp.csv") <(sort -k1 "$OUTPUT_DIR/names.csv") | \
awk -F'\t' 'BEGIN {OFS="\t"} {print $2, $3, $1}' | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/out_directors.csv"

# 处理演员信息并抽样
gunzip -c "$DATASET_DIR/title.principals.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $4 ~ /actor|actress/) print $1, $2}' | \
join -t $'\t' -1 2 -2 1 -o 1.1,1.2,2.2 <(sort -k2 "$OUTPUT_DIR/names.csv") - | \
sort -k1,1 -k2,2 | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/out_cast.csv"

# 提取电影评分信息并抽样
gunzip -c "$DATASET_DIR/title.ratings.tsv.gz" | awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $1 != "\\N") print $1, $2, $3}' | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/out_grade.csv"

# 提取电影类型信息并抽样
awk -F'\t' 'BEGIN {OFS="\t"} {if (NR==1 || $2 != "\\N") print $1, $2}' "$OUTPUT_DIR/out_movies.csv" | \
awk -v fraction=$SAMPLE_FRACTION 'BEGIN {srand()} NR == 1 {print $0} NR > 1 {if (rand() <= fraction) print $0}' > "$OUTPUT_DIR/out_genre.csv"

# 清理临时文件
rm "$OUTPUT_DIR/directors_temp.csv"
rm "$OUTPUT_DIR/names.csv"

echo "代表性数据处理完成，生成了以下文件："
echo "1. out_movies.csv"
echo "2. out_directors.csv"
echo "3. out_cast.csv"
echo "4. out_grade.csv"
echo "5. out_genre.csv"

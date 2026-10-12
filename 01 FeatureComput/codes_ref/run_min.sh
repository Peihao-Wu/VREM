#!/bin/bash

# 获得当前脚本所在目录的绝对路径
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 定义输出文件路径
output_file="$script_dir/md_min.csv"

# 定义输入 CSV 文件路径
csv_files=(
    "$script_dir/min_pocket1.csv"
    "$script_dir/min_pocket2.csv"
    "$script_dir/min_pocket3.csv"
    "$script_dir/min_pocket4.csv"
    "$script_dir/min_pocket5.csv"
)

# 打印参数以确认
echo "Output file: $output_file"
echo "Input CSV files:"
printf "  %s\n" "${csv_files[@]}"


# 运行 Python 脚本并传递参数
python3 getmin2.py "$output_file" "${csv_files[@]}"
import pandas as pd
import numpy as np
import os
import argparse

def calculate_min(csv_files, output_file):
    # 读取所有 CSV 文件
    dfs = []
    for file in csv_files:
        if os.path.exists(file):
            df = pd.read_csv(file, index_col=0)
            dfs.append(df)
        else:
            print(f"Warning: File {file} does not exist. Skipping...")
    
    if not dfs:
        print("No valid CSV files provided. Exiting.")
        return
    
    # 确保所有 DataFrame 的索引和列名是字符串类型
    for df in dfs:
        df.index = df.index.astype(str)
        df.columns = df.columns.astype(str)
    
    # 检查所有 DataFrame 的索引和列是否一致
    base_df = dfs[0]
    for df in dfs[1:]:
        if not (df.index.equals(base_df.index) and df.columns.equals(base_df.columns)):
            print("Error: Index or columns of CSV files do not match. Please ensure all files have the same structure.")
            return
    
    # 将所有 DataFrame 的值堆叠成一个 3D 数组
    stacked = np.stack([df.values for df in dfs])
    
    # 使用 numpy 的 nanmin 函数计算每个位置的最小值，自动忽略 NaN
    df_min = pd.DataFrame(np.nanmin(stacked, axis=0), index=base_df.index, columns=base_df.columns)
    
    # 保存结果
    df_min.to_csv(output_file)
    print(f"Minimum values DataFrame saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the minimum values across multiple CSV files.")
    parser.add_argument("output_file", type=str, help="Output CSV file to save the minimum values.")
    parser.add_argument("csv_files", type=str, nargs='+', help="Input CSV files.")
    
    args = parser.parse_args()
    
    print("Starting the minimum value calculation script...")
    calculate_min(args.csv_files, args.output_file)
    print("Script execution completed.")
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import re
import argparse

def move_files(src_dir, dest_dir):
    print(f"Moving files from {src_dir} to {dest_dir}...")
    # 遍历源目录的所有二级目录，并建立进度条
    for root, dirs, files in tqdm(os.walk(src_dir), desc="Moving files"):
        # 遍历每个文件
        for file in files:
            # 构造源文件路径
            src_file = os.path.join(root, file)
            # 构造目标文件路径
            dest_file = os.path.join(dest_dir, file)
            # 移动文件
            os.rename(src_file, dest_file)
    print("Files moved successfully.")

def delete_empty_dirs(dir_path):
    print(f"Deleting empty directories in {dir_path}...")
    # 遍历目录，并建立进度条
    for root, dirs, files in tqdm(os.walk(dir_path), desc="Deleting empty directories"):
        # 如果目录为空，则删除
        if not dirs and not files:
            os.rmdir(root)
    print("Empty directories deleted successfully.")

def check_for_subdirectories(src_dir):
    # 检查源目录下是否存在二级文件夹
    for root, dirs, files in os.walk(src_dir):
        if dirs:  # 如果存在子目录
            return True
    return False

def main(src_dir, dest_dir, receptors_file, ligands_file, output_file):
    # 检查源目录下是否存在二级文件夹
    if check_for_subdirectories(src_dir):
        print("Secondary directories found. Proceeding with file moving and empty directory deletion.")
        # 移动文件
        move_files(src_dir, dest_dir)
        
        # 删除空文件夹
        delete_empty_dirs(dest_dir)
    else:
        print("No secondary directories found. Skipping file moving and empty directory deletion.")
    
    # 读取 receptors 和 ligands 文件
    print("Reading receptors and ligands files...")
    receptors = []
    ligands = []
    with open(receptors_file, 'r') as f:
        for line in f:
            receptors.append(line.strip())
    with open(ligands_file, 'r') as f:
        for line in f:
            ligands.append(line.strip())
    print(f"Loaded {len(receptors)} receptors and {len(ligands)} ligands.")
    
    # 创建空的 DataFrame
    df = pd.DataFrame(index=ligands, columns=receptors)
    print("Empty DataFrame created.")
    
    # 列举文件并处理
    print(f"Listing files in {dest_dir}...")
    files = os.listdir(dest_dir)
    files = pd.DataFrame(files, columns=['path'])
    files['path'] = files['path'].apply(lambda x: x.split('.')[0])
    files['receptor'] = files['path'].apply(lambda x: x.split('_')[0])
    files['ligand'] = files['path'].apply(lambda x: x.split('_')[1])
    
    # 修复 os.path.join 的问题
    files['full_path'] = files['path'].apply(lambda x: os.path.join(dest_dir, x + '.txt'))
    print(f"Generated full paths for {len(files)} files.")
    
    # 提取第 40 行的信息
    print("Extracting affinity data from files...")
    for index, row in tqdm(files.iterrows(), total=len(files), desc='Processing'):
        filename = row['full_path']
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 40:
                line_40 = lines[39].strip()
                files.at[index, 'affinity_unclean'] = line_40
    
    # 删除 affinity_unclean 为空值的行
    files = files[~files['affinity_unclean'].isnull()]
    print(f"Removed {len(files[files['affinity_unclean'].isnull()])} rows with missing affinity data.")
    
    # 去除多余信息
    files['affinity'] = files['affinity_unclean'].apply(lambda x: re.sub(r'^\d+\s+|\s+\d+\s+\d+$', '', x))
    files['affinity'] = files['affinity'].astype(float)
    print("Cleaned and converted affinity data.")
    
    # 确保索引和列名是字符串类型
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    
    # 填充 DataFrame
    print("Filling DataFrame with affinity data...")
    for index, row in tqdm(files.iterrows(), total=len(files), desc='Processing'):
        receptor = row['receptor']
        ligand = row['ligand']
        affinity = row['affinity']
        if ligand in df.index and receptor in df.columns:
            df.loc[ligand, receptor] = affinity
    
    # 计算空值数量
    print(f"Number of null values in DataFrame: {df.isnull().sum().sum()}")
    
    # 保存结果
    df.to_csv(output_file)
    print(f"DataFrame saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and organize docking results.")
    parser.add_argument("src_dir", type=str, help="Source directory containing nested directories with files.")
    parser.add_argument("dest_dir", type=str, help="Destination directory to move files to.")
    parser.add_argument("receptors_file", type=str, help="File containing receptor names.")
    parser.add_argument("ligands_file", type=str, help="File containing ligand names.")
    parser.add_argument("output_file", type=str, help="Output CSV file to save the affinity matrix.")
    
    args = parser.parse_args()
    
    print("Starting the processing script...")
    main(args.src_dir, args.dest_dir, args.receptors_file, args.ligands_file, args.output_file)
    print("Script execution completed.")
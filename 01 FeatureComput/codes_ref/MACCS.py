# -*- coding: utf-8 -*-
"""
Peihao Wu 2024/03/22
revision
"""
import pandas as pd
from rdkit import Chem
from rdkit.Chem import MACCSkeys

class MACCS:
    def __init__(self, smiles): # 初始化
        self.mols = [Chem.MolFromSmiles(i) for i in smiles] # 生成分子对象
        self.smiles = smiles # smiles列表

    def compute_MACCS(self, name): # 计算MACCS
        MACCS_list = [] # 用于存储MACCS特征
        header = ['bit' + str(i) for i in range(167)] # MACCS特征的列名
        for i in range(len(self.mols)): # 遍历每个分子
            ds = list(MACCSkeys.GenMACCSKeys(self.mols[i]).ToBitString()) # 计算MACCS特征
            MACCS_list.append(ds) # 存储MACCS特征
        df = pd.DataFrame(MACCS_list,columns=header) # 生成DataFrame
        df.insert(loc=0, column='smiles', value=self.smiles)  # 插入smiles列
        df.to_csv(name[:-4]+'_MACCS.csv', index=False) # 保存MACCS特征
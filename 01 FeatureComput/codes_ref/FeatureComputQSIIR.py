import time, os
import pandas as pd
from molvs import standardize_smiles
from rdkit import Chem
from MACCS import *
from RDKit_2D import *
from ECFP6 import *
from Mordred import *

# 如果没有desc文件夹，就创建一个
if not os.path.exists('desc'):
    os.makedirs('desc')
    
# 将上述过程合并为一个函数
# __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
def compute_desc(filename):
    df = pd.read_csv(filename)
    smiles = [standardize_smiles(i) for i in df['SMILES'].values]
    output_filename = 'desc' + filename[4:]
    myMACCS = MACCS(smiles)     # create your MACCS object and provide smiles
    myMACCS.compute_MACCS(output_filename) # compute MACCS Fingerprints and export file.
    myECFP6 = ECFP6(smiles)
    myECFP6.compute_ECFP6(output_filename)
    myRDKit = RDKit_2D(smiles)
    myRDKit.compute_2Drdkit(output_filename)
    mrc_descriptor = Macrocycle_Descriptors(smiles)
    mrc_descriptor.mordred_compute(output_filename)
    print("Descriptors have been computed and saved in desc folder.")
    
filename1 = "data/CAESAR.csv"
filename2 = "data/PG.csv"

if __name__ == '__main__':
    compute_desc(filename1)
    compute_desc(filename2)
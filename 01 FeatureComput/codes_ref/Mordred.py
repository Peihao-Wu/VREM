# -*- coding: utf-8 -*-
"""
Created on 2024/04/22

@author: WPH
"""

import itertools
import pandas as pd
from rdkit import Chem
from mordred import Calculator, descriptors

class Macrocycle_Descriptors:

    def __init__(self, smiles):
        self.mols = [Chem.MolFromSmiles(i) for i in smiles]
        self.smiles = smiles
        self.mordred = None

    def mordred_compute(self, name):
        calc = Calculator(descriptors, ignore_3D=True)
        self.mordred = calc.pandas(self.mols)
        self.mordred.insert(loc=0, column='smiles', value=self.smiles)
        self.mordred.to_csv(name[:-4]+'_Mordred.csv', index=False)

import pandas as pd
import pubchempy as pcp
import time
from rdkit.Chem.MolStandardize.rdMolStandardize import StandardizeSmiles

# df = pd.read_csv('./DILI/DILI_notProcessed.csv')
df = pd.read_csv('./DILI/Name_only_DILI.csv')

def standardize(smiles):
    if smiles != 'none':
        try:
            s_smiles = StandardizeSmiles(smiles)
            print(".",end="")
        except Exception as e:
            print(e,'\t',name,'\n')
            s_smiles = None
    else:
        s_smiles = None
    return s_smiles

    
def get_smiles(name):
    try:
        smiles = pcp.get_compounds(name, namespace='name', as_dataframe=True)['canonical_smiles'].values[0]
        print(".",end="")
    except Exception as e:
        print(e,'\t',name,'\n')
        smiles = 'none'
    return smiles
        

begin = time.time()
name_list = pd.Series(list(df['Name']))
df['SMILES'] = name_list.map(get_smiles)
smiles_list = pd.Series(list(df['SMILES']))
df['Canonical_SMILES'] = smiles_list.map(standardize)
end = time.time()

elapsed = end - begin

print(elapsed)
df
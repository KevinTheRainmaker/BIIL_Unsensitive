import pandas as pd

def dropDupl(df):
    grouped = df.iloc[:,-1].groupby(df['Canonical_SMILES'])
    std = grouped.std().to_frame('std')
    mean = grouped.mean().to_frame('mean')
    temp = pd.merge(std, mean, on='Canonical_SMILES', how='outer')
    filtering = pd.merge(a, temp, on='Canonical_SMILES', how='outer')
    filtering['std'].fillna(0, inplace=True)
    name = df.columns[-1]
    for i,row in filtering.iterrows():
        if filtering.at[i, 'std'] < 0.05:
            filtering.at[i,f'{name}'] = filtering.at[i,'mean']
            filtering.at[i,'status'] = '1'
        else:
            filtering.at[i,'status'] = '0'
            
    final = filtering.loc[filtering['status']=='1'].drop_duplicates('Canonical_SMILES')[['Canonical_SMILES',f'{name}']]
    final.reset_index(inplace=True, drop=True)
    final.to_csv(f'./drop/{name}.csv')


a = pd.read_csv('./canonical/IC50_canonicalized.csv',  index_col=0)
b = pd.read_csv('./canonical/EC50_canonicalized.csv',  index_col=0)
c = pd.read_csv('./canonical/Ki_canonicalized.csv',  index_col=0)
d = pd.read_csv('./canonical/IP_canonicalized.csv',  index_col=0)
e = pd.read_csv('./canonical/Inhibition_canonicalized.csv', index_col=0)
f = pd.read_csv('./canonical/Kd_canonicalized.csv', index_col=0)
g = pd.read_csv('./canonical/hERG_Inhibition_1uM_canonicalized.csv',index_col=0)
h = pd.read_csv('./canonical/hERG_Inhibition_10uM_canonicalized.csv',index_col=0)
i = pd.read_csv('./canonical/pIC50_canonicalized.csv', index_col=0)

for df in [a,b,c,d,e,f,g,h,i]:
    dropDupl(df)


a = pd.read_csv('./drop/IC50(uM).csv', low_memory=False, index_col=0)
b = pd.read_csv('./drop/EC50(uM).csv', low_memory=False, index_col=0)
c = pd.read_csv('./drop/Ki(uM).csv', low_memory=False, index_col=0)
d = pd.read_csv('./drop/IP(uM).csv', low_memory=False, index_col=0)
e = pd.read_csv('./drop/Inhibition(%).csv', low_memory=False, index_col=0)
f = pd.read_csv('./drop/Kd(uM).csv', low_memory=False, index_col=0)
g = pd.read_csv('./drop/hERG inhibition (%) at 1uM.csv', low_memory=False, index_col=0)
h = pd.read_csv('./drop/hERG inhibition (%) at 10uM.csv', low_memory=False, index_col=0)
i = pd.read_csv('./drop/pIC50.csv', low_memory=False, index_col=0)

result = a
for df in [b,c,d,e,f,g,h,i]:
    result = pd.merge(result, df, on='Canonical_SMILES', how='outer')

result.reset_index(inplace=True)
result.reset_index(inplace=True)
name = 'BIIL_hERG'
result['name'] = name
result['index'] = result['index'].astype(str)
result['index'] = result['index'].apply(lambda x: x.zfill(6))
result['ID'] = (result['name'] + result['index'])

final = result[['ID','Canonical_SMILES','IC50(uM)','EC50(uM)','Ki(uM)','IP(uM)','Inhibition(%)','Kd(uM)','hERG inhibition (%) at 1uM','hERG inhibition (%) at 10uM','pIC50']]

final.to_csv('./hERG_FINAL.csv')
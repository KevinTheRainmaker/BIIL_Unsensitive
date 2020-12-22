import pandas as pd
import numpy as np
import pubchempy as pcp
import time
import multiprocessing #멀티프로세싱
df = pd.read_csv('./333SMILES_re.csv') #cid 데이터 로드
def cid_to_smiles(cid):
    flag = False
    while not flag: #무한루프
        try:
            com = pcp.Compound.from_cid(cid)
            flag = True
        except Exception as e:
            print("cid failed")
            flag = False
            time.sleep(1) #1초 쉬기
    com_smiles = com.canonical_smiles
    time.sleep(0.5)
    return com_smiles #str 반환
cid_list = list(df['PubChem CID']) #cid를 list로 가져오기
output_dict = {} #빈 딕셔너리 생성
n = len(cid_list)//1000 #리스트를 1000으로 나눈 몫 저장
for i in range(n):
    example = './333/MP_SMILES'+'_'.join(["{}"])+'.csv'
    filename= example.format(i+1) #포맷팅 사용하여 중간중간 저장을 위한 파일네임 형성
    pool = multiprocessing.Pool(processes=3) #프로세서 3개 사용
    smiles = pool.map(cid_to_smiles, cid_list[i*1000:(i+1)*1000])
    cid_smiles_dict = dict(zip(cid_list[i*1000:(i+1)*1000], smiles)) #cid_smiles_dict라는 이름으로 딕셔너리 형성
    output_dict.update(cid_smiles_dict) #out_put_dict에 업데이트
    DF = pd.DataFrame.from_dict(output_dict, orient='index', columns=['SMILES']) #딕셔너리를 데이터프레임으로 변환
    #첫 번째 column에 cid, 두 번째 column에 SMILES 저장
    DF.to_csv(filename) #데이터프레임을 csv파일로 저장
#     pickle.dump(output_dict, f)를 사용할 수도 있음 - 나중에 공부해 볼 것! (edited) 
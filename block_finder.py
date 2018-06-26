import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time

def find_lots():
    df = pd.read_csv('ACRIS_-_Personal_Property_Legals.csv')

    df_mhn = df[df['BOROUGH'] == 1]
    df_brx = df[df['BOROUGH'] == 2]
    df_bkn = df[df['BOROUGH'] == 3]
    df_qns = df[df['BOROUGH'] == 4]
    df_stn = df[df['BOROUGH'] == 5] #no values?

    brx_blocks = sorted(df_brx['BLOCK'].unique())
    brx_brh = []
    brx_blk = []
    brx_lot = []
    for i in brx_blocks:
        for j in range(len(df_brx[df_brx['BLOCK'] == i]['LOT'].unique())):
            brx_brh.append(1)
            brx_blk.append(str(i).zfill(5))
            brx_lot.append(str(df_brx[df_brx['BLOCK'] == i]['LOT'].unique()[j]).zfill(4))
    return brx_brh, brx_blk, brx_lot

def one_lot(borough, block, lot):
    url = "http://webapps.nyc.gov:8084/CICS/f704/f403001I?BBL={0}-{1}-{2}-".format(borough, block, lot)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    table = []

    if len(soup) <= 4:
        table = np.array([borough, block, lot, 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'])
        df = pd.DataFrame(table).T
        df.columns = ['Borough', 'Block', 'Lot', 'Account_Type', 'Account_ID', 'Period_Begin_Date', 'Due_Date', 'Period_End_Date', 'Interest_Begin_Date', 'Period_Balance', 'Assessed_Value']
    else:
        rows = range(len(soup.find_all('tr')))
        k = 0

        while k < 9:
            rows.remove(rows[-1])
            k += 1


        for j in range(21):
            rows.remove(j)

        for i in rows:
            table.extend([borough, block, lot])
            for t in range(1, 9):
                schtuff = soup.find_all('tr')[i].find_all('td')[t].text.strip('\n\t\r').strip(' ')
                if schtuff == u'\xa0':
                    schtuff = 'null'
                if len(schtuff) >= 35:
                    schtuff = schtuff[:-35]
                table.append(schtuff)

        table = np.array(table).reshape(len(rows), 11)
        df = pd.DataFrame(table, columns=['Borough', 'Block', 'Lot', 'Account_Type', 'Account_ID', 'Period_Begin_Date', 'Due_Date', 'Period_End_Date', 'Interest_Begin_Date', 'Period_Balance', 'Assessed_Value'])
    return df

if __name__ == '__main__':
    brx_deal = pd.read_csv('redos.csv')
    brx_brh = brx_deal['Borough']
    print('First:')
    for i in range(len(brx_brh)):
        brx_brh[i] = str(brx_brh[i])
        print('Borough: {0} out of {1}'.format(i, len(brx_brh)))
    brx_blk = brx_deal['Block']
    for i in range(len(brx_blk)):
        brx_blk[i] = str(brx_blk[i]).zfill(5)
        print('Block: {0} out of {1}'.format(i, len(brx_blk)))
    brx_lot = brx_deal['Lot']
    for i in range(len(brx_lot)):
        brx_lot[i] = str(brx_lot[i]).zfill(4)
        print('Lot: {0} out of {1}'.format(i, len(brx_lot)))
    brx_brh = list(brx_brh)
    brx_blk = list(brx_blk)
    brx_lot = list(brx_lot)
    # brx_brh.remove(brx_brh[0])
    # brx_blk.remove(brx_blk[0])
    # brx_lot.remove(brx_lot[0])
    df = one_lot(brx_brh[0], brx_blk[0], brx_lot[0])
    brx_brh.remove(brx_brh[0])
    brx_blk.remove(brx_blk[0])
    brx_lot.remove(brx_lot[0])
    for i in range(162358):
        df2 = one_lot(brx_brh[i], brx_blk[i], brx_lot[i])
        df = df.append(df2, ignore_index=True)
        print('{0} out of {1}'.format(i, len(brx_lot)))
    print('AAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!!!')

# u'.00\n\n \xa0\xa0\xa0\xa0'

# brx_blocks = sorted(df_brx['BLOCK'].unique())
# brx_list = []
# for i in brx_blocks:
#     brx_list.append('BLOCK {0}: {1}'.format(i, sorted(df_brx[df_brx['BLOCK'] == i]['LOT'].unique())))
#
# bkn_blocks = sorted(df_bkn['BLOCK'].unique())
# bkn_list = []
# for i in bkn_blocks:
#     bkn_list.append('BLOCK {0}: {1}'.format(i, sorted(df_bkn[df_bkn['BLOCK'] == i]['LOT'].unique())))
#
# qns_blocks = sorted(df_qns['BLOCK'].unique())
# qns_list = []
# for i in qns_blocks:
#     qns_list.append('BLOCK {0}: {1}'.format(i, sorted(df_qns[df_qns['BLOCK'] == i]['LOT'].unique())))

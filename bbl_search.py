import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import time

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
    df = one_lot(mhn_brh[0], mhn_blk[0], mhn_lot[0])
    mhn_brh.remove(mhn_brh[0])
    mhn_blk.remove(mhn_blk[0])
    mhn_lot.remove(mhn_lot[0])
    for i in range(len(mhn_lot)):
        df2 = one_lot(mhn_brh[i], mhn_blk[i], mhn_lot[i])
        df = df.append(df2, ignore_index=True)
        print(mhn_brh[i], mhn_blk[i], mhn_lot[i])

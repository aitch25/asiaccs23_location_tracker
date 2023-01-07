import os
import sys
import numpy as np
import pandas as pd
from time import sleep 
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

from dtw import *
from scipy.signal import medfilt

from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler

from copy import deepcopy
from random import randint


class Path_Analyzer:
    def mod(self, a, b):
        return float(a) % float(b)

    def get_station_timegap(self, mDuration, mTimegap, mAlpha_mins=5):
        oMax_minutes = np.round(int(mDuration)/(20*60)) + mAlpha_mins

        mTimegap['line'] = mTimegap['filename'].copy()
        mTimegap['line'] = mTimegap['line'].replace('line_01_1', '01호선')
        mTimegap['line'] = mTimegap['line'].replace('line_01_2', '01호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02', '02호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03', '03호선')
        mTimegap['line'] = mTimegap['line'].replace('line_04', '04호선')
        mTimegap['line'] = mTimegap['line'].replace('line_05_1', '05호선')
        mTimegap['line'] = mTimegap['line'].replace('line_05_2', '05호선')
        mTimegap['line'] = mTimegap['line'].replace('line_06', '06호선')
        mTimegap['line'] = mTimegap['line'].replace('line_07', '07호선')
        mTimegap['line'] = mTimegap['line'].replace('line_08', '08호선')
        mTimegap['line'] = mTimegap['line'].replace('line_09', '09호선')

        mTimegap['line'] = mTimegap['line'].replace('line_bds', '분당선')
        mTimegap['line'] = mTimegap['line'].replace('line_sbds', '신분당선')
        mTimegap['line'] = mTimegap['line'].replace('line_center', '경의중앙선')

        mTimegap['line'] = mTimegap['line'].replace('line_01_busan', '부산1호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02_busan', '부산2호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03_busan', '부산3호선')
        mTimegap['line'] = mTimegap['line'].replace('line_04_busan', '부산4호선')
        mTimegap['line'] = mTimegap['line'].replace('line_donghae_busan', '동해선')

        mTimegap['line'] = mTimegap['line'].replace('line_01_daegu', '대구1호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02_daegu', '대구2호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03_daegu', '대구3호선')
        
        mTimegap['line'] = mTimegap['line'].replace('line_01_daejeon', '대전1호선') 

        mTimegap['line'] = mTimegap['line'].replace('line_01_incheon', '인천1호선') 
        mTimegap['line'] = mTimegap['line'].replace('line_02_incheon', '인천2호선') 



        oTimegap = pd.DataFrame()
        for i in range(mTimegap.shape[0]):
            for j in range(i, mTimegap.shape[0]):
                if mTimegap[i:j+1]['mins'].sum()>=oMax_minutes: 
                    oTmp = mTimegap[i:j+1]
                    oTmp['id'] = mTimegap.values[i][0] + ':' + mTimegap.values[j][1]
                    if oTimegap.empty:
                        oTimegap = oTmp.copy()
                    else:
                        oTimegap = oTimegap.append(oTmp)
                    break

        return oTimegap


    def get_station_timegap_ngram(self, mTimegap, mLen=3):

        mTimegap['line'] = mTimegap['filename'].copy()
        mTimegap['line'] = mTimegap['line'].replace('line_01_1', '01호선')
        mTimegap['line'] = mTimegap['line'].replace('line_01_2', '01호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02', '02호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03', '03호선')
        mTimegap['line'] = mTimegap['line'].replace('line_04', '04호선')
        mTimegap['line'] = mTimegap['line'].replace('line_05_1', '05호선')
        mTimegap['line'] = mTimegap['line'].replace('line_05_2', '05호선')
        mTimegap['line'] = mTimegap['line'].replace('line_06', '06호선')
        mTimegap['line'] = mTimegap['line'].replace('line_07', '07호선')
        mTimegap['line'] = mTimegap['line'].replace('line_08', '08호선')
        mTimegap['line'] = mTimegap['line'].replace('line_09', '09호선')

        mTimegap['line'] = mTimegap['line'].replace('line_bds', '분당선')
        mTimegap['line'] = mTimegap['line'].replace('line_sbds', '신분당선')
        mTimegap['line'] = mTimegap['line'].replace('line_center', '경의중앙선')

        mTimegap['line'] = mTimegap['line'].replace('line_01_busan', '부산1호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02_busan', '부산2호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03_busan', '부산3호선')
        mTimegap['line'] = mTimegap['line'].replace('line_04_busan', '부산4호선')
        mTimegap['line'] = mTimegap['line'].replace('line_donghae_busan', '동해선')

        mTimegap['line'] = mTimegap['line'].replace('line_01_daegu', '대구1호선')
        mTimegap['line'] = mTimegap['line'].replace('line_02_daegu', '대구2호선')
        mTimegap['line'] = mTimegap['line'].replace('line_03_daegu', '대구3호선')
        
        mTimegap['line'] = mTimegap['line'].replace('line_01_daejeon', '대전1호선') 

        mTimegap['line'] = mTimegap['line'].replace('line_01_incheon', '인천1호선') 
        mTimegap['line'] = mTimegap['line'].replace('line_02_incheon', '인천2호선') 


        oTimegap = pd.DataFrame()
        for i in range(mTimegap.shape[0]-(mLen-1)):
            oTmp = mTimegap[i:i+mLen]
            oTmp['id'] = mTimegap.values[i][0] + ':' + mTimegap.values[i+(mLen-1)][1]
            if oTimegap.empty:
                oTimegap = oTmp.copy()
            else:
                oTimegap = oTimegap.append(oTmp)
            #break

        return oTimegap

    def get_station_seq(self, mStation_seq, mLine):
        mStation_seq.sort()
        if len(mStation_seq) == 2:
            return [(mStation_seq[0], mStation_seq[1])]
        elif len(mStation_seq)>2:
            return [(mStation_seq[0], mStation_seq[1]), (mStation_seq[1], mStation_seq[2])]



    def get_paths(self, mSrc, mDst, mLine, mPath_len=5):
    
        #print(os.system('pwd'))
        oTimegap_path = './input/timegap/subways/'
        oTimegap_files = os.listdir(oTimegap_path)
        #print(oTimegap_files)
        #exit()
        oTimegap_files.sort()
    
        oCandidate_ans = list()
        for tg_file in oTimegap_files[:]:
            #print('a:t', mLine, tg_file)
            if mLine in tg_file:
                atimegap = pd.read_csv(oTimegap_path + tg_file)
                #print('a:t', atimegap)
                atimegap['filename'] = tg_file.split('.')[0]
                atimegap = atimegap[['srcs', 'filename']].append(atimegap[['dsts', 'filename']].rename(columns={'dsts':'srcs'})[-1:])
                atimegap = atimegap.reset_index()[['srcs', 'filename']].rename(columns={'srcs':'stations'})
                atimegap['index'] = atimegap.index
                atimegap = atimegap[['index', 'stations', 'filename']]
    
                #print('src', tg_file, mSrc, atimegap['stations'].values)
                #print('dst', tg_file, mDst, atimegap['stations'].values)
    
                if (mSrc in atimegap['stations'].values) & (mDst in atimegap['stations'].values):
                    src = atimegap[atimegap['stations']==mSrc]['index'].values
                    dst = atimegap[atimegap['stations']==mDst]['index'].values
                    station_idx = list()
                    [station_idx.append(s) for s in src]
                    [station_idx.append(d) for d in dst]
    
                    idxs = self.get_station_seq(station_idx, atimegap)
                    for idx in idxs:
                        at = atimegap[idx[0]:idx[1]+1]['stations'].values
                        at += mLine
                        oCandidate_ans.append(list(at))
    
        #oCandidate_ans.sort(key=len)
        #return np.unique(oCandidate_ans)
        oCandidate_ans = np.unique(oCandidate_ans)
        oCandidate_ans = sorted(oCandidate_ans, key=len)
        #print('candi', oCandidate_ans)
    
        if len(oCandidate_ans)==0:
            return list()
        elif type(oCandidate_ans[0])==list:
            for oc in oCandidate_ans:
                if len(oc)==mPath_len:
                    return oc
                elif (len(oc)-1)==mPath_len:
                    return oc
                elif (len(oc)+1)==mPath_len:
                    return oc
                elif (len(oc)-2)==mPath_len:
                    return oc
                elif (len(oc)+2)==mPath_len:
                    return oc
                else:
                    return oCandidate_ans[0] # need to fix 220504
        else:
            return oCandidate_ans

    
    def calc_angle(self, mIntSec, mVec1, mVec2):
    
        mVec1[0] = mVec1[0] - mIntSec[0]
        mVec1[1] = mVec1[1] - mIntSec[1]
    
        mVec2[0] = mVec2[0] - mIntSec[0]
        mVec2[1] = mVec2[1] - mIntSec[1]

        mVec1[0] += np.finfo(float).eps
        mVec1[1] += np.finfo(float).eps
        mVec2[0] += np.finfo(float).eps
        mVec2[1] += np.finfo(float).eps
    
    
        if (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 1, 1
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >=0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 2, 2
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 3, 3
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 4, 4
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 1, 2
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            #retAng = mod(retAng, 360)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 2, 1
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 1, 3
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng > 180:
                retAng = -(360-retAng)
    
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 3, 1
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng =(v2Ang - v1Ang)
            if retAng < -180:
                retAng = (360+retAng)
    
        elif (mVec1[0] >= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 1, 4
            v1Ang = abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = -(360-(v2Ang - v1Ang))
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] >= 0): # quad 4, 1
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = 360+(v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 2, 3
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 3, 2
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
            ##################################
    
        elif (mVec1[0] <= 0) & (mVec1[1] >= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 2, 4
            v1Ang = 180 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng > 180:
                retAng = -(360-retAng)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] >= 0): # quad 4, 2
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
            if retAng < -180:
                retAng = 360+retAng
    
    
        elif (mVec1[0] <= 0) & (mVec1[1] <= 0) & (mVec2[0] >= 0) & (mVec2[1] <= 0): # quad 3, 4
            v1Ang = 180 + abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 360 - abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        elif (mVec1[0] >= 0) & (mVec1[1] <= 0) & (mVec2[0] <= 0) & (mVec2[1] <= 0): # quad 4, 3
            v1Ang = 360 - abs(np.degrees(np.arctan(mVec1[1] / mVec1[0])))
            v2Ang = 180 + abs(np.degrees(np.arctan(mVec2[1] / mVec2[0])))
    
            retAng = (v2Ang - v1Ang)
    
        if abs(retAng) == 180.0:
            retAng = 0.0
        elif retAng > 0:
            retAng = (180.0 - retAng)
        elif retAng < 0:
            retAng = -(180.0 + retAng)
    
        #print(retAng)
        return retAng
    
    
    def tune_adj_matrix_2d(self, mVec_tmp, mVec, mOVec, mErr):
        
        oOVec = mOVec.copy()
    
        for i in range(len(mVec)):
            oZeros_idx = list()
            oZeros_ang = dict()

            for j in range(len(mVec[i])):
                if (float(mVec_tmp[i][j].split(':')[0]) <= mErr) & (float(mVec_tmp[i][j].split(':')[0]) >= -mErr):
                    oZeros_idx.append(j)
                    oZeros_ang[j] = float(mVec[i][j].split(':')[0])

    
            for j in oZeros_idx:
                for k in range(len(mVec)):
                    if (float(mVec[i][k].split(':')[0]) == np.inf) & (float(oOVec[j][k].split(':')[0]) != np.inf):
                        mVec_tmp[i][k] = str(float(oOVec[j][k].split(':')[0])) + ':' + str(mVec[i][j].split(':')[1])[0] + str(oOVec[j][k].split(':')[1])[1]
                        mVec[i][k] = str(float(oOVec[j][k].split(':')[0]) + oZeros_ang[j]) + ':' + str(mVec[i][j].split(':')[1])[0] + str(oOVec[j][k].split(':')[1])[1]

        return mVec_tmp, mVec

    
    def get_adjacency_matrix(self, mVec):
        oAd_Mat = list()
        
        for i in range(mVec.shape[0]):
            oAd_Mat.append(list())
            for j in range(mVec.shape[0]):
                oAd_Mat[i].append(str(np.inf) + ':')
    
        X1 = mVec['src_x'].values
        Y1 = mVec['src_y'].values
        X2 = mVec['dst_x'].values
        Y2 = mVec['dst_y'].values
    
        for i in range(mVec.shape[0]):
            for j in range(mVec.shape[0]):
                if i==j: 
                    oAd_Mat[i][j] = '180.0:'
                    
                if ((X1[i] == X1[j]) & (Y1[i] == Y1[j])):
                    oAd_Mat[i][j] = str(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X2[j], Y2[j]])) + ':ss'
                     
                elif ((X1[i] == X2[j]) & (Y1[i] == Y2[j])):
                    oAd_Mat[i][j] = str(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X1[j], Y1[j]])) + ':sd'
                    
                elif ((X2[i] == X1[j]) & (Y2[i] == Y1[j])):
                    oAd_Mat[i][j] = str(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[j], Y2[j]])) + ':ds'
                     
                elif ((X2[i] == X2[j]) & (Y2[i] == Y2[j])):
                    oAd_Mat[i][j] = str(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X1[j], Y1[j]])) + ':dd'
    
        return oAd_Mat
    
    def get_adjacency_sequence(self, mVec, mErr):

        X1 = mVec['src_x'].values
        Y1 = mVec['src_y'].values
        X2 = mVec['dst_x'].values
        Y2 = mVec['dst_y'].values

        oAd_seq = list()
        for i in range(mVec.shape[0]):
            for j in range(i+1, mVec.shape[0]):
                    
                if ((X1[i] == X1[j]) & (Y1[i] == Y1[j])):
                    if abs(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X2[j], Y2[j]])) > mErr:
                        oAd_seq.append(str(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X2[j], Y2[j]])) + ':ss')
                     
                elif ((X1[i] == X2[j]) & (Y1[i] == Y2[j])):
                    if abs(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X1[j], Y1[j]])) > mErr:
                        oAd_seq.append(str(self.calc_angle([X1[i], Y1[i]], [X2[i], Y2[i]], [X1[j], Y1[j]])) + ':sd')
                    
                elif ((X2[i] == X1[j]) & (Y2[i] == Y1[j])):
                    if abs(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[j], Y2[j]])) > mErr:
                        oAd_seq.append(str(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[j], Y2[j]])) + ':ds')
                     
                elif ((X2[i] == X2[j]) & (Y2[i] == Y2[j])):
                    if abs(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X1[j], Y1[j]])) > mErr:
                        oAd_seq.append(str(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X1[j], Y1[j]])) + ':dd')
    
        return oAd_seq


    def drop_seq_dups(self, mVec):

        oCur = 0
        oData = list()
        for i in range(len(mVec)):
            if not mVec[oCur] == mVec[i]:
                oData.append(mVec[oCur])
                oCur = i

        return oData

    def into_bins(self, mData, mBin_gap=2):
        oBins = list(range(-360, 360+mBin_gap, mBin_gap))
        oData = list()
        
        for d in mData:
            for i in range(len(oBins)-1):
                if (oBins[i] < d) & (oBins[i+1] > d):
                    oData.append(float((oBins[i] + oBins[i+1])/2))

        oData = self.drop_seq_dups(oData)
           
        return oData


    def target_scaler(self, mData):
        #oMin = mScale[0]
        #oMax = mScale[1]

        for i in range(len(mData)):
            if mData[i] >= 0:
                mData[i] = mData[i] - 360.
            #elif mData[i] < 0:
            #    mData[i] = mData[i] + 360.
        
        return mData

    def adjusting_sig_pos(self, mStraights, mVec):

        #oVec = mVec.copy() #pd.Series(mVec)

        oStraights_pair = list()
        for i in range(len(mStraights)-1):
            if (mStraights[i]+mStraights[i+1]) == 1:
                oStraights_pair.append(i+1)

        oStraights_on = list() 
        oStraight_pair = list()
        for straight in oStraights_pair[1:-1]:
            if len(oStraight_pair) < 2:
                oStraight_pair.append(straight)
            else:
                oStraights_on.append(oStraight_pair)
                oStraight_pair = list()


        for straight in oStraights_on:
            if mVec[straight[0]] - mVec[straight[1]] > 180.:
                oMin = mVec[straight[1]] + 360
                oMax = mVec[straight[0]]

                if oMin < oMax:
                    oScaler = MinMaxScaler((oMin, oMax))
                elif oMin > oMax:
                    oScaler = MinMaxScaler((oMax, oMin))
                else:
                    oScaler = MinMaxScaler((oMin, oMin+0.00000000001))

                #print(oMin, oMax)
                mVec[straight[0]:straight[1]] = oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1)[0]
                mVec[straight[1]:] = [val+360. for val in mVec[straight[1]:]] 

            elif mVec[straight[1]] - mVec[straight[0]] > 180.:
                oMin = mVec[straight[0]]
                oMax = mVec[straight[1]] - 360
                if oMin < oMax:
                    oScaler = MinMaxScaler((oMin, oMax))
                elif oMin > oMax:
                    oScaler = MinMaxScaler((oMax, oMin))
                else:
                    oScaler = MinMaxScaler((oMin, oMin+0.00000000001))

                #print(mVec[straight[0]:straight[1]])
                #print(oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1))
                mVec[straight[0]:straight[1]] = oScaler.fit_transform(np.array(mVec[straight[0]:straight[1]]).reshape(-1, 1)).reshape(1, -1)[0]

                mVec[straight[1]:] = [val-360. for val in mVec[straight[1]:]] 

        return mVec


    def get_continuous_sequence(self, mVec):
        X1 = mVec['src_x'].values
        Y1 = mVec['src_y'].values
        X2 = mVec['dst_x'].values
        Y2 = mVec['dst_y'].values

        oAd_seq = [0]
        for i in range(mVec.shape[0]-1):
            oDist = distance.euclidean((X1[i], Y1[i]), (X2[i], Y2[i])) 

            oZero_pad = [oAd_seq[-1] for _ in range(round(oDist))] 
            oAd_seq.extend(oZero_pad)
            oAd_seq.append(oAd_seq[-1] + float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]])))
            #if abs(oAd_seq[-1] - float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]]))) > 180:
            #    oAd_seq.append(oAd_seq[-1] + (float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]]))-180))
            #else:
            #    oAd_seq.append(oAd_seq[-1] + float(self.calc_angle([X2[i], Y2[i]], [X1[i], Y1[i]], [X2[i+1], Y2[i+1]])))


        return medfilt(oAd_seq, 25)



    
    def search_path(self, mPPath, mFPath, mErr):
        # mPPath : Partial Path
        # mFPath : Full Path
    
        #oPPath = mPPath.split('>')
        oPPath = mPPath.copy()
        oFPath = mFPath.copy()
    
        oRecursive_Path = dict()
    
        for i, angle in enumerate(oPPath):
            oRecursive_Path[str(i) + '_loop'] = list()
            for j in list(range(len(oFPath))):
                for k, angle_map in enumerate(oFPath[j]):
                    if (float(angle) < (float(angle_map.split(':')[0])+float(mErr))) & (float(angle) > (float(angle_map.split(':')[0])-float(mErr))):
                        #print(angle, angle_map)
                        oRecursive_Path[str(i) + '_loop'].append([j, k])
    
        
        oCur_Path = list()
        oCur_Filtered = list()
    
        for pair in oRecursive_Path['0_loop']:
            oCur_Path.append(pair)
        
        for i in range(1, len(oPPath)):
            for pair1 in oCur_Path:
                if len(pair1) == (i+1):
                    oCur_Filtered.append(pair1)
    
            for pair1 in oCur_Filtered:
                for pair2 in oRecursive_Path[str(i) + '_loop']:
                    oCur_Path2 = list()
                    if (float(mFPath[pair1[-2]][pair2[1]].split(':')[0])==np.inf) & ((pair1[-1]==pair2[0]) & (pair1[-2]!=pair2[1])) & (str(oFPath[pair1[-2]][pair1[-1]].split(':')[1])[1] != (str(oFPath[pair2[0]][pair2[1]].split(':')[1])[0])):
                        for p1 in pair1:
                            oCur_Path2.append(p1)
                        oCur_Path2.append(pair2[1])
                        oCur_Path.append(oCur_Path2)
    
    
        oRet_list = list()
        for pl in oCur_Path:
            if len(pl) == len(oPPath)+1:
                oRet_list.append(pl)
    
        
        if len(oRet_list):
            return oRet_list
        else:
            return list()

    
    def matched_path_with_suffix(self, mPatch_ang, mTemplate_ang, mErr):
        if ((float(mPatch_ang)>0) & (float(mTemplate_ang.split(':')[0])>0)) | ((float(mPatch_ang)<0) & (float(mTemplate_ang.split(':')[0])<0)):
            if abs(float(mPatch_ang)-float(mTemplate_ang.split(':')[0])) < mErr:
                return True
            else:
                return False
        else:
            return False

    def matched_path(self, mPatch_ang, mTemplate_ang, mErr):
        if ((float(mPatch_ang)>0) & (float(mTemplate_ang)>0)) | ((float(mPatch_ang)<0) & (float(mTemplate_ang)<0)):
            if abs(float(mPatch_ang)-float(mTemplate_ang)) < mErr:
                return True
            else:
                return False
        else:
            return False

    def search_path_discrete_bus(self, mSeq, mFPath, mNgram, mErr):
        oNgram_lst = list()
        for i in range(len(mSeq)-(mNgram)):
            oNgram_lst.append(mSeq[i:i+(mNgram)])

        oRetFlag = False
        oRetLst = list()
        for ngram in oNgram_lst:
            #print(mFPath[:len(mFPath)-(mNgram-1)])
            for i, ang in enumerate(mFPath[:len(mFPath)-(mNgram-1)]):
                if self.matched_path(ngram[0], ang, mErr):
                    if mNgram==1:
                        oRetFlag = True
                    #print(i+1, i+(mNgram+1)) 
                    for j, ang_idx in enumerate(range(i+1, i+(mNgram))):
                        #print(j+1, ang_idx)
                        #print(ngram[j+1], mFPath[ang_idx])
                        #print(ngram[j+1])
                        if self.matched_path(ngram[j+1], mFPath[ang_idx], mErr):
                            oRetFlag = True
                        else: 
                            oRetFlag = False
                            break
            oRetLst.append(oRetFlag)
        return oRetLst

    
    
    def plot_graph(self, mData, mAdj_mat, mRet_list, mType):
    
        if mType == 'all':
            for i, rl in enumerate(mRet_list):
                print(i, rl)
                for i in range(len(rl)-1):
                    print(mAdj_mat[rl[i]][rl[i+1]])
                
                oData_plot = pd.DataFrame()
                oData_plot = oData_plot.append(mData.loc[rl])
    
                plt.figure(figsize=(20, 20))
                plt.plot([oData_plot['src_x'], oData_plot['dst_x']], [oData_plot['src_y'], oData_plot['dst_y']], '-', linewidth=5)
    
                plt.grid(True)
                plt.savefig('./plot_vir.png')
                #plt.show()
    
                sleep(1)
    
    
        elif mType == 'origin':
            plt.figure(figsize=(20, 20))
            plt.plot([mData['src_x'], mData['dst_x']], [mData['src_y'], mData['dst_y']], '-', linewidth=5)
    
            plt.grid(True)
            plt.savefig('./plot_vir.png')
            #plt.show()
    
    
        else:
            oData_plot = mData.loc[mRet_list[int(mType)]]
    
            for i in range(len(mRet_list[int(mType)])-1):
                print(mAdj_mat[mRet_list[int(mType)][i]][mRet_list[int(mType)][i+1]])
    
    
            plt.figure(figsize=(20, 20))
            plt.plot([oData_plot['src_x'], oData_plot['dst_x']], [oData_plot['src_y'], oData_plot['dst_y']], '-', linewidth=5)
    
            plt.grid(True)
            plt.savefig('./plot_vir.png')
            #plt.show()
    
    
    def get_angle_vec(self, mAdj_mat_o):
    
        oAng_vec = list()
        for angs in mAdj_mat_o:
            oAng_vec.extend(angs)
            oAng_vec = list(set(oAng_vec))
    
        for i in range(len(oAng_vec)):
            oAng_vec[i] = float(oAng_vec[i].split(':')[0])
    
        oAng_hist = list()
        for angs in oAng_vec:
            if angs != np.inf:
                oAng_hist.append(angs)
    
    
        return oAng_hist

    def gen_sequence(self, mAdj_mat, mErr):
        oCur_path = randint(0, len(mAdj_mat))
        oNum_loop = randint(2, 3)

        oSequence = list()
        oDirection = ['sd']
        while True:
            oNew_path = randint(0, len(mAdj_mat)-1)
            oNew_ang = mAdj_mat[oCur_path][oNew_path]
            oNew_ang = oNew_ang.split(':')

            #print(oNew_ang[0], oNew_ang[1])
            if (oNew_ang[1] in ['ss', 'dd', 'sd', 'ds']) & (abs(float(oNew_ang[0])) > mErr):
                oDirection.append(oNew_ang[1])
                oNew_ang = oNew_ang[0]
                #print(oDirection)

                if (float(oNew_ang) > 0.0) & (float(oNew_ang) < 180.0) | (float(oNew_ang) < 0.0) & (float(oNew_ang) > -180.0):
                    if oDirection[-2][1] == oDirection[-1][0]:
                        oSequence.append(str(oNew_ang))

                oCur_path = oNew_path
                if len(oSequence) == oNum_loop:
                    break
        
        oSeq_str = ''
        for seq in oSequence:
            oSeq_str += seq + '>'

        return oSeq_str[:-1]



    def sliding_MAE(self, mQuery, mReference):
        oCostMat = list()
        oReferences = list()

        for i in range(len(mReference)-len(mQuery)):
            #oReferences.append(np.array(mReference[i:i+len(mQuery)]))
            oReferences.append(np.array(mReference[i:i+len(mQuery)]) - mReference[i])

        for r in oReferences[:]:
            #oCostMat.append(self.myMSE(np.array(mQuery), r))
            oCostMat.append(self.myMSE(np.array(mQuery)-mQuery[0], r))

        return oCostMat.index(min(oCostMat))


    def sliding_DTW(self, mQuery, mReference):
        oCostMat = list()
        oReferences = list()

        for i in range(len(mReference)-len(mQuery)):
            oReferences.append(np.array(mReference[i:i+len(mQuery)]))

        for r in oReferences[:]:
            oAlignment = dtw(mQuery, r, keep_internals=True)
            #print(afile, oAlignment.normalizedDistance, '- len:', len(template))
            oCostMat.append(oAlignment.normalizedDistance)


        if len(oCostMat)==0:
            return 1000000000000000.
        else:
            return min(oCostMat)


    def myMAE(self, mX, mY):
        oDat = list()
        for x, y in zip(mX, mY):
            oDat.append(abs(x-y))

        return np.mean(oDat)
    
    def myMSE(self, mX, mY):
        oDat = list()
        for x, y in zip(mX, mY):
            oDat.append((x-y)**2)

        return np.mean(oDat)

    def myDTW(self, mQuery, mReference, mWinSize):

        oWinSize = int(mWinSize/2)
        oCostMat = list()

        oQuerys = list()
        oReferences = list()
        for i in range(oWinSize, len(mQuery)-oWinSize):
            oQuerys.append(np.array(mQuery[i-oWinSize:i+oWinSize]) - mQuery[i-oWinSize])

        for i in range(oWinSize, len(mReference)-oWinSize):
            oReferences.append(np.array(mReference[i-oWinSize:i+oWinSize]) - mReference[i-oWinSize])


        for q in oQuerys[:]:
            oCostMat.append(list())
            for r in oReferences[:]:
                #plt.plot(q)
                #plt.plot(r)
                #plt.grid(True)
                #plt.show()

                #oCostMat[-1].append(self.myMAE(q, r))
                oCostMat[-1].append(self.myMSE(q, r))

        oCost = 0
        oCur = [0]

        for qCol in oCostMat:
            if len(oCur)==1:
                oMin = min(qCol[oCur[-1]:])
                oCost += oMin
                oCur.append(qCol.index(oMin))
            else:
                oMin = min(qCol[oCur[-1]:oCur[-1]+10])
                oCost += oMin
                oCur.append(qCol.index(oMin))
            
        return oCur, oCost




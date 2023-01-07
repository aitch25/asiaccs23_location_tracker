import os
import sys
from dtw import *
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from scipy import integrate
from scipy.signal import medfilt

from src.Data_Processor import *

from scipy import signal

from numpy import random

from src.detect_peaks import detect_peaks

import editdistance

def get_references(mRefpath, mNgram=3):
    oReffiles = os.listdir(mRefpath)
    oReffiles.sort()

    oRef_name = list()
    oRef_list = list()
    oRef_lists = list()
    oRef_2d_list = list()

    for i in range(len(oReffiles)-(mNgram-1)):
        oRef = pd.DataFrame()
        for j in range(i, i+mNgram):
            oRef = oRef.append(pd.read_csv(mRefpath + oReffiles[j]))
        
        oRef = oRef[['name', 'latitude', 'longitude']].drop_duplicates()
        oRef_name.append(oRef[oRef['name']!='none']['name'].values)
        
        oRef_new = pd.DataFrame()
        oRef_new['src_name'] = oRef['name'].values[:-1]
        oRef_new['dst_name'] = oRef['name'].values[1:]
        oRef_new['src_x'] = oRef['latitude'].values[:-1] 
        oRef_new['src_y'] = oRef['longitude'].values[:-1]
        oRef_new['dst_x'] = oRef['latitude'].values[1:]
        oRef_new['dst_y'] = oRef['longitude'].values[1:]
        oRef_2d_list.append(oRef_new)

        oRef_list.append(rp.get_continuous_sequence(oRef_new))
        #oRef_list.append(oRef)
        #oRef_list.append(oReferences_2d)

    return oRef_name, oRef_list, oRef_2d_list

def validity_checker(mStations, mRefpath):
    oReffiles = os.listdir(mRefpath)
    oReffiles.sort()

    oEntire_ref_name = list()
    oRef = pd.DataFrame()

    for rfile in oReffiles:
        oRef = oRef.append(pd.read_csv(mRefpath + rfile))
        
    oRef = oRef[['name', 'latitude', 'longitude']].drop_duplicates()
    oEntire_ref_name.append(oRef[oRef['name']!='none']['name'].values)
    oEntire_ref_name = list(oEntire_ref_name[0])

    #for i in range(len(oEntire_ref_name)-len(mStations)):
    #    if (editdistance.eval(mStations, oEntire_ref_name[i:i+len(mStations)])<=1) | (editdistance.eval(mStations[::-1], oEntire_ref_name[i:i+len(mStations)])<=1):
    #        return True
    #return False

    #print(':'.join(mStations[::-1]))
    #print(':'.join(oEntire_ref_name))

    if (':'.join(mStations) in ':'.join(oEntire_ref_name)) | (':'.join(mStations[::-1]) in ':'.join(oEntire_ref_name)):
        return True
    else:
        return False

def query_split_nGram(mData, mNgram=2):
    oPartial_paths = list()
    for i in range(len(mData)-(mNgram-1)):
        oPartial_path = list()
        for j in range(i, i+mNgram):
            oPartial_path.extend(mData[j])
        oPartial_paths.append(oPartial_path[::7])

    return oPartial_paths


if __name__=='__main__':

    dirpath = './DATA/sensors/'
    filepaths = os.listdir(dirpath)
    filepaths.sort()


    if len(sys.argv) < 2:
        for idx, path in enumerate(filepaths):
            print(str(idx) + ')', path)

        file_idx = int(input('Select a file by index number: '))
        print(filepaths[file_idx] + ' is selected')
        ngram = int(input('Select n of n-gram: '))
        print('Processing with ' + str(ngram) + '-gram')
    else:
        file_idx = int(sys.argv[1])
        ngram = int(sys.argv[2])
        

    accl = pd.read_csv(dirpath + filepaths[file_idx] + '/accelerometer.csv')
    gyro = pd.read_csv(dirpath + filepaths[file_idx] + '/gyroscope.csv')

    sp = Sensor_Processor()
    rp = Ref_Processor()
    
    accl = accl[['x', 'y', 'z']]
    gyro = gyro[['x', 'y', 'z']]

    angs1 = sp.sensor_rotation(accl, mAxis='x')
    accl_tfd = sp.sensor_compensation(accl, angs1, mAxis='x')
    gyro_tfd = sp.sensor_compensation(gyro, angs1, mAxis='x')

    angs2 = sp.sensor_rotation(accl_tfd, mAxis='y')
    accl_tfd = sp.sensor_compensation(accl_tfd, -angs2, mAxis='y')
    gyro_tfd = sp.sensor_compensation(gyro_tfd, -angs2, mAxis='y')
    
    gyro_new = pd.DataFrame()
    gyro_new['x'] = gyro_tfd['x'].copy()
    gyro_new['y'] = gyro_tfd['y'].copy()
    gyro_new['z'] = gyro_tfd['z'].copy()

    move_idx = sp.get_move_moment_idx(sp.butter_lowpass_filter(gyro_new['z'], cutoff=0.1, fs=20, order=2), mWin_size=30, mThd=0.005)
    gyro_m = gyro_new['z'][move_idx]
    
    accl_comb = np.sqrt((accl['x'] ** 2) + (accl['y'] ** 2) + (accl['z'] ** 2)) 
    accl_comb = accl_comb[move_idx]
    
    split_points = sp.find_stops(accl_comb)

    fs = 20
    gyro_m = sp.butter_lowpass_filter(gyro_m, 0.1, fs, 2)
    query = sp.get_trace_from_sensor(gyro_m, mBias=0.0)
    query = query-((max(query)+min(query))/2)

    path_2d = sp.get_2d_path(query[::-7])

    queries = sp.split_path(query, mSplit_points=split_points)
    ngram_cnt = len(queries)
    queries = query_split_nGram(queries, mNgram=ngram)
    #print(len(queries))

    ############################################################################################

    refpath = './DATA/references/'
    ref_name, ref_list, ref_2d_list = get_references(refpath, mNgram=ngram)

    best_matches = pd.DataFrame()

    for idx, q in tqdm(enumerate(queries)):
        find_best_matches = dict()
        find_best_matches['query_idx'] = list()
        find_best_matches['reverse_tf'] = list()
        find_best_matches['location'] = list()
        find_best_matches['DTW_dist'] = list()

        for station_name, ref, ref_2d in zip(ref_name, ref_list, ref_2d_list):
            ref = list(ref-((max(ref)+min(ref))/2))
            for rev, r in enumerate([ref, ref[::-1]]):
                find_best_matches['query_idx'].append(idx)
                find_best_matches['reverse_tf'].append(rev)
                find_best_matches['location'].append(station_name[::-1]) if rev else find_best_matches['location'].append(station_name)

                #if rev:
                #    find_best_matches['location'].append(station_name[::-1])
                #else:
                #    find_best_matches['location'].append(station_name)

                alignment = dtw(q, r, keep_internals=True)
                find_best_matches['DTW_dist'].append(alignment.distance)

                ### Display the warping curve, i.e. the alignment curve
                #alignment.plot(type="threeway")

                ## Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
                #dtw(q, r, keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c")).plot(type="twoway", offset=0)

        if best_matches.empty:
            best_matches = pd.DataFrame.from_dict(find_best_matches).sort_values(by='DTW_dist')
        else:
            best_matches = best_matches.merge(pd.DataFrame.from_dict(find_best_matches).sort_values(by='DTW_dist'), on=['reverse_tf'], suffixes=['', '_{}'.format(idx)]).sort_values(by='DTW_dist')

            best_matches['DTW_dist'] += best_matches['DTW_dist_{}'.format(idx)]
            best_matches['location'] = best_matches[['location', 'location_{}'.format(idx)]].apply(lambda x: (list(x[0]) + [x[1][-1]]), axis=1)
            best_matches['validity'] = best_matches['location'].map(lambda x: validity_checker(x, refpath))
            best_matches = best_matches[best_matches['validity']==True]
        

    #best_matches = best_matches[['reverse_tf', 'location', 'DTW_dist', 'validity']].sort_values(by='DTW_dist')
    best_matches = best_matches.sort_values(by='DTW_dist')
    best_matches.to_csv('./DATA/output/res_{}.csv'.format(str('%03d' % file_idx)), index=False)


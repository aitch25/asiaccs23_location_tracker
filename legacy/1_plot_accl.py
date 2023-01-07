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


if __name__=='__main__':

    dirpath = './DATA/sensors/'
    filepaths = os.listdir(dirpath)
    filepaths.sort()

    if len(sys.argv) < 2:
        for idx, path in enumerate(filepaths):
            print(str(idx) + ')', path)

        file_idx = int(input('Select a file by index number: '))
        print(filepaths[file_idx] + ' is selected')
    else:
        file_idx = int(sys.argv[1])

    accl = pd.read_csv(dirpath + filepaths[file_idx] + '/accelerometer.csv')
    gyro = pd.read_csv(dirpath + filepaths[file_idx] + '/gyroscope.csv')

    sp = Sensor_Processor()
    rp = Ref_Processor()
    
    accl = accl[['x', 'y', 'z']]
    gyro = gyro[['x', 'y', 'z']]


    plt.figure(figsize=(10, 7))    
    plt.subplot(2, 1, 1)
    plt.plot(accl['x'])
    plt.plot(accl['y'])
    plt.plot(accl['z'])
    plt.legend(['accl-x', 'accl-y', 'accl-z'], loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3, fontsize=20)
    plt.ylabel('Accelerometer', fontsize=20)
    plt.xticks(visible=False)
    plt.grid(True)

    plt.subplot(2, 1, 2)
    accl_comb = np.sqrt((accl['x'] ** 2) + (accl['y'] ** 2) + (accl['z'] ** 2)) 
    split_points = sp.find_stops(accl_comb)
    plt.plot(accl_comb, 'r')

    plt.grid(True)
    for sp in split_points[1:-1]:
        plt.axvline(x=sp, color='dimgrey', ls='--', lw=3)
    #plt.ylabel('Magnitude\n& Estimated change points', fontsize=20)

    for sp in [2855, 6400, 10130, 12650, 16180]:
        plt.axvline(x=sp, color='k', ls=':', lw=3)

    plt.ylim(8.5, 11)
    plt.ylabel('Magnitude &\nchange points', fontsize=20)
    plt.xlabel('Time', fontsize=20)
    from matplotlib.lines import Line2D
    plt.legend(handles=[Line2D([0], [0], ls='--', color='dimgray', lw=3, label='estimated change points'), Line2D([0], [0], ls=':', color='k', lw=3, label='ground truth')], fontsize=20, ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.25))
    plt.show()
    exit()



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
    print(file_idx, len(split_points), split_points)
    exit()

    
    fs = 20
    gyro_m = sp.butter_lowpass_filter(gyro_m, 0.1, fs, 2)
    heading = sp.get_trace_from_sensor(gyro_m, mBias=0.0)
    heading = heading-((max(heading)+min(heading))/2)

    path_2d = sp.get_2d_path(heading[::-8])

    headings = sp.split_path(heading, mSplit_points=split_points)
    #for h in headings:
    #    print(h.shape)

    #print(sys.argv[1], end=' ')
    #if len(headings) < 6:
    #    print('### ', end=' ')
    #print(len(headings))
    #exit()
    ##plt.plot(heading)
    #plt.plot(headings)
    #plt.show()
    ############################################################################################

    refpath = './DATA/references/'

    ref_name, ref_list, ref_2d_list = get_references(refpath, mNgram=len(headings))

    heading = list(heading[::-8])
    for station_name, ref, ref_2d in zip(ref_name, ref_list, ref_2d_list):
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.plot(heading)
        ref = list(ref-((max(ref)+min(ref))/2))
        plt.plot(ref)

        plt.subplot(1, 3, 2)
        plt.plot(path_2d[0]/10000, path_2d[1]/10000)
        plt.subplot(1, 3, 3)
        plt.plot(ref_2d['src_x'] - ref_2d['src_x'].values[0], ref_2d['src_y'] - ref_2d['src_y'].values[0])

        print(station_name)
        plt.show()

        print(heading)
        print(ref)
        alignment = dtw(heading, ref, keep_internals=True)
        print(alignment.normalizedDistance)

        ## Display the warping curve, i.e. the alignment curve
        alignment.plot(type="threeway")

        ## Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
        dtw(heading, ref, keep_internals=True, 
        step_pattern=rabinerJuangStepPattern(6, "c"))\
            .plot(type="twoway", offset=0)



    #all_references = list()
    #references_2d = rp.get_continuous_sequence(out_df)
    #references_2d = meanfilt(references_2d, 25)
    #references_2d = meanfilt(references_2d, 25)
    #references_2d = meanfilt(references_2d, 25)
    #references_2d = meanfilt(references_2d, 25)
    #references_2d = meanfilt(references_2d, 25)
    #references_2d = references_2d - ((max(references_2d)+min(references_2d))/2)
    #plt.plot(-template_2d)
    #plt.show()
    #all_references.append(-references_2d)





    #id_lst = list()
    #ids_lst = list()
    #costs_lst = list()
    #sidx_lst = list()
    #prep_tf_lst = list()
    #timegap_path = './DATA/timegap/'
    #timegap_files = os.listdir(timegap_path)
    #timegap_files.sort()

    #ref_path = './DATA/references/'
    #ref_files = os.listdir(ref_path)
    #ref_files.sort()


    #all_references = list()
    #for tg_file in tqdm(timegap_files):
    #    atimegap = pd.read_csv(timegap_path + tg_file)
    #    atimegap['index'] = atimegap.index
    #    atimegap['filename'] = tg_file.split('.')[0]

    #    templates = rp.get_station_timegap_ngram(mTimegap=atimegap, mLen=6)
    #    if templates.empty: continue
    #    templates = templates[templates[['srcs', 'dsts', 'line', 'id']].duplicated()==False]

    #    for path_id in tqdm(templates['id'].drop_duplicates().values):
    #        id_lst.append(path_id)

    #        lines = templates[templates['id']==path_id]

    #        out_df = pd.DataFrame()
    #        for line in lines.values:
    #            aline = pd.read_csv(csv_path + line[5].split('_')[0] + '_' + line[0] + '_' + line[1] + '.csv')

    #            if out_df.empty:
    #                out_df = out_df.append(aline)
    #            else:
    #                aline['src_x'] = aline['src_x'] + out_df.tail(1)['dst_x'].values
    #                aline['src_y'] = aline['src_y'] + out_df.tail(1)['dst_y'].values

    #                aline['dst_x'] = aline['dst_x'] + out_df.tail(1)['dst_x'].values
    #                aline['dst_y'] = aline['dst_y'] + out_df.tail(1)['dst_y'].values

    #                out_df = out_df.append(aline)


    #        out_df = out_df.reset_index()

    #        template_2d = rp.get_continuous_sequence(out_df)
    #        template_2d = meanfilt(template_2d, 25)
    #        template_2d = meanfilt(template_2d, 25)
    #        template_2d = meanfilt(template_2d, 25)
    #        template_2d = meanfilt(template_2d, 25)
    #        template_2d = meanfilt(template_2d, 25)
    #        template_2d = template_2d - ((max(template_2d)+min(template_2d))/2)
    #        #plt.plot(-template_2d)
    #        #plt.show()
    #        all_references.append(-template_2d)




    #for j in tqdm(range(len(all_references))):
    #    oAlignmentOBE = dtw(signals, all_references[j], keep_internals=True)
    #    costs_lst.append(float((oAlignmentOBE.distance) / (max(oAlignmentOBE.index2) - min(oAlignmentOBE.index2))))
    #    sidx_lst.append(idx)
    #    prep_tf_lst.append(prep_tf)

    #ids_lst.extend(id_lst)










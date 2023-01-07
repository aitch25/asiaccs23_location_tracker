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

    refpath = './DATA/references/'

    ref_list = get_references(refpath, mNgram=len(headings))

    for ref in ref_list:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(path_2d[0], path_2d[1])
        plt.subplot(1, 2, 2)
        plt.plot(ref['latitude'], ref['longitude'])

        plt.show()


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










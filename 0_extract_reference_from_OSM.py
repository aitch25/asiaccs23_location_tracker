import numpy as np
import pandas as pd
from tqdm import tqdm
import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
 


def auto_swap(mData):
    mat = np.array(mData['adj_matrix'])

    for i in tqdm(range(len(mat))):
        for j in range(len(mat)):
            for k in range(j+1, len(mat)):
                if mat[i, j] > mat[i, k]:
                    mat[:, [j,k]] = mat[:, [k,j]]
                    mat[[j,k], :] = mat[[k,j], :]

                    mData['types'][j], mData['types'][k] = mData['types'][k], mData['types'][j] 
                    mData['name'][j], mData['name'][k] = mData['name'][k], mData['name'][j] 
                    mData['coordinates'][j], mData['coordinates'][k] = mData['coordinates'][k], mData['coordinates'][j] 

    mData['adj_matrix'] = mat
   
    return mData



if __name__=="__main__":
    tree = elemTree.parse('./DATA/OSM/map_Shinbundang.osm')

    columns = dict()
    columns['types'] = list()
    columns['name'] = list()
    columns['coordinates'] = list()
    columns['adj_matrix'] = list()

    coord_list = list()
    cnt = 0
    for elm in tree.findall('./node'):
        if (elm.get('changeset')=='105914894') | (elm.get('changeset')=='109089044'): # Shinbundang line
            cnt+=1
            for elm2 in elm.findall('./tag'):
                if elm2.get('k')=='name:en':
                    columns['coordinates'].append((float(elm.get('lon')), float(elm.get('lat'))))
                    columns['types'].append('station')
                    columns['name'].append(elm2.get('v'))

            if not (float(elm.get('lon')), float(elm.get('lat'))) in columns['coordinates']:
                columns['coordinates'].append((float(elm.get('lon')), float(elm.get('lat'))))
                columns['types'].append('path')
                columns['name'].append('none')
    
    for i in range(len(columns['coordinates'])):
        tmp_list = list()
        for j in range(len(columns['coordinates'])):
            dist = np.linalg.norm(np.array(columns['coordinates'][i]) - np.array(columns['coordinates'][j]))
            tmp_list.append(dist)
        columns['adj_matrix'].append(tmp_list)
            
    columns = auto_swap(columns)

    coord_list = np.array(columns['coordinates']).T
    coord_df = pd.DataFrame({'types':columns['types'], 'name':columns['name'], 'longitude':coord_list[0], 'latitude':coord_list[1]})
    coord_df = coord_df[((coord_df['types']=='station') & (coord_df['name'].duplicated()==False)) | (coord_df['types']=='path')].reset_index()
    coord_df = coord_df.drop(columns=['index'])

    mean_lat_list = list() 
    mean_lon_list = list() 
    for i in range(coord_df.shape[0]):
        mean_lat_list.append(coord_df['latitude'].values[(0 if (i-2)<0 else (i-2)):i+2].mean())
        mean_lon_list.append(coord_df['longitude'].values[(0 if (i-2)<0 else (i-2)):i+2].mean())
    coord_df['latitude'] = mean_lat_list
    coord_df['longitude'] = mean_lon_list


    stations_df = coord_df[coord_df['types']=='station']
    print(stations_df)


    coord_df.to_csv('./DATA/OSM/logs/path_entire_shinbundang.csv', index=False)
    for i in range(stations_df.shape[0]-1):
        coord_df.iloc[stations_df.index[i]:(stations_df.index[i+1]+1)].to_csv('./DATA/references/path_shinbundang_{}_{}_{}.csv'.format(str('%02d' % i), stations_df['name'].values[i], stations_df['name'].values[i+1]), index=False)
    

    plt.figure(figsize=(10, 10))
    plt.plot(coord_df['longitude'].values, coord_df['latitude'].values, '-')
    plt.plot(stations_df['longitude'].values, stations_df['latitude'].values, 'o')
    plt.grid(True)
    plt.show()

    


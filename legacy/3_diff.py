import pandas as pd

if __name__=="__main__":
    data = pd.read_csv('./DATA/OSM/logs/path_entire_shinbundang.csv')
    print(list(data['longitude'].diff()))
    print(list(data['latitude'].diff()))
    print(data['longitude'].diff().min())
    print(data['latitude'].diff().min())

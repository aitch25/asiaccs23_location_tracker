import os
from time import sleep

for i in range(0, 101, 8):
    for j in range(8):
        os.system('python3 -W ignore 1_tracking_location.py {} {} &'.format((i+j), 2))
        print('python3 -W ignore 1_tracking_location.py {} {} &'.format((i+j), 2))
        #print(i+j)
    sleep(30)
    #print('---')


class Data_Loader:
    def get_data(self):
        oSubway_paths = [
                './sensor_data/subway/sensorlab_2020-10-19-신분당선_출근/',
                './sensor_data/subway/sensorlab_2020-10-19-신분당선_퇴근/',
                './sensor_data/subway/subway_20201218_상현역_판교역/',
                './sensor_data/subway/subway_20201218_판교역_상현역/',
                './sensor_data/subway/sensorlab_2020-12-30-09.54.14_sub_상현_미금/',
                './sensor_data/subway/sensorlab_2020-12-30-10.17.58_sub_미금_가천대/', # 5
                './sensor_data/subway/sensorlab_2020-12-30-10.41.05_sub_수서_왕십리/',
                './sensor_data/subway/sensorlab_2020-12-30-11.18.34_sub_line_02_왕십리_강남/', ############
                './sensor_data/subway/sensorlab_2020-12-31-12.02.12_sub_강남_상현/', # 8

                './sensor_data/subway/sensorlab_2021-01-06-08.50.20_sub_미금_모란/', # 9
                './sensor_data/subway/sensorlab_2021-01-06-09.13.34_sub_line_08_모란_천호/', ############
                './sensor_data/subway/sensorlab_2021-01-06-09.52.26_sub_line_05_천호_충정로/', ############
                './sensor_data/subway/sensorlab_2021-01-06-10.35.31_sub_line_02_아현_강남/', ############
                './sensor_data/subway/sensorlab_2021-01-06-11.38.13_sub_line_sbds_강남_광교/', ############
                './sensor_data/subway/sensorlab_2021-01-07-12.27.18_sub_광교_상현/',

                './sensor_data/subway/sensorlab_2021-01-17-02.57.44_sub_4호선_인덕원_동작/',  # 15
                './sensor_data/subway/sensorlab_2021-01-17-03.27.05_sub_9호선_동작_보훈병원/',
                './sensor_data/subway/sensorlab_2021-01-23-10.11.26_ys1_잠실_신림_추정/',
                './sensor_data/subway/sensorlab_2021-01-23-12.00.28_ys2/',
                './sensor_data/subway/sensorlab_2021-01-23-03.01.31_ys3_군자역_하남풍산역_추정/', # 군자역_하남풍산역
                './sensor_data/subway/sensorlab_2021-01-24-02.11.47_line_bds_정자_왕십리/',  # 20 # 3500, -2500 ############
                './sensor_data/subway/sensorlab_2021-01-25-07.55.20_line_center_도농_옥수/', ############
                './sensor_data/subway/sensorlab_2021-01-25-08.43.05_line_03_옥수_양재/', ############

                './sensor_data/subway/sensorlab_2021-02-27-06.51.13_line_01_incheon_국제업무지구_계양/', ############
                './sensor_data/subway/sensorlab_2021-02-27-07.50.59_인천1호선_계양_인천시청/',
                './sensor_data/subway/sensorlab_2021-02-27-08.29.13_line_02_incheon_인천시청_검단오류/', # 25 ############
                './sensor_data/subway/sensorlab_2021-02-27-09.17.25_인천2호선_검단오류_인천시청/',
                './sensor_data/subway/sensorlab_2021-02-27-10.08.33_인천1호선_인천시청_국제업무지구/',

                './sensor_data/subway/sensorlab_2021-03-07-01.05.36_line_01_daegu_동대구_설화명곡/', ############
                './sensor_data/subway/sensorlab_2021-03-07-01.47.36_daegu_설화명곡_명덕/',
                './sensor_data/subway/sensorlab_2021-03-07-02.23.16_line_03_daegu_명덕_칠곡경대병원/', ############
                './sensor_data/subway/sensorlab_2021-03-07-03.01.03_daegu_칠곡경대병원_청라언덕/',
                './sensor_data/subway/sensorlab_2021-03-07-03.34.43_daegu_X_청라언덕_영남대/',
                './sensor_data/subway/sensorlab_2021-03-07-04.10.38_line_02_daegu_영남대_반월당/', ############
                './sensor_data/subway/sensorlab_2021-03-08-04.58.37_busan_X_오시리아_센텀/',
                './sensor_data/subway/sensorlab_2021-03-08-05.42.44_busan_수영_대저/',
                './sensor_data/subway/sensorlab_2021-03-08-06.37.18_line_02_busan_덕천_장산/', ############
                './sensor_data/subway/sensorlab_2021-03-09-12.57.13_line_donghae_busan_오시리아_부전/', ############
                './sensor_data/subway/sensorlab_2021-03-09-01.49.10_busan_부전_다대포해수욕장/',
                './sensor_data/subway/sensorlab_2021-03-09-05.40.03_line_01_daejeon_대전_반석/', ############
                './sensor_data/subway/sensorlab_2021-03-09-06.18.46_daejeon_반석_신흥/',

                './sensor_data/subway/sensorlab_2021-03-20-03.52.53_line_01_busan_부산_다대포해수욕장/', ############
                './sensor_data/subway/sensorlab_2021-03-20-04.34.28_다대포해수욕장_부산/',

                './sensor_data/subway/sensorlab_2021-11-15-07.12.35_판교_강남/',
                './sensor_data/subway/sensorlab_2021-11-15-07.33.19_강남_강변/',
                './sensor_data/subway/sensorlab_2021-11-15-08.08.43_옥수_양재/',
                './sensor_data/subway/sensorlab_2021-11-15-08.29.40_양재_판교/',

                './sensor_data/subway/sensorlab_2021-11-17-06.40.27_판교_강남/', 
                './sensor_data/subway/sensorlab_2021-11-17-07.52.58_도농_옥수/',
                './sensor_data/subway/sensorlab_2021-11-17-08.39.42_옥수_양재/',
                './sensor_data/subway/sensorlab_2021-11-17-08.52.59_강남_강변/',
                './sensor_data/subway/sensorlab_2021-11-17-09.04.06_양재_판교/',
                './sensor_data/subway/sensorlab_2021-11-22-08.26.13_상현_판교/',
                './sensor_data/subway/sensorlab_2021-11-22-06.48.06_판교_상현/',

                './sensor_data/subway/sensorlab_2021-11-24-08.52.11_상현_판교/',
                #'./sensor_data/subway/sensorlab_2021-11-24-04.50.18_판교_상현/',

                './sensor_data/subway/sensorlab_2021-11-25-12.24.58_상현_판교/',
                './sensor_data/subway/sensorlab_2021-11-25-08.41.56_판교_상현/',

                './sensor_data/subway/sensorlab_2021-11-26-09.31.56_상현_판교/',
                './sensor_data/subway/sensorlab_2021-11-26-07.40.42_판교_상현/',
                
                './sensor_data/subway/sensorlab_2021-11-29-09.25.42_상현_판교/',
                './sensor_data/subway/sensorlab_2021-11-29-08.00.25_판교_상현/',

                './sensor_data/subway/sensorlab_2021-11-30-09.32.19_상현_판교/',
                './sensor_data/subway/sensorlab_2021-11-30-05.54.33_판교_상현/',

                './sensor_data/subway/sensorlab_2021-12-01-09.05.18_상현_판교/',
                './sensor_data/subway/sensorlab_2021-12-01-08.10.21_판교_상현/',

                './sensor_data/subway/sensorlab_2021-12-02-08.16.27_상현_판교/',
                './sensor_data/subway/sensorlab_2021-12-02-06.24.00_판교_상현/',

                './sensor_data/subway/sensorlab_2021-12-08-09.32.09_상현_판교/',
                './sensor_data/subway/sensorlab_2021-12-09-08.01.12_상현_판교/',
                './sensor_data/subway/sensorlab_2021-12-09-10.19.43_판교_상현/',
                './sensor_data/subway/sensorlab_2021-12-10-09.17.47_판교_상현/',

                './sensor_data/subway/sensorlab_2021-12-20-08.15.56_상현_판교/',
                './sensor_data/subway/sensorlab_2021-12-20-08.42.17_판교_상현/',

                './sensor_data/subway/sensorlab_2021-12-23-05.46.09_판교_상현/',
                './sensor_data/subway/sensorlab_2021-12-23-07.46.29_상현_판교/',

                './sensor_data/subway/sensorlab_2022-01-03-09.06.04_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-03-10.52.04_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-04-06.19.01_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-04-08.42.19_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-05-06.24.02_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-05-09.17.49_상현_판교/',

                './sensor_data/subway/sensordata_220105_상현_판교/',
                './sensor_data/subway/sensordata_220105_판교_상현/',

		'./sensor_data/subway/sensorlab_2022-01-08-03.57.39_남구로_신대방삼거리/',
		'./sensor_data/subway/sensorlab_2022-01-08-04.43.50_신대방삼거리_군자/',
		'./sensor_data/subway/sensorlab_2022-01-08-05.27.59_군자_길동/',
		'./sensor_data/subway/sensorlab_2022-01-08-11.01.27_길동_군자/',
		'./sensor_data/subway/sensorlab_2022-01-08-11.19.23_군자_대림/',

                './sensor_data/subway/sensordata_220108_군자_길동/',
                './sensor_data/subway/sensordata_220108_남구로_신대방삼거리/',
                './sensor_data/subway/sensordata_220108_길동_군자/',
                './sensor_data/subway/sensordata_220108_신대방삼거리_군자/',
                './sensor_data/subway/sensordata_220108_군자_대림/',

                './sensor_data/subway/sensorlab_2022-01-10-07.10.08_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-10-08.52.28_상현_판교/',

                './sensor_data/subway/sensordata_220110_판교_상현/',
                './sensor_data/subway/sensordata_220110_상현_판교/',


                './sensor_data/subway/sensordata_220112_판교_상현/',
                './sensor_data/subway/sensordata_220112_상현_판교/',
                './sensor_data/subway/sensordata_220117_상현_판교/',
                './sensor_data/subway/sensordata_220117_판교_상현/',
                './sensor_data/subway/sensordata_220119_판교_상현/',
                './sensor_data/subway/sensordata_220119_상현_판교/',
                './sensor_data/subway/sensordata_220121_상현_판교/',
                './sensor_data/subway/sensordata_220121_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-12-09.39.29_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-12-10.33.58_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-17-08.42.36_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-17-08.49.46_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-19-07.51.02_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-19-08.42.20_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-21-09.39.26_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-21-09.45.50_판교_상현/',

                './sensor_data/subway/sensorlab_2022-01-26-07.10.30_판교_상현/',
                './sensor_data/subway/sensorlab_2022-01-26-09.33.26_상현_판교/',
                './sensor_data/subway/sensorlab_2022-01-27-09.47.29_상현_판교/',

                './sensor_data/subway/sensordata_220126_상현_판교/',
                './sensor_data/subway/sensordata_220127_상현_판교/',


                './sensor_data/subway/sensordata_220208_상현_판교/',
                './sensor_data/subway/sensordata_220210_상현_판교/',
                './sensor_data/subway/sensordata_220211_상현_판교/',
                './sensor_data/subway/sensordata_220217_상현_판교/',
                './sensor_data/subway/sensorlab_2022-02-08-09.25.33_상현_판교/',
                './sensor_data/subway/sensorlab_2022-02-10-08.58.52_상현_판교/',
                './sensor_data/subway/sensorlab_2022-02-11-09.47.29_상현_판교/',
                './sensor_data/subway/sensorlab_2022-02-18-06.26.21_상현_양재/',
                './sensor_data/subway/sensorlab_2022-02-18-07.00.05_양재_약수/',
                './sensor_data/subway/sensorlab_2022-02-18-07.27.48_약수_공덕/',
                './sensor_data/subway/sensorlab_2022-03-24-11.55.23_상현_판교/',
                './sensor_data/subway/sensorlab_2022-04-22-07.38.19_판교_상현/',
                './sensor_data/subway/sensorlab_2022-04-22-09.14.32_상현_판교/',
                './sensor_data/subway/sensorlab_2022-04-25-09.02.14_상현_판교/',
                './sensor_data/subway/sensorlab_2022-05-02-07.08.42_판교_상현_actively/',
                './sensor_data/subway/sensorlab_2022-05-02-09.02.15_상현_판교/',

                './sensor_data/subway/sensorlab_2022-05-04-07.33.18_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-05-04-09.20.59_판교_상현_sd/',
                './sensor_data/subway/sensorlab_2022-05-09-07.38.43_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-05-09-09.31.55_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-05-11-07.08.52_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-05-11-08.17.21_상현_판교_su/',

                './sensor_data/subway/sensorlab_2022-05-23-05.27.30_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-05-23-06.42.19_상현_판교_sd/',

                './sensor_data/subway/sensorlab_2022-05-24-09.26.38_상현_판교_sd/', 
                './sensor_data/subway/sensorlab_2022-05-24-10.24.30_판교_상현_sd/', 
                './sensor_data/subway/sensorlab_2022-05-25-07.18.31_판교_상현_sd/', 
                './sensor_data/subway/sensorlab_2022-05-30-09.15.18_상현_판교_sd/', 
                './sensor_data/subway/sensorlab_2022-05-30-07.32.08_판교_상현_su/', 
                './sensor_data/subway/sensorlab_2022-06-02-07.47.15_상현_판교_sd/', 
                './sensor_data/subway/sensorlab_2022-06-02-06.52.33_판교_상현_su/', 

                './sensor_data/subway/sensorlab_2022-06-03-09.08.14_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-06-03-08.12.03_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-06-03-09.08.09_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-03-08.11.59_판교_상현_su_s7/',

                './sensor_data/subway/sensorlab_2022-06-07-09.15.22_상현_판교_su/',
                './sensor_data/subway/sensorlab_2022-06-07-07.26.33_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-06-07-09.15.23_상현_판교_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-07-07.26.31_판교_상현_su_s7/',

                './sensor_data/subway/sensorlab_2022-06-08-09.27.51_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-06-08-07.52.01_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-06-08-09.27.48_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-08-07.52.03_판교_상현_su_s7/',
    
                './sensor_data/subway/sensorlab_2022-06-09-09.33.48_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-06-09-07.27.09_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-06-09-09.33.50_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-09-07.27.10_판교_상현_su_s7/',

                './sensor_data/subway/sensorlab_2022-06-10-09.33.52_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-06-10-04.22.54_판교_상현_su/',
                './sensor_data/subway/sensorlab_2022-06-10-09.33.47_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-10-04.22.48_판교_상현_su_s7/',

                './sensor_data/subway/sensorlab_2022-06-13-08.57.16_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-14-07.41.43_판교_상현_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-14-09.33.39_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-06-14-07.41.37_판교_상현_su/',

                './sensor_data/subway/sensorlab_2022-06-15-07.43.20_판교_상현_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-15-09.34.01_상현_판교_sd_s7/',

                './sensor_data/subway/sensorlab_2022-06-16-07.47.03_판교_상현_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-16-09.15.23_상현_판교_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-17-07.47.24_판교_상현_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-17-09.41.44_상현_판교_sd_s7/',

                './sensor_data/subway/sensorlab_2022-06-20-08.32.01_상현_판교_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-21-09.21.45_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-21-07.56.59_판교_상현_su_s7/',
                './sensor_data/subway/sensorlab_2022-06-23-09.41.18_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-23-09.01.51_판교_상현_su_s7/',

                './sensor_data/subway/sensorlab_2022-06-27-09.08.12_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-27-10.58.38_판교_상현_sd_s7/',

                './sensor_data/subway/sensorlab_2022-06-28-09.33.51_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-06-29-09.34.03_상현_판교_sd_s7/',

                './sensor_data/subway/sensorlab_2022-06-30-09.07.18_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-01-09.33.40_상현_판교_sd/',

                './sensor_data/subway/sensorlab_2022-07-04-09.33.44_상현_판교_sd_s7/',
                './sensor_data/subway/sensorlab_2022-07-06-08.27.14_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-07-09.33.49_상현_판교_sd_s7/',

                './sensor_data/subway/sensorlab_2022-07-11-09.27.16_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-12-09.33.53_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-13-07.32.45_상현_판교_sd_actively/',
                './sensor_data/subway/sensorlab_2022-07-14-09.33.41_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-15-09.34.04_상현_판교_sd/',

                './sensor_data/subway/sensorlab_2022-07-19-09.33.47_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-20-09.34.00_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-21-09.34.02_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-26-09.02.24_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-27-09.34.12_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-07-28-09.15.35_상현_판교_sd/',
                './sensor_data/subway/sensorlab_2022-08-03-10.37.24_판교_상현_sd/',

                './sensor_data/bus/sensorlab_2020-10-19-bus670_퇴근/',               
                './sensor_data/bus/sensorlab_2020-10-21-bus720-2_s수지구청_d상현동/',
                './sensor_data/bus/sensorlab_2020-10-23-bus720-2_s수지구청_d린/',
                './sensor_data/bus/sensorlab_2020-10-28-bus700-2_s미금역_d린/',
                './sensor_data/bus/sensorlab_2020-10-19-bus670_s수지구청_d상현역/',
                './sensor_data/bus/sensorlab_2020-10-22-bus720-2_s오리역_d린/',
                './sensor_data/bus/sensorlab_2020-10-26-bus146_s강남역_d성수사거리/',
                './sensor_data/bus/sensorlab_2020-10-29-bus720-1_s미금역_d린/',
                './sensor_data/bus/sensorlab_2020-10-21-bus720-2/',
                './sensor_data/bus/sensorlab_2020-10-22-bus720-3_s수지구청_d상현역/',  
                './sensor_data/bus/sensorlab_2020-10-27-bus700-2_s동천역_d린/',

                './sensor_data/legacy_210302/sensorlab_2020-04-30-11.28.00-상현1/',
                './sensor_data/legacy_210302/sensorlab_2020-05-19-11.55.04-상현2/',


                ]

        oSubway_paths_dic = {
                './sensor_data/subway/sensorlab_2020-12-30-11.18.34_sub_line_02_왕십리_강남/':[650, 35700], ############
                './sensor_data/subway/sensorlab_2021-01-06-09.13.34_sub_line_08_모란_천호/':[600, 41400], ############
                './sensor_data/subway/sensorlab_2021-01-06-09.52.26_sub_line_05_천호_충정로/':[1100, 38900], ############
                './sensor_data/subway/sensorlab_2021-01-06-10.35.31_sub_line_02_아현_강남/':[3500, 58300], ############
                './sensor_data/subway/sensorlab_2021-01-06-11.38.13_sub_line_sbds_강남_광교/':[800, 46600], ############
                './sensor_data/subway/sensorlab_2021-01-24-02.11.47_line_bds_정자_왕십리/':[4900, 61300], ############
                './sensor_data/subway/sensorlab_2021-01-25-07.55.20_line_center_도농_옥수/':[800, 51900], ############
                './sensor_data/subway/sensorlab_2021-01-25-08.43.05_line_03_옥수_양재/':[2200, 23400], ############

                './sensor_data/subway/sensorlab_2021-02-27-06.51.13_line_01_incheon_국제업무지구_계양/':[800, 66000], ############
                './sensor_data/subway/sensorlab_2021-02-27-07.50.59_인천1호선_계양_인천시청/':[2100, 38700],
                './sensor_data/subway/sensorlab_2021-02-27-08.29.13_line_02_incheon_인천시청_검단오류/':[1900, 49000], # 25 ############
                #'./sensor_data/subway/sensorlab_2021-02-27-08.29.13_인천2호선_인천시청_검단오류/':[3600, 43100], # 25
                './sensor_data/subway/sensorlab_2021-02-27-09.17.25_인천2호선_검단오류_인천시청/':[5800, 49300],
                './sensor_data/subway/sensorlab_2021-02-27-10.08.33_인천1호선_인천시청_국제업무지구/':[0, -1],

                './sensor_data/subway/sensorlab_2021-03-07-01.05.36_line_01_daegu_동대구_설화명곡/':[2300, 43800], ############
                './sensor_data/subway/sensorlab_2021-03-07-01.47.36_daegu_설화명곡_명덕/':[3000, 30700], # not important
                './sensor_data/subway/sensorlab_2021-03-07-02.23.16_line_03_daegu_명덕_칠곡경대병원/':[2800, 40600], # 30 ############
                './sensor_data/subway/sensorlab_2021-03-07-03.01.03_daegu_칠곡경대병원_청라언덕/':[0, -1], 
                './sensor_data/subway/sensorlab_2021-03-07-03.34.43_daegu_X_청라언덕_영남대/':[0, -1], 
                './sensor_data/subway/sensorlab_2021-03-07-04.10.38_line_02_daegu_영남대_반월당/':[7700, 40000], ############
                './sensor_data/subway/sensorlab_2021-03-08-04.58.37_busan_X_오시리아_센텀/':[0, -1], 
                './sensor_data/subway/sensorlab_2021-03-08-05.42.44_busan_수영_대저/':[650, 41400], # 35
                './sensor_data/subway/sensorlab_2021-03-08-06.37.18_line_02_busan_덕천_장산/':[1700, 74500], ############
                './sensor_data/subway/sensorlab_2021-03-09-12.57.13_line_donghae_busan_오시리아_부전/':[3900, 40300], ############
                './sensor_data/subway/sensorlab_2021-03-09-01.49.10_busan_부전_다대포해수욕장/':[2200, 64700], 
                './sensor_data/subway/sensorlab_2021-03-09-05.40.03_line_01_daejeon_대전_반석/':[600, 41800], ############
                './sensor_data/subway/sensorlab_2021-03-09-06.18.46_daejeon_반석_신흥/':[2500, 49200], # 40
                
                './sensor_data/subway/sensorlab_2021-03-20-03.52.53_line_01_busan_부산_다대포해수욕장/':[1100, 48000], ############
                './sensor_data/subway/sensorlab_2021-03-20-04.34.28_다대포해수욕장_부산/':[3800, 44900],

                './sensor_data/subway/sensorlab_2021-01-17-02.57.44_sub_4호선_인덕원_동작/':[0, -1],  
                './sensor_data/subway/sensorlab_2021-01-17-03.27.05_sub_9호선_동작_보훈병원/':[0, -1],
                './sensor_data/subway/sensorlab_2021-01-23-10.11.26_ys1_잠실_신림_추정/':[0, -1],
                './sensor_data/subway/sensorlab_2021-01-23-12.00.28_ys2/':[0, -1],
                './sensor_data/subway/sensorlab_2021-01-23-03.01.31_ys3_군자역_하남풍산역_추정/':[0, -1], # 군자역_하남풍산역

                './sensor_data/subway/sensorlab_2021-11-15-08.08.43_옥수_양재/':[600, 21000], # 43
                './sensor_data/subway/sensorlab_2021-11-15-08.29.40_양재_판교/':[250, 13350],
                './sensor_data/subway/sensorlab_2021-11-15-07.12.35_판교_강남/':[1000, 16150], # 
                './sensor_data/subway/sensorlab_2021-11-15-07.33.19_강남_강변/':[1100, 17750],

                './sensor_data/subway/sensorlab_2021-11-17-06.40.27_판교_강남/':[4570, 16500], 
                './sensor_data/subway/sensorlab_2021-11-17-07.52.58_도농_옥수/':[1400, 50200],
                './sensor_data/subway/sensorlab_2021-11-17-08.39.42_옥수_양재/':[5200, 19300], #19800],
                './sensor_data/subway/sensorlab_2021-11-17-08.52.59_강남_강변/':[950, 18850],
                './sensor_data/subway/sensorlab_2021-11-17-09.04.06_양재_판교/':[250, 16100],


                './sensor_data/subway/sensorlab_2021-11-22-08.26.13_상현_판교/':[1000, 19450],
                './sensor_data/subway/sensorlab_2021-11-22-06.48.06_판교_상현/':[1780, 20000],

                './sensor_data/subway/sensorlab_2021-11-24-08.52.11_상현_판교/':[800, 20290],
                #'./sensor_data/subway/sensorlab_2021-11-24-04.50.18_판교_상현/':[7000, 16000],

                './sensor_data/subway/sensorlab_2021-11-25-12.24.58_상현_판교/':[3000, 19350],
                './sensor_data/subway/sensorlab_2021-11-25-08.41.56_판교_상현/':[2850, 20100],

                './sensor_data/subway/sensorlab_2021-11-26-09.31.56_상현_판교/':[1000, 20000],
                './sensor_data/subway/sensorlab_2021-11-26-07.40.42_판교_상현/':[1000, 20100],

                './sensor_data/subway/sensorlab_2021-11-29-09.25.42_상현_판교/':[730, 20000],
                './sensor_data/subway/sensorlab_2021-11-29-08.00.25_판교_상현/':[4800, 16650],

                './sensor_data/subway/sensorlab_2021-11-30-09.32.19_상현_판교/':[750, 19700], 
                './sensor_data/subway/sensorlab_2021-11-30-05.54.33_판교_상현/':[0, -1],

                './sensor_data/subway/sensorlab_2021-12-01-09.05.18_상현_판교/':[600, 19980],
                './sensor_data/subway/sensorlab_2021-12-01-08.10.21_판교_상현/':[1000, 20300],

                './sensor_data/subway/sensorlab_2021-12-02-08.16.27_상현_판교/':[0, -1],
                './sensor_data/subway/sensorlab_2021-12-02-06.24.00_판교_상현/':[600, 20350],

                './sensor_data/subway/sensorlab_2021-12-08-09.32.09_상현_판교/':[800, 20000],
                './sensor_data/subway/sensorlab_2021-12-09-08.01.12_상현_판교/':[600, 20150],
                './sensor_data/subway/sensorlab_2021-12-09-10.19.43_판교_상현/':[500, 20550],
                './sensor_data/subway/sensorlab_2021-12-10-09.17.47_판교_상현/':[800, 20000],

                './sensor_data/subway/sensorlab_2021-12-20-08.15.56_상현_판교/':[600, 20250],
                './sensor_data/subway/sensorlab_2021-12-20-08.42.17_판교_상현/':[750, 19500],
                
                './sensor_data/subway/sensorlab_2021-12-23-05.46.09_판교_상현/':[500, 20600],
                './sensor_data/subway/sensorlab_2021-12-23-07.46.29_상현_판교/':[400, 20400],

                './sensor_data/subway/sensorlab_2022-01-03-09.06.04_상현_판교/':[400, 20000],
                './sensor_data/subway/sensorlab_2022-01-03-10.52.04_판교_상현/':[250, 19450],
                './sensor_data/subway/sensorlab_2022-01-04-06.19.01_판교_상현/':[600, 20000],
                './sensor_data/subway/sensorlab_2022-01-04-08.42.19_상현_판교/':[300, 20300],
                './sensor_data/subway/sensorlab_2022-01-05-06.24.02_판교_상현/':[0, -1],
                './sensor_data/subway/sensorlab_2022-01-05-09.17.49_상현_판교/':[300, 19600],

                './sensor_data/subway/sensordata_220105_상현_판교/':[400, 19250],
                './sensor_data/subway/sensordata_220105_판교_상현/':[800, 19900],

                './sensor_data/subway/sensorlab_2022-01-08-03.57.39_남구로_신대방삼거리/':[0, -1],
                './sensor_data/subway/sensorlab_2022-01-08-04.43.50_신대방삼거리_군자/':[0, -1],
                './sensor_data/subway/sensorlab_2022-01-08-05.27.59_군자_길동/':[0, -1],
		'./sensor_data/subway/sensorlab_2022-01-08-11.01.27_길동_군자/':[0, -1],
		'./sensor_data/subway/sensorlab_2022-01-08-11.19.23_군자_대림/':[0, -1],

                './sensor_data/subway/sensordata_220108_군자_길동/':[0, -1],
                './sensor_data/subway/sensordata_220108_남구로_신대방삼거리/':[0, -1],
                './sensor_data/subway/sensordata_220108_길동_군자/':[0, -1],
                './sensor_data/subway/sensordata_220108_신대방삼거리_군자/':[0, -1],
                './sensor_data/subway/sensordata_220108_군자_대림/':[0, -1],

                './sensor_data/subway/sensorlab_2022-01-10-07.10.08_판교_상현/':[0, -1],
                './sensor_data/subway/sensorlab_2022-01-10-08.52.28_상현_판교/':[500, 20200],

                './sensor_data/subway/sensordata_220110_판교_상현/':[0, -1],
                './sensor_data/subway/sensordata_220110_상현_판교/':[500, 20100],

                './sensor_data/subway/sensordata_220112_판교_상현/':[0, -1],
                './sensor_data/subway/sensordata_220112_상현_판교/':[600, 19700],
                './sensor_data/subway/sensordata_220117_상현_판교/':[800, 19350],
                './sensor_data/subway/sensordata_220117_판교_상현/':[0, -1],
                './sensor_data/subway/sensordata_220119_판교_상현/':[800, 19900],
                './sensor_data/subway/sensordata_220119_상현_판교/':[1000, 19500],
                './sensor_data/subway/sensordata_220121_상현_판교/':[300, 19800],
                './sensor_data/subway/sensordata_220121_판교_상현/':[950, 19800],
                './sensor_data/subway/sensorlab_2022-01-12-09.39.29_상현_판교/':[750, 19600],
                './sensor_data/subway/sensorlab_2022-01-12-10.33.58_판교_상현/':[900, 19650],
                './sensor_data/subway/sensorlab_2022-01-17-08.42.36_상현_판교/':[300, 19800],
                './sensor_data/subway/sensorlab_2022-01-17-08.49.46_판교_상현/':[400, 19700],
                './sensor_data/subway/sensorlab_2022-01-19-07.51.02_판교_상현/':[900, 20000],
                './sensor_data/subway/sensorlab_2022-01-19-08.42.20_상현_판교/':[1000, 19600],
                './sensor_data/subway/sensorlab_2022-01-21-09.39.26_상현_판교/':[300, 19900],
                './sensor_data/subway/sensorlab_2022-01-21-09.45.50_판교_상현/':[900, 19900],


                './sensor_data/subway/sensorlab_2022-01-26-07.10.30_판교_상현/':[0, -1],
                './sensor_data/subway/sensorlab_2022-01-26-09.33.26_상현_판교/':[550, 20300],
                './sensor_data/subway/sensorlab_2022-01-27-09.47.29_상현_판교/':[600, 20000],

                './sensor_data/subway/sensordata_220126_상현_판교/':[600, 20000],
                './sensor_data/subway/sensordata_220127_상현_판교/':[600, 20000],

                './sensor_data/subway/sensordata_220208_상현_판교/':[600, 19670],
                './sensor_data/subway/sensordata_220210_상현_판교/':[270, 20200],
                './sensor_data/subway/sensordata_220211_상현_판교/':[650, 20000],
                './sensor_data/subway/sensordata_220217_상현_판교/':[500, 19950],
                './sensor_data/subway/sensorlab_2022-02-08-09.25.33_상현_판교/':[650, 19680],
                './sensor_data/subway/sensorlab_2022-02-10-08.58.52_상현_판교/':[450, 20100],
                './sensor_data/subway/sensorlab_2022-02-11-09.47.29_상현_판교/':[700, 20000],
                './sensor_data/subway/sensorlab_2022-02-18-06.26.21_상현_양재/':[0, -1],
                './sensor_data/subway/sensorlab_2022-02-18-07.00.05_양재_약수/':[0, -1],
                './sensor_data/subway/sensorlab_2022-02-18-07.27.48_약수_공덕/':[0, -1],
                './sensor_data/subway/sensorlab_2022-03-24-11.55.23_상현_판교/':[450, 19900],
                './sensor_data/subway/sensorlab_2022-04-22-07.38.19_판교_상현/':[750, 20200],
                './sensor_data/subway/sensorlab_2022-04-22-09.14.32_상현_판교/':[850, 19200],
                './sensor_data/subway/sensorlab_2022-04-25-09.02.14_상현_판교/':[1100, 19250],
                './sensor_data/subway/sensorlab_2022-05-02-07.08.42_판교_상현_actively/':[1050, 19800],
                './sensor_data/subway/sensorlab_2022-05-02-09.02.15_상현_판교/':[500, 20050],

                './sensor_data/subway/sensorlab_2022-05-04-07.33.18_판교_상현_su/':[600, 20350],
                './sensor_data/subway/sensorlab_2022-05-04-09.20.59_판교_상현_sd/':[600, 19900],
                './sensor_data/subway/sensorlab_2022-05-09-07.38.43_판교_상현_su/':[300, 20350],
                './sensor_data/subway/sensorlab_2022-05-09-09.31.55_상현_판교_sd/':[700, 19900],
                './sensor_data/subway/sensorlab_2022-05-11-07.08.52_판교_상현_su/':[300, 20250],
                './sensor_data/subway/sensorlab_2022-05-11-08.17.21_상현_판교_su/':[500, 19900],

                './sensor_data/subway/sensorlab_2022-05-23-05.27.30_판교_상현_su/':[500, 20330],
                './sensor_data/subway/sensorlab_2022-05-23-06.42.19_상현_판교_sd/':[550, 20050],

                './sensor_data/subway/sensorlab_2022-05-24-09.26.38_상현_판교_sd/':[500, 20020], 
                './sensor_data/subway/sensorlab_2022-05-24-10.24.30_판교_상현_sd/':[420, 20100], 
                './sensor_data/subway/sensorlab_2022-05-25-07.18.31_판교_상현_sd/':[700, 20300], 
                './sensor_data/subway/sensorlab_2022-05-30-09.15.18_상현_판교_sd/':[600, 19700], 
                './sensor_data/subway/sensorlab_2022-05-30-07.32.08_판교_상현_su/':[700, 19800], 
                './sensor_data/subway/sensorlab_2022-06-02-07.47.15_상현_판교_sd/':[550, 19780], 
                './sensor_data/subway/sensorlab_2022-06-02-06.52.33_판교_상현_su/':[200, 20100], 

                './sensor_data/subway/sensorlab_2022-06-03-09.08.14_상현_판교_sd/':[600, 19850],
                './sensor_data/subway/sensorlab_2022-06-03-08.12.03_판교_상현_su/':[670, 19970],
                './sensor_data/subway/sensorlab_2022-06-03-09.08.09_상현_판교_sd_s7/':[700, 19750],
                './sensor_data/subway/sensorlab_2022-06-03-08.11.59_판교_상현_su_s7/':[700, 19950],

                './sensor_data/subway/sensorlab_2022-06-07-09.15.22_상현_판교_su/':[630, 19750],
                './sensor_data/subway/sensorlab_2022-06-07-07.26.33_판교_상현_su/':[1110, 20000],
                './sensor_data/subway/sensorlab_2022-06-07-09.15.23_상현_판교_su_s7/':[650, 19700],
                './sensor_data/subway/sensorlab_2022-06-07-07.26.31_판교_상현_su_s7/':[1200, 19930],

                './sensor_data/subway/sensorlab_2022-06-08-09.27.51_상현_판교_sd/':[430, 19380],
                './sensor_data/subway/sensorlab_2022-06-08-07.52.01_판교_상현_su/':[710, -1],
                './sensor_data/subway/sensorlab_2022-06-08-09.27.48_상현_판교_sd_s7/':[500, 19375],
                './sensor_data/subway/sensorlab_2022-06-08-07.52.03_판교_상현_su_s7/':[700, 20020],

                './sensor_data/subway/sensorlab_2022-06-09-09.33.48_상현_판교_sd/':[650, 19920],
                './sensor_data/subway/sensorlab_2022-06-09-07.27.09_판교_상현_su/':[600, 19900],
                './sensor_data/subway/sensorlab_2022-06-09-09.33.50_상현_판교_sd_s7/':[650, 19930],
                './sensor_data/subway/sensorlab_2022-06-09-07.27.10_판교_상현_su_s7/':[870, 19500],


                './sensor_data/subway/sensorlab_2022-06-10-09.33.52_상현_판교_sd/':[700, 19870],
                './sensor_data/subway/sensorlab_2022-06-10-04.22.54_판교_상현_su/':[1000, 19780],
                './sensor_data/subway/sensorlab_2022-06-10-09.33.47_상현_판교_sd_s7/':[700, 19630],
                './sensor_data/subway/sensorlab_2022-06-10-04.22.48_판교_상현_su_s7/':[1000, 19800],

                './sensor_data/subway/sensorlab_2022-06-13-08.57.16_상현_판교_sd_s7/':[460, 19835],
                './sensor_data/subway/sensorlab_2022-06-14-07.41.43_판교_상현_su_s7/':[1450, 19550],
                './sensor_data/subway/sensorlab_2022-06-14-09.33.39_상현_판교_sd/':[570, 19800],
                './sensor_data/subway/sensorlab_2022-06-14-07.41.37_판교_상현_su/':[1450, 19500],

                './sensor_data/subway/sensorlab_2022-06-15-07.43.20_판교_상현_su_s7/':[0, -1],
                './sensor_data/subway/sensorlab_2022-06-15-09.34.01_상현_판교_sd_s7/':[0, -1],

                './sensor_data/subway/sensorlab_2022-06-16-07.47.03_판교_상현_su_s7/':[830, 19760],
                './sensor_data/subway/sensorlab_2022-06-16-09.15.23_상현_판교_su_s7/':[600, 19730],
                './sensor_data/subway/sensorlab_2022-06-17-07.47.24_판교_상현_su_s7/':[600, 19600],
                './sensor_data/subway/sensorlab_2022-06-17-09.41.44_상현_판교_sd_s7/':[0, -1],

                './sensor_data/subway/sensorlab_2022-06-20-08.32.01_상현_판교_su_s7/':[720, 19850],
                './sensor_data/subway/sensorlab_2022-06-21-09.21.45_상현_판교_sd_s7/':[0, -1],
                './sensor_data/subway/sensorlab_2022-06-21-07.56.59_판교_상현_su_s7/':[0, -1],
                './sensor_data/subway/sensorlab_2022-06-23-09.41.18_상현_판교_sd_s7/':[830, 19500],
                './sensor_data/subway/sensorlab_2022-06-23-09.01.51_판교_상현_su_s7/':[1250, 19740],

                './sensor_data/subway/sensorlab_2022-06-27-09.08.12_상현_판교_sd_s7/':[0, -1],
                './sensor_data/subway/sensorlab_2022-06-27-10.58.38_판교_상현_sd_s7/':[0, -1],

                './sensor_data/subway/sensorlab_2022-06-28-09.33.51_상현_판교_sd_s7/':[0, -1],
                './sensor_data/subway/sensorlab_2022-06-29-09.34.03_상현_판교_sd_s7/':[430, 19600],

                './sensor_data/subway/sensorlab_2022-06-30-09.07.18_상현_판교_sd/':[1750, 21600],
                './sensor_data/subway/sensorlab_2022-07-01-09.33.40_상현_판교_sd/':[510, 20500],

                './sensor_data/subway/sensorlab_2022-07-04-09.33.44_상현_판교_sd_s7/':[500, 20450],
                './sensor_data/subway/sensorlab_2022-07-06-08.27.14_상현_판교_sd/':[500, 20470],
                './sensor_data/subway/sensorlab_2022-07-07-09.33.49_상현_판교_sd_s7/':[500, 20250],

                './sensor_data/subway/sensorlab_2022-07-11-09.27.16_상현_판교_sd/':[600, 20300], 
                './sensor_data/subway/sensorlab_2022-07-12-09.33.53_상현_판교_sd/':[330, 20170],
                './sensor_data/subway/sensorlab_2022-07-13-07.32.45_상현_판교_sd_actively/':[350, 19720],
                './sensor_data/subway/sensorlab_2022-07-14-09.33.41_상현_판교_sd/':[650, 20600],
                './sensor_data/subway/sensorlab_2022-07-15-09.34.04_상현_판교_sd/':[200, 20000],

                './sensor_data/subway/sensorlab_2022-07-19-09.33.47_상현_판교_sd/':[500, 20400],
                './sensor_data/subway/sensorlab_2022-07-20-09.34.00_상현_판교_sd/':[310, 20100],
                './sensor_data/subway/sensorlab_2022-07-21-09.34.02_상현_판교_sd/':[350, 19950],
                './sensor_data/subway/sensorlab_2022-07-26-09.02.24_상현_판교_sd/':[400, 20200],
                './sensor_data/subway/sensorlab_2022-07-27-09.34.12_상현_판교_sd/':[200, 19750],
                './sensor_data/subway/sensorlab_2022-07-28-09.15.35_상현_판교_sd/':[150, 20000],
                './sensor_data/subway/sensorlab_2022-08-03-10.37.24_판교_상현_sd/':[450, 20370],






                './sensor_data/bus/sensorlab_2020-10-19-bus670_퇴근/':[0, -1],               
                './sensor_data/bus/sensorlab_2020-10-21-bus720-2_s수지구청_d상현동/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-23-bus720-2_s수지구청_d린/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-28-bus700-2_s미금역_d린/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-19-bus670_s수지구청_d상현역/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-22-bus720-2_s오리역_d린/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-26-bus146_s강남역_d성수사거리/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-29-bus720-1_s미금역_d린/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-21-bus720-2/':[0, -1],
                './sensor_data/bus/sensorlab_2020-10-22-bus720-3_s수지구청_d상현역/':[0, -1],  
                './sensor_data/bus/sensorlab_2020-10-27-bus700-2_s동천역_d린/':[0, -1],

                './sensor_data/legacy_210302/sensorlab_2020-04-30-11.28.00-상현1/':[0, -1],
                './sensor_data/legacy_210302/sensorlab_2020-05-19-11.55.04-상현2/':[0, -1],
                }


        subway_paths_step_points = {
                './sensor_data/subway/sensorlab_2020-12-30-11.18.34_sub_line_02_왕십리_강남/':[0, 2100, 4500, 7100, 9100, 11700, 15000, 18500, 21400, 23900, 26200, 28500, 30800, 33100, -1],
                './sensor_data/subway/sensorlab_2021-01-06-09.13.34_sub_line_08_모란_천호/':[3500, 5700, 7800, 9800, 12100, 15400, 19900, 22300, 24500, 26500, 28600, 30700, 33500, 35800, 38900, -1],
                './sensor_data/subway/sensorlab_2021-01-06-09.52.26_sub_line_05_천호_충정로/':[0, 3000, 5900, 8300, 10900, 13500, 16100, 18000, 19900, 22100, 24300, 26500, 29000, 31600, 34200, 36600, -1],
                './sensor_data/subway/sensorlab_2021-01-06-10.35.31_sub_line_02_아현_강남/':[0, 2700, 5200, 8000, 10400, 13300, 15900, 18000, 20900, 24400, 26500, 28700, 30500, 34500, 36700, 39200, 44700, 47400, 50600, 52600, -1],
                './sensor_data/subway/sensorlab_2021-01-06-11.38.13_sub_line_sbds_강남_광교/':[0, 2900, 5600, 9300, 17300, 21300, 24300, 27500, 30900, 34000, 37700, 41600, -1],
                './sensor_data/subway/sensorlab_2021-01-24-02.11.47_line_bds_정자_왕십리/':[0, 2800, 5100, 7800, 10900, 14500, 16650, 19000, 22900, 27600, 32700, 34500, 36350, 38100, 40200, 42400, 44600, 46600, 49400, 52200, -1],
                './sensor_data/subway/sensorlab_2021-01-25-07.55.20_line_center_도농_옥수/':[0, 6800, 11400, 17000, 22300, 28100, 35300, 40100, 45600, 48500, -1],
                './sensor_data/subway/sensorlab_2021-01-25-08.43.05_line_03_옥수_양재/':[0, 4200, 7300, 9400, 12000, 15800, 17900, -1],

                './sensor_data/subway/sensorlab_2021-02-27-06.51.13_line_01_incheon_국제업무지구_계양/':[0, 2500, 4900, 7000, 9900, 11900, 14500, 16700, 19000, 20700, 23000, 24800, 26900, 28800, 31000, 34300, 36700, 39000, 41400, 43400, 45800, 47900, 50400, 52500, 54800, 57400, 59900, 63000, -1],
                './sensor_data/subway/sensorlab_2021-02-27-08.29.13_line_02_incheon_인천시청_검단오류/':[0, 1700, 3900, 6900, 8800, 11400, 14100, 16300, 18100, 20300, 22900, 26100, 27700, 29800, 32300, 35900, 37900, 39700, 42300, 44800, -1],

                './sensor_data/subway/sensorlab_2021-03-07-01.05.36_line_01_daegu_동대구_설화명곡/':[0, 1900, 4400, 6100, 8500, 10300, 12700, 14300, 16700, 18700, 20700, 22500, 24500, 26500, 28600, 30700, 32600, 34500, 37000, -1],
                './sensor_data/subway/sensorlab_2021-03-07-02.23.16_line_03_daegu_명덕_칠곡경대병원/':[0, 1900, 3950, 6500, 8500, 10900, 13100, 14400, 16400, 18300, 20300, 22100, 24600, 26900, 28600, 30400, 31900, 34000, 35900, -1], # 30
                './sensor_data/subway/sensorlab_2021-03-07-04.10.38_line_02_daegu_영남대_반월당/':[0, 2100, 4800, 7100, 9500, 11800, 14100, 16300, 19400, 21700, 23800, 25800, 28100, 30500, -1],
                './sensor_data/subway/sensorlab_2021-03-08-06.37.18_line_02_busan_덕천_장산/':[0, 3100, 5100, 7700, 9800, 11700, 14700, 17100, 19500, 21600, 24100, 25900, 28000, 29900, 32500, 35200, 37700, 39100, 41600, 43900, 45600, 47900, 51900, 54000, 56200, 57900, 59100, 61600, 64100, 65800, 68500, 70900, -1],
                './sensor_data/subway/sensorlab_2021-03-09-12.57.13_line_donghae_busan_오시리아_부전/':[0, 2100, 6000, 11500, 14300, 16800, 19200, 22000, 24300, 27500, 29700, 32100, -1],
                './sensor_data/subway/sensorlab_2021-03-09-05.40.03_line_01_daejeon_대전_반석/':[0, 2000, 3900, 6700, 8900, 11600, 14300, 16500, 18700, 20700, 22800, 25300, 27700, 30000, 32200, 34500, 36500, 39000, -1],
                './sensor_data/subway/sensorlab_2021-03-20-03.52.53_line_01_busan_부산_다대포해수욕장/':[0, 2200, 4500, 6500, 9400, 12800, 16000, 18500, 20300, 22300, 24400, 26300, 29800, 33500, 36500, 38400, 41000, 43600, -1],

                }

        subway_paths_step_points_name = {
                './sensor_data/subway/sensorlab_2020-12-30-11.18.34_sub_line_02_왕십리_강남/':['왕십리', '한양대', '뚝섬', '성수', '건대입구', '구의', '강변', '잠실나루', '잠실', '잠실새내', '종합운동장', '삼성', '선릉', '역삼', '강남'],
                './sensor_data/subway/sensorlab_2021-01-06-09.13.34_sub_line_08_모란_천호/':['모란', '수진', '신흥', '단대오거리', '남한산성입구', '산성', '복정', '장지', '문정', '가락시장', '송파', '석촌', '잠실', '몽촌토성', '강동구청', '천호'],
                './sensor_data/subway/sensorlab_2021-01-06-09.52.26_sub_line_05_천호_충정로/':['천호', '광나루', '아차산', '군자', '장한평', '답십리', '마장', '왕십리', '행당', '신금호', '청구', '동대문역사문화공원', '을지로4가', '종로3가', '광화문', '서대문', '충정로'],
                #'./sensor_data/subway/sensorlab_2021-01-06-10.35.31_sub_line_02_아현_강남/':['충정로', '아현', '이대', '신촌', '홍대입구', '합정', '당산', '영등포구청', '문래', '신도림', '대림', '구로디지털단지', '신대방', '신림', '봉천', '서울대입구', '낙성대', '사당', '방배', '서초', '교대', '강남'],
                './sensor_data/subway/sensorlab_2021-01-06-10.35.31_sub_line_02_아현_강남/':['아현', '이대', '신촌', '홍대입구', '합정', '당산', '영등포구청', '문래', '신도림', '대림', '구로디지털단지', '신대방', '신림', '봉천', '서울대입구', '낙성대', '사당', '방배', '서초', '교대', '강남'],
                './sensor_data/subway/sensorlab_2021-01-06-11.38.13_sub_line_sbds_강남_광교/':['강남', '양재', '양재시민의숲', '청계산입구', '판교', '정자', '미금', '동천', '수지구청', '성복', '상현', '광교중앙', '광교'],
                './sensor_data/subway/sensorlab_2021-01-24-02.11.47_line_bds_정자_왕십리/':['정자', '수내', '서현', '이매', '야탑', '모란', '태평', '가천대', '복정', '수서', '대모산입구', '개포동', '구룡', '도곡', '한티', '선릉', '선정릉', '강남구청', '압구정로데오', '서울숲', '왕십리'],
                './sensor_data/subway/sensorlab_2021-01-25-07.55.20_line_center_도농_옥수/':['도농', '구리', '양원', '망우', '상봉', '중랑', '회기', '청량리', '왕십리', '응봉', '옥수'],
                './sensor_data/subway/sensorlab_2021-01-25-08.43.05_line_03_옥수_양재/':['옥수', '압구정', '신사', '잠원', '고속터미널', '교대', '남부터미널', '양재'],

                './sensor_data/subway/sensorlab_2021-02-27-06.51.13_line_01_incheon_국제업무지구_계양/':['국제업무지구', '센트럴파크', '인천대입구', '지식정보단지', '테크노파크', '캠퍼스타운', '동막', '동춘', '원인재', '신연수', '선학', '문학경기장', '인천터미널', '예술회관', '인천시청', '간석오거리', '부평삼거리', '동수', '부평', '부평시장', '부평구청', '갈산', '작전', '경인교대입구', '계산', '임학', '박촌', '귤현', '계양'],
                './sensor_data/subway/sensorlab_2021-02-27-08.29.13_line_02_incheon_인천시청_검단오류/':['인천시청', '석바위시장', '시민공원', '주안', '주안국가산단', '가재울', '인천가좌', '서부여성회관', '석남', '가정중앙시장', '가정', '서구청', '아시아드경기장', '검바위', '검암', '독정', '완정', '마전', '검단사거리', '왕길', '검단오류'],

                './sensor_data/subway/sensorlab_2021-03-07-01.05.36_line_01_daegu_동대구_설화명곡/':['동대구', '신천', '칠성시장', '대구', '중앙로', '반월당', '명덕', '교대', '영대병원', '현충로', '안지랑', '대명', '성당못', '송현', '월촌', '상인', '월배', '진천', '대곡', '화원', '설화명곡'],
                './sensor_data/subway/sensorlab_2021-03-07-02.23.16_line_03_daegu_명덕_칠곡경대병원/':['명덕', '남산', '신남', '서문시장', '달성공원', '북구청', '원대', '팔달시장', '만평', '공단', '팔달', '매천시장', '매천', '태전', '구암', '칠곡운암', '동천', '팔거', '학정', '칠곡경대병원'], # 30
                './sensor_data/subway/sensorlab_2021-03-07-04.10.38_line_02_daegu_영남대_반월당/':['영남대', '임당', '정평', '사월', '신매', '고산', '대공원', '연호', '담티', '만촌', '수성구청', '범어', '대구은행', '경대병원', '반월당'],
                './sensor_data/subway/sensorlab_2021-03-08-06.37.18_line_02_busan_덕천_장산/':['덕천', '구명', '구남', '모라', '모덕', '덕포', '사상', '감전', '주례', '냉정', '개금', '동의대', '가야', '부암', '서면', '전포', '국제금융센터.부산은행', '문현', '지게골', '못골', '대연', '경성대.부경대', '남천', '금련산', '광안', '수영', '민락', '센텀시티', '벡스코', '동백', '해운대', '중동', '장산'],
                './sensor_data/subway/sensorlab_2021-03-09-12.57.13_line_donghae_busan_오시리아_부전/':['오시리아', '송정', '신해운대', '벡스코', '센텀', '재송', '원동', '안락', '동래', '교대', '거제', '거제해맞이', '부전'],
                './sensor_data/subway/sensorlab_2021-03-09-05.40.03_line_01_daejeon_대전_반석/':['대전', '중앙로', '중구청', '서대전네거리', '오룡', '용문', '탄방', '시청', '정부청사', '갈마', '월평', '갑천', '유성온천', '구암', '현충원', '월드컵경기장', '노은', '지족', '반석'],
                './sensor_data/subway/sensorlab_2021-03-20-03.52.53_line_01_busan_부산_다대포해수욕장/':['부산', '중앙', '남포', '자갈치', '토성', '동대신', '서대신', '대티', '괴정', '사하', '당리', '하단', '신평', '동매', '장림', '신장림', '낫개', '다대포항', '다대포해수욕장'],

                }

        return oSubway_paths, oSubway_paths_dic, subway_paths_step_points, subway_paths_step_points_name 





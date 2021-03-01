import ast
from pylab import *
import os
import re
import csv
import xlrd
from shutil import copyfile
import pandas as pd
import numpy as np
import scipy.signal as scisig
from test_load_files import getInputLoadFile, getOutputPath
import shutil

enter_directory_path = "C:/Users/ascmeor/Desktop/"

# parameter definitions
input_folder_name="ASCMEOR DATASET TEST/"
output_folder_name= "ASCMEOR DATASET PREPROCESSED OUTPUT/"
input_directory_path = enter_directory_path +output_folder_name +"0000-PROCESSED data/"
output_directory_path = enter_directory_path+ output_folder_name
### folders to be created

#stage 1 folders
folder1 = "0001_RAW_DATA_EDA"
folder2 = "0002_RAW_DATA_HRV"
folder3 = "0003_LEGO-LOF (HRV) processed"
folder4 = "0004_BASELINE (HRV) processed"
folder5 = "0009_LEGO-LOF (EDA) processed"
folder6 = "0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED"
folder7 = "0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED"
folder8 = "0010_BASELINE (EDA) processed"
folder9 = "0011_LEGO-LOF (ACC) processed"
#stage 2 folders
folder10 = "0009_batch_LEGO-LOF (EDA) processed"
folder11 = "0009_batch5_LEGO-LOF (EDA) processed"
folder12 = "0010_batch_BASELINE (EDA) processed"
folder13 = "0010_batch_break_BASELINE (EDA) processed"
folder14 = "0011_batch_all_LEGO-LOF (ACC) processed"
folder15 = '0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED'

folder16 = "0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH"
folder17 = "0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH"
folder18 = "0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH"
folder19 =  '0015_OUTPUT'

folder20 = "0005-LEGO-LOF (HRV) extracted features_EVENT"
folder21 = "0005-LEGO-LOF (HRV) extracted features_EVENT2"
folder22 = "0005-LEGO-LOF (HRV) extracted features_EVENT3"
folder23 = "0006-BASELINE (HRV) extracted features"
folder24 = "0017-RESULT-ECG-EVENT"
folder25 = "RESULT"
folder26 = "0005-LEGO-LOF (HRV) extracted features"

###
data_path= input_directory_path
output_path_main =  output_directory_path
physio_raw_data_path= input_directory_path+ '0000-RAW data'
###
directory_batch5_LEGO_LOF = input_directory_path + '0009_batch5_LEGO-LOF (EDA) processed/'
directory_batch_LEGO_LOF= input_directory_path+ '0009_batch_LEGO-LOF (EDA) processed/'
directory_batch_baseline_LEGO_LOF = input_directory_path+'0010_batch_BASELINE (EDA) processed/'
directory_batch_break_baselineLEGO_LOF = input_directory_path+'0010_batch_break_BASELINE (EDA) processed/'
directory_batch_all_LEGO_LOF_ACC = input_directory_path+ '0011_batch_all_LEGO-LOF (ACC) processed/'
directory_batch_all2_LEGO_LOF_ACC = directory_batch_all_LEGO_LOF_ACC
###
video_code_input_destination_ASC = input_directory_path + "0008-VIDEO-CODING/"
video_code_output_destination_ASC= output_directory_path+ "0008-VIDEO-CODING/"
video_code_input_destination_NONASC = input_directory_path+"0008-VIDEO-CODING - NONASC/"
video_code_output_destination_NONASC= output_directory_path+"0008-VIDEO-CODING - NONASC/"
###
system_log_input_destination = input_directory_path +"0007-SYSTEM_LOGS/"
system_log_output_destination= output_directory_path+ "0007-SYSTEM_LOGS/"
###
qst_input_destination = input_directory_path +"0009-Questionnaires/"
qst_output_destination= output_directory_path+ "0009-Questionnaires/"

main_loop_start_count = 0  # for experiment 0018 , it should be 17# main for loopu 16,numberofexperiments ile basla vev count down step by step
samplingrate = 500
samplingfreq = 0.002
skipped_experiment = 10
skipped_experiment2 = 30
skipped_experiment3 = 31
skipped_experiment4 = 6
flag_second_session_exist = 1
experiment_number_which_doesnot_have_2nd_session = 6
numberofexperiments = 34  # for experiment 0018 , it should be 18
starting_point = 1
wzscore = 0

#########stage
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
def move_processeddata_out_for_processeing():

    source3 = input_directory_path+'0003_LEGO-LOF (HRV) processed/'
    source4 = input_directory_path+'0004_BASELINE (HRV) processed/'
    #source5 = input_directory_path+'0009_LEGO-LOF (EDA) processed/'
    #source6 = input_directory_path+'0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED/'
    #source7 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED/'
    #source8 = input_directory_path+'0010_BASELINE (EDA) processed/'
    #source9 = input_directory_path+'0011_LEGO-LOF (ACC) processed/'

    source10 = input_directory_path+'0009_batch_LEGO-LOF (EDA) processed/'
    source11 = input_directory_path+'0009_batch5_LEGO-LOF (EDA) processed/'
    source12 = input_directory_path+'0010_batch_BASELINE (EDA) processed/'
    source13 = input_directory_path+'0010_batch_break_BASELINE (EDA) processed/'
    source14 = input_directory_path+'0011_batch_all_LEGO-LOF (ACC) processed/'
    #source15 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED/'

    source16 = input_directory_path+ "0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH/"
    source17 = input_directory_path+"0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH/"
    source18 = input_directory_path+ "0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH/"
    #source19 = input_directory_path + "0015_OUTPUT/"


    destination = output_directory_path

    shutil.move(source3, destination)
    shutil.move(source4, destination)
    #shutil.move(source5, destination)
    #shutil.move(source6, destination)
    #shutil.move(source7, destination)
    #shutil.move(source8, destination)
    #shutil.move(source9, destination)

    shutil.move(source10, destination)
    shutil.move(source11, destination)
    shutil.move(source12, destination)
    shutil.move(source13, destination)
    shutil.move(source14, destination)
    #shutil.move(source15, destination)

    shutil.move(source16, destination)
    shutil.move(source17, destination)
    shutil.move(source18, destination)
    #shutil.move(source19, destination)
def move_processeddata_out_for_processeing_back():
    source3 = '0003_LEGO-LOF (HRV) processed/'
    source4 = '0004_BASELINE (HRV) processed/'
    #source5 = input_directory_path+'0009_LEGO-LOF (EDA) processed/'
    #source6 = input_directory_path+'0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED/'
    #source7 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED/'
    #source8 = input_directory_path+'0010_BASELINE (EDA) processed/'
    #source9 = input_directory_path+'0011_LEGO-LOF (ACC) processed/'

    source10 ='0009_batch_LEGO-LOF (EDA) processed/'
    source11 = '0009_batch5_LEGO-LOF (EDA) processed/'
    source12 = '0010_batch_BASELINE (EDA) processed/'
    source13 = '0010_batch_break_BASELINE (EDA) processed/'
    source14 = '0011_batch_all_LEGO-LOF (ACC) processed/'
    #source15 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED/'

    source16 = "0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH/"
    source17 = "0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH/"
    source18 = "0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH/"
    #source19 = input_directory_path + "0015_OUTPUT/"

    os.chdir(output_directory_path)

    destination = output_directory_path

    shutil.move(source3,input_directory_path)
    shutil.move(source4,input_directory_path)
    #shutil.move(source5, destination)
    #shutil.move(source6, destination)
    #shutil.move(source7, destination)
    #shutil.move(source8, destination)
    #shutil.move(source9, destination)

    shutil.move(source10,input_directory_path)
    shutil.move(source11,input_directory_path)
    shutil.move(source12,input_directory_path)
    shutil.move(source13,input_directory_path)
    shutil.move(source14,input_directory_path)
    #shutil.move(source15, destination)

    shutil.move(source16,input_directory_path)
    shutil.move(source17,input_directory_path)
    shutil.move(source18,input_directory_path)
    #shutil.move(source19, destination)


    os.chdir(output_directory_path)
    shutil.rmtree(output_directory_path+"0015_OUTPUT")
    shutil.rmtree(output_directory_path+"0017-RESULT-ECG-EVENT")
    shutil.rmtree(output_directory_path+"0005-LEGO-LOF (HRV) extracted features")
    shutil.rmtree(output_directory_path+"0005-LEGO-LOF (HRV) extracted features_EVENT")
    shutil.rmtree(output_directory_path+"0005-LEGO-LOF (HRV) extracted features_EVENT2")
    shutil.rmtree(output_directory_path+"0005-LEGO-LOF (HRV) extracted features_EVENT3")
    shutil.rmtree(output_directory_path+"0006-BASELINE (HRV) extracted features")
    # os.remove("0015_OUTPUT")
    # os.remove("0017-RESULT-ECG-EVENT")
    # os.remove("0005-LEGO-LOF (HRV) extracted features")
    # os.remove("0005-LEGO-LOF (HRV) extracted features_EVENT")
    # os.remove("0005-LEGO-LOF (HRV) extracted features_EVENT2")
    # os.remove("0005-LEGO-LOF (HRV) extracted features_EVENT3")
    # os.remove("0006-BASELINE (HRV) extracted features")

    # shutil.move("0015_OUTPUT",input_directory_path)
    # shutil.move("0017-RESULT-ECG-EVENT",input_directory_path)
    # shutil.move("0005-LEGO-LOF (HRV) extracted features",input_directory_path)
    # shutil.move("0005-LEGO-LOF (HRV) extracted features_EVENT",input_directory_path)
    # shutil.move("0005-LEGO-LOF (HRV) extracted features_EVENT2",input_directory_path)
    # shutil.move("0005-LEGO-LOF (HRV) extracted features_EVENT3",input_directory_path)
    # shutil.move("0006-BASELINE (HRV) extracted features",input_directory_path)



#10--------- ECG manual processing  & Manuel artifact correction
def datafolder_preparation_ECG():
    os.chdir(output_directory_path)
    ####stage 1 folders

    createFolder(output_directory_path + folder19)
    createFolder(output_directory_path+folder20)
    createFolder(output_directory_path+folder21)
    createFolder(output_directory_path+folder22)
    createFolder(output_directory_path+folder23)

    createFolder(output_directory_path + folder24)
    os.chdir(output_directory_path + folder24)

    for i in range (1,numberofexperiments+1):
        if i < 10:
            folder_number = "000" + str(i)
        elif i >= 10 and i < 100:
            folder_number = "00" + str(i)
        elif i >= 100 and i < 1000:
            folder_number = "0" + str(i)
        elif i >= 1000:
            folder_number = str(i)
        # if i ==10:
        #     print "pass"
        # else:
        #     createFolder(output_directory_path + folder24+"/"+folder_number)
        createFolder(output_directory_path + folder24 + "/" + folder_number)

    createFolder(output_directory_path + folder26)
def ECG_feature_extraction():
    os.chdir(output_directory_path)
    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index", "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn", "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 80, 81, 82, 83, 84
        , 85, 86]

    def first_step():

        test1 = 1
        test2 = 1
        test3 = 1



        def system_log_marking(trial, participant, condition):
            os.chdir('..')  # os.chdir('./' + 'event' + '/')
            os.chdir('..')  # os.chdir('./' + condition + '/')
            os.chdir('..')  # os.chdir('./' + trial + '_' + str(participant) + '/')
            os.chdir('..')  # os.chdir('./0003_LEGO-LOF (HRV) processed')

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')
            file_name = 'output_kubios_merge_time_' + trial + '_total_3' + '.txt'

            data = pd.read_csv(file_name, delimiter='\t', header=None)
            length = data.shape[0]
            list_system_log = []

            # print length
            for i in range(0, length):
                list_system_log.append(data.iloc[i, 0])

            # print list_system_log
            # print str(trial) + ' ' + str(participant) + ' ' + str(condition)

            # for i in range(0, len(s2a.iloc[0])):
            #     list.append(s2a.iloc[0, i])

            # for i in range(0, len(s2a.iloc[0])):
            #     list.append(s2a.iloc[0, i])
            #
            # rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

            os.chdir('..')  # os.chdir('./' + trial +'/')
            os.chdir('..')  # os.chdir('./0007-SYSTEM_LOGS2')

            os.chdir('./0003_LEGO-LOF (HRV) processed')
            os.chdir('./' + trial + '_' + str(participant) + '/')
            os.chdir('./' + condition + '/')
            os.chdir('./' + 'event' + '/')

            return list_system_log

        def video_log_marking(trial, participant, condition):

            list_video_log = []
            list_video_log_type = []
            feature_set_array_sizes = []

            if participant == 44:
                os.chdir('..')  # os.chdir('./' + 'event' + '/')
                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('..')  # os.chdir('./0003_LEGO-LOF (HRV) processed')

                os.chdir('./0008-VIDEO-CODING - NONASC')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                file_name = 'output_kubios_all_' + trial + '_' + condition + '_time_WO_headers3' + '.txt'

                data = pd.read_csv(file_name, delimiter='\t', header=None, skiprows=1)
                length = data.shape[0]

                # print length
                for i in range(0, length):
                    if data.iloc[i, 0] == 'time':
                        # print str(data.iloc[i, 2])
                        feature_set_array_sizes.append(data.iloc[i, 2])
                    else:
                        list_video_log.append(data.iloc[i, 0])
                        list_video_log_type.append(data.iloc[i, 2])

                # print list_video_log
                # print str(trial) + ' ' + str(participant) + ' ' + str(condition)

                # for i in range(0, len(s2a.iloc[0])):
                #     list.append(s2a.iloc[0, i])

                # for i in range(0, len(s2a.iloc[0])):
                #     list.append(s2a.iloc[0, i])
                #
                # rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial +'/')
                os.chdir('..')  # os.chdir('./0007-SYSTEM_LOGS2')

                os.chdir('./0003_LEGO-LOF (HRV) processed')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                os.chdir('./' + 'event2' + '/')
            elif participant == 55:
                os.chdir('..')  # os.chdir('./' + 'event' + '/')
                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('..')  # os.chdir('./0003_LEGO-LOF (HRV) processed')

                os.chdir('./0008-VIDEO-CODING')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                file_name = 'output_kubios_all_' + trial + '_' + condition + '_time_WO_headers3' + '.txt'

                data = pd.read_csv(file_name, delimiter='\t', header=None, skiprows=1)
                length = data.shape[0]

                # print length
                for i in range(0, length):
                    if data.iloc[i, 0] == 'time':
                        # print str(data.iloc[i, 2])
                        feature_set_array_sizes.append(data.iloc[i, 2])
                    else:
                        list_video_log.append(data.iloc[i, 0])
                        list_video_log_type.append(data.iloc[i, 2])

                # print list_video_log
                # print str(trial) + ' ' + str(participant) + ' ' + str(condition)

                # for i in range(0, len(s2a.iloc[0])):
                #     list.append(s2a.iloc[0, i])

                # for i in range(0, len(s2a.iloc[0])):
                #     list.append(s2a.iloc[0, i])
                #
                # rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial +'/')
                os.chdir('..')  # os.chdir('./0007-SYSTEM_LOGS2')

                os.chdir('./0003_LEGO-LOF (HRV) processed')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                os.chdir('./' + 'event2' + '/')

            return list_video_log, list_video_log_type


        def write_feature_datasets(rawdata_name):
            if feature_to_be_extracted >= 80:
                # s1a = pd.read_csv(rawdata_filename, delimiter =';',skiprows = feature_to_be_extracted)
                # print s1a
                output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted - 52] + ';' + "\n")
                pass
            else:

                s2a = pd.read_csv(rawdata_filename, delimiter=';', skiprows=(feature_to_be_extracted), header=None)

                # print list

                if feature_to_be_extracted >= 55 and feature_to_be_extracted <= 70:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    output_feature.write(rawdata_name + ";")

                    k = 1
                    list2 = []
                    for i in range(1, len(list)):
                        if k >= len(list):
                            break
                        else:
                            output_feature.write(str(list[k]) + ';')
                            if k + 1 >= len(list):
                                pass
                            else:
                                list2.append(list[k + 1])
                            k = k + 2

                    output_feature.write("\n")

                    output_feature.write(rawdata_name + '2' + ";")

                    for i in range(0, len(list2)):
                        output_feature.write(str(list2[i]) + ';')
                    output_feature.write("\n")




                elif feature_to_be_extracted >= 77 and feature_to_be_extracted <= 79:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        if i == 1:
                            pass
                        else:
                            list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    # print rawdata_name

                    output_feature.write(rawdata_name + ";")

                    k = 2
                    for i in range(1, len(list)):
                        if k >= len(list):
                            break
                        else:
                            output_feature.write(str(list[k]) + ';')
                            k = k + 2

                    output_feature.write("\n")



                else:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])
                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    output_feature.write(rawdata_name + ";")

                    k = 1
                    for i in range(1, len(list)):
                        if k >= len(list):
                            break
                        else:
                            output_feature.write(str(list[k]) + ';')
                            k = k + 2

                    output_feature.write("\n")
                    # print list

        def write_feature_datasets_row_format(rawdata_name):
            no_calc1 = 1
            no_calc2 = 1
            no_calc3 = 1

            if feature_to_be_extracted >= 80:
                # s1a = pd.read_csv(rawdata_filename, delimiter =';',skiprows = feature_to_be_extracted)
                # print s1a
                output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted - 52] + ';' + "\n")
                pass
            else:

                # print rawdata_filename
                # print feature_to_be_extracted

                # if feature_to_be_extracted>=61 and  feature_to_be_extracted<=79 and trial =='0012':
                #     print 'x'
                # else:
                s2a = pd.read_csv(rawdata_filename, delimiter=';', skiprows=(feature_to_be_extracted), header=None)

                if feature_to_be_extracted >= 55 and feature_to_be_extracted <= 70:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    system_log_list = system_log_marking(trial, participant, condition)

                    k = 1
                    list2 = []
                    no_calc1 = 1
                    no_calc2 = 1
                    no_calc3 = 1

                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2

                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            if a == len(system_log_list):
                                # part ='nan'
                                break
                            elif system_log_list[a] < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif system_log_list[a] >= 300 and system_log_list[a] < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif system_log_list[a] >= 600 and system_log_list[a] <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':
                                if system_log_list[a] > 870:
                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";")
                                    output_feature.write("\n")

                                else:
                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";" + str(
                                            list[k]))
                                    output_feature.write("\n")

                            if k + 1 >= len(list):
                                pass
                            else:
                                list2.append(list[k + 1])

                            k = k + 2

                    system_log_list = system_log_marking(trial, participant, condition)

                    no_calc1 = 1
                    no_calc2 = 1
                    no_calc3 = 1

                    for i in range(0, len(list2)):

                        if i == len(system_log_list):
                            # part = 'nan'
                            break
                        elif system_log_list[i] < 300:
                            part = 'first'
                            no_calc1 = no_calc1 + 1
                        elif system_log_list[i] >= 300 and system_log_list[i] < 600:
                            part = 'mid'
                            no_calc2 = no_calc2 + 1
                        elif system_log_list[i] >= 600 and system_log_list[i] <= 900:
                            part = 'last'
                            no_calc3 = no_calc3 + 1

                        if part == 'first':
                            output_feature.write(
                                rawdata_name + '2' + ';' + part + ';' + str(no_calc1) + ';' + '5' + ";" + str(list2[i]))
                            output_feature.write("\n")
                        elif part == 'mid':
                            output_feature.write(
                                rawdata_name + '2' + ';' + part + ';' + str(no_calc2) + ';' + '5' + ";" + str(list2[i]))
                            output_feature.write("\n")
                        elif part == 'last':
                            if system_log_list[i] > 870:
                                output_feature.write(
                                    rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";")
                                output_feature.write("\n")
                            else:
                                output_feature.write(
                                    rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";" + str(
                                        list2[i]))
                                output_feature.write("\n")
                    test1 = no_calc1
                    test2 = no_calc2
                    test3 = no_calc3



                elif feature_to_be_extracted >= 77 and feature_to_be_extracted <= 79:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        if i == 1:
                            pass
                        else:
                            list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    # print rawdata_name

                    system_log_list = system_log_marking(trial, participant, condition)

                    k = 1

                    no_calc1 = 1
                    no_calc2 = 1
                    no_calc3 = 1
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            if a == len(system_log_list):
                                # part ='nan'
                                break
                            elif system_log_list[a] < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif system_log_list[a] >= 300 and system_log_list[a] < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif system_log_list[a] >= 600 and system_log_list[a] <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':

                                if system_log_list[a] > 870:
                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";")
                                    output_feature.write("\n")
                                else:

                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";" + str(
                                            list[k]))
                                    output_feature.write("\n")

                            k = k + 2

                    test1 = no_calc1
                    test2 = no_calc2
                    test3 = no_calc3

                else:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])
                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    system_log_list = system_log_marking(trial, participant, condition)

                    # print list

                    k = 1
                    no_calc1 = 1
                    no_calc2 = 1
                    no_calc3 = 1
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            if a == len(system_log_list):
                                # part ='nan'
                                break
                            elif system_log_list[a] < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif system_log_list[a] >= 300 and system_log_list[a] < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif system_log_list[a] >= 600 and system_log_list[a] <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(
                                    rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + '5' + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':
                                if system_log_list[a] > 870:
                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";")
                                    output_feature.write("\n")

                                else:

                                    output_feature.write(
                                        rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + '5' + ";" + str(
                                            list[k]))
                                    output_feature.write("\n")

                            k = k + 2

                    test1 = no_calc1
                    test2 = no_calc2
                    test3 = no_calc3

            print 'test1: ' + str(no_calc1)
            print 'test2: ' + str(no_calc2)
            print 'test3: ' + str(no_calc3)

            return no_calc1, no_calc2, no_calc3


        def write_feature_datasets_row_format_video(rawdata_name):

            if feature_to_be_extracted >= 80:

                # s1a = pd.read_csv(rawdata_filename, delimiter =';',skiprows = feature_to_be_extracted)
                # print s1a
                output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted - 52] + ';' + "\n")
                pass
            else:
                # print feature_to_be_extracted
                print rawdata_filename
                print feature_to_be_extracted
                s2a = pd.read_csv(rawdata_filename, delimiter=';', skiprows=(feature_to_be_extracted), header=None, )

                if feature_to_be_extracted >= 55 and feature_to_be_extracted <= 70:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    video_log_list, list_video_log_type = video_log_marking(trial, participant, condition)

                    k = 1
                    list2 = []
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3

                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':

                                if video_log_list[a] > 870:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")
                                else:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            if k + 1 >= len(list):
                                pass
                            else:
                                list2.append(list[k + 1])

                            k = k + 2

                    video_log_list, list_video_log_type = video_log_marking(trial, participant, condition)

                    # print 'asdasdasd'
                    # print len(list2)
                    # print len(video_log_list)
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    for i in range(0, len(list2)):

                        if i == len(video_log_list):
                            # part = 'nan'
                            break
                        elif float(video_log_list[i]) < 300:
                            part = 'first'
                            no_calc1 = no_calc1 + 1
                        elif float(video_log_list[i]) >= 300 and float(video_log_list[i]) < 600:
                            part = 'mid'
                            no_calc2 = no_calc2 + 1
                        elif float(video_log_list[i]) >= 600 and float(video_log_list[i]) <= 900:
                            part = 'last'
                            no_calc3 = no_calc3 + 1

                        if part == 'first':
                            output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc1) + ';' + str(
                                list_video_log_type[i]) + ";" + str(list2[i]))
                            output_feature.write("\n")

                        elif part == 'mid':
                            output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc2) + ';' + str(
                                list_video_log_type[i]) + ";" + str(list2[i]))
                            output_feature.write("\n")
                        elif part == 'last':

                            if video_log_list[i] > 870:
                                output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + str(
                                    list_video_log_type[i]) + ";")
                                output_feature.write("\n")
                            else:
                                output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + str(
                                    list_video_log_type[i]) + ";" + str(list2[i]))
                                output_feature.write("\n")




                elif feature_to_be_extracted >= 77 and feature_to_be_extracted <= 79:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        if i == 1:
                            pass
                        else:
                            list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    # print rawdata_name

                    video_log_list, list_video_log_type = video_log_marking(trial, participant, condition)

                    k = 1
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)

                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                no_calc1 = no_calc1 + 1
                                part = 'first'
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                no_calc2 = no_calc2 + 1
                                part = 'mid'
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                no_calc3 = no_calc3 + 1
                                part = 'last'

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':

                                if video_log_list[a] > 870:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")

                                else:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            k = k + 2





                else:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])
                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    video_log_list, list_video_log_type = video_log_marking(trial, participant, condition)
                    print video_log_list
                    # print list

                    k = 1
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            # print 'video_log_list:  '+ str(video_log_list[a])
                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")

                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")

                            elif part == 'last':

                                if video_log_list[a] > 870:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")

                                else:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            k = k + 2


        def SYSTEM_video_log_marking(trial, participant, condition):

            list_video_log = []
            list_video_log_type = []
            feature_set_array_sizes = []

            if participant == 44:
                os.chdir('..')  # os.chdir('./' + 'event' + '/')
                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('..')  # os.chdir('./0003_LEGO-LOF (HRV) processed')

                os.chdir('./0007-SYSTEM_LOGS')
                os.chdir('./' + trial + '/')

                file_name = 'kubious_all_new_' + trial + '_NONASC.txt'

                data = pd.read_csv(file_name, delimiter='\t', header=None, skiprows=1)
                length = data.shape[0]

                # print length
                for i in range(0, length):
                    if data.iloc[i, 0] == 'time':
                        # print str(data.iloc[i, 2])
                        feature_set_array_sizes.append(data.iloc[i, 2])
                    else:
                        list_video_log.append(data.iloc[i, 0])
                        list_video_log_type.append(data.iloc[i, 2])

                os.chdir('..')  # os.chdir('./' + trial +'/')
                os.chdir('..')  # os.chdir('./0007-SYSTEM_LOGS2')

                os.chdir('./0003_LEGO-LOF (HRV) processed')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                os.chdir('./' + 'event' + '/')
            elif participant == 55:
                os.chdir('..')  # os.chdir('./' + 'event' + '/')
                os.chdir('..')  # os.chdir('./' + condition + '/')
                os.chdir('..')  # os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('..')  # os.chdir('./0003_LEGO-LOF (HRV) processed')

                os.chdir('./0007-SYSTEM_LOGS')
                os.chdir('./' + trial + '/')

                file_name = 'kubious_all_new_' + trial  + '_ASC.txt'

                data = pd.read_csv(file_name, delimiter='\t', header=None, skiprows=1)
                length = data.shape[0]

                # print length
                for i in range(0, length):
                    if data.iloc[i, 0] == 'time':
                        # print str(data.iloc[i, 2])
                        feature_set_array_sizes.append(data.iloc[i, 2])
                    else:
                        list_video_log.append(data.iloc[i, 0])
                        list_video_log_type.append(data.iloc[i, 2])




                os.chdir('..')  # os.chdir('./' + trial +'/')
                os.chdir('..')  # os.chdir('./0007-SYSTEM_LOGS2')

                os.chdir('./0003_LEGO-LOF (HRV) processed')
                os.chdir('./' + trial + '_' + str(participant) + '/')
                os.chdir('./' + condition + '/')
                os.chdir('./' + 'event' + '/')

            return list_video_log, list_video_log_type

        def SYSTEM_write_feature_datasets_row_format_video(rawdata_name):

            a_no_calc1=1
            a_no_calc2=1
            a_no_calc3=1

            if feature_to_be_extracted >= 80:

                # s1a = pd.read_csv(rawdata_filename, delimiter =';',skiprows = feature_to_be_extracted)
                # print s1a
                output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted - 52] + ';' + "\n")
                pass
            else:
                # print feature_to_be_extracted
                print rawdata_filename
                print feature_to_be_extracted
                s2a = pd.read_csv(rawdata_filename, delimiter=';', skiprows=(feature_to_be_extracted), header=None, )

                if feature_to_be_extracted >= 55 and feature_to_be_extracted <= 70:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    video_log_list, list_video_log_type = SYSTEM_video_log_marking(trial, participant, condition)

                    k = 1
                    list2 = []
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3

                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':

                                if video_log_list[a] > 870:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")
                                else:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            if k + 1 >= len(list):
                                pass
                            else:
                                list2.append(list[k + 1])

                            k = k + 2

                    video_log_list, list_video_log_type = SYSTEM_video_log_marking(trial, participant, condition)

                    # print 'asdasdasd'
                    # print len(list2)
                    # print len(video_log_list)
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    for i in range(0, len(list2)):

                        if i == len(video_log_list):
                            # part = 'nan'
                            break
                        elif float(video_log_list[i]) < 300:
                            part = 'first'
                            no_calc1 = no_calc1 + 1
                        elif float(video_log_list[i]) >= 300 and float(video_log_list[i]) < 600:
                            part = 'mid'
                            no_calc2 = no_calc2 + 1
                        elif float(video_log_list[i]) >= 600 and float(video_log_list[i]) <= 900:
                            part = 'last'
                            no_calc3 = no_calc3 + 1

                        if part == 'first':
                            output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc1) + ';' + str(
                                list_video_log_type[i]) + ";" + str(list2[i]))
                            output_feature.write("\n")

                        elif part == 'mid':
                            output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc2) + ';' + str(
                                list_video_log_type[i]) + ";" + str(list2[i]))
                            output_feature.write("\n")
                        elif part == 'last':

                            if video_log_list[i] > 870:
                                output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + str(
                                    list_video_log_type[i]) + ";")
                                output_feature.write("\n")
                            else:
                                output_feature.write(rawdata_name + '2' + ';' + part + ';' + str(no_calc3) + ';' + str(
                                    list_video_log_type[i]) + ";" + str(list2[i]))
                                output_feature.write("\n")




                elif feature_to_be_extracted >= 77 and feature_to_be_extracted <= 79:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        if i == 1:
                            pass
                        else:
                            list.append(s2a.iloc[0, i])

                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    # print rawdata_name

                    video_log_list, list_video_log_type = SYSTEM_video_log_marking(trial, participant, condition)

                    k = 1
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)

                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                no_calc1 = no_calc1 + 1
                                part = 'first'
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                no_calc2 = no_calc2 + 1
                                part = 'mid'
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                no_calc3 = no_calc3 + 1
                                part = 'last'

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")
                            elif part == 'last':

                                if video_log_list[a] > 870:
                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")

                                else:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            k = k + 2





                else:

                    list = []
                    for i in range(0, len(s2a.iloc[0])):
                        list.append(s2a.iloc[0, i])
                    rawdata_name = rawdata_name + ';' + s2a.iloc[0, 0]

                    video_log_list, list_video_log_type = SYSTEM_video_log_marking(trial, participant, condition)
                    print video_log_list
                    # print list

                    k = 1
                    no_calc1 = a_no_calc1
                    no_calc2 = a_no_calc2
                    no_calc3 = a_no_calc3
                    while True:
                        if k >= len(list):
                            break
                        else:
                            a = k / 2
                            # print 'k ' + str(k)
                            # print 'a ' + str(a)
                            # print 'video_log_list:  '+ str(video_log_list[a])
                            if a == len(video_log_list):
                                # part ='nan'
                                break
                            elif float(video_log_list[a]) < 300:
                                part = 'first'
                                no_calc1 = no_calc1 + 1
                            elif float(video_log_list[a]) >= 300 and float(video_log_list[a]) < 600:
                                part = 'mid'
                                no_calc2 = no_calc2 + 1
                            elif float(video_log_list[a]) >= 600 and float(video_log_list[a]) <= 900:
                                part = 'last'
                                no_calc3 = no_calc3 + 1

                            if part == 'first':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc1) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")

                            elif part == 'mid':
                                output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc2) + ';' + str(
                                    list_video_log_type[a]) + ";" + str(list[k]))
                                output_feature.write("\n")

                            elif part == 'last':

                                if video_log_list[a] > 870:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";")
                                    output_feature.write("\n")

                                else:

                                    output_feature.write(rawdata_name + ';' + part + ';' + str(no_calc3) + ';' + str(
                                        list_video_log_type[a]) + ";" + str(list[k]))
                                    output_feature.write("\n")

                            k = k + 2



        # numberofexperiments = 1
        # starting_point = 1
        # skipped_experiment = 10
        # # def system_log_event_marking_main():
        for z in range(0, len(feature_list)):

            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT')
            feature_name = feature_list[z]
            feature_to_be_extracted = feature_list_no[z]

            createFolder('./' + feature_name + '/')
            os.chdir('./' + feature_name + '/')
            # print feature_name
            output_feature = open(feature_name + '.txt', 'w')
            os.chdir('..')
            os.chdir('..')

            os.chdir('./0003_LEGO-LOF (HRV) processed')

            #####################################

            for i in range(starting_point, numberofexperiments + 1):

                if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
                    continue
                else:
                    if i < 10:
                        trial = "000" + str(i)
                    elif i >= 10 and i < 100:
                        trial = "00" + str(i)
                    elif i >= 100 and i < 1000:
                        trial = "0" + str(i)
                    elif i >= 1000:
                        trial = str(i)
                    for j in range(1, 3):
                        doesnotexistcatch = [0, 0]
                        if j == 1:
                            participant = 44
                            # continue # this should be different for ECG system llog tagging
                        elif j == 2:
                            participant = 55
                        # print  './' + trial +'_' + str(participant) + '/'
                        # print(os.getcwd())
                        os.chdir('./' + trial + '_' + str(participant) + '/')
                        arr = os.listdir('.')
                        # print arr

                        for k in range(1, len(arr) + 1):

                            if str(arr[k - 1]) == "LEGO":
                                continue
                                # condition = "LEGO"
                                # doesnotexistcatch[0] = 1
                                # os.chdir('./' + condition + '/')
                                # os.chdir('./' + 'event' + '/')
                                # ###############################START OF FEATURE EXTRACTION
                                #
                                # input_file = open('output_'+trial + '_' + str(participant)+'_'+condition+'_ECG_hrv_event.txt', 'r')
                                # output_file = open('output_'+trial + '_' + str(participant)+'_'+condition+'_ECG_hrv_event_end.txt', 'w')
                                # ######### to remove the end of the file
                                # n = 1
                                #
                                #
                                #
                                # while True:
                                #
                                #     line = input_file.readline()
                                #     #print line
                                #     if (n == 113):
                                #         #print line
                                #         #print "file finished"
                                #         break
                                #
                                #     output_file.write(line)
                                #     n = n + 1
                                #
                                # ######### Dataset creation
                                #
                                #
                                # rawdata_filename = 'output_'+trial + '_' + str(participant)+'_'+condition+'_ECG_hrv_event_end.txt'
                                # rawdata_name = 'output_'+trial + ';' + str(participant)+';'+condition
                                #
                                # write_feature_datasets_row_format(rawdata_name)
                                # #video_log_marking(trial, participant, condition)
                                #
                                #
                                # #output_feature.write(rawdata_name+ ";" + s1a[0] + "\n")
                                #
                                #
                                #
                                #
                                # # s1a= np.loadtxt(rawdata_filename, usecols=(0),unpack=True, dtype= str, delimiter='\t', skiprows = feature_to_be_extracted)
                                # # #print s1a
                                # # output_feature.write(rawdata_name+ ";" + s1a[0] + "\n")
                                #
                                # ################################################END OF FEATURE EXTRACTION
                                # os.chdir('..')
                                # os.chdir('..')
                            elif str(arr[k - 1]) == "LOF":
                                condition = "LOF"
                                doesnotexistcatch[1] = 1
                                os.chdir('./' + condition + '/')
                                os.chdir('./' + 'event' + '/')
                                ###############################START OF FEATURE EXTRACTION

                                input_file = open(
                                    'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_event.txt',
                                    'r')
                                output_file = open(
                                    'output_' + trial + '_' + str(
                                        participant) + '_' + condition + '_ECG_hrv_event_end.txt',
                                    'w')
                                ######### to remove the end of the file
                                n = 1
                                while True:

                                    line = input_file.readline()

                                    if (n == 113):
                                        # print "file finished"
                                        break

                                    output_file.write(line)
                                    n = n + 1

                                ######### Dataset creation

                                rawdata_filename = 'output_' + trial + '_' + str(
                                    participant) + '_' + condition + '_ECG_hrv_event_end.txt'
                                rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition

                                SYSTEM_write_feature_datasets_row_format_video(rawdata_name)
                                # video_log_marking(trial, participant, condition)
                                # if feature_to_be_extracted >= 80:
                                #     #print feature_list[feature_to_be_extracted-52]
                                #     output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted-52]+';' + "\n")
                                #     pass
                                # else:
                                #     s1a = np.loadtxt(rawdata_filename, usecols=(0), unpack=True, dtype=str, delimiter='\t',
                                #                      skiprows=feature_to_be_extracted)
                                #     output_feature.write(rawdata_name + ";" + s1a[0] + "\n")

                                ################################################END OF FEATURE EXTRACTION

                                os.chdir('..')
                                os.chdir('..')
                            elif str(arr[k - 1]) == "ZDOESNOTEXIST":
                                # print doesnotexistcatch
                                # print "batu"
                                if doesnotexistcatch[0] == 1 and doesnotexistcatch[1] == 0:
                                    rawdata_name = 'output_' + trial + ';' + str(
                                        participant) + ';' + "LOF" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                    output_feature.write(rawdata_name + " " + "\n")
                                    doesnotexistcatch[0] == 0
                                    doesnotexistcatch[1] == 0
                                elif doesnotexistcatch[0] == 0 and doesnotexistcatch[1] == 1:
                                    rawdata_name = 'output_' + trial + ';' + str(
                                        participant) + ';' + "LEGO" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                    output_feature.write(rawdata_name + " " + "\n")
                                    doesnotexistcatch[0] == 0
                                    doesnotexistcatch[1] == 0
                                else:
                                    continue

                            else:

                                continue

                        os.chdir('..')
            os.chdir('..')

            # numberofexperiments=12
            # starting_point = 12
            # skipped_experiment = 10
            # def video_log_event_fmarking_main():

            print 'no_calc1: ' + str(test1)
            print 'no_calc2: ' + str(test2)
            print 'no_calc3: ' + str(test3)

            a_no_calc1 = test1
            a_no_calc2 = test2
            a_no_calc3 = test3

        for z in range(0, len(feature_list)):
            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT2')
            feature_name = feature_list[z]
            feature_to_be_extracted = feature_list_no[z]

            createFolder('./' + feature_name + '/')
            os.chdir('./' + feature_name + '/')
            # print feature_name
            output_feature = open(feature_name + '.txt', 'w')
            os.chdir('..')
            os.chdir('..')

            os.chdir('./0003_LEGO-LOF (HRV) processed')

            #####################################

            for i in range(starting_point, numberofexperiments + 1):

                if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
                    continue
                else:
                    if i < 10:
                        trial = "000" + str(i)
                    elif i >= 10 and i < 100:
                        trial = "00" + str(i)
                    elif i >= 100 and i < 1000:
                        trial = "0" + str(i)
                    elif i >= 1000:
                        trial = str(i)
                    for j in range(1, 3):
                        doesnotexistcatch = [0, 0]
                        if j == 1:
                            participant = 44
                            # continue # this should be different for ECG system llog tagging
                            #continue
                        elif j == 2:
                            participant = 55
                        # print  './' + trial +'_' + str(participant) + '/'
                        # print(os.getcwd())
                        os.chdir('./' + trial + '_' + str(participant) + '/')
                        arr = os.listdir('.')
                        # print arr


                        for k in range(1, len(arr) + 1):

                            if trial == "0011":
                                print "trial 0011"
                            else:
                                if str(arr[k - 1]) == "LEGO":
                                    condition = "LEGO"
                                    doesnotexistcatch[0] = 1
                                    os.chdir('./' + condition + '/')
                                    os.chdir('./' + 'event2' + '/')
                                    ###############################START OF FEATURE EXTRACTION

                                    if not os.listdir('./'):
                                        print("Directory is empty")

                                        os.chdir('..')
                                        os.chdir('..')
                                    else:


                                        input_file = open(
                                            'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_event.txt',
                                            'r')
                                        output_file = open('output_' + trial + '_' + str(
                                            participant) + '_' + condition + '_ECG_hrv_event_end.txt', 'w')
                                        ######### to remove the end of the file
                                        n = 1

                                        while True:

                                            line = input_file.readline()
                                            # print line
                                            if (n == 113):
                                                # print line
                                                # print "file finished"
                                                break

                                            output_file.write(line)
                                            n = n + 1

                                        ######### Dataset creation

                                        rawdata_filename = 'output_' + trial + '_' + str(
                                            participant) + '_' + condition + '_ECG_hrv_event_end.txt'
                                        rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # print 'batuaaaaaaaaa'
                                        print rawdata_filename
                                        print rawdata_name
                                        write_feature_datasets_row_format_video(rawdata_name)
                                        # video_log_marking(trial, participant, condition)

                                        # output_feature.write(rawdata_name+ ";" + s1a[0] + "\n")

                                        # s1a= np.loadtxt(rawdata_filename, usecols=(0),unpack=True, dtype= str, delimiter='\t', skiprows = feature_to_be_extracted)
                                        # #print s1a
                                        # output_feature.write(rawdata_name+ ";" + s1a[0] + "\n")

                                        ################################################END OF FEATURE EXTRACTION
                                        os.chdir('..')
                                        os.chdir('..')
                                elif str(arr[k - 1]) == "LOF":
                                    condition = "LOF"
                                    doesnotexistcatch[1] = 1
                                    os.chdir('./' + condition + '/')
                                    os.chdir('./' + 'event2' + '/')
                                    if not os.listdir('./') or trial == "0001" or trial == "0011":
                                        print("Directory is empty")

                                        os.chdir('..')
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                        ###############################START OF FEATURE EXTRACTION

                                        input_file = open(
                                            'output_' + trial + '_' + str(
                                                participant) + '_' + condition + '_ECG_hrv_event.txt',
                                            'r')
                                        output_file = open('output_' + trial + '_' + str(
                                            participant) + '_' + condition + '_ECG_hrv_event_end.txt', 'w')
                                        ######### to remove the end of the file
                                        n = 1
                                        while True:

                                            line = input_file.readline()

                                            if (n == 113):
                                                # print "file finished"
                                                break

                                            output_file.write(line)
                                            n = n + 1

                                        ######### Dataset creation

                                        rawdata_filename = 'output_' + trial + '_' + str(
                                            participant) + '_' + condition + '_ECG_hrv_event_end.txt'
                                        rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # print 'batu2'
                                        write_feature_datasets_row_format_video(rawdata_name)
                                        # video_log_marking(trial, participant, condition)
                                        # if feature_to_be_extracted >= 80:
                                        #     #print feature_list[feature_to_be_extracted-52]
                                        #     output_feature.write(rawdata_name + ";" + feature_list[feature_to_be_extracted-52]+';' + "\n")
                                        #     pass
                                        # else:
                                        #     s1a = np.loadtxt(rawdata_filename, usecols=(0), unpack=True, dtype=str, delimiter='\t',
                                        #                      skiprows=feature_to_be_extracted)
                                        #     output_feature.write(rawdata_name + ";" + s1a[0] + "\n")

                                        ################################################END OF FEATURE EXTRACTION

                                        os.chdir('..')
                                        os.chdir('..')
                                elif str(arr[k - 1]) == "ZDOESNOTEXIST":
                                    # print doesnotexistcatch
                                    # print "batu"
                                    if doesnotexistcatch[0] == 1 and doesnotexistcatch[1] == 0:
                                        rawdata_name = 'output_' + trial + ';' + str(
                                            participant) + ';' + "LOF" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                        output_feature.write(rawdata_name + " " + "\n")
                                        doesnotexistcatch[0] == 0
                                        doesnotexistcatch[1] == 0
                                    elif doesnotexistcatch[0] == 0 and doesnotexistcatch[1] == 1:
                                        rawdata_name = 'output_' + trial + ';' + str(
                                            participant) + ';' + "LEGO" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                        output_feature.write(rawdata_name + " " + "\n")
                                        doesnotexistcatch[0] == 0
                                        doesnotexistcatch[1] == 0
                                    else:
                                        continue

                                else:

                                    continue

                        os.chdir('..')
            os.chdir('..')

        # video_log_event_marking_main()

    def second_step(number):
        def main_system_log(number):
            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT')

            output_feature = open("allfeatures_(HRV)_extracted_features_EVENT" + '_' + str(number) + '_.txt', 'w')

            output_feature_1 = open("time_domain" + '.txt', 'w')
            output_feature_2 = open("frequency_domain" + '.txt', 'w')
            output_feature_3 = open("non_linear" + '.txt', 'w')

            # with open('log.txt', 'r') as in_file:
            #     stripped = (line.strip() for line in in_file)
            #     lines = (line.split(",") for line in stripped if line)
            #     with open('log.csv', 'w') as out_file:
            #         writer = csv.writer(out_file)
            #         writer.writerow(('title', 'intro'))
            #         writer.writerows(lines)

            # k=0
            # matrix = np.empty((64, 10))

            for z in range(0, len(feature_list)):

                feature_name = feature_list[z]
                feature_to_be_extracted = feature_list_no[z]
                os.chdir('./' + feature_name + '/')
                # print z
                if z <= 8:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        output_feature.write(x)
                        output_feature_1.write(x)

                elif z >= 9 and z <= 22:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        output_feature.write(x)
                        output_feature_2.write(x)

                elif z >= 23 and z <= 35:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        # print output
                        # print x
                        output_feature.write(x)
                        output_feature_3.write(x)

                os.chdir('..')

        def main_video_log(number):
            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT2')
            output_feature = open("allfeatures_(HRV)_extracted_features_EVENT2" + '_' + str(number) + '_.txt', 'w')
            output_feature_1 = open("time_domain" + '.txt', 'w')
            output_feature_2 = open("frequency_domain" + '.txt', 'w')
            output_feature_3 = open("non_linear" + '.txt', 'w')

            # with open('log.txt', 'r') as in_file:
            #     stripped = (line.strip() for line in in_file)
            #     lines = (line.split(",") for line in stripped if line)
            #     with open('log.csv', 'w') as out_file:
            #         writer = csv.writer(out_file)
            #         writer.writerow(('title', 'intro'))
            #         writer.writerows(lines)

            # k=0
            # matrix = np.empty((64, 10))

            for z in range(0, len(feature_list)):

                feature_name = feature_list[z]
                feature_to_be_extracted = feature_list_no[z]
                os.chdir('./' + feature_name + '/')
                # print z
                if z <= 8:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        output_feature.write(x)
                        output_feature_1.write(x)

                elif z >= 9 and z <= 22:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        output_feature.write(x)
                        output_feature_2.write(x)

                elif z >= 23 and z <= 35:

                    rawdata_filename = feature_name + '.txt'
                    file = open(rawdata_filename, 'r')
                    output = []
                    # matrix = np.zeros((2, 5))

                    i = 0
                    for line in file:
                        x = str(line)
                        x = x.replace(" ", "")
                        # x = x.replace(";", ",")
                        output = x.split(';')
                        # print output
                        # print x
                        output_feature.write(x)
                        output_feature_3.write(x)

                os.chdir('..')

        def merge_files(number):

            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT3')
            output_merged_full_dataset = open('output__all_video_system_logstime_' + str(number) + '_.txt', 'w')
            os.chdir('..')

            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT')
            f = open("allfeatures_(HRV)_extracted_features_EVENT" + '_' + str(number) + '_.txt', 'r+')
            os.chdir('..')

            for line in f.readlines():
                # write line to output file
                output_merged_full_dataset.write(line)

            os.chdir('./0005-LEGO-LOF (HRV) extracted features_EVENT2')
            f2 = open("allfeatures_(HRV)_extracted_features_EVENT2" + '_' + str(number) + '_.txt', 'r+')
            os.chdir('..')

            for line in f2.readlines():
                # write line to output file
                output_merged_full_dataset.write(line)

        # numberofexperiments = 1
        # skipped_experiment = 10  # check for skipped experiments such as experiment 10, check if there is more

        main_system_log(number)
        os.chdir('..')
        main_video_log(number)
        os.chdir('..')

        merge_files(number)

    skipped_experiment = 10

    for i in range (0,34): #till 0013 not including 0013
        if  i == 4  or i == 5 or i == 8  or i == 11 or i == 15 or i == 29 or i == 30 :
            pass
        # elif i >=11 and i <=15:
        #     starting_point = i
        #     numberofexperiments = starting_point
        #     first_step()
        #     second_step(i+1)
        else:



            starting_point = i+1
            numberofexperiments = starting_point
            #print os.getcwd()
            first_step()
            #print os.getcwd()
            second_step(i+1)
def move_folders():
    import glob
    os.chdir(output_directory_path + folder22)
    path = output_directory_path + folder22
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
    print paths
    print len(paths)
    for i in range (0,len(paths)):
        ECG_processed_file_name= paths[i]
        cutted_version1= ECG_processed_file_name[34:]
        cutted_version2= cutted_version1[:-5]

        if len(cutted_version2) ==1:
            folder_number = "000" + str(cutted_version2)
        elif len(cutted_version2) ==2:
            folder_number = "00" + str(cutted_version2)
        elif len(cutted_version2) == 3:
            folder_number = "0" + str(cutted_version2)
        elif len(cutted_version2) == 4:
            folder_number = str(cutted_version2)

        source = output_directory_path + folder22 + "/"+ paths[i]
        destination = output_directory_path + folder24 + "/" + folder_number
        files = glob.glob(output_directory_path + folder24 + "/" + folder_number+'/*')
        for f in files:
            os.remove(f)
        shutil.move(source, destination)
def merge_results_ECG():
    os.chdir(output_directory_path)

    list = []
    for x in os.listdir('./0017-RESULT-ECG-EVENT'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list


    os.chdir('./0017-RESULT-ECG-EVENT')
    ALL_allfeatures_HRV_extracted_features_EVENT = open('ALL_allfeatures_(HRV)_extracted_features_EVENT_batu.txt', 'w')



    for i in range (1,numberofexperiments+1):
        if i < 10:
            folder_number = "000" + str(i)
        elif i >= 10 and i < 100:
            folder_number = "00" + str(i)
        elif i >= 100 and i < 1000:
            folder_number = "0" + str(i)
        elif i >= 1000:
            folder_number = str(i)

        print folder_number

        path =output_directory_path + folder24+ "/" + folder_number
        os.chdir(path)

        directory = os.listdir(path)
        if len(directory) == 0:
            print "empty folder"
        else:
            f1 = open("output__all_video_system_logstime_" + str(i) + '_.txt', 'r+')
            print "output__all_video_system_logstime_" + str(i)

        for line in f1.readlines():
            # write line to output file

            ALL_allfeatures_HRV_extracted_features_EVENT.write(line)
        os.chdir("..")
def one_preprocessing_LEGO_LOF_HRV_feature_extraction():
    os.chdir(output_directory_path)
    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index", "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn", "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 81, 82, 84, 85, 86
        , 87, 88]

    for z in range(0, len(feature_list)):

        os.chdir('./0005-LEGO-LOF (HRV) extracted features')
        feature_name = feature_list[z]
        feature_to_be_extracted = feature_list_no[z]

        createFolder('./' + feature_name + '/')
        os.chdir('./' + feature_name + '/')
        print feature_name
        output_feature = open(feature_name + '.txt', 'w')
        os.chdir('..')
        os.chdir('..')

        os.chdir('./0003_LEGO-LOF (HRV) processed')

        #####################################

        for i in range(1, numberofexperiments + 1):
            if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4:
                continue
            else:
                if i < 10:
                    trial = "000" + str(i)
                elif i >= 10 and i < 100:
                    trial = "00" + str(i)
                elif i >= 100 and i < 1000:
                    trial = "0" + str(i)
                elif i >= 1000:
                    trial = str(i)
                for j in range(1, 3):
                    doesnotexistcatch = [0, 0]
                    if j == 1:
                        participant = 44
                    elif j == 2:
                        participant = 55
                    # print  './' + trial +'_' + str(participant) + '/'
                    # print(os.getcwd())
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    # print arr

                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "LEGO":
                            condition = "LEGO"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')

                            ###############################START OF FEATURE EXTRACTION

                            input_file = open(
                                'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv.txt', 'r')
                            output_file = open(
                                'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_end.txt', 'w')
                            ######### to remove the end of the file
                            n = 1
                            while True:

                                line = input_file.readline()

                                if (n == 113):
                                    # print "file finished"
                                    break

                                output_file.write(line)
                                n = n + 1

                            ######### Dataset creation

                            rawdata_filename = 'output_' + trial + '_' + str(
                                participant) + '_' + condition + '_ECG_hrv_end.txt'
                            rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition

                            s1a = np.loadtxt(rawdata_filename, usecols=(0), unpack=True, dtype=str, delimiter='\t',
                                             skiprows=feature_to_be_extracted)
                            output_feature.write(rawdata_name + ";" + s1a[0] + "\n")

                            ################################################END OF FEATURE EXTRACTION

                            os.chdir('..')
                        elif str(arr[k - 1]) == "LOF":
                            condition = "LOF"
                            doesnotexistcatch[1] = 1
                            os.chdir('./' + condition + '/')

                            ###############################START OF FEATURE EXTRACTION

                            input_file = open(
                                'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv.txt', 'r')
                            output_file = open(
                                'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_end.txt', 'w')
                            ######### to remove the end of the file
                            n = 1
                            while True:

                                line = input_file.readline()

                                if (n == 113):
                                    # print "file finished"
                                    break

                                output_file.write(line)
                                n = n + 1

                            ######### Dataset creation

                            rawdata_filename = 'output_' + trial + '_' + str(
                                participant) + '_' + condition + '_ECG_hrv_end.txt'
                            rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition

                            s1a = np.loadtxt(rawdata_filename, usecols=(0), unpack=True, dtype=str, delimiter='\t',
                                             skiprows=feature_to_be_extracted)
                            output_feature.write(rawdata_name + ";" + s1a[0] + "\n")

                            ################################################END OF FEATURE EXTRACTION

                            os.chdir('..')

                        elif str(arr[k - 1]) == "ZDOESNOTEXIST":
                            # print doesnotexistcatch
                            # print "batu"
                            if doesnotexistcatch[0] == 1 and doesnotexistcatch[1] == 0:
                                rawdata_name = 'output_' + trial + ';' + str(
                                    participant) + ';' + "LOF" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                output_feature.write(rawdata_name + " " + "\n")
                                doesnotexistcatch[0] == 0
                                doesnotexistcatch[1] == 0
                            elif doesnotexistcatch[0] == 0 and doesnotexistcatch[1] == 1:
                                rawdata_name = 'output_' + trial + ';' + str(
                                    participant) + ';' + "LEGO" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                                output_feature.write(rawdata_name + " " + "\n")
                                doesnotexistcatch[0] == 0
                                doesnotexistcatch[1] == 0
                            else:
                                continue

                        else:

                            continue

                    os.chdir('..')
        os.chdir('..')
def second_preprocessing_BASELINE_HRV_feature_extraction():
    os.chdir(output_directory_path)
    def extract_ECG_features(trial, participant, condition):

        ###############################START OF FEATURE EXTRACTION

        input_file = open('output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv.txt', 'r')
        output_file = open('output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_end.txt', 'w')
        ######### to remove the end of the file
        n = 1
        while True:

            line = input_file.readline()

            if (n == 113):
                print "file finished"
                break

            output_file.write(line)
            n = n + 1

        ######### Dataset creation

        rawdata_filename = 'output_' + trial + '_' + str(participant) + '_' + condition + '_ECG_hrv_end.txt'
        rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + condition

        s1a = np.loadtxt(rawdata_filename, usecols=(0), unpack=True, dtype=str, delimiter='\t',
                         skiprows=feature_to_be_extracted)
        output_feature.write(rawdata_name + ";" + s1a[0] + "\n")

        ################################################END OF FEATURE EXTRACTION

    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index", "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn", "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 81, 82, 84, 85, 86
        , 87, 88]

    for z in range(0, len(feature_list)):

        os.chdir('./0006-BASELINE (HRV) extracted features')
        feature_name = feature_list[z]
        feature_to_be_extracted = feature_list_no[z]

        createFolder('./' + feature_name + '/')
        os.chdir('./' + feature_name + '/')
        output_feature = open(feature_name + '.txt', 'w')
        os.chdir('..')
        os.chdir('..')

        os.chdir('./0004_BASELINE (HRV) processed')

        #####################################

        for i in range(1, numberofexperiments + 1):

            if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
                continue
            else:
                if i < 10:
                    trial = "000" + str(i)
                elif i >= 10 and i < 100:
                    trial = "00" + str(i)
                elif i >= 100 and i < 1000:
                    trial = "0" + str(i)
                elif i >= 1000:
                    trial = str(i)
                for j in range(1, 3):
                    doesnotexistcatch = [0, 0, 0, 0, 0, 0, 0]
                    doesnotexistcatch_ciera = ["b1", "b2", "break", "cb1", "cb2", "cb3", "cb4"]
                    doesnotexistcatch_juan = ["b1", "b2", "break", "jb1", "jb2", "jb3", "jb4"]
                    if j == 1:
                        participant = 44
                    elif j == 2:
                        participant = 55
                    print  './' + trial + '_' + str(participant) + '/'
                    # print(os.getcwd())
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    print arr

                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "b1":
                            condition = "b1"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')
                        elif str(arr[k - 1]) == "b2":
                            condition = "b2"
                            doesnotexistcatch[1] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "break":
                            condition = "break"
                            doesnotexistcatch[2] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "cb1":
                            condition = "cb1"
                            doesnotexistcatch[3] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "cb2":
                            condition = "cb2"
                            doesnotexistcatch[4] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "cb3":
                            condition = "cb3"
                            doesnotexistcatch[5] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "cb4":
                            condition = "cb4"
                            doesnotexistcatch[6] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "jb1":
                            condition = "jb1"
                            doesnotexistcatch[3] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "jb2":
                            condition = "jb2"
                            doesnotexistcatch[4] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "jb3":
                            condition = "jb3"
                            doesnotexistcatch[5] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')
                        elif str(arr[k - 1]) == "jb4":
                            condition = "jb4"
                            doesnotexistcatch[6] = 1
                            os.chdir('./' + condition + '/')

                            extract_ECG_features(trial, participant, condition)

                            os.chdir('..')

                        else:

                            continue

                    if j == 1:

                        for P in range(0, len(doesnotexistcatch) - 1):
                            if doesnotexistcatch[P] == 0:
                                rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                                               doesnotexistcatch_ciera[P]
                                output_feature.write(rawdata_name + " " + "\n")
                            else:
                                continue

                    elif j == 2:
                        for P in range(0, len(doesnotexistcatch) - 1):
                            if doesnotexistcatch[P] == 0:
                                rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                                               doesnotexistcatch_juan[P]
                                output_feature.write(rawdata_name + " " + "\n")
                            else:
                                continue

                    os.chdir('..')
        os.chdir('..')
def third_preprocessing_LEGO_LOF_HRV_all_feature_dataset_MERGE_ALL():
    os.chdir(output_directory_path)
    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index", "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn", "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 81, 82, 84, 85, 86
        , 87, 88]
    os.chdir('./0005-LEGO-LOF (HRV) extracted features')
    output_feature = open("allfeatures" + '.txt', 'w')
    output_feature_1 = open("time_domain" + '.txt', 'w')
    output_feature_2 = open("frequency_domain" + '.txt', 'w')
    output_feature_3 = open("non_linear" + '.txt', 'w')

    # output_feature4 = open("frequency_domain2" + '.txt','w')

    def write_row(rawdata_filename, output_name_main, output_name_separate, flag):
        print rawdata_filename
        s2a = pd.read_csv(rawdata_filename, delimiter=';', header=None)
        # print s2a
        # print s2a.iloc[0]
        print s2a.shape[0]

        for k in range(0, s2a.shape[0]):
            rawdata_name = str(s2a.iloc[k, 0]) + ';' + str(s2a.iloc[k, 1]) + ';' + str(s2a.iloc[k, 2]) + ';' + str(
                s2a.iloc[k, 3])

            list = []
            for i in range(0, len(s2a.iloc[k])):
                list.append(s2a.iloc[k, i])
            print rawdata_name

            if flag == 1:
                output_name_main.write(
                    rawdata_name + ";" + str(list[4]) + ";" + str(list[6]) + ";" + str(list[8]) + ";" + str(list[10]))
                output_name_main.write("\n")
                output_name_main.write(
                    rawdata_name + '2' + ";" + str(list[5]) + ";" + str(list[7]) + ";" + str(list[9]) + ";" + str(
                        list[11]))
                output_name_main.write("\n")

                output_name_separate.write(
                    rawdata_name + ";" + str(list[4]) + ";" + str(list[6]) + ";" + str(list[8]) + ";" + str(list[10]))
                output_name_separate.write("\n")
                output_name_separate.write(
                    rawdata_name + '2' + ";" + str(list[5]) + ";" + str(list[7]) + ";" + str(list[9]) + ";" + str(
                        list[11]))
                output_name_separate.write("\n")
            elif flag == 0:
                output_name_main.write(
                    rawdata_name + ";" + str(list[4]) + ";" + str(list[6]) + ";" + str(list[8]) + ";" + str(list[10]))
                output_name_main.write("\n")

                output_name_separate.write(
                    rawdata_name + ";" + str(list[4]) + ";" + str(list[6]) + ";" + str(list[8]) + ";" + str(list[10]))
                output_name_separate.write("\n")

    # with open('log.txt', 'r') as in_file:
    #     stripped = (line.strip() for line in in_file)
    #     lines = (line.split(",") for line in stripped if line)
    #     with open('log.csv', 'w') as out_file:
    #         writer = csv.writer(out_file)
    #         writer.writerow(('title', 'intro'))
    #         writer.writerows(lines)

    # k=0
    # matrix = np.empty((64, 10))

    flag = 0
    for z in range(0, len(feature_list)):

        feature_name = feature_list[z]
        # feature_to_be_extracted = feature_list_no[z]
        os.chdir('./' + feature_name + '/')

        if z <= 8:

            rawdata_filename = feature_name + '.txt'
            # print rawdata_filename
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # output_feature.write(x)
                # output_feature_1.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_1, flag)


        #######

        elif z >= 9 and z <= 22:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # output_feature.write(x)
                # output_feature_2.write(x)
                flag = 1

            ########
            write_row(rawdata_filename, output_feature, output_feature_2, flag)
            flag = 0


        #######

        elif z >= 23 and z <= 35:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # print output
                # print x
                # output_feature.write(x)
                # output_feature_3.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_3, flag)

        os.chdir('..')

    f = open('allfeatures.txt')
    outF = open("allfeatures2.txt", "w")
    # use readline() to read the first line
    line = f.readline()
    # use the read line to read further.
    # If the file is not empty keep reading one line
    # at a time, till the file is empty
    while line:
        # in python 2+
        # print line
        # in python 3 print is a builtin function, so

        # use realine() to read next line
        line = f.readline()
        x = str(line)
        x = x.replace(" ", "")
        print(x)
        outF.write(x)

    f.close()
    outF.close
def third_preprocessing_LEGO_LOF_HRV_all_feature_dataset_MERGE_BASELINE():
    os.chdir(output_directory_path)
    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index", "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn", "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 81, 82, 84, 85, 86
        , 87, 88]
    os.chdir('./0006-BASELINE (HRV) extracted features')
    output_feature = open("allfeatures" + '.txt', 'w')
    output_feature_1 = open("time_domain" + '.txt', 'w')
    output_feature_2 = open("frequency_domain" + '.txt', 'w')
    output_feature_3 = open("non_linear" + '.txt', 'w')

    # output_feature4 = open("frequency_domain2" + '.txt','w')

    def write_row(rawdata_filename, output_name_main, output_name_separate, flag):
        print rawdata_filename
        s2a = pd.read_csv(rawdata_filename, delimiter=';', header=None)
        # print s2a
        # print s2a.iloc[0]
        print s2a.shape[0]

        for k in range(0, s2a.shape[0]):

            rawdata_name = str(s2a.iloc[k, 0]) + ';' + str(s2a.iloc[k, 1]) + ';' + str(s2a.iloc[k, 2]) + ';' + str(
                s2a.iloc[k, 3])

            list = []
            for i in range(0, len(s2a.iloc[0])):
                list.append(s2a.iloc[0, i])
            print rawdata_name

            if flag == 1:
                output_name_main.write(
                    rawdata_name + ";" + str(list[4]))
                output_name_main.write("\n")
                output_name_main.write(
                    rawdata_name + '2' + ";" + str(list[5]))
                output_name_main.write("\n")

                output_name_separate.write(
                    rawdata_name + ";" + str(list[4]))
                output_name_separate.write("\n")
                output_name_separate.write(
                    rawdata_name + '2' + ";" + str(list[5]))
                output_name_separate.write("\n")
            elif flag == 0:
                output_name_main.write(
                    rawdata_name + ";" + str(list[4]))
                output_name_main.write("\n")

                output_name_separate.write(
                    rawdata_name + ";" + str(list[4]))
                output_name_separate.write("\n")

    # with open('log.txt', 'r') as in_file:
    #     stripped = (line.strip() for line in in_file)
    #     lines = (line.split(",") for line in stripped if line)
    #     with open('log.csv', 'w') as out_file:
    #         writer = csv.writer(out_file)
    #         writer.writerow(('title', 'intro'))
    #         writer.writerows(lines)

    # k=0
    # matrix = np.empty((64, 10))

    flag = 0
    for z in range(0, len(feature_list)):

        feature_name = feature_list[z]
        # feature_to_be_extracted = feature_list_no[z]
        os.chdir('./' + feature_name + '/')

        if z <= 8:

            rawdata_filename = feature_name + '.txt'
            # print rawdata_filename
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                output_feature.write(x)
                output_feature_1.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_1, flag)


        #######

        elif z >= 9 and z <= 22:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # output_feature.write(x)
                # output_feature_2.write(x)
                flag = 1

            ########
            write_row(rawdata_filename, output_feature, output_feature_2, flag)
            flag = 0


        #######

        elif z >= 23 and z <= 35:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # print output
                # print x
                output_feature.write(x)
                output_feature_3.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_3, flag)

        os.chdir('..')
def transpose_baseline2():
    os.chdir(output_directory_path)
    feature_list = ["00_MeanRR", "01_STDRR", "02_MeanHR", "03_STDHR", "04_RMSSD", "05_NN50", "06_pNN50",
                    "07_RR_tri_index",
                    "08_TINN"
        , "09_VLF(Hz)", "10_LF (Hz)", "11_HF (Hz)", "12_VLF (ms^2)", "13_LF (ms^2)", "14_HF (ms^2)", "15_VLF (%)",
                    "16_LF (%)", "17_HF (%)", "18_LF (n.u.)", "19_HF (n.u.)"
        , "20_Total power (ms^2)", "21_LF_HF ratio", "22_EDR (Hz)", "23_SD1 (ms)", "24_SD2 (ms)", "25_ApEn",
                    "26_SampEn",
                    "27_Correlation dimension"
        , "28_alpha1", "29_alpha2", "30_Mean line length (beats)", "31_Max line length (beats)", "32_REC (%)"
        , "33_DET (%)", "34_Shannon entropy"]
    feature_list_no = [40, 41, 42, 43, 44, 45, 46, 50, 51
        , 55, 56, 57, 59, 60, 61, 63, 64, 65, 67, 68, 69,
                       70, 71, 75, 76, 77, 78, 79
        , 81, 82, 84, 85, 86
        , 87, 88]



    os.chdir('./0006-BASELINE (HRV) extracted features')
    output_feature = open("allfeatures" + '.txt', 'w')
    output_feature_1 = open("time_domain" + '.txt', 'w')
    output_feature_2 = open("frequency_domain" + '.txt', 'w')
    output_feature_3 = open("non_linear" + '.txt', 'w')

    # output_feature4 = open("frequency_domain2" + '.txt','w')

    def write_row(rawdata_filename, output_name_main, output_name_separate, flag, numberofexperiments):
        print rawdata_filename
        # s2a = pd.read_csv(rawdata_filename, delimiter=';',
        #                  names=["index", "experiment", "participant", "phase", "feature", "value1"])

        s2a = pd.read_csv(rawdata_filename, delimiter=';',
                          names=["index", "experiment", "participant", "phase", "feature", "value1", "value2"])
        # print s2a
        # print s2a.iloc[0]
        # print s2a

        # print s2a
        # numberofexperiments=18
        # numberofexprows = 18*2
        #
        # array = np.empty((numberofexprows, 14))
        #
        # for i in range(0, (numberofexprows)):
        #     for j in range(0, 14):
        #         array[i][j] = '-1'
        # print list(s2a.columns.values)

        # data2 = pd.pivot_table(s2a, index=["index", "experiment", "participant", "feature"], columns=["phase"],
        #                        values=["value1"])
        # data2.to_csv('out2.csv')
        #
        # print data2

        # for i in range(0, (s2a.shape[0])):
        #     print 'batu'
        #     print s2a.iat[i,1] # experiment
        #     print s2a.iat[i, 2] #participant
        #     print s2a.iat[i, 3] #phase
        #     print s2a.iat[i, 4] #feature
        #     print s2a.iat[i, 5]  # value1
        #     print s2a.iat[i, 6]  # value2
        #     # list = []
        #     # for m in range(0, len(s2a.iloc[0])):
        #     #     list.append(s2a.iloc[0, m])
        #     # print list
        #     #
        #     a = s2a.iat[i,0]
        #     b= a[7:11]
        #     experiment_no = b.strip("0")
        #     participant = s2a.iat[i, 2]
        #     phase =s2a.iat[i, 3]
        #     feature =s2a.iat[i, 4] #feature
        #     value1= s2a.iat[i, 5]  # value1
        #     value2= s2a.iat[i, 6]  # value2
        #
        #
        #
        #     phase2 = phase
        #     count = 0
        #     count_main = 0
        #     for i in range (0,numberofexperiments):
        #         if i == 9:# skippedexperiment
        #             continue
        #         else:
        #
        #
        #             count =1
        #             while  phase==phase2:
        #                 phase2 = s2a.iat[i+count,0]
        #                 print 'batuuuu' + str(experiment_no) +' '+str(phase) + ' '+ str(count_main)
        #                 count_main= count_main+1
        #                 count =count+1
        #             phase = phase2
        #

        array = np.empty(((numberofexperiments + 1), 14))
        array2 = np.empty(((numberofexperiments + 1), 14))
        # print array

        for i in range(0, (numberofexperiments + 1)):
            for j in range(0, 14):
                array[i][j] = '-1'
                array2[i][j] = '-1'
        for i in range(0, (s2a.shape[0])):

            a = s2a.iat[i, 0]
            #        print a
            b = a[7:11]
            # print b
            experiment_no = int(b.strip("0"))
            # print experiment_no
            # array[experiment_no] =
            # participant = s2a.iat[i, 2]
            # phase =s2a.iat[i, 3]
            # print s2a.iat[i, 1]
            # print s2a.iloc[i][2]
            # print s2a.iat[i, 4]
            # for m in range (0,numberofexperiments):
            #     for i in range (0, (s2a.shape[0])):
            if s2a.iat[i, 1] == 44:
                # print '44 ' + str(experiment_no)

                if flag == 0:
                    if str(s2a.iloc[i][2]) == 'b1':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][0] = s2a.iat[i, 4]

                    elif str(s2a.iloc[i][2]) == 'b2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][1] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'break':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][2] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb1':

                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:

                            array[experiment_no][3] = s2a.iat[i, 4]
                            # print 'aaaaaaa' + str(array[experiment_no][3])
                    elif str(s2a.iloc[i][2]) == 'cb2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][4] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb3':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][5] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb4':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][6] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb1':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][3] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][4] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb3':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][5] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb4':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array[experiment_no][6] = s2a.iat[i, 4]
                elif flag == 1:
                    if str(s2a.iloc[i][2]) == 'b1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:

                            array[experiment_no][0] = s2a.iat[i, 4]
                            array[experiment_no][7] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'b2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][1] = s2a.iat[i, 4]
                            array[experiment_no][8] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'break':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:

                            array[experiment_no][2] = s2a.iat[i, 4]
                            array[experiment_no][9] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:

                            array[experiment_no][3] = s2a.iat[i, 4]
                            # print 'sadasdasd' + str(s2a.iat[i, 5])
                            array[experiment_no][10] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][4] = s2a.iat[i, 4]
                            array[experiment_no][11] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb3':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][5] = s2a.iat[i, 4]
                            array[experiment_no][12] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb4':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][6] = s2a.iat[i, 4]
                            array[experiment_no][13] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][3] = s2a.iat[i, 4]
                            array[experiment_no][10] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][4] = s2a.iat[i, 4]
                            array[experiment_no][11] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb3':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][5] = s2a.iat[i, 4]
                            array[experiment_no][12] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb4':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array[experiment_no][6] = s2a.iat[i, 4]
                            array[experiment_no][13] = s2a.iat[i, 5]

            elif s2a.iat[i, 1] == 55:
                # print '55 '+ str(experiment_no)

                if flag == 0:
                    if str(s2a.iloc[i][2]) == 'b1':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][0] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'b2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][1] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'break':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][2] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb1':
                        # print 'batu'
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][3] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][4] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb3':
                        if s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][5] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'cb4':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][6] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb1':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][3] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb2':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][4] = s2a.iat[i, 4]
                    elif str(s2a.iloc[i][2]) == 'jb3':
                        # print 'asdasdasd' +str(s2a.iat[i, 4])
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][5] = s2a.iat[i, 4]
                        # print experiment_no
                        # print '----------' + str(array[experiment_no+1][5])
                    elif str(s2a.iloc[i][2]) == 'jb4':
                        if s2a.iat[i, 4] == '            ':
                            pass
                        else:
                            array2[experiment_no][6] = s2a.iat[i, 4]
                elif flag == 1:
                    if str(s2a.iloc[i][2]) == 'b1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:

                            array2[experiment_no][0] = s2a.iat[i, 4]
                            array2[experiment_no][7] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'b2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][1] = s2a.iat[i, 4]
                            array2[experiment_no][8] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'break':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:

                            array2[experiment_no][2] = s2a.iat[i, 4]
                            array2[experiment_no][9] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][3] = s2a.iat[i, 4]
                            array2[experiment_no][10] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][4] = s2a.iat[i, 4]
                            array2[experiment_no][11] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb3':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][5] = s2a.iat[i, 4]
                            array2[experiment_no][12] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'cb4':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][6] = s2a.iat[i, 4]
                            array2[experiment_no][13] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb1':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][3] = s2a.iat[i, 4]
                            array2[experiment_no][10] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb2':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][4] = s2a.iat[i, 4]
                            array2[experiment_no][11] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb3':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][5] = s2a.iat[i, 4]
                            array2[experiment_no][12] = s2a.iat[i, 5]
                    elif str(s2a.iloc[i][2]) == 'jb4':
                        if s2a.iat[i, 4] == '            ' or s2a.iat[i, 5] == '            ':
                            pass
                        else:
                            array2[experiment_no][6] = s2a.iat[i, 4]
                            array2[experiment_no][13] = s2a.iat[i, 5]

            # print array [0][0]

        # for k in range(0, s2a.shape[0]):
        #
        #     rawdata_name = str(s2a.iloc[k, 0]) + ';' + str(s2a.iloc[k, 1]) + ';' + str(s2a.iloc[k, 2]) + ';' + str(
        #         s2a.iloc[k, 3])
        #
        #     list = []
        #     for i in range(0, len(s2a.iloc[0])):
        #         list.append(s2a.iloc[0, i])
        #     print rawdata_name
        #
        #     if flag == 1:
        #         output_name_main.write(
        #             rawdata_name + ";" + str(list[4]))
        #         output_name_main.write("\n")
        #         output_name_main.write(
        #             rawdata_name + '2' + ";" + str(list[5]))
        #         output_name_main.write("\n")
        #
        #         output_name_separate.write(
        #             rawdata_name + ";" + str(list[4]))
        #         output_name_separate.write("\n")
        #         output_name_separate.write(
        #             rawdata_name + '2' + ";" + str(list[5]))
        #         output_name_separate.write("\n")
        #     elif flag == 0:
        #         output_name_main.write(
        #             rawdata_name + ";" + str(list[4]))
        #         output_name_main.write("\n")
        #
        #         output_name_separate.write(
        #             rawdata_name + ";" + str(list[4]))
        #         output_name_separate.write("\n")
        #
        # rawdata_name = str(s2a.iloc[k, 0]) + ';' + str(s2a.iloc[k, 1]) + ';' + str(s2a.iloc[k, 2]) + ';' + str(s2a.iloc[k, 3])

        for i in range(0, (numberofexperiments + 1)):
            output_name_main.write(str(i) + ';' + '44;' + str(s2a.iat[0, 3]))
            for j in range(0, 14):
                if flag == 0:
                    if j > 6:
                        break
                    else:
                        output_name_main.write(';' + str(array[i][j]))
                        # output_name_main.write("\n")

                elif flag == 1:
                    if j < 6:
                        output_name_main.write(';' + str(array[i][j]))
                    elif j == 6:
                        output_name_main.write(';' + str(array[i][j]))
                        output_name_main.write("\n")
                        output_name_main.write(str(i) + ';' + '44;' + str(s2a.iat[0, 3]) + '2')
                    if j > 6:
                        output_name_main.write(';' + str(array[i][j]))
            output_name_main.write("\n")

        for i in range(0, (numberofexperiments + 1)):
            output_name_main.write(str(i) + ';' + '55;' + str(s2a.iat[0, 3]))
            for j in range(0, 14):
                if flag == 0:
                    if j > 6:
                        break
                    else:
                        output_name_main.write(';' + str(array2[i][j]))
                        # output_name_main.write("\n")

                elif flag == 1:
                    if j < 6:
                        output_name_main.write(';' + str(array2[i][j]))
                    elif j == 6:
                        output_name_main.write(';' + str(array2[i][j]))
                        output_name_main.write("\n")
                        output_name_main.write(str(i) + ';' + '55;' + str(s2a.iat[0, 3]) + '2')
                    if j > 6:
                        output_name_main.write(';' + str(array2[i][j]))
            output_name_main.write("\n")

        print "array"
        print array
        print "array2"
        print array2

    # with open('log.txt', 'r') as in_file:
    #     stripped = (line.strip() for line in in_file)
    #     lines = (line.split(",") for line in stripped if line)
    #     with open('log.csv', 'w') as out_file:
    #         writer = csv.writer(out_file)
    #         writer.writerow(('title', 'intro'))
    #         writer.writerows(lines)

    # k=0
    # matrix = np.empty((64, 10))

    flag = 0
    numberofexperiments = 34
    for z in range(0, len(feature_list)):

        feature_name = feature_list[z]
        # feature_to_be_extracted = feature_list_no[z]
        os.chdir('./' + feature_name + '/')

        if z <= 8:

            rawdata_filename = feature_name + '.txt'
            # print rawdata_filename
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # output_feature.write(x)
                # output_feature_1.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_1, flag, numberofexperiments)


        #######

        elif z >= 9 and z <= 22:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # output_feature.write(x)
                # output_feature_2.write(x)
                flag = 1

            ########
            write_row(rawdata_filename, output_feature, output_feature_2, flag, numberofexperiments)
            flag = 0


        #######

        elif z >= 23 and z <= 35:

            rawdata_filename = feature_name + '.txt'
            file = open(rawdata_filename, 'r')
            output = []
            # matrix = np.zeros((2, 5))

            i = 0
            for line in file:
                x = str(line)
                x = x.replace(" ", "")
                # x = x.replace(";", ",")
                output = x.split(',')
                # print output
                # print x
                # output_feature.write(x)
                # output_feature_3.write(x)

            ########
            write_row(rawdata_filename, output_feature, output_feature_3, flag, numberofexperiments)

        os.chdir('..')

    f = open('allfeatures.txt')
    outF = open("allfeatures2.txt", "w")
    # use readline() to read the first line
    line = f.readline()
    # use the read line to read further.
    # If the file is not empty keep reading one line
    # at a time, till the file is empty
    while line:
        # in python 2+
        # print line
        # in python 3 print is a builtin function, so

        # use realine() to read next line
        line = f.readline()
        x = str(line)
        x = x.replace(" ", "")
        print(x)
        outF.write(x)

    f.close()
    outF.close
#########stage 11 extract features from preprocessed data & create dataframes accordingly
def eda_video_code_marked_feature_extraction_all(numberofexperiments):
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    os.chdir(output_directory_path)

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH')
    output_feature = open("allfeatures_eda_VIDEO_EVENT_MARKED" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,no,event_no,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 16)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'ast5_E':
            part = 'last5'
        if part == 'id5_ED':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'
        if part == 'EDA_er':
            part = 'total'
        if part == 'DA_era':
            part = 'total'

        # print part

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
                elif part == 'total':
                    array_index_part = 3
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 4
                elif part == 'mid5':
                    array_index_part = 5
                elif part == 'last5':
                    array_index_part = 6
                elif part == 'total':
                    array_index_part = 7
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 8
                elif part == 'mid5':
                    array_index_part = 9
                elif part == 'last5':
                    array_index_part = 10
                elif part == 'total':
                    array_index_part = 11
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 12
                elif part == 'mid5':
                    array_index_part = 13
                elif part == 'last5':
                    array_index_part = 14
                elif part == 'total':
                    array_index_part = 15

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 16 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 16):
        if allocation_array[i] == -1:

            event_no = '-1'
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output +'0,'+ str(event_no) + ',' + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_'


            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore ==0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'


            workbook = xlrd.open_workbook(rawdata_name)
            worksheet = workbook.sheet_by_name('CDA')

            length_sheet = worksheet.nrows  # Version 1.x.x Syntax

            print rawdata_name
            print length_sheet

            for m in range(1, length_sheet):

                event_no = int(worksheet.cell(m, 2).value)
                print event_no
                # print 'event_no : ' + str(event_no)

                feature_value = np.zeros(12)
                no =  str(worksheet.cell(m, 0).value)
                for p in range(3, 15):

                    if worksheet.cell(m, p).value == '' or worksheet.cell(m, p).value == None:
                        pass
                    else:
                        x2 = str(worksheet.cell(m, p).value)
                        feature_value[p - 3] = float(x2)

                count = 0

                for k in range(0, len(feature_list)):
                    output_feature.write(
                        text_output+str(no)+ ','+ str(event_no)+',' + feature_list[k] + ',' + str(feature_value[k]))
                    output_feature.write("\n")
                    count = count + 1

    data = pd.read_csv("allfeatures_eda_VIDEO_EVENT_MARKED.txt")


    # f = open('allfeatures_eda_VIDEO_EVENT_MARKED', 'r+')
    # os.chdir('./0015_OUTPUT')
    # output_dataset = open('allfeatures_eda_VIDEO_EVENT_MARKED.txt', 'w')
    # for line in f.readlines():
    #     # write line to output file
    #     output_dataset.write(line)
    # os.chdir('..')


    # data2 = pd.pivot_table(data,index=["experiment","participant","session","feature"],columns=["part"],values=["value"])
    #
    # data2.to_csv('out2.csv') # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')


    os.chdir('./0015_OUTPUT')
    data.to_csv(
        'allfeatures_eda_VIDEO_EVENT_MARKED.csv')
    os.chdir('..')
def eda_system_log_marked_feature_extraction_all(numberofexperiments):
    os.chdir(output_directory_path)

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    # ############################################# PARAMETERS TO CHANGE ################



    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH'):

        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH')
    output_feature = open("allfeatures_eda_SYSTEM_EVENT_MARKED" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,no,event_no,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 16)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'ast5_E':
            part = 'last5'
        if part == 'id5_ED':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'
        if part == 'EDA_er':
            part = 'total'
        if part == 'DA_era':
            part = 'total'

        # print part

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
                elif part == 'total':
                    array_index_part = 3
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 4
                elif part == 'mid5':
                    array_index_part = 5
                elif part == 'last5':
                    array_index_part = 6
                elif part == 'total':
                    array_index_part = 7
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 8
                elif part == 'mid5':
                    array_index_part = 9
                elif part == 'last5':
                    array_index_part = 10
                elif part == 'total':
                    array_index_part = 11
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 12
                elif part == 'mid5':
                    array_index_part = 13
                elif part == 'last5':
                    array_index_part = 14
                elif part == 'total':
                    array_index_part = 15

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 16 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 16):
        if allocation_array[i] == -1:

            event_no = '-1'
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + '0,'+str(event_no) + ',' + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)
            worksheet = workbook.sheet_by_name('CDA')

            length_sheet = worksheet.nrows  # Version 1.x.x Syntax

            print rawdata_name
            print length_sheet

            for m in range(1, length_sheet):

                event_no = int(worksheet.cell(m, 2).value)
                print event_no
                # print 'event_no : ' + str(event_no)

                feature_value = np.zeros(12)
                no =  str(worksheet.cell(m, 0).value)


                for p in range(3, 15):

                    if worksheet.cell(m, p).value == '' or worksheet.cell(m, p).value == None:
                        pass
                    else:
                        x2 = str(worksheet.cell(m, p).value)
                        feature_value[p - 3] = float(x2)

                count = 0

                for k in range(0, len(feature_list)):
                    output_feature.write(
                        text_output +str(no)+ ','+ str(event_no)+ ',' + feature_list[k] + ',' + str(feature_value[k]))
                    output_feature.write("\n")
                    count = count + 1

    data = pd.read_csv("allfeatures_eda_SYSTEM_EVENT_MARKED.txt")

    print os.getcwd()
    f = open('allfeatures_eda_SYSTEM_EVENT_MARKED.txt', 'r+')



    # data2 = pd.pivot_table(data,index=["experiment","participant","session","feature"],columns=["part"],values=["value"])
    #
    # data2.to_csv('out2.csv') # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')
    # print os.getcwd()
    # os.chdir('./0015_OUTPUT')
    # output_dataset = open('allfeatures_eda_SYSTEM_EVENT_MARKED.txt', 'w')
    # for line in f.readlines():
    #     # write line to output file
    #     output_dataset.write(line)
    # os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data.to_csv(
        'allfeatures_eda_SYSTEM_EVENT_MARKED.csv')
    os.chdir('..')
def eda_video_code_system_log_marked_feature_extraction_all(numberofexperiments):
    os.chdir(output_directory_path)
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    # ############################################# PARAMETERS TO CHANGE ################



    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH'):

        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH')
    output_feature = open("allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,no,event_no,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 16)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'ast5_E':
            part = 'last5'
        if part == 'id5_ED':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'
        if part == 'EDA_er':
            part = 'total'
        if part == 'DA_era':
            part = 'total'

        # print part

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
                elif part == 'total':
                    array_index_part = 3
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 4
                elif part == 'mid5':
                    array_index_part = 5
                elif part == 'last5':
                    array_index_part = 6
                elif part == 'total':
                    array_index_part = 7
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 8
                elif part == 'mid5':
                    array_index_part = 9
                elif part == 'last5':
                    array_index_part = 10
                elif part == 'total':
                    array_index_part = 11
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 12
                elif part == 'mid5':
                    array_index_part = 13
                elif part == 'last5':
                    array_index_part = 14
                elif part == 'total':
                    array_index_part = 15

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 16 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 16):
        if allocation_array[i] == -1:

            event_no = '-1'
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output +'0'+','+ str(event_no) + ',' + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)
            worksheet = workbook.sheet_by_name('CDA')

            length_sheet = worksheet.nrows  # Version 1.x.x Syntax

            print rawdata_name
            print length_sheet
            #
            # no = 0
            for m in range(1, length_sheet):

                event_no = int(worksheet.cell(m, 2).value)
                print event_no
                # print 'event_no : ' + str(event_no)
                # if m %11 ==0:
                #     no = no +1

                feature_value = np.zeros(12)

                no =  str(worksheet.cell(m, 0).value)
                for p in range(3, 15):

                    if worksheet.cell(m, p).value == '' or worksheet.cell(m, p).value == None:
                        pass
                    else:
                        x2 = str(worksheet.cell(m, p).value)
                        feature_value[p - 3] = float(x2)


                count = 0

                for k in range(0, len(feature_list)):
                    output_feature.write(
                        text_output +str(no)+','+ str(event_no) + ',' + feature_list[k] + ',' + str(feature_value[k]))
                    output_feature.write("\n")
                    count = count + 1

    data = pd.read_csv("allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED.txt")




    # data2 = pd.pivot_table(data,index=["experiment","participant","session","feature"],columns=["part"],values=["value"])
    #
    # data2.to_csv('out2.csv') # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')


    # f = open('allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED', 'r+')
    # os.chdir('./0015_OUTPUT')
    # output_dataset = open('allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED.txt', 'w')
    # for line in f.readlines():
    #     # write line to output file
    #     output_dataset.write(line)
    # os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data.to_csv(
        'allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED.csv')
    os.chdir('..')
def acc_feature_extraction_wtotal(numberofexperiments):
    os.chdir(output_directory_path)
    def count_initiation_response(rawdata_filename, number_of_initiations, number_of_responses):
        # FUNTION START /////////////////////////////////////////////////////////


        print rawdata_filename
        # SUB FUNCTION , EXCEL TO CSV CONVERTER
        with xlrd.open_workbook(rawdata_filename) as wb:
            sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
            with open('a_file.csv', 'wb') as f:  # open('a_file.csv', 'w', newline="") for python 3
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))
        rawdata_filename = 'a_file.csv'

        test = []
        row_counter = 0  # FLAG for 2 different dataset
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                test.append(row)
                if test[row_counter][0] == 'Time':
                    break
                row_counter = row_counter + 1

        row_counter2 = 0
        code_line = []
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                if row_counter2 < row_counter:
                    row_counter2 = row_counter2 + 1
                else:
                    code_line.append(row)

        # coder = [None] * len(code_line)
        T = [None] * len(code_line)
        # direction = [None] * len(code_line)
        direction1 = [None] * len(code_line)
        # direction2 = [None] * len(code_line)
        # initiation = [None] * len(code_line)
        initiation1 = [None] * len(code_line)
        # initiation2 = [None] * len(code_line)
        # initiation3 = [None] * len(code_line)
        response = [None] * len(code_line)
        type = [None] * len(code_line)
        # type1 = [None] * len(code_line)
        # type2 = [None] * len(code_line)
        # type3 = [None] * len(code_line)


        # count_x = 0
        # if trial_no > 20:
        #     count_x = 0
        # elif trial_no <= 20 and trial_no > 3:
        #     count_x = 1
        # elif trial_no <= 3:
        #     count_y = 1

        for i in range(1, len(code_line)):
            # coder[i - 1] = str(code_line[i][0])
            T[i - 1] = str(code_line[i][0])
            direction1[i - 1] = str(code_line[i][7])
            # direction2[i - 1] = str(code_line[i][13])
            initiation1[i - 1] = str(code_line[i][8])
            # initiation2[i - 1] = str(code_line[i][7])
            # initiation3[i - 1] = str(code_line[i][6])
            response[i - 1] = str(code_line[i][8])
            type[i - 1] = str(code_line[i][14])
            # type2[i - 1] = str(code_line[i][14 + count_x])
            # type3[i - 1] = str(code_line[i][12])

        # if trial_no > 20:
        direction = direction1
        initiation = initiation1

        # elif trial_no <= 20 and trial_no > 3:
        #     direction = direction2
        #     initiation = initiation2
        #     type = type2
        #
        # elif trial_no <= 3 :
        #     direction = type3
        #     initiation = initiation3
        #     type = type2




        # print coder
        print T
        print direction
        print initiation
        print response
        print type

        initiation_count = 0
        response_count = 0
        externalization_count = 0

        for i in range(0, len(initiation)):
            if direction[i] == 'Child':
                if initiation[i] == "Initiation":
                    initiation_count = initiation_count + 1
                    initiation_time_array_first5.append(time[i])
                    if type[i] == "STOP":
                        initiation_count = initiation_count - 1
                elif initiation[i] == "Response":
                    response_count = response_count + 1
                    if type[i] == "STOP":
                        response_count = response_count - 1
            if direction[i] == 'Externalization':
                externalization_count = externalization_count + 1
                if type[i] == "STOP":
                    externalization_count = externalization_count - 1


                    # if response[i] == "Response":
                    #     response_count = response_count + 1
                    #     if type[i] == "STOP":
                    #         response_count = response_count - 1

            else:
                continue

        number_of_initiations = initiation_count
        number_of_responses = response_count
        number_of_externalizations = externalization_count
        return number_of_initiations, number_of_responses, number_of_externalizations

        # FUNTION END &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    # ############################################# PARAMETERS TO CHANGE ################


    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(starting_point, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0011_batch_all_LEGO-LOF (ACC) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.csv'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0011_batch_all_LEGO-LOF (ACC) processed')
    output_feature = open("allfeatures_eda_ACC_processed" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 16)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    #print allocation_array

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_A':
            part = 'mid5'
        if part == 'mid5_A':
            part = 'mid5'
        if part == 'ast5_A':
            part = 'last5'
        if part == 'id5_AC':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'
        if part == 'ACC.tx':
            part = 'total'
        if part == 'CC.txt':
            part = 'total'
        if part == 'total_':
            part = 'total'
        if part == 'otal_A':
            part = 'total'

        #print part

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
                elif part == 'total':
                    array_index_part = 3
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 4
                elif part == 'mid5':
                    array_index_part = 5
                elif part == 'last5':
                    array_index_part = 6
                elif part == 'total':
                    array_index_part = 7
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 8
                elif part == 'mid5':
                    array_index_part = 9
                elif part == 'last5':
                    array_index_part = 10
                elif part == 'total':
                    array_index_part = 11
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 12
                elif part == 'mid5':
                    array_index_part = 13
                elif part == 'last5':
                    array_index_part = 14
                elif part == 'total':
                    array_index_part = 15

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        #print i

        allocation_array[array_index * 16 + array_index_part] = 22
        #print allocation_array
    print allocation_array

    feature_list = ["Step_count", "Mean_step_time_during_movement", " Percent_stillness"]

    value_array = []
    for i in range((starting_point-1)*16, numberofexperiments * 16):
        if allocation_array[i] == -1:

            y = i % 16
            x = i / 16
            x = x + 1

            print "batuuuuuuuuuuuuuuuuuuuu" + str(x)

            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 16
            x = i / 16
            x = x + 1

            print "batuuuuuuuuuuuuuuuuuuuu" + str(x)

            #print 'x' + str(x)
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_total_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_total_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_total_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_total_'

            rawdata_name = 'output_' + str(rawdata_name_part1) + 'ACC.csv'

            print rawdata_name

            data = pd.read_csv(rawdata_name)
            # sheet_name='output_'+str(rawdata_name_part1) +'ACC'
            #
            #
            # workbook = xlrd.open_workbook(rawdata_name)
            #
            #
            # worksheet = workbook.sheet_by_index(0)

            feature_value = np.zeros(3)
            print data.iat[0, 2]

            feature_value[0] = data.iat[0, 2]
            feature_value[1] = data.iat[0, 3]
            feature_value[2] = data.iat[0, 4]

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + str(feature_value[k]))
                output_feature.write("\n")

    # print value_array


    data = pd.read_csv("allfeatures_eda_ACC_processed.txt")

    data2 = pd.pivot_table(data, index=["experiment", "participant", "session", "feature"], columns=["part"],
                           values=["value"])

    # print data2

    data2.to_csv(
        'allfeatures_eda_ACC_processed.csv')  # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment



    # print data2

    # data2 = data.pivot(index=['experiment,participant,session'], columns='part', values='value')
    #
    # print data2

    # for i in range(0, numberofexperiments):
    #     for i in range
    #
    # (data.replace(0, np.nan)
    #             .set_index('Time', append=True)
    #             .stack()
    #             .reset_index()
    #             .rename(columns={0:'val'})
    #             .drop('level_2',1))

    # print data

    os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data2.to_csv(
        'allfeatures_eda_ACC_processed.csv')
    os.chdir('..')
def eda_feature_extraction(numberofexperiments):
    os.chdir(output_directory_path)
    def count_initiation_response(rawdata_filename, number_of_initiations, number_of_responses):
        # FUNTION START /////////////////////////////////////////////////////////


        print rawdata_filename
        # SUB FUNCTION , EXCEL TO CSV CONVERTER
        with xlrd.open_workbook(rawdata_filename) as wb:
            sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
            with open('a_file.csv', 'wb') as f:  # open('a_file.csv', 'w', newline="") for python 3
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))
        rawdata_filename = 'a_file.csv'

        test = []
        row_counter = 0  # FLAG for 2 different dataset
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                test.append(row)
                if test[row_counter][0] == 'Time':
                    break
                row_counter = row_counter + 1

        row_counter2 = 0
        code_line = []
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                if row_counter2 < row_counter:
                    row_counter2 = row_counter2 + 1
                else:
                    code_line.append(row)

        # coder = [None] * len(code_line)
        T = [None] * len(code_line)
        # direction = [None] * len(code_line)
        direction1 = [None] * len(code_line)
        # direction2 = [None] * len(code_line)
        # initiation = [None] * len(code_line)
        initiation1 = [None] * len(code_line)
        # initiation2 = [None] * len(code_line)
        # initiation3 = [None] * len(code_line)
        response = [None] * len(code_line)
        type = [None] * len(code_line)
        # type1 = [None] * len(code_line)
        # type2 = [None] * len(code_line)
        # type3 = [None] * len(code_line)


        # count_x = 0
        # if trial_no > 20:
        #     count_x = 0
        # elif trial_no <= 20 and trial_no > 3:
        #     count_x = 1
        # elif trial_no <= 3:
        #     count_y = 1

        for i in range(1, len(code_line)):
            # coder[i - 1] = str(code_line[i][0])
            T[i - 1] = str(code_line[i][0])
            direction1[i - 1] = str(code_line[i][7])
            # direction2[i - 1] = str(code_line[i][13])
            initiation1[i - 1] = str(code_line[i][8])
            # initiation2[i - 1] = str(code_line[i][7])
            # initiation3[i - 1] = str(code_line[i][6])
            response[i - 1] = str(code_line[i][8])
            type[i - 1] = str(code_line[i][14])
            # type2[i - 1] = str(code_line[i][14 + count_x])
            # type3[i - 1] = str(code_line[i][12])

        # if trial_no > 20:
        direction = direction1
        initiation = initiation1

        # elif trial_no <= 20 and trial_no > 3:
        #     direction = direction2
        #     initiation = initiation2
        #     type = type2
        #
        # elif trial_no <= 3 :
        #     direction = type3
        #     initiation = initiation3
        #     type = type2




        # print coder
        print T
        print direction
        print initiation
        print response
        print type

        initiation_count = 0
        response_count = 0
        externalization_count = 0

        for i in range(0, len(initiation)):
            if direction[i] == 'Child':
                if initiation[i] == "Initiation":
                    initiation_count = initiation_count + 1
                    initiation_time_array_first5.append(time[i])
                    if type[i] == "STOP":
                        initiation_count = initiation_count - 1
                elif initiation[i] == "Response":
                    response_count = response_count + 1
                    if type[i] == "STOP":
                        response_count = response_count - 1
            if direction[i] == 'Externalization':
                externalization_count = externalization_count + 1
                if type[i] == "STOP":
                    externalization_count = externalization_count - 1


                    # if response[i] == "Response":
                    #     response_count = response_count + 1
                    #     if type[i] == "STOP":
                    #         response_count = response_count - 1

            else:
                continue

        number_of_initiations = initiation_count
        number_of_responses = response_count
        number_of_externalizations = externalization_count
        return number_of_initiations, number_of_responses, number_of_externalizations

        # FUNTION END &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    # ############################################# PARAMETERS TO CHANGE ################




    # if there is participant 44 , the comment should be removed # participant = 44




    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0009_batch5_LEGO-LOF (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0009_batch5_LEGO-LOF (EDA) processed')
    output_feature = open("allfeatures_eda_batch5_LEGO-LOF" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 12)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'ast5_E':
            part = 'last5'
        if part == 'id5_ED':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 3
                elif part == 'mid5':
                    array_index_part = 4
                elif part == 'last5':
                    array_index_part = 5
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 6
                elif part == 'mid5':
                    array_index_part = 7
                elif part == 'last5':
                    array_index_part = 8
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 9
                elif part == 'mid5':
                    array_index_part = 10
                elif part == 'last5':
                    array_index_part = 11

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 12 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 12):
        if allocation_array[i] == -1:

            y = i % 12
            x = i / 12
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 6:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 12
            x = i / 12
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 6:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)

            worksheet = workbook.sheet_by_name('CDA')
            feature_value = np.zeros(12)

            for p in range(3, 15):

                if worksheet.cell(1, p).value == '' or worksheet.cell(1, p).value == None:
                    pass
                else:
                    x2 = str(worksheet.cell(1, p).value)
                    feature_value[p - 3] = float(x2)

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + str(feature_value[k]))
                output_feature.write("\n")

    data = pd.read_csv("allfeatures_eda_batch5_LEGO-LOF.txt")

    data2 = pd.pivot_table(data, index=["experiment", "participant", "session", "feature"], columns=["part"],
                           values=["value"])


    data2.to_csv(
        'allfeatures_eda_batch5_LEGO-LOF.csv')  # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data2.to_csv(
        'allfeatures_eda_batch5_LEGO-LOF.csv')
    os.chdir('..')
def eda_feature_extraction_baseline(numberofexperiments):
    os.chdir(output_directory_path)
    # ############################################# PARAMETERS TO CHANGE ################



    # if there is participant 44 , the comment should be removed # participant = 44



    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0010_batch_BASELINE (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0010_batch_BASELINE (EDA) processed')
    output_feature = open("allfeatures_eda_batch_BASELINE" + '.txt', 'w')

    output_feature.write('experiment,participant,part,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 14)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        part = x[15:20]

        if part == 'break':
            part = 'break'
        if part == 'b1_ED':
            part = 'b1'
        if part == 'b2_ED':
            part = 'b2'
        if part == 'cb1_E':
            part = 'cb1'
        if part == 'cb2_E':
            part = 'cb2'
        if part == 'cb3_E':
            part = 'cb3'
        if part == 'cb4_E':
            part = 'cb4'
        if part == 'jb1_E':
            part = 'jb1'
        if part == 'jb2_E':
            part = 'jb2'
        if part == 'jb3_E':
            part = 'jb3'
        if part == 'jb4_E':
            part = 'jb4'

        array_index_part = 0
        if participant == '44':

            if part == 'b1':
                array_index_part = 0
            elif part == 'b2':
                array_index_part = 1
            elif part == 'break':
                array_index_part = 2
            elif part == 'cb1':
                array_index_part = 3
            elif part == 'cb2':
                array_index_part = 4
            elif part == 'cb3':
                array_index_part = 5
            elif part == 'cb4':
                array_index_part = 6

        elif participant == '55':
            if part == 'b1':
                array_index_part = 7
            elif part == 'b2':
                array_index_part = 8
            elif part == 'break':
                array_index_part = 9
            elif part == 'jb1':
                array_index_part = 10
            elif part == 'jb2':
                array_index_part = 11
            elif part == 'jb3':
                array_index_part = 12
            elif part == 'jb4':
                array_index_part = 13

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 14 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 14):
        if allocation_array[i] == -1:

            y = i % 14
            x = i / 14
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'b1' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'b2' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'break' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'rb1' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'rb2' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'rb3' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'rb4' + ','
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'b1' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'b2' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'break' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'rb1' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'rb2' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'rb3' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'rb4' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 14
            x = i / 14
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'b1' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'b1' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'b2' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'b2' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'break' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'break' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'rb1' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb1' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'rb2' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb2' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'rb3' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb3' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'rb4' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb4' + '_'
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'b1' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'b1' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'b2' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'b2' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'break' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'break' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'rb1' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb1' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'rb2' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb2' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'rb3' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb3' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'rb4' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb4' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)

            worksheet = workbook.sheet_by_name('CDA')
            feature_value = np.zeros(12)
            # feature_value = np.empty(12, dtype='string')


            for p in range(3, 15):

                if worksheet.cell(1, p).value == '' or worksheet.cell(1, p).value == None:
                    pass
                else:
                    x2 = str(worksheet.cell(1, p).value)
                    feature_value[p - 3] = float(x2)

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + str(feature_value[k]))
                output_feature.write("\n")

    # print value_array


    data = pd.read_csv("allfeatures_eda_batch_BASELINE.txt")

    data2 = pd.pivot_table(data, index=["experiment", "participant", "feature"], columns=["part"], values=["value"])

    # print data2

    data2.to_csv(
        'allfeatures_eda_batch_BASELINE.csv')  # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data2.to_csv(
        'allfeatures_eda_batch_BASELINE.csv')
    os.chdir('..')
def eda_feature_extraction_baseline_break(numberofexperiments):
    os.chdir(output_directory_path)
    # ############################################# PARAMETERS TO CHANGE ################



    # if there is participant 44 , the comment should be removed # participant = 44



    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0010_batch_break_BASELINE (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0010_batch_break_BASELINE (EDA) processed')
    output_feature = open("allfeatures_eda_batch_break_BASELINE" + '.txt', 'w')

    output_feature.write('experiment,participant,part,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 14)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        part = x[15:20]

        if part == 'break':
            part = 'break'
        if part == 'b1_ED':
            part = 'b1'
        if part == 'b2_ED':
            part = 'b2'
        if part == 'cb1_E':
            part = 'cb1'
        if part == 'cb2_E':
            part = 'cb2'
        if part == 'cb3_E':
            part = 'cb3'
        if part == 'cb4_E':
            part = 'cb4'
        if part == 'jb1_E':
            part = 'jb1'
        if part == 'jb2_E':
            part = 'jb2'
        if part == 'jb3_E':
            part = 'jb3'
        if part == 'jb4_E':
            part = 'jb4'

        array_index_part = 0
        if participant == '44':

            if part == 'b1':
                array_index_part = 0
            elif part == 'b2':
                array_index_part = 1
            elif part == 'break':
                array_index_part = 2
            elif part == 'cb1':
                array_index_part = 3
            elif part == 'cb2':
                array_index_part = 4
            elif part == 'cb3':
                array_index_part = 5
            elif part == 'cb4':
                array_index_part = 6

        elif participant == '55':
            if part == 'b1':
                array_index_part = 7
            elif part == 'b2':
                array_index_part = 8
            elif part == 'break':
                array_index_part = 9
            elif part == 'jb1':
                array_index_part = 10
            elif part == 'jb2':
                array_index_part = 11
            elif part == 'jb3':
                array_index_part = 12
            elif part == 'jb4':
                array_index_part = 13

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 14 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 14):
        if allocation_array[i] == -1:

            y = i % 14
            x = i / 14
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'b1' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'b2' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'break' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'rb1' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'rb2' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'rb3' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'rb4' + ','
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'b1' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'b2' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'break' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'rb1' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'rb2' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'rb3' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'rb4' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 14
            x = i / 14
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'b1' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'b1' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'b2' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'b2' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'break' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'break' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'rb1' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb1' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'rb2' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb2' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'rb3' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb3' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'rb4' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'cb4' + '_'
            elif value == 7:
                text_output = trial + ',' + '55' + ',' + 'b1' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'b1' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'b2' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'b2' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'break' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'break' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'rb1' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb1' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'rb2' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb2' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'rb3' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb3' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'rb4' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'jb4' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)

            worksheet = workbook.sheet_by_name('CDA')
            feature_value = np.zeros(12)
            # feature_value = np.empty(12, dtype='string')


            for p in range(3, 15):

                if worksheet.cell(1, p).value == '' or worksheet.cell(1, p).value == None:
                    pass
                else:
                    x2 = str(worksheet.cell(1, p).value)
                    feature_value[p - 3] = float(x2)

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + str(feature_value[k]))
                output_feature.write("\n")

    # print value_array


    data = pd.read_csv("allfeatures_eda_batch_break_BASELINE.txt")

    data2 = pd.pivot_table(data, index=["experiment", "participant", "feature"], columns=["part"], values=["value"])

    # print data2

    data2.to_csv(
        'allfeatures_eda_batch_break_BASELINE.csv')  # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment

    os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data2.to_csv(
        'allfeatures_eda_batch_break_BASELINE.csv')
    os.chdir('..')
def eda_feature_extraction_wtotal(numberofexperiments):
    os.chdir(output_directory_path)
    def count_initiation_response(rawdata_filename, number_of_initiations, number_of_responses):
        # FUNTION START /////////////////////////////////////////////////////////


        print rawdata_filename
        # SUB FUNCTION , EXCEL TO CSV CONVERTER
        with xlrd.open_workbook(rawdata_filename) as wb:
            sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
            with open('a_file.csv', 'wb') as f:  # open('a_file.csv', 'w', newline="") for python 3
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))
        rawdata_filename = 'a_file.csv'

        test = []
        row_counter = 0  # FLAG for 2 different dataset
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                test.append(row)
                if test[row_counter][0] == 'Time':
                    break
                row_counter = row_counter + 1

        row_counter2 = 0
        code_line = []
        with open(rawdata_filename, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                if row_counter2 < row_counter:
                    row_counter2 = row_counter2 + 1
                else:
                    code_line.append(row)

        # coder = [None] * len(code_line)
        T = [None] * len(code_line)
        # direction = [None] * len(code_line)
        direction1 = [None] * len(code_line)
        # direction2 = [None] * len(code_line)
        # initiation = [None] * len(code_line)
        initiation1 = [None] * len(code_line)
        # initiation2 = [None] * len(code_line)
        # initiation3 = [None] * len(code_line)
        response = [None] * len(code_line)
        type = [None] * len(code_line)
        # type1 = [None] * len(code_line)
        # type2 = [None] * len(code_line)
        # type3 = [None] * len(code_line)


        # count_x = 0
        # if trial_no > 20:
        #     count_x = 0
        # elif trial_no <= 20 and trial_no > 3:
        #     count_x = 1
        # elif trial_no <= 3:
        #     count_y = 1

        for i in range(1, len(code_line)):
            # coder[i - 1] = str(code_line[i][0])
            T[i - 1] = str(code_line[i][0])
            direction1[i - 1] = str(code_line[i][7])
            # direction2[i - 1] = str(code_line[i][13])
            initiation1[i - 1] = str(code_line[i][8])
            # initiation2[i - 1] = str(code_line[i][7])
            # initiation3[i - 1] = str(code_line[i][6])
            response[i - 1] = str(code_line[i][8])
            type[i - 1] = str(code_line[i][14])
            # type2[i - 1] = str(code_line[i][14 + count_x])
            # type3[i - 1] = str(code_line[i][12])

        # if trial_no > 20:
        direction = direction1
        initiation = initiation1

        # elif trial_no <= 20 and trial_no > 3:
        #     direction = direction2
        #     initiation = initiation2
        #     type = type2
        #
        # elif trial_no <= 3 :
        #     direction = type3
        #     initiation = initiation3
        #     type = type2




        # print coder
        print T
        print direction
        print initiation
        print response
        print type

        initiation_count = 0
        response_count = 0
        externalization_count = 0

        for i in range(0, len(initiation)):
            if direction[i] == 'Child':
                if initiation[i] == "Initiation":
                    initiation_count = initiation_count + 1
                    initiation_time_array_first5.append(time[i])
                    if type[i] == "STOP":
                        initiation_count = initiation_count - 1
                elif initiation[i] == "Response":
                    response_count = response_count + 1
                    if type[i] == "STOP":
                        response_count = response_count - 1
            if direction[i] == 'Externalization':
                externalization_count = externalization_count + 1
                if type[i] == "STOP":
                    externalization_count = externalization_count - 1


                    # if response[i] == "Response":
                    #     response_count = response_count + 1
                    #     if type[i] == "STOP":
                    #         response_count = response_count - 1

            else:
                continue

        number_of_initiations = initiation_count
        number_of_responses = response_count
        number_of_externalizations = externalization_count
        return number_of_initiations, number_of_responses, number_of_externalizations

        # FUNTION END &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    # ############################################# PARAMETERS TO CHANGE ################


    # if there is participant 44 , the comment should be removed # participant = 44




    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []

    for i in range(1, numberofexperiments + 1):
        if i < 10:
            trial = "000" + str(i)
        elif i >= 10 and i < 100:
            trial = "00" + str(i)
        elif i >= 100 and i < 1000:
            trial = "0" + str(i)
        elif i >= 1000:
            trial = str(i)

        trial_array.append(trial)

    print trial_array

    list = []
    for x in os.listdir('./0009_batch_LEGO-LOF (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.xls'):
            list_excel.append(list[i])

    print list_excel

    os.chdir('./0009_batch_LEGO-LOF (EDA) processed')
    output_feature = open("allfeatures_eda_batch_LEGO-LOF" + '.txt', 'w')

    output_feature.write('experiment,participant,session,part,feature,value')
    output_feature.write("\n")

    allocation_array = np.zeros(numberofexperiments * 16)

    print len(allocation_array)

    for i in range(0, len(allocation_array)):
        allocation_array[i] = -1

    for i in range(0, len(list_excel)):
        x = list_excel[i]
        trial = x[0:11]
        trial_no = x[7:11]
        participant = x[12:14]
        session = x[15:19]
        if x[15:19] == 'LOF_':
            session = 'LOF'
        part = x[20:26]
        if part == 'last5_':
            part = 'last5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'mid5_E':
            part = 'mid5'
        if part == 'ast5_E':
            part = 'last5'
        if part == 'id5_ED':
            part = 'mid5'
        if part == 'irst5':
            part = 'first5'
        if part == 'irst5_':
            part = 'first5'
        if part == 'EDA_er':
            part = 'total'
        if part == 'DA_era':
            part = 'total'

        # print part

        array_index_part = 0
        if participant == '44':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 0
                elif part == 'mid5':
                    array_index_part = 1
                elif part == 'last5':
                    array_index_part = 2
                elif part == 'total':
                    array_index_part = 3
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 4
                elif part == 'mid5':
                    array_index_part = 5
                elif part == 'last5':
                    array_index_part = 6
                elif part == 'total':
                    array_index_part = 7
        elif participant == '55':
            if session == 'LEGO':
                if part == 'first5':
                    array_index_part = 8
                elif part == 'mid5':
                    array_index_part = 9
                elif part == 'last5':
                    array_index_part = 10
                elif part == 'total':
                    array_index_part = 11
            elif session == 'LOF':
                if part == 'first5':
                    array_index_part = 12
                elif part == 'mid5':
                    array_index_part = 13
                elif part == 'last5':
                    array_index_part = 14
                elif part == 'total':
                    array_index_part = 15

        array_index = 0
        for i in range(0, len(trial_array)):
            if trial_array[i] == trial_no:
                array_index = i
                break

        allocation_array[array_index * 16 + array_index_part] = 22

    print allocation_array

    feature_list = ["CDAnSCR", "CDALatency", "CDAAmpSum", "CDASCR", "CDAISCR", "CDAPhasicMax", "CDATonic", "TTPnSCR",
                    "TTPLatency", "TTPAmpSum", "GlobalMean", "GlobalMaxDeflection"]

    value_array = []
    for i in range(0, numberofexperiments * 16):
        if allocation_array[i] == -1:

            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print

            value_array.append(x)
            value = y
            # print value

            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + '-1')
                output_feature.write("\n")


        elif allocation_array[i] == 22:
            y = i % 16
            x = i / 16
            x = x + 1
            if x < 10:
                trial = "000" + str(x)
            elif x >= 10 and x < 100:
                trial = "00" + str(x)
            elif x >= 100 and x < 1000:
                trial = "0" + str(x)
            elif x >= 1000:
                trial = str(x)

            # if x > 12:
            #     value = x - 12
            #     print value
            # elif  x<=12:
            #     value = x
            #     print value
            value_array.append(x)
            value = y
            # print value

            rawdata_name_part1 = ''
            text_output = ''
            if value == 0:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 1:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 2:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 3:
                text_output = trial + ',' + '44' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LEGO' + '_'
            elif value == 4:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 5:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 6:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 7:
                text_output = trial + ',' + '44' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '44' + '_' + 'LOF' + '_'
            elif value == 8:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'first5' + '_'
            elif value == 9:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'mid5' + '_'
            elif value == 10:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_' + 'last5' + '_'
            elif value == 11:
                text_output = trial + ',' + '55' + ',' + 'LEGO' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LEGO' + '_'
            elif value == 12:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'first5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'first5' + '_'
            elif value == 13:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'mid5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'mid5' + '_'
            elif value == 14:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'last5' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_' + 'last5' + '_'
            elif value == 15:
                text_output = trial + ',' + '55' + ',' + 'LOF' + ',' + 'total' + ','
                rawdata_name_part1 = trial + '_' + '55' + '_' + 'LOF' + '_'

            if wzscore == 1:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era_z.xls'
            elif wzscore == 0:
                rawdata_name = 'output_' + str(rawdata_name_part1) + 'EDA_era.xls'

            workbook = xlrd.open_workbook(rawdata_name)

            worksheet = workbook.sheet_by_name('CDA')
            feature_value = np.zeros(12)

            for p in range(3, 15):

                if worksheet.cell(1, p).value == '' or worksheet.cell(1, p).value == None:
                    pass
                else:
                    x2 = str(worksheet.cell(1, p).value)
                    feature_value[p - 3] = float(x2)

            for k in range(0, len(feature_list)):
                output_feature.write(text_output + feature_list[k] + ',' + str(feature_value[k]))
                output_feature.write("\n")

    # print value_array


    data = pd.read_csv("allfeatures_eda_batch_LEGO-LOF.txt")

    data2 = pd.pivot_table(data, index=["experiment", "participant", "session", "feature"], columns=["part"],
                           values=["value"])

    # print data2

    data2.to_csv(
        'allfeatures_eda_batch_LEGO-LOF.csv')  # it is not working well , always set the numberofexpperiments parameter +1 , and then remove the variables from the extra experiment


    os.chdir('..')

    os.chdir('./0015_OUTPUT')
    data2.to_csv(
        'allfeatures_eda_batch_LEGO-LOF.csv')
    os.chdir('..')

#12-a system log create merged dataframe
def systemlog_create_merged_dataframe():
    os.chdir(system_log_output_destination)

    def dataframe_change_column_name(dataframe,participant,phase):

        dataframe.columns = ["empty",'experiment', 'char_greeting',
                                            "hunted_fireflies","char_texture_change",
                                            "char_being_idle","point_at_action",
                                            "area_covered","time_of_first_char",
                                            "manipulate_prop","distance_btw_participants",
                                            "merge_char"]
        #"participant","session","phase",

        dataframe = dataframe.drop(["empty"], axis=1)

        dataframe.insert(loc=1, column="phase", value=phase)
        dataframe.insert(loc=1, column="session", value="LOF")
        dataframe.insert(loc=1, column="participant", value=participant)

        return dataframe

    dataframe_modified_ASC_total= pd.read_csv('dataframe_modified_ASC_total.csv')
    dataframe_modified_ASC_total = dataframe_change_column_name(dataframe_modified_ASC_total,"ASC","total")
    dataframe_modified_ASC_first5= pd.read_csv('dataframe_modified_ASC_first.csv')
    dataframe_modified_ASC_first5 = dataframe_change_column_name(dataframe_modified_ASC_first5,"ASC","first5")
    dataframe_modified_ASC_mid5= pd.read_csv('dataframe_modified_ASC_mid.csv')
    dataframe_modified_ASC_mid5 = dataframe_change_column_name(dataframe_modified_ASC_mid5,"ASC","mid5")
    dataframe_modified_ASC_last5= pd.read_csv('dataframe_modified_ASC_last.csv')
    dataframe_modified_ASC_last5 = dataframe_change_column_name(dataframe_modified_ASC_last5,"ASC","last5")

    dataframe_modified_NONASC_total= pd.read_csv('dataframe_modified_NONASC_total.csv')
    dataframe_modified_NONASC_total = dataframe_change_column_name(dataframe_modified_NONASC_total,"NONASC","total")
    dataframe_modified_NONASC_first5= pd.read_csv('dataframe_modified_NONASC_first.csv')
    dataframe_modified_NONASC_first5 = dataframe_change_column_name(dataframe_modified_NONASC_first5,"NONASC","first5")
    dataframe_modified_NONASC_mid5= pd.read_csv('dataframe_modified_NONASC_mid.csv')
    dataframe_modified_NONASC_mid5 = dataframe_change_column_name(dataframe_modified_NONASC_mid5,"NONASC","mid5")
    dataframe_modified_NONASC_last5= pd.read_csv('dataframe_modified_NONASC_last.csv')
    dataframe_modified_NONASC_last5 = dataframe_change_column_name(dataframe_modified_NONASC_last5,"NONASC","last5")

    frames = [dataframe_modified_ASC_total, dataframe_modified_ASC_first5, dataframe_modified_ASC_mid5,dataframe_modified_ASC_last5,
              dataframe_modified_NONASC_total, dataframe_modified_NONASC_first5, dataframe_modified_NONASC_mid5,dataframe_modified_NONASC_last5]

    result = pd.concat(frames)

    result = result.replace(-1, 0)
    result = result.replace(-2, 0)

    result.to_csv("systemlog_create_merged_dataframe.csv",index=False)


    src_file = output_directory_path +"0007-SYSTEM_LOGS/systemlog_create_merged_dataframe.csv"
    dst_file = output_directory_path + folder25 + "/0002_system_logging"
    shutil.copy(src_file, dst_file)

    # 1 - char_greeting
    # 2 - hunted_fireflies
    # 3 - char_texture_change
    # 4 - char_being_idle
    # 5 - point_at_action
    # 6 - manipulate_prop
    # 7 - area_covered
    # 8 - distance_btw_participants
    # 9 - merge_char
    # 10 - time_of_first_char


#12 RESULT FOLDER
def create_result_folder():
    os.chdir(output_directory_path)
    createFolder(output_directory_path + folder25)
    os.chdir(output_directory_path + folder25)

    ##################VIDEO CODING
    createFolder("0001_video_coding")
    src_file = output_directory_path +"0008-VIDEO-CODING/all_features_video_coding_ASC.txt"
    dst_file = output_directory_path + folder25 + "/0001_video_coding"
    shutil.copy(src_file, dst_file)
    src_file = output_directory_path +"0008-VIDEO-CODING - NONASC/all_features_video_coding_NONASC.txt"
    dst_file = output_directory_path + folder25 + "/0001_video_coding"
    shutil.copy(src_file, dst_file)

    createFolder("0002_system_logging")

    ##################ACC
    createFolder("0004_ACC")
    src_file = output_directory_path +"0011_batch_all_LEGO-LOF (ACC) processed/allfeatures_eda_ACC_processed.csv"
    dst_file = output_directory_path + folder25 + "/0004_ACC"
    shutil.copy(src_file, dst_file)

    ##################EDA

    createFolder("0005_EDA")
    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_batch_LEGO-LOF.csv"
    dst_file = output_directory_path + folder25 + "/0005_EDA"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_batch5_LEGO-LOF.csv"
    dst_file = output_directory_path + folder25 + "/0005_EDA"
    shutil.copy(src_file, dst_file)

    ##################EDA BASELINE

    createFolder("0006_EDA_and_Baseline")
    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_batch_BASELINE.csv"
    dst_file = output_directory_path + folder25 + "/0006_EDA_and_Baseline"
    shutil.copy(src_file, dst_file)
    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_batch_break_BASELINE.csv"
    dst_file = output_directory_path + folder25 + "/0006_EDA_and_Baseline"
    shutil.copy(src_file, dst_file)

    ##################ECG batch

    createFolder("0007_ECG")
    src_file = output_directory_path +"0005-LEGO-LOF (HRV) extracted features/allfeatures2.txt"
    dst_file = output_directory_path + folder25 + "/0007_ECG"
    shutil.copy(src_file, dst_file)

    ##################ECG baseline

    createFolder("0008_ECG-Baseline")
    src_file = output_directory_path +"0006-BASELINE (HRV) extracted features/allfeatures2.txt"
    dst_file = output_directory_path + folder25 + "/0008_ECG-Baseline"
    shutil.copy(src_file, dst_file)

    ##################ECG event

    createFolder("0009_ECG_and_VideoLog")
    src_file = output_directory_path +"0017-RESULT-ECG-EVENT/ALL_allfeatures_(HRV)_extracted_features_EVENT_batu.txt"
    dst_file = output_directory_path + folder25 + "/0009_ECG_and_VideoLog"
    shutil.copy(src_file, dst_file)

    ##################EDA batch merger

    createFolder("0010_ALL_EDA_MERGED")
    src_file = output_directory_path +"experiment_order.csv"
    dst_file = output_directory_path + folder25 + "/0010_ALL_EDA_MERGED"
    shutil.copy(src_file, dst_file)

    ##################ECG batch merger

    createFolder("0011_ALL_ECG_MERGED")
    src_file = output_directory_path +"experiment_order.csv"
    dst_file = output_directory_path + folder25 + "/0011_ALL_ECG_MERGED"
    shutil.copy(src_file, dst_file)

    ################## EDA ECG batch merger

    createFolder("0013_ALL_EDA_ECG_MERGED")

    # 15 MERGE ECG BATCH & EDA BATCH with VIDEO CODING
    createFolder("0015_ALL_EDA_ECG_VIDEO_MERGED")

    createFolder("0016_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED")

    createFolder("0017_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC")

    createFolder("0018_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC_QST")

#13 MERGE EDA BASELINE
def merge_EDA_baselines():

    def change_column(allfeatures_eda_batch_BASELINE):
        allfeatures_eda_batch_BASELINE.at[1, 3] = allfeatures_eda_batch_BASELINE.at[0, 3]
        allfeatures_eda_batch_BASELINE.at[1, 4] = allfeatures_eda_batch_BASELINE.at[0, 4]
        allfeatures_eda_batch_BASELINE.at[1, 5] = allfeatures_eda_batch_BASELINE.at[0, 5]
        allfeatures_eda_batch_BASELINE.at[1, 6] = allfeatures_eda_batch_BASELINE.at[0, 6]
        allfeatures_eda_batch_BASELINE.at[1, 7] = allfeatures_eda_batch_BASELINE.at[0, 7]
        allfeatures_eda_batch_BASELINE.at[1, 8] = allfeatures_eda_batch_BASELINE.at[0, 8]
        allfeatures_eda_batch_BASELINE.at[1, 9] = allfeatures_eda_batch_BASELINE.at[0, 9]
        allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE.drop([0])

        new_header = allfeatures_eda_batch_BASELINE.iloc[0]  # grab the first row for the header
        allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE[1:]  # take the data less the header row
        allfeatures_eda_batch_BASELINE.columns = new_header  # set the header row as the df header

        return allfeatures_eda_batch_BASELINE


    os.chdir(output_directory_path + folder25 + "/0006_EDA_and_Baseline")
    allfeatures_eda_batch_BASELINE = pd.read_csv("allfeatures_eda_batch_BASELINE.csv",skiprows=[0], header=None)
    allfeatures_eda_batch_break_BASELINE = pd.read_csv("allfeatures_eda_batch_break_BASELINE.csv",skiprows=[0], header=None)

    allfeatures_eda_batch_BASELINE = change_column(allfeatures_eda_batch_BASELINE)
    allfeatures_eda_batch_break_BASELINE = change_column(allfeatures_eda_batch_break_BASELINE)


    allfeatures_eda_batch_BASELINE["break"] = allfeatures_eda_batch_break_BASELINE["break"]

    allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE[allfeatures_eda_batch_BASELINE.experiment != "35"]
    allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE[allfeatures_eda_batch_BASELINE.experiment != "36"]

    allfeatures_eda_batch_BASELINE.to_csv("allfeatures_eda_batch_BASELINE_MERGED_OUTLIERS_CLEANED.csv",index=False)
def merge_EDA_batch():

    def change_column(allfeatures_eda_batch_BASELINE):

        allfeatures_eda_batch_BASELINE.at[1, 4] = allfeatures_eda_batch_BASELINE.at[0, 4]
        allfeatures_eda_batch_BASELINE.at[1, 5] = allfeatures_eda_batch_BASELINE.at[0, 5]
        allfeatures_eda_batch_BASELINE.at[1, 6] = allfeatures_eda_batch_BASELINE.at[0, 6]
        allfeatures_eda_batch_BASELINE.at[1, 7] = allfeatures_eda_batch_BASELINE.at[0, 7]

        allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE.drop([0])

        new_header = allfeatures_eda_batch_BASELINE.iloc[0]  # grab the first row for the header
        allfeatures_eda_batch_BASELINE = allfeatures_eda_batch_BASELINE[1:]  # take the data less the header row
        allfeatures_eda_batch_BASELINE.columns = new_header  # set the header row as the df header

        return allfeatures_eda_batch_BASELINE

    os.chdir(output_directory_path + folder25 + "/0005_EDA")
    allfeatures_eda_batch_LEGO_LOF = pd.read_csv("allfeatures_eda_batch_LEGO-LOF.csv",skiprows=[0], header=None)
    allfeatures_eda_batch5_LEGO_LOF = pd.read_csv("allfeatures_eda_batch5_LEGO-LOF.csv",skiprows=[0], header=None)


    allfeatures_eda_batch_LEGO_LOF= change_column(allfeatures_eda_batch_LEGO_LOF)
    allfeatures_eda_batch5_LEGO_LOF.at[0,7] = "total"
    allfeatures_eda_batch5_LEGO_LOF = change_column(allfeatures_eda_batch5_LEGO_LOF)

    allfeatures_eda_batch5_LEGO_LOF = allfeatures_eda_batch5_LEGO_LOF[['experiment', 'participant', 'session', 'feature', 'first5', 'mid5', 'last5', 'total']]


    allfeatures_eda_batch5_LEGO_LOF["total"] = allfeatures_eda_batch_LEGO_LOF["total"]

    allfeatures_eda_batch5_LEGO_LOF.to_csv("allfeatures_eda_batch5_LEGO-LOF_MERGED.csv", index=False)
def merge_EDA_batch_baseline():


    src_file = output_directory_path +folder25 +"/0006_EDA_and_Baseline/allfeatures_eda_batch_BASELINE_MERGED_OUTLIERS_CLEANED.csv"
    dst_file = output_directory_path + folder25 + "/0010_ALL_EDA_MERGED"
    shutil.copy(src_file, dst_file)


    src_file = output_directory_path +folder25 +"/0005_EDA/allfeatures_eda_batch5_LEGO-LOF_MERGED.csv"
    dst_file = output_directory_path + folder25 + "/0010_ALL_EDA_MERGED"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path + folder25 + "/0010_ALL_EDA_MERGED")

    def create_new_baseline():
        f = open('allfeatures_eda_batch_BASELINE_MERGED_OUTLIERS_CLEANED.csv')

        counter = 0

        outF = open("allfeatures2.txt", "w")
        # use readline() to read the first line
        line = f.readline()
        # use the read line to read further.
        # If the file is not empty keep reading one line
        # at a time, till the file is empty
        while line:
            # in python 2+
            # print line
            # in python 3 print is a builtin function, so

            # use realine() to read next line
            line = f.readline()
            x = str(line)
            print(x)
            outF.write(x)
            outF.write(x)
            counter = counter + 1

        f.close()
        outF.close

        rawdata_order2 = 'allfeatures2.txt'
        EDA_baseline = pd.read_csv(rawdata_order2, sep=',',
                                   names=["experiment", "participant", "feature", "b1", "b2", "break", "rb1", "rb2",
                                          "rb3", "rb4"])

        # print batch_LEGO_LOF.iloc[0]["experiment"]

        size = EDA_baseline.shape[0]

        EDA_baseline.insert(2, "session", "")

        # df.insert(3, "Age", [21, 23, 24, 21], True)

        t = 0
        for i in range(0, size):

            # print(index, row)
            # print (row)
            if t % 2 == 0:
                EDA_baseline.at[t, 'session'] = "LEGO"

            else:
                EDA_baseline.at[t, 'session'] = "LOF"
            # print (row)
            t = t + 1

        EDA_baseline.to_csv('EDA_baseline_new.csv', index=False)

        ##########################################

        rawdata_order2 = 'EDA_baseline_new.csv'
        EDA_baseline_new = pd.read_csv(rawdata_order2, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        rawdata_order3 = 'experiment_order.csv'
        experiment_order = pd.read_csv(rawdata_order3, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        i = 0
        for index, row in EDA_baseline_new.iterrows():
            # print(index, row)
            # print (row)
            index_session = EDA_baseline_new.at[i, 'experiment']
            condition = experiment_order['condition'][index_session - 1]
            session = EDA_baseline_new['session'][i]

            if condition == "LEGO" and session == "LEGO":
                EDA_baseline_new.at[i, 'rb3'] = -2
                EDA_baseline_new.at[i, 'rb4'] = -2
            elif condition == "LOF" and session == "LEGO":
                EDA_baseline_new.at[i, 'rb1'] = -2
                EDA_baseline_new.at[i, 'rb2'] = -2
            elif condition == "LEGO" and session == "LOF":
                EDA_baseline_new.at[i, 'rb1'] = -2
                EDA_baseline_new.at[i, 'rb2'] = -2
            elif condition == "LOF" and session == "LOF":
                EDA_baseline_new.at[i, 'rb3'] = -2
                EDA_baseline_new.at[i, 'rb4'] = -2

            i = i + 1

        EDA_baseline_new.to_csv('EDA_baseline_new.csv', index=False)
    def merge_everything():
        rawdata_order2 = 'EDA_baseline_new.csv'
        batch_BASELINE = pd.read_csv(rawdata_order2, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        # print batch_LEGO_LOF

        rawdata_order3 = 'allfeatures_eda_batch5_LEGO-LOF_MERGED.csv'
        batch_LEGO_LOF = pd.read_csv(rawdata_order3, sep=',')

        batch_LEGO_LOF.set_index(['experiment', 'participant', 'session', 'feature'])

        batch_BASELINE.set_index(['experiment', 'participant', 'session', 'feature'])

        result = pd.merge(batch_LEGO_LOF, batch_BASELINE, on=['experiment', 'participant', 'session', 'feature'])
        result.to_csv('EDA_batch_baseline_MERGED.csv', index=False)

        dataset_name = 'EDA_batch_baseline_MERGED.csv'
        merged = pd.read_csv(dataset_name, sep=',')

        ECG_baseline_new = merged

        i = 0
        for index, row in ECG_baseline_new.iterrows():
            # print(index, row)
            # print (row)

            if ECG_baseline_new.at[i, 'rb1'] == -2:
                ECG_baseline_new.at[i, 'rb1'] = ECG_baseline_new.at[i, 'rb3']
                ECG_baseline_new.at[i, 'rb2'] = ECG_baseline_new.at[i, 'rb4']
            else:
                print ("ok")

            i = i + 1

        ECG_baseline_new = ECG_baseline_new.drop(columns=['rb3', 'rb4'], axis=1)

        ECG_baseline_new = ECG_baseline_new.replace(-1, np.nan)

        ECG_baseline_new.to_csv('ALL_EDA.csv', index=False)

    create_new_baseline()
    merge_everything()

#14 MERGE ECG BATCH with BASELINE
def merge_ECG_baselines():
    os.chdir(output_directory_path +folder25 +"/0008_ECG-Baseline")
    BASELINE_HRV_extracted_features = pd.read_csv("allfeatures2.txt",  delimiter=';', header = None)
    BASELINE_HRV_extracted_features = BASELINE_HRV_extracted_features.rename(columns={0: 'experiment',1: 'participant',
                                                                                      2: 'feature',3: 'b1',4: 'b2',5: 'break',6: 'rb1',
                                                                                      7: 'rb2',8: 'rb3',9: 'rb4'})

    BASELINE_HRV_extracted_features = BASELINE_HRV_extracted_features[BASELINE_HRV_extracted_features.experiment != 0]
    BASELINE_HRV_extracted_features = BASELINE_HRV_extracted_features.sort_values(by=['experiment','participant','feature'])


    BASELINE_HRV_extracted_features.to_csv("ECG_baseline.csv",index=False)
    print BASELINE_HRV_extracted_features
def merge_ECG_batch():
    os.chdir(output_directory_path +folder25 +"/0007_ECG")
    HRV_extracted_features = pd.read_csv("allfeatures2.txt",  delimiter=';', header = None)
    HRV_extracted_features = HRV_extracted_features.rename(columns={0: 'experiment',1: 'participant',
                                                                                      2: 'condition',3: 'feature',4: 'first5',5: 'mid5',6: 'last5',
                                                                                      7: 'total'})

    #BASELINE_HRV_extracted_features = BASELINE_HRV_extracted_features[BASELINE_HRV_extracted_features.experiment != 0]
    HRV_extracted_features = HRV_extracted_features.sort_values(by=['experiment','participant',"condition",'feature'])


    HRV_extracted_features.to_csv("ECG_batch.csv",index=False)
    print HRV_extracted_features
def merge_ECG_batch_baseline():

    src_file = output_directory_path +folder25 +"/0008_ECG-Baseline/ECG_baseline.csv"
    dst_file = output_directory_path + folder25 + "/0011_ALL_ECG_MERGED"
    shutil.copy(src_file, dst_file)


    src_file = output_directory_path +folder25 +"/0007_ECG/ECG_batch.csv"
    dst_file = output_directory_path + folder25 + "/0011_ALL_ECG_MERGED"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path + folder25 + "/0011_ALL_ECG_MERGED")

    def create_new_baseline():
        import pandas as pd
        import numpy as np

        def isNaN(string):
            return string != string

        f = open('ECG_baseline.csv')
        outF = open("allfeatures2.txt", "w")
        # use readline() to read the first line
        line = f.readline()
        # use the read line to read further.
        # If the file is not empty keep reading one line
        # at a time, till the file is empty
        while line:
            # in python 2+
            # print line
            # in python 3 print is a builtin function, so

            # use realine() to read next line
            line = f.readline()
            x = str(line)
            print(x)
            outF.write(x)
            outF.write(x)

        f.close()
        outF.close

        rawdata_order2 = 'allfeatures2.txt'
        ECG_baseline = pd.read_csv(rawdata_order2, sep=',',
                                   names=["experiment", "participant", "feature", "b1", "b2", "break", "rb1", "rb2",
                                          "rb3", "rb4"])

        # print batch_LEGO_LOF.iloc[0]["experiment"]

        ECG_baseline.insert(2, "session", "")

        # df.insert(3, "Age", [21, 23, 24, 21], True)

        i = 0
        for index, row in ECG_baseline.iterrows():
            # print(index, row)
            # print (row)
            if i % 2 == 0:
                ECG_baseline.at[i, 'session'] = "LEGO"

            else:
                ECG_baseline.at[i, 'session'] = "LOF"
            # print (row)
            i = i + 1

        ECG_baseline.to_csv('ECG_baseline_new.csv', index=False)

        ###########################################

        rawdata_order2 = 'ECG_baseline_new.csv'
        ECG_baseline_new = pd.read_csv(rawdata_order2, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        rawdata_order3 = 'experiment_order.csv'
        experiment_order = pd.read_csv(rawdata_order3, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        i = 0
        for index, row in ECG_baseline_new.iterrows():
            # print(index, row)
            # print (row)
            index_session = ECG_baseline_new.at[i, 'experiment']
            condition = experiment_order['condition'][index_session - 1]
            session = ECG_baseline_new['session'][i]

            if condition == "LEGO" and session == "LEGO":
                ECG_baseline_new.at[i, 'rb3'] = -2
                ECG_baseline_new.at[i, 'rb4'] = -2
            elif condition == "LOF" and session == "LEGO":
                ECG_baseline_new.at[i, 'rb1'] = -2
                ECG_baseline_new.at[i, 'rb2'] = -2
            elif condition == "LEGO" and session == "LOF":
                ECG_baseline_new.at[i, 'rb1'] = -2
                ECG_baseline_new.at[i, 'rb2'] = -2
            elif condition == "LOF" and session == "LOF":
                ECG_baseline_new.at[i, 'rb3'] = -2
                ECG_baseline_new.at[i, 'rb4'] = -2

            i = i + 1

        ECG_baseline_new.to_csv('ECG_baseline_new.csv', index=False)

        ###########################################

        import pandas as pd

        rawdata_order2 = 'ECG_batch.csv'
        ECG_batch = pd.read_csv(rawdata_order2, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        i = 0
        for index, row in ECG_batch.iterrows():
            # print(index, row)
            # print (row)
            output_removed = ECG_batch.at[i, 'experiment']

            # output_removed = output_removed.replace('output_', '')
            # output_removed = output_removed[7:11]

            if isNaN(output_removed):
                print (output_removed)
            else:
                output_removed = output_removed.replace('output_', '')
                output_removed = int(output_removed)

            #     print (output_removed)

            ECG_batch.at[i, 'experiment'] = output_removed

            #         ECG_baseline.at[i,'session'] ="LOF"
            #     print (row)
            i = i + 1

        ECG_batch.to_csv('ECG_batch_new.csv', index=False)
    def merge_everything():
        import pandas as pd
        import numpy as np

        rawdata_order2 = 'ECG_baseline_new.csv'
        batch_BASELINE = pd.read_csv(rawdata_order2, sep=',')
        # print batch_LEGO_LOF.iloc[0]["experiment"]

        # print batch_LEGO_LOF

        rawdata_order3 = 'ECG_batch_new.csv'
        batch_LEGO_LOF = pd.read_csv(rawdata_order3, sep=',')

        batch_LEGO_LOF.rename(columns={'condition': 'session'},
                              inplace=True)

        batch_LEGO_LOF.set_index(['experiment', 'participant', 'session', 'feature'])

        batch_BASELINE.set_index(['experiment', 'participant', 'session', 'feature'])

        result = pd.merge(batch_LEGO_LOF, batch_BASELINE, on=['experiment', 'participant', 'session', 'feature'])
        result.to_csv('AAAAout4.csv', index=False)

        dataset_name = 'AAAAout4.csv'
        merged = pd.read_csv(dataset_name, sep=',')

        ECG_baseline_new = merged

        i = 0
        for index, row in ECG_baseline_new.iterrows():
            # print(index, row)
            # print (row)

            if ECG_baseline_new.at[i, 'rb1'] == -2:
                ECG_baseline_new.at[i, 'rb1'] = ECG_baseline_new.at[i, 'rb3']
                ECG_baseline_new.at[i, 'rb2'] = ECG_baseline_new.at[i, 'rb4']
            else:
                print ("ok")

            i = i + 1

        ECG_baseline_new = ECG_baseline_new.drop(columns=['rb3', 'rb4'], axis=1)

        ECG_baseline_new = ECG_baseline_new.replace(-1, np.nan)

        ECG_baseline_new.to_csv('ALL_ECG.csv', index=False)

    create_new_baseline()
    merge_everything()

#15 MERGE ECG BATCH & EDA BATCH
def merge_ECG_EDA():
    os.chdir(output_directory_path + folder25 + "/0013_ALL_EDA_ECG_MERGED")

    src_file = output_directory_path + folder25 + "/0010_ALL_EDA_MERGED/ALL_EDA.csv"
    dst_file = output_directory_path + folder25 + "/0013_ALL_EDA_ECG_MERGED"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path + folder25 + "/0011_ALL_ECG_MERGED/ALL_ECG.csv"
    dst_file = output_directory_path + folder25 + "/0013_ALL_EDA_ECG_MERGED"
    shutil.copy(src_file, dst_file)

    ALL_ECG = pd.read_csv('ALL_ECG.csv', sep=',')
    ALL_EDA = pd.read_csv('ALL_EDA.csv', sep=',')

    def merged_session(which_part,ALL_DATA,player):



        if player == "ASC":
            ALL_DATA = ALL_DATA[ALL_DATA.participant != 44]
            value_player =55
        elif player == "NONASC":
            ALL_DATA = ALL_DATA[ALL_DATA.participant != 55]
            value_player = 44

        if which_part == 'total':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","b1","b2","break","rb1","rb2"], axis=1)
        if which_part == 'first5':
            ALL_DATA = ALL_DATA.drop(columns=['total',"mid5","last5","b1","b2","break","rb1","rb2"], axis=1)
        if which_part == 'mid5':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"total","last5","b1","b2","break","rb1","rb2"], axis=1)
        if which_part == 'last5':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","total","b1","b2","break","rb1","rb2"], axis=1)
        if which_part == 'b1':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","total","b2","break","rb1","rb2"], axis=1)
        if which_part == 'b2':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","b1","total","break","rb1","rb2"], axis=1)
        if which_part == 'break':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","b1","b2","total","rb1","rb2"], axis=1)
        if which_part == 'rb1':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","b1","b2","break","total","rb2"], axis=1)
        if which_part == 'rb2':
            ALL_DATA = ALL_DATA.drop(columns=['first5',"mid5","last5","b1","b2","break","rb1","total"], axis=1)


        ALL_DATA_LOF = ALL_DATA[ALL_DATA.session != "LEGO"]
        ALL_DATA_LOF = ALL_DATA_LOF.drop(columns=['session'], axis=1)

        ALL_DATA_LEGO = ALL_DATA[ALL_DATA.session != "LOF"]
        ALL_DATA_LEGO = ALL_DATA_LEGO.drop(columns=['session'], axis=1)


        ALL_DATA_LOF = ALL_DATA_LOF.pivot(index='experiment', columns='feature', values=which_part)
        ALL_DATA_LOF.insert(loc=0, column='session', value="LOF")
        ALL_DATA_LOF.insert(loc=0, column='participant', value=value_player)

        ALL_DATA_LEGO = ALL_DATA_LEGO.pivot(index='experiment', columns='feature', values=which_part)
        ALL_DATA_LEGO.insert(loc=0, column='session', value="LEGO")
        ALL_DATA_LEGO.insert(loc=0, column='participant', value=value_player)

        ALL_DATA_new = pd.concat([ALL_DATA_LOF, ALL_DATA_LEGO])

        return ALL_DATA_new

    def merged_final(ALL_ECG_new,ALL_EDA_new,part_no,player_type):
        ALL_ECG_new = ALL_ECG_new.reset_index()
        ALL_EDA_new = ALL_EDA_new.reset_index()

        ALL_ECG_new.set_index(['experiment', 'participant', 'session'])
        ALL_EDA_new.set_index(['experiment', 'participant', 'session'])

        ALL_ECG_EDA = pd.merge(ALL_ECG_new, ALL_EDA_new, on=['experiment', 'participant', 'session'])

        ALL_ECG_EDA = ALL_ECG_EDA.drop(columns=['participant'], axis=1)

        ALL_ECG_EDA.insert(1, 'participant', player_type)
        ALL_ECG_EDA.insert(3, 'phase', part_no)

        return ALL_ECG_EDA

    def merged_final_final(ALL_ECG,ALL_EDA,player_type):
        ALL_ECG_new = merged_session("total", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("total", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_total = merged_final(ALL_ECG_new, ALL_EDA_new, "total", player_type)

        ALL_ECG_new = merged_session("first5", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("first5", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_first5 = merged_final(ALL_ECG_new, ALL_EDA_new, "first5", player_type)

        ALL_ECG_new = merged_session("mid5", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("mid5", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_mid5 = merged_final(ALL_ECG_new, ALL_EDA_new, "mid5", player_type)

        ALL_ECG_new = merged_session("last5", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("last5", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_last5 = merged_final(ALL_ECG_new, ALL_EDA_new, "last5", player_type)

        ALL_ECG_new = merged_session("b1", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("b1", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_b1 = merged_final(ALL_ECG_new, ALL_EDA_new, "b1", player_type)

        ALL_ECG_new = merged_session("b2", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("b2", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_b2 = merged_final(ALL_ECG_new, ALL_EDA_new, "b2", player_type)

        ALL_ECG_new = merged_session("break", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("break", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_break = merged_final(ALL_ECG_new, ALL_EDA_new, "break", player_type)

        ALL_ECG_new = merged_session("rb1", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("rb1", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_rb1 = merged_final(ALL_ECG_new, ALL_EDA_new, "rb1", player_type)

        ALL_ECG_new = merged_session("rb2", ALL_ECG, player_type)
        ALL_EDA_new = merged_session("rb2", ALL_EDA, player_type)
        ALL_ECG_EDA_ASC_rb2 = merged_final(ALL_ECG_new, ALL_EDA_new, "rb2", player_type)


        ALL_ECG_EDA_full = pd.concat([ALL_ECG_EDA_ASC_total, ALL_ECG_EDA_ASC_first5,ALL_ECG_EDA_ASC_mid5,
                                 ALL_ECG_EDA_ASC_last5,ALL_ECG_EDA_ASC_b1,ALL_ECG_EDA_ASC_b2,
                                 ALL_ECG_EDA_ASC_break,ALL_ECG_EDA_ASC_rb1,ALL_ECG_EDA_ASC_rb2])

        return ALL_ECG_EDA_full

    ALL_ECG_EDA_full_ASC = merged_final_final(ALL_ECG, ALL_EDA, "ASC")
    ALL_ECG_EDA_full_NONASC = merged_final_final(ALL_ECG, ALL_EDA, "NONASC")

    ALL_ECG_EDA_full_ASC_NONASC = pd.concat([ALL_ECG_EDA_full_ASC,ALL_ECG_EDA_full_NONASC])

    ALL_ECG_EDA_full_ASC_NONASC.to_csv("ALL_ECG_EDA_ASC_NONASC"  + ".csv", index=False)

#16 create Multilevel dataframe
def create_multilevel_dataframe():
    os.chdir(output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED")

    src_file = output_directory_path +"/0008-VIDEO-CODING/all_features_video_coding_ASC.txt"
    dst_file = output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"/0008-VIDEO-CODING - NONASC/all_features_video_coding_NONASC.txt"
    dst_file = output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED"
    shutil.copy(src_file, dst_file)

    video_coding_ASC = pd.read_csv("all_features_video_coding_ASC.txt")
    video_coding_NONASC = pd.read_csv("all_features_video_coding_NONASC.txt")


    video_coding_ASC.columns = ["experiment", "participant", "condition", "interaction","first5","last5","mid5"]
    video_coding_NONASC.columns = ["experiment", "participant", "condition", "interaction","first5","last5","mid5"]
    video_coding_ASC_NONASC = pd.concat([video_coding_ASC, video_coding_NONASC])


    video_coding_ASC_NONASC = video_coding_ASC_NONASC[video_coding_ASC_NONASC.experiment != "output_ "]

    def changetonumber(x):
        x = x[7:]
        x = int(x)
        return x

    def change_column(a):

        a.at[1, 4] = a.at[0, 4]
        a.at[1, 5] = a.at[0, 5]
        a.at[1, 6] = a.at[0, 6]
        a = a.drop([0])

        new_header = a.iloc[0]  # grab the first row for the header
        a = a[1:]  # take the data less the header row
        a.columns = new_header  # set the header row as the df header

        return a


    video_coding_ASC_NONASC["experiment"] = video_coding_ASC_NONASC["experiment"].apply(changetonumber)
    video_coding_ASC_NONASC = video_coding_ASC_NONASC.replace(-1, 0)
    video_coding_ASC_NONASC = video_coding_ASC_NONASC.replace(-2, 0)


    video_coding_ASC_NONASC.loc[video_coding_ASC_NONASC.participant == 44, "participant"] = "NONASC"
    video_coding_ASC_NONASC.loc[video_coding_ASC_NONASC.participant == 55, "participant"] = "ASC"



    #video_coding_ASC_NONASC.fillna(0, inplace=True)
    # video_coding_ASC_NONASC.replace(video_coding_ASC_NONASC.isnull().values == True, 0, inplace=True)
    # print video_coding_ASC_NONASC.isnull().values

    video_coding_ASC_NONASC["total"] = video_coding_ASC_NONASC["first5"] +  video_coding_ASC_NONASC["last5"]

    video_coding_ASC_NONASC = video_coding_ASC_NONASC.melt(['experiment', 'participant',"condition","interaction"], var_name='phase',value_name='value')

    video_coding_ASC_NONASC = video_coding_ASC_NONASC[['experiment', 'participant',"condition",'phase',"interaction",'value']]

    table = pd.pivot_table(video_coding_ASC_NONASC, index=['experiment', 'participant',"condition","phase"], columns="interaction",values=["value"])



    table.to_csv("video_coding_ASC_NONASC.csv")

    video_coding_ASC_NONASC= pd.read_csv("video_coding_ASC_NONASC.csv",skiprows=[0], header=None)
    video_coding_ASC_NONASC = change_column(video_coding_ASC_NONASC)


    video_coding_ASC_NONASC.to_csv("video_coding_ASC_NONASC.csv", index = False)

#17 MERGE ECG BATCH & EDA BATCH with VIDEO CODING
def merge_ECG_EDA_video_coding():
    os.chdir(output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED")

    src_file = output_directory_path + folder25 + "/0013_ALL_EDA_ECG_MERGED/ALL_ECG_EDA_ASC_NONASC.csv"
    dst_file = output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED"
    shutil.copy(src_file, dst_file)


    video_coding_ASC_NONASC = pd.read_csv('video_coding_ASC_NONASC.csv')
    video_coding_ASC_NONASC = video_coding_ASC_NONASC.rename(columns={"condition": "session"})
    video_coding_ASC_NONASC.set_index(['experiment',"participant", 'session', 'phase' ])

    ALL_ECG_EDA_ASC_NONASC= pd.read_csv("ALL_ECG_EDA_ASC_NONASC.csv", sep=',')

    ALL_BATCH_MERGE = pd.merge(video_coding_ASC_NONASC,ALL_ECG_EDA_ASC_NONASC,on=['experiment',"participant", 'session', 'phase' ],how="outer")


    ALL_BATCH_MERGE.to_csv("ALL_ECG_EDA_ASC_NONASC_MULTILEVEL" + ".csv", index=False)

#18 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG
def merge_ECG_EDA_video_coding_systemlog():
    os.chdir(output_directory_path + folder25 + "/0016_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED")

    src_file = output_directory_path + folder25 + "/0015_ALL_EDA_ECG_VIDEO_MERGED/ALL_ECG_EDA_ASC_NONASC_MULTILEVEL.csv"
    dst_file = output_directory_path + folder25 + "/0016_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path + folder25 + "/0002_system_logging/systemlog_create_merged_dataframe.csv"
    dst_file = output_directory_path + folder25 + "/0016_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED"
    shutil.copy(src_file, dst_file)

    ALL_ECG_EDA_ASC_NONASC_MULTILEVEL = pd.read_csv('ALL_ECG_EDA_ASC_NONASC_MULTILEVEL.csv')
    systemlog_create_merged_dataframe = pd.read_csv('systemlog_create_merged_dataframe.csv')


    systemlog_create_merged_dataframe.set_index(['experiment',"participant", 'session', 'phase' ])
    ALL_ECG_EDA_ASC_NONASC_MULTILEVEL.set_index(['experiment',"participant", 'session', 'phase' ])

    ALL_BATCH_MERGE_W_SYSTEMLOG = pd.merge(ALL_ECG_EDA_ASC_NONASC_MULTILEVEL,systemlog_create_merged_dataframe,on=['experiment',"participant", 'session', 'phase' ],how="outer")


    ALL_BATCH_MERGE_W_SYSTEMLOG.to_csv("ALL_BATCH_MERGE_W_SYSTEMLOG" + ".csv", index=False)


    print ALL_BATCH_MERGE_W_SYSTEMLOG

#19 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG & ACC
def merge_ECG_EDA_video_coding_systemlog_acc():
    os.chdir(output_directory_path + folder25 + "/0017_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC")

    src_file = output_directory_path + folder25 + "/0016_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED/ALL_BATCH_MERGE_W_SYSTEMLOG.csv"
    dst_file = output_directory_path + folder25 + "/0017_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path + folder25 + "/0004_ACC/allfeatures_eda_ACC_processed.csv"
    dst_file = output_directory_path + folder25 + "/0017_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC"
    shutil.copy(src_file, dst_file)

    ALL_BATCH_MERGE_W_SYSTEMLOG = pd.read_csv('ALL_BATCH_MERGE_W_SYSTEMLOG.csv')
    allfeatures_eda_ACC_processed = pd.read_csv('allfeatures_eda_ACC_processed.csv',skiprows=[0], header=None)

    def changetonumber(x):
        x = x[7:]
        x = int(x)
        return x

    def change_column(a):

        a.at[1, 4] = a.at[0, 4]
        a.at[1, 5] = a.at[0, 5]
        a.at[1, 6] = a.at[0, 6]
        a.at[1, 7] = a.at[0, 7]
        a = a.drop([0])

        new_header = a.iloc[0]  # grab the first row for the header
        a = a[1:]  # take the data less the header row
        a.columns = new_header  # set the header row as the df header

        return a

    allfeatures_eda_ACC_processed = change_column(allfeatures_eda_ACC_processed)

    allfeatures_eda_ACC_processed.loc[allfeatures_eda_ACC_processed.participant == "44", "participant"] = "NONASC"
    allfeatures_eda_ACC_processed.loc[allfeatures_eda_ACC_processed.participant == "55", "participant"] = "ASC"
    # allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed.replace(-1.0, 0)
    # allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed.replace(-2.0, 0)


    allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed[allfeatures_eda_ACC_processed.feature=="Step_count"]


    allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed.melt(['experiment', 'participant',"session","feature"], var_name='phase',value_name='step_count')
    allfeatures_eda_ACC_processed=allfeatures_eda_ACC_processed.drop(columns=['feature'])

    allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed[allfeatures_eda_ACC_processed.experiment != "35"]
    allfeatures_eda_ACC_processed = allfeatures_eda_ACC_processed[allfeatures_eda_ACC_processed.experiment != "36"]

    allfeatures_eda_ACC_processed.to_csv("allfeatures_eda_ACC_processed_new.csv", index = False)
    allfeatures_eda_ACC_processed = pd.read_csv('allfeatures_eda_ACC_processed_new.csv')

    allfeatures_eda_ACC_processed.set_index(['experiment',"participant", 'session', 'phase' ])
    ALL_BATCH_MERGE_W_SYSTEMLOG.set_index(['experiment',"participant", 'session', 'phase' ])
    #
    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC = pd.merge(ALL_BATCH_MERGE_W_SYSTEMLOG,allfeatures_eda_ACC_processed,on=['experiment',"participant", 'session', 'phase' ],how="outer")
    #
    #
    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC.to_csv("ALL_BATCH_MERGE_W_SYSTEMLOG_ACC" + ".csv", index=False)

#20 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG & ACC
def create_questionnaire_dataframe():
    os.chdir(qst_output_destination+"Questionnaires")

    arousal_AS_ASC = pd.read_csv('arousal_AS_ASC.csv')
    arousal_AS_TDC =pd.read_csv('arousal_AS_TDC.csv')
    desiretoknowmore_ASC = pd.read_csv('desiretoknowmore_ASC.csv')
    desiretoknowmore_TDC = pd.read_csv('desiretoknowmore_TDC.csv')
    social_status_ASC = pd.read_csv('social_status_ASC.csv')
    social_status_TDC = pd.read_csv('social_status_TDC.csv')
    valence_AS_ASC = pd.read_csv('valence_AS_ASC.csv')
    valence_AS_TDC = pd.read_csv('valence_AS_TDC.csv')
    staic_ASC =pd.read_csv('staic_ASC.csv')
    staic_TDC = pd.read_csv('staic_TDC.csv')

    def change_structure(dataframe,participant,type):

        pre_type = "pre_" + type
        post_type = "post_" + type

        columns = ["experiment","participant","session",'phase',pre_type,post_type]

        df_ = pd.DataFrame(index=dataframe.index, columns=columns)
        df_.experiment = dataframe.trial_no
        df_.participant = participant
        df_.phase = "total"
        df_.session = "LEGO"
        df_[pre_type] = dataframe.pre_LEGO
        df_[post_type] = dataframe.post_LEGO

        df_2 = pd.DataFrame(index=dataframe.index, columns=columns)
        df_2.experiment = dataframe.trial_no
        df_2.participant = participant
        df_2.phase = "total"
        df_2.session = "LOF"
        df_2[pre_type] = dataframe.pre_LOF
        df_2[post_type] = dataframe.post_LOF

        concatted_qst = pd.concat([df_, df_2])


        print concatted_qst # with 0s rather than NaNs
        return concatted_qst

    arousal_AS_ASC= change_structure(arousal_AS_ASC,"ASC","arousal_level")
    arousal_AS_TDC =change_structure(arousal_AS_TDC,"NONASC","arousal_level")
    concatted_arousal = pd.concat([arousal_AS_ASC, arousal_AS_TDC])
    concatted_arousal.set_index(['experiment', "participant", 'session', 'phase'])

    desiretoknowmore_ASC = change_structure(desiretoknowmore_ASC,"ASC","desire_to_know_more")
    desiretoknowmore_TDC = change_structure(desiretoknowmore_TDC,"NONASC","desire_to_know_more")
    concatted_desiretoknowmore = pd.concat([desiretoknowmore_ASC, desiretoknowmore_TDC])
    concatted_desiretoknowmore.set_index(['experiment', "participant", 'session', 'phase'])

    social_status_ASC = change_structure(social_status_ASC,"ASC","social_status")
    social_status_TDC = change_structure(social_status_TDC,"NONASC","social_status")
    concatted_social_status = pd.concat([social_status_ASC, social_status_TDC])
    concatted_social_status.set_index(['experiment', "participant", 'session', 'phase'])

    valence_AS_ASC = change_structure(valence_AS_ASC,"ASC","valence_level")
    valence_AS_TDC = change_structure(valence_AS_TDC,"NONASC","valence_level")
    concatted_valence = pd.concat([valence_AS_ASC, valence_AS_TDC])
    concatted_valence.set_index(['experiment', "participant", 'session', 'phase'])

    staic_ASC = change_structure(staic_ASC,"ASC","staic_level")
    staic_TDC = change_structure(staic_TDC,"NONASC","staic_level")
    concatted_staic = pd.concat([staic_ASC, staic_TDC])
    concatted_staic.set_index(['experiment', "participant", 'session', 'phase'])


    #
    ALL_QST_MERGE = pd.merge(concatted_arousal,concatted_desiretoknowmore,on=['experiment',"participant", 'session', 'phase' ],how="outer")
    ALL_QST_MERGE = pd.merge(ALL_QST_MERGE, concatted_social_status,
                             on=['experiment', "participant", 'session', 'phase'], how="outer")
    ALL_QST_MERGE = pd.merge(ALL_QST_MERGE, concatted_valence,
                             on=['experiment', "participant", 'session', 'phase'], how="outer")
    ALL_QST_MERGE = pd.merge(ALL_QST_MERGE, concatted_staic,
                             on=['experiment', "participant", 'session', 'phase'], how="outer")
    #
    ALL_QST_MERGE.to_csv("ALL_QST_MERGE.csv", index = False)

def merge_ECG_EDA_video_coding_systemlog_acc_qst():
    os.chdir(output_directory_path + folder25 + "/0018_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC_QST")

    src_file = output_directory_path + folder25 + "/0017_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC/ALL_BATCH_MERGE_W_SYSTEMLOG_ACC.csv"
    dst_file = output_directory_path + folder25 + "/0018_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC_QST"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path + "/0009-Questionnaires/Questionnaires/ALL_QST_MERGE.csv"
    dst_file = output_directory_path + folder25 + "/0018_ALL_EDA_ECG_VIDEO_SYSTEM_MERGED_ACC_QST"
    shutil.copy(src_file, dst_file)

    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC = pd.read_csv('ALL_BATCH_MERGE_W_SYSTEMLOG_ACC.csv')
    ALL_QST_MERGE = pd.read_csv('ALL_QST_MERGE.csv')

    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC.set_index(['experiment',"participant", 'session', 'phase' ])
    ALL_QST_MERGE.set_index(['experiment',"participant", 'session', 'phase'])

    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST = pd.merge(ALL_BATCH_MERGE_W_SYSTEMLOG_ACC, ALL_QST_MERGE,
                                               on=['experiment', "participant", 'session', 'phase'], how="outer")
    #
    #
    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST = ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST.drop(columns=["pre_staic_level"])
    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST["staic_level"] = ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST["post_staic_level"]
    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST = ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST.drop(columns=["post_staic_level"])

    ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST.to_csv("ALL_BATCH_MERGE_W_SYSTEMLOG_ACC_QST" + ".csv", index=False)

def EDA_preperation():

    ###################EDA PREPERATION

    os.chdir(output_directory_path)
    createFolder("0021_EDA_ECG_EVENT_allignment")

    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_SYSTEM_EVENT_MARKED.csv"
    dst_file = output_directory_path + "/0021_EDA_ECG_EVENT_allignment"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"0015_OUTPUT/allfeatures_eda_VIDEO_EVENT_MARKED.csv"
    dst_file = output_directory_path + "/0021_EDA_ECG_EVENT_allignment"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path+ "/0021_EDA_ECG_EVENT_allignment")

    rawdata_order2 = 'allfeatures_eda_SYSTEM_EVENT_MARKED.csv'
    system = pd.read_csv(rawdata_order2, sep=',')

    rawdata_order3 = 'allfeatures_eda_VIDEO_EVENT_MARKED.csv'
    video = pd.read_csv(rawdata_order3, sep=',')

    frames = [system, video]
    result = pd.concat(frames)
    result  = result.drop(result.columns[0], axis=1)

    result.to_csv('allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED_MANUAL.csv',index = False)

    os.chdir(output_directory_path+ "RESULT")
    createFolder("0003_EDA_and_SystemLog")

    src_file = output_directory_path +"0021_EDA_ECG_EVENT_allignment/allfeatures_eda_SYSTEM_EVENT_MARKED.csv"
    dst_file = output_directory_path +"/RESULT" +"/0003_EDA_and_SystemLog"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"0021_EDA_ECG_EVENT_allignment/allfeatures_eda_VIDEO_EVENT_MARKED.csv"
    dst_file = output_directory_path +"RESULT" +"/0003_EDA_and_SystemLog"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"0021_EDA_ECG_EVENT_allignment/allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED_MANUAL.csv"
    dst_file = output_directory_path +"RESULT" +"/0003_EDA_and_SystemLog"
    shutil.copy(src_file, dst_file)

    shutil.rmtree(output_directory_path + "0021_EDA_ECG_EVENT_allignment")

    os.chdir(output_directory_path + "RESULT")
    createFolder("0019_baseline_batch_merging - Event Based")

    src_file = output_directory_path +"RESULT" +"/0003_EDA_and_SystemLog/allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED_MANUAL.csv"
    dst_file = output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"experiment_order.csv"
    dst_file = output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based"
    shutil.copy(src_file, dst_file)

    # src_file = output_directory_path +"RESULT"+"/0006_EDA_and_Baseline/allfeatures_eda_batch_BASELINE_MERGED_OUTLIERS_CLEANED.csv"
    # dst_file = output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based"
    # shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"RESULT"+"/0010_ALL_EDA_MERGED/EDA_baseline_new.csv"
    dst_file = output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based")

    def eda_baseline_batch_dataset_merger_event_based_new2():
        # rawdata_order = 'experiment_order.csv'
        # order = pd.read_csv(rawdata_order, sep=',')
        #
        # rawdata_order2 = 'allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED_MANUAL.csv'
        # batch_LEGO_LOF = pd.read_csv(rawdata_order2, sep=',')
        #
        #
        # rawdata_order3 = 'allfeatures_eda_batch_BASELINE_MERGED_OUTLIERS_CLEANED.csv'
        # batch_BASELINE = pd.read_csv(rawdata_order3, sep=',')
        #
        #
        #
        #
        # batch_LEGO_LOF.set_index(['experiment', 'participant', 'feature'])
        #
        # batch_BASELINE.set_index(['experiment', 'participant', 'feature'])
        #
        #
        # result = pd.merge(batch_LEGO_LOF, batch_BASELINE, on=['experiment', 'participant', 'feature'])

        EDA_baseline_new = pd.read_csv('EDA_baseline_new.csv')
        EDA_event_marked = pd.read_csv('allfeatures_eda_VIDEO_SYSTEM_EVENT_MARKED_MANUAL.csv')

        # print table2

        #

        EDA_baseline_new.set_index(['experiment', 'participant', 'feature'])

        EDA_event_marked.set_index(['experiment', 'participant', 'feature'])

        result = pd.merge(EDA_event_marked, EDA_baseline_new, on=['experiment', 'participant', "session", 'feature'])

        ########organize baseline

        def organize_baseline(merged):
            ECG_baseline_new = merged

            i = 0
            for index, row in ECG_baseline_new.iterrows():
                # print(index, row)
                # print (row)

                if ECG_baseline_new.at[i, 'rb1'] == -2:
                    ECG_baseline_new.at[i, 'rb1'] = ECG_baseline_new.at[i, 'rb3']
                    ECG_baseline_new.at[i, 'rb2'] = ECG_baseline_new.at[i, 'rb4']
                else:
                    print ("ok")

                i = i + 1

            ECG_baseline_new = ECG_baseline_new.drop(columns=['rb3', 'rb4'], axis=1)

            ECG_baseline_new = ECG_baseline_new.replace(-1, np.nan)

            return ECG_baseline_new

        result = organize_baseline(result)

        def phased_EDA_baseline_data(LAST_ECG):

            LAST_ECG = pd.melt(LAST_ECG,
                               id_vars=['experiment', 'participant', "session", 'feature', 'part', 'no', 'event_no'],
                               value_vars=['value', 'b1', 'b2', 'break', 'rb1', 'rb2'])

            LAST_ECG_copy = LAST_ECG[LAST_ECG.variable == "value"]
            LAST_ECG = LAST_ECG[LAST_ECG.variable != "value"]

            LAST_ECG_copy = LAST_ECG_copy.drop(columns=["variable"], axis=1)
            print LAST_ECG_copy.columns

            LAST_ECG = LAST_ECG.drop(columns=['no', 'event_no', "part"], axis=1)
            LAST_ECG = LAST_ECG.drop_duplicates()

            LAST_ECG = LAST_ECG.rename(columns={'variable': 'part'})

            LAST_ECG.insert(loc=5, column="event_no", value=99)
            LAST_ECG.insert(loc=5, column="no", value=99)

            LAST_ECG_new = pd.concat([LAST_ECG_copy, LAST_ECG])
            print LAST_ECG.columns

            return LAST_ECG_new

        result = phased_EDA_baseline_data(result)


        result.to_csv('LAST_EDA.csv',index=False)

    eda_baseline_batch_dataset_merger_event_based_new2()

    os.chdir(output_directory_path + "RESULT")

    createFolder("0010_ALL_EDA_MERGED_EVENT")

    src_file = output_directory_path +"RESULT"+"/0019_baseline_batch_merging - Event Based/LAST_EDA.csv"
    dst_file = output_directory_path +"RESULT" +"/0010_ALL_EDA_MERGED_EVENT"
    shutil.copy(src_file, dst_file)

    shutil.rmtree(output_directory_path +"RESULT" +"/0019_baseline_batch_merging - Event Based")
def ECG_preperation():


    ###################ECG PREPERATION

    createFolder("0011_ALL_ECG_MERGED_EVENT")

    src_file = output_directory_path +"RESULT"+"/0009_ECG_and_VideoLog/ALL_allfeatures_(HRV)_extracted_features_EVENT_batu.txt"
    dst_file = output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED_EVENT"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED_EVENT")

    filehandle = open('HRV_extracted_features_EVENT.txt', 'w')
    filehandle.write(';;;;;;;;;;;;\n')
    filehandle.close()

    f1 = open('HRV_extracted_features_EVENT.txt', 'a+')
    f2 = open("ALL_allfeatures_(HRV)_extracted_features_EVENT_batu.txt", 'r')

    f1.write(f2.read())

    HRV_extracted_features_EVENT = pd.read_csv("HRV_extracted_features_EVENT.txt", sep = ";")
    HRV_extracted_features_EVENT.columns = ["experiment", "participant", "session", "feature","part","no","event_no","value","empty2","empty3","empty4","empty5","empty6"]
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.drop(["empty2"], axis=1)
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.drop(["empty3"], axis=1)
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.drop(["empty4"], axis=1)
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.drop(["empty5"], axis=1)
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.drop(["empty6"], axis=1)

    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT.sort_values(by=['experiment', 'participant', "session", 'feature',"part",'no','event_no'])
    HRV_extracted_features_EVENT.fillna(-1, inplace=True)
    HRV_extracted_features_EVENT = HRV_extracted_features_EVENT[HRV_extracted_features_EVENT.part != -1]

    def changetonumber(x):
        x = x[7:]
        x = int(x)
        return x

    HRV_extracted_features_EVENT["experiment"] = HRV_extracted_features_EVENT["experiment"].apply(changetonumber)

    HRV_extracted_features_EVENT.loc[(HRV_extracted_features_EVENT.part == 'first'), 'part'] = 'first5'
    HRV_extracted_features_EVENT.loc[(HRV_extracted_features_EVENT.part == 'mid'), 'part'] = 'mid5'
    HRV_extracted_features_EVENT.loc[(HRV_extracted_features_EVENT.part == 'last'), 'part'] = 'last5'

    #HRV_extracted_features_EVENT.to_csv("teste.csv",  index=False)
    #HRV_extracted_features_EVENT.to_csv("ALL_allfeatures_(HRV)_extracted_features_EVENT_batu_eventno_updated_wtab.txt",sep="\t", index = False)
    HRV_extracted_features_EVENT.to_csv("ALL_allfeatures_(HRV)_extracted_features_EVENT_batu_eventno_updated_wtab.csv", index=False)

    src_file = output_directory_path +"experiment_order.csv"
    dst_file = output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED_EVENT"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED/ECG_baseline_new.csv"
    dst_file = output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED_EVENT"
    shutil.copy(src_file, dst_file)

    #######

    event_BASELINE = pd.read_csv('ECG_baseline_new.csv', sep=',')

    event_LEGO_LOF = pd.read_csv('ALL_allfeatures_(HRV)_extracted_features_EVENT_batu_eventno_updated_wtab.csv', sep=',')

    event_LEGO_LOF.set_index(['experiment', 'participant', 'session', 'feature'])

    event_BASELINE.set_index(['experiment', 'participant', 'session', 'feature'])



    result = pd.merge(event_LEGO_LOF, event_BASELINE, on=['experiment', 'participant', 'session', 'feature'])

    def organize_baseline(merged):
        ECG_baseline_new = merged

        i = 0
        for index, row in ECG_baseline_new.iterrows():
            # print(index, row)
            # print (row)

            if ECG_baseline_new.at[i, 'rb1'] == -2:
                ECG_baseline_new.at[i, 'rb1'] = ECG_baseline_new.at[i, 'rb3']
                ECG_baseline_new.at[i, 'rb2'] = ECG_baseline_new.at[i, 'rb4']
            else:
                print ("ok")

            i = i + 1

        ECG_baseline_new = ECG_baseline_new.drop(columns=['rb3', 'rb4'], axis=1)

        ECG_baseline_new = ECG_baseline_new.replace(-1, np.nan)

        return ECG_baseline_new

    result = organize_baseline(result)

    def phased_ECG_baseline_data(LAST_ECG):


        LAST_ECG = pd.melt(LAST_ECG,
                           id_vars=['experiment', 'participant', "session", 'feature', 'part', 'no', 'event_no'],
                           value_vars=['value', 'b1', 'b2', 'break', 'rb1', 'rb2'])

        LAST_ECG_copy = LAST_ECG[LAST_ECG.variable == "value"]
        LAST_ECG = LAST_ECG[LAST_ECG.variable != "value"]

        LAST_ECG_copy = LAST_ECG_copy.drop(columns=["variable"], axis=1)
        print LAST_ECG_copy.columns

        LAST_ECG = LAST_ECG.drop(columns=['no', 'event_no', "part"], axis=1)
        LAST_ECG = LAST_ECG.drop_duplicates()

        LAST_ECG = LAST_ECG.rename(columns={'variable': 'part'})

        LAST_ECG.insert(loc=5, column="event_no", value=99)
        LAST_ECG.insert(loc=5, column="no", value=99)

        LAST_ECG_new = pd.concat([LAST_ECG_copy, LAST_ECG])
        print LAST_ECG.columns



        return LAST_ECG_new

    result = phased_ECG_baseline_data(result)

    result.to_csv('LAST_ECG.csv',index=False)
def eda_ecg_event_allignment():
    EDA_preperation()
    ECG_preperation()

    ######0012_MERGE_EVENT

    os.chdir(output_directory_path +"RESULT")
    createFolder("0012_MERGE_EVENT")

    src_file = output_directory_path +"RESULT" +"/0011_ALL_ECG_MERGED_EVENT/LAST_ECG.csv"
    dst_file = output_directory_path +"RESULT" +"/0012_MERGE_EVENT"
    shutil.copy(src_file, dst_file)

    src_file = output_directory_path +"RESULT" +"/0010_ALL_EDA_MERGED_EVENT/LAST_EDA.csv"
    dst_file = output_directory_path +"RESULT" +"/0012_MERGE_EVENT"
    shutil.copy(src_file, dst_file)

    os.chdir(output_directory_path + "RESULT"+ "/0012_MERGE_EVENT")

    rawdata_order2 = 'LAST_EDA.csv'
    EDA = pd.read_csv(rawdata_order2, sep=',')
    EDA_WEKA = EDA.pivot_table(index=['experiment', 'participant', 'session', 'part', 'no', 'event_no'],
                               columns='feature', values='value')
    EDA_WEKA.to_csv('EDA_WEKA2.csv')
    #
    rawdata_order3 = 'LAST_ECG.csv'
    ECG = pd.read_csv(rawdata_order3, sep=',')
    ECG_WEKA = ECG.pivot_table(index=['experiment', 'participant', 'session', 'part', 'no', 'event_no'],
                               columns='feature', values='value')
    ECG_WEKA.to_csv('ECG_WEKA2.csv')

    rawdata_order4 = 'EDA_WEKA2.csv'
    EDA_WEKA = pd.read_csv(rawdata_order4, sep=',')

    rawdata_order5 = 'ECG_WEKA2.csv'
    ECG_WEKA = pd.read_csv(rawdata_order5, sep=',')
    #
    #
    EDA_WEKA.set_index(['experiment', 'participant', 'session', 'part', 'no', 'event_no'])
    print EDA_WEKA
    # #
    ECG_WEKA.set_index(['experiment', 'participant', 'session', 'part', 'no', 'event_no'])
    print ECG_WEKA
    # #
    #
    result = pd.merge(EDA_WEKA, ECG_WEKA, on=['experiment', 'participant', 'session', 'part', 'no', 'event_no'],
                      how='outer')

    result = result[result.event_no != 22]
    result.loc[result.participant == 44, "participant"] = "NONASC"
    result.loc[result.participant == 55, "participant"] = "ASC"
    result = result.rename(columns={'event_no': 'event_type'})
    result = result.rename(columns={'no': 'event_no'})
    result = result.rename(columns={'part': 'phase'})

    result.to_csv('MERGED_EVENTS.csv',index=False)

######################################################BATCH BASED ANALYSIS STARTS

# 10--------- ECG manual processing  & Manuel artifact correction

move_processeddata_out_for_processeing()

####################################EVENT BASED
datafolder_preparation_ECG()
ECG_feature_extraction()
move_folders()
merge_results_ECG()
####################################BATCH BASED
one_preprocessing_LEGO_LOF_HRV_feature_extraction()
second_preprocessing_BASELINE_HRV_feature_extraction()
third_preprocessing_LEGO_LOF_HRV_all_feature_dataset_MERGE_ALL()
third_preprocessing_LEGO_LOF_HRV_all_feature_dataset_MERGE_BASELINE()
transpose_baseline2()

# #11--------- extract features from preprocessed data & create dataframes accordingly
a = numberofexperiments
numberofexperiments = numberofexperiments + 2
eda_video_code_marked_feature_extraction_all(numberofexperiments)
eda_system_log_marked_feature_extraction_all(numberofexperiments)
eda_video_code_system_log_marked_feature_extraction_all(numberofexperiments)
acc_feature_extraction_wtotal(numberofexperiments)
eda_feature_extraction(numberofexperiments)
eda_feature_extraction_baseline(numberofexperiments)
eda_feature_extraction_baseline_break(numberofexperiments)
eda_feature_extraction_wtotal(numberofexperiments)
numberofexperiments = a


#12 RESULT FOLDER
create_result_folder()

# system log create merged dataframe
systemlog_create_merged_dataframe()

#13 MERGE EDA BATCH with BASELINE
merge_EDA_baselines()
merge_EDA_batch()
merge_EDA_batch_baseline()

#14 MERGE ECG BATCH with BASELINE
merge_ECG_baselines()
merge_ECG_batch()
merge_ECG_batch_baseline()

#15 MERGE ECG BATCH & EDA BATCH#
merge_ECG_EDA()

#16 create multilevel dataframe
create_multilevel_dataframe()

#17 MERGE ECG BATCH & EDA BATCH with VIDEO CODING
merge_ECG_EDA_video_coding()

#18 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG
merge_ECG_EDA_video_coding_systemlog()

#19 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG & ACC
merge_ECG_EDA_video_coding_systemlog_acc()

#20 MERGE ECG BATCH & EDA BATCH & VIDEO CODING & SYSTEM LOG & ACC
create_questionnaire_dataframe()
merge_ECG_EDA_video_coding_systemlog_acc_qst()

######################################################EVENT BASED ANALYSIS STARTS

# EVENT BASED ANALYSIS
eda_ecg_event_allignment()

move_processeddata_out_for_processeing_back()
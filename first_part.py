from pylab import *
import csv
import xlrd
from shutil import copyfile
import numpy as np
import pandas as pd
import scipy.signal as scisig
import os
from test_load_files import getInputLoadFile, getOutputPath
import shutil

enter_directory_path = "C:/Users/ascmeor/Desktop/"

# parameter definitions
input_folder_name="ASCMEOR DATASET TEST/"
output_folder_name= "ASCMEOR DATASET TEST OUTPUT/"
input_directory_path = enter_directory_path + input_folder_name
output_directory_path = enter_directory_path + output_folder_name
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
####

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
def datafolder_preparation():
    os.chdir(input_directory_path)
    ###stage 1 folders
    createFolder(input_directory_path+folder1)
    createFolder(input_directory_path+folder2)
    createFolder(input_directory_path+folder3)
    createFolder(input_directory_path+folder4)
    createFolder(input_directory_path+folder5)
    createFolder(input_directory_path+folder6)
    createFolder(input_directory_path+folder7)
    createFolder(input_directory_path+folder8)
    createFolder(input_directory_path+folder9)
    #stage 2 folders
    createFolder(input_directory_path + folder10)
    createFolder(input_directory_path + folder11)
    createFolder(input_directory_path + folder12)
    createFolder(input_directory_path + folder13)
    createFolder(input_directory_path + folder14)
    createFolder(input_directory_path + folder15)
    #stage 3 folders
    copytree(video_code_input_destination_ASC, video_code_output_destination_ASC)
    copytree(video_code_input_destination_NONASC, video_code_output_destination_NONASC)
    #stage 4 folders
    copytree(system_log_input_destination , system_log_output_destination)
    # stage
    createFolder(input_directory_path + folder16)
    createFolder(input_directory_path + folder17)
    createFolder(input_directory_path + folder18)
    # stage
    createFolder(input_directory_path + folder19)

    #copy experimentorder files
    src_file = input_directory_path +"experiment_order.csv"
    dst_file = output_directory_path
    shutil.copy(src_file, dst_file)

    src_file = input_directory_path +"experiment_order_w_creature_v2.csv"
    dst_file = output_directory_path
    shutil.copy(src_file, dst_file)

    src_file = qst_input_destination
    dst_file = qst_output_destination
    shutil.copytree(src_file , dst_file)



#########stage 1
def clean_csv(directory_path):
    files_in_directory = os.listdir(directory_path)
    filtered_files = [file for file in files_in_directory if file.endswith("2_EDA.txt")]
    for file in filtered_files:
        path_to_file = os.path.join(directory_path, file)
        os.remove(path_to_file)
def clean_eda():
    list = []
    for x in os.listdir(physio_raw_data_path):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))



    os.chdir(physio_raw_data_path)

    for i in range(main_loop_start_count, numberofexperiments):

        if i == skipped_experiment - 1 or i == skipped_experiment2 - 1 or i == skipped_experiment3 - 1 or i == skipped_experiment4 - 1:
            continue
        else:
            # print(os.getcwd())

            os.chdir('./' + list[i])
            os.chdir('./' + 'ASD')  ################## MAIN ENTERANCE TO LEGO

            # to control the sessions which does not have 2nd session
            if i == experiment_number_which_doesnot_have_2nd_session - 1:
                flag_second_session_exist = 0
            else:
                flag_second_session_exist = 1

            # to control plux raw data delimeter issue
            if i + 1 <= 5:  # experiment 0005 and below 0004,0003, since before and after raw datas merged manually
                text_type = 2
            elif i + 1 > 5 and i + 1 <= 11:  # experiment 0011 and below 0010,0009, ....
                text_type = 0
            elif i + 1 > 11:  # experiment 0012 and above 0012,0013, ....
                text_type = 1

            if i <= 11:  # experiment 0011 and below 0010,0009, ....

                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')
                clean_csv('.')

                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')
                clean_csv('.')

                os.chdir(physio_raw_data_path)

                ########Function Calls-end



            elif i > 11:  # experiment 0012 and above 0012,0013, ....

                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')
                clean_csv('.')

                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')
                clean_csv('.')

                os.chdir(physio_raw_data_path)
                ########Function Calls-end

    print(os.getcwd())
    os.chdir('..')
def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    paths = filter(lambda x: x.endswith('.txt'),os.listdir('.'))
    return min(paths, key=os.path.getctime)
def data_import(text_type,rawdata_filename):

    if text_type == 2:

        data = pd.read_csv(rawdata_filename, sep=",")

        EDA = data.iloc[:, 2].values
        X = data.iloc[:, 3].values
        Y = data.iloc[:, 4].values
        Z = data.iloc[:, 5].values
        ECG = data.iloc[:, 6].values
        #
        # f = open(rawdata_filename, "r")
        # lines = f.readlines()
        # result = []
        # result2 = []
        # result3 = []
        # result4 = []
        # result5 = []
        # result6 = []
        #
        #
        #
        # for x in lines:
        #     a = re.split(',', x)
        #     result.append(a[1])
        #     result2.append(a[2])
        #     result3.append(a[3])
        #     result4.append(a[4])
        #     result5.append(a[5])
        # f.close()
        #
        # EDA = result2
        # X = result3
        # Y = result4
        # Z = result5
        # ECG = result6
        # # EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
        # #                                delimiter=',',
        # #                                skiprows=3)
    print rawdata_filename
    print text_type
    if text_type ==2:
        print 'text_type =2'
    elif text_type ==0:
        print 'text_type =0'
    ####use delimiter='\t' for experiments before ....

        data = pd.read_csv(rawdata_filename, sep="\t", skiprows=3)

        EDA = data.iloc[:, 2].values
        X = data.iloc[:, 3].values
        Y = data.iloc[:, 4].values
        Z = data.iloc[:, 5].values
        ECG = data.iloc[:, 6].values


        print "EDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        #EDA,X,Y,Z,ECG= np.loadtxt(rawdata_filename, usecols=(2,3,4,5,6),unpack=True, dtype=float, delimiter='\t', skiprows = 3)

        print EDA
    elif text_type==1:
    ####use delimiter=' ' for experiments after .... (0012-0016)

        data = pd.read_csv(rawdata_filename, sep=" ", skiprows=3)

        EDA = data.iloc[:, 2].values
        X = data.iloc[:, 3].values
        Y = data.iloc[:, 4].values
        Z = data.iloc[:, 5].values
        ECG = data.iloc[:, 6].values


        #EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float, delimiter=' ',
        #                           skiprows=3)

    return EDA,X,Y,Z,ECG
def eda_seperation(rawdata_filename,participant,timeline_filename,trial,text_type,samplingrate,samplingfreq,flag_second_session_exist,EDA,X,Y,Z,ECG  ):

    time_data = 0
    time_data2 = 0

    print rawdata_filename

    # if text_type == 2:
    #     f = open(rawdata_filename, "r")
    #     lines = f.readlines()
    #     result = []
    #     result2 = []
    #     result3 = []
    #     result4 = []
    #     result5 = []
    #     result6 = []
    #
    #     for x in lines:
    #         a = re.split(',', x)
    #         result.append(a[1])
    #         result2.append(a[2])
    #         result3.append(a[3])
    #         result4.append(a[4])
    #         result5.append(a[5])
    #     f.close()
    #
    #     EDA = result2
    #     X = result3
    #     Y = result4
    #     Z = result5
    #     ECG = result6
    #     # EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
    #     #                                delimiter=',',
    #     #                                skiprows=3)
    # print rawdata_filename
    # print text_type
    # if text_type ==2:
    #     print 'text_type =2'
    # elif text_type ==0:
    # ####use delimiter='\t' for experiments before ....
    #     EDA,X,Y,Z,ECG= np.loadtxt(rawdata_filename, usecols=(2,3,4,5,6),unpack=True, dtype=float, delimiter='\t', skiprows = 3)
    # elif text_type==1:
    # ####use delimiter=' ' for experiments after .... (0012-0016)
    #     EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float, delimiter=' ',
    #                                skiprows=3)

    ##############################################################################



    ##################2_EDA preprocessing raw data conversion to real values
    np.savetxt('2_EDA.txt', EDA, fmt="%s")

    input_file = open('2_EDA.txt', 'r')

    os.chdir('..') #goes out from ASD folder
    os.chdir('..') #goes out from the experiment folder
    os.chdir('..')  # goes out from the 0000-RAW data folder

    os.chdir('./0001_RAW_DATA_EDA')
    createFolder('./' + trial + '/')
    os.chdir('./' + trial + '/')
    output_file = open('output_EDA_' + rawdata_filename, 'w')

    while True:

        line = input_file.readline()

        if ("" == line):
            print "file finished"
            break

        eda_real = ((float(line) / (2 ** 16)) * 3) / (0.12)
        output_file.write(str(eda_real))
        output_file.write("\n")

    EDA = np.loadtxt('output_EDA_' + rawdata_filename, usecols=(0), unpack=True, dtype=float, delimiter=' ')
    #################ECG preprocessing  raw data conversion to real values ( missing now ...) but we save ECG value as txt value
    os.chdir('..')#goes out from trial folder
    os.chdir('..')#goes out from RAW-DATA-EDA

    os.chdir('./0000_TIMELINE')
    title, min, sec = np.loadtxt(timeline_filename, usecols=(0, 1, 2), unpack=True, dtype=str, delimiter=',')
    min_real = min.astype(np.int)
    sec_real = sec.astype(np.int)
    total_sec = min_real * 60 + sec_real
    print total_sec

    os.chdir('..')#goes out from 0000-TIMELINE

    ############## session order description

    if min[3] == "1":
        session1 = "LEGO"
        session2 = "LOF"
    elif min[3] == "2":
        session1 = "LOF"
        session2 = "LEGO"
    else:
        print "session order is not defined!"

    ############## session start time calculation LOF & LEGO

    for i in range(len(title)):
        if title[i] == "1":
            gamestarts = total_sec[i] * 500
        if title[i] == "2":
            gamestarts2 = total_sec[i] * 500

    if flag_second_session_exist == 1:
        print 'flag_second_session_exist'
    elif flag_second_session_exist == 0:
        gamestarts2 = gamestarts #requires mannually removing the data

############1 w/o any event mark eda
    os.chdir('./0009_LEGO-LOF (EDA) processed')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./' + session1 + '/')
    createFolder('./' + session2 + '/')
    #################################################session1
    os.chdir('./' + session1 + '/')
    output_file = open('output_' + trial + '_' + participant + '_' + session1 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file_first5 = open('output_' + trial + '_' + participant + '_' + session1 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file_mid5 = open('output_' + trial + '_' + participant + '_' + session1 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file_last5 = open('output_' + trial + '_' + participant + '_' + session1 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..')


    ###############################################session2
    os.chdir('./' + session2 + '/')
    output_file2 = open('output_' + trial + '_' + participant + '_' + session2 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file2_first5 = open('output_' + trial + '_' + participant + '_' + session2 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file2_mid5 = open('output_' + trial + '_' + participant + '_' + session2 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file2_last5 = open('output_' + trial + '_' + participant + '_' + session2 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..') #GOES OUT LEGO
    ##############################################
    os.chdir('..')#GOES OUT LEGO 0017-55
    os.chdir('..')#GOES OUT ./0009_LEGO-LOF (EDA) processed_TEST

    # ecg_rawdata_filename = 'output_ECG_' + rawdata_filename
    # PUSH= np.loadtxt(ecg_rawdata_filename, usecols=(0),unpack=True, dtype=float, delimiter='\t')
#############1


############2 w video events marked eda
    os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./' + session1 + '/')
    createFolder('./' + session2 + '/')
    #################################################session1
    os.chdir('./' + session1 + '/')
    output_filev = open('output_' + trial + '_' + participant + '_' + session1 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file_first5v = open('output_' + trial + '_' + participant + '_' + session1 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file_mid5v = open('output_' + trial + '_' + participant + '_' + session1 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file_last5v = open('output_' + trial + '_' + participant + '_' + session1 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..')

    ###############################################session2
    os.chdir('./' + session2 + '/')
    output_file2v = open('output_' + trial + '_' + participant + '_' + session2 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file2_first5v = open('output_' + trial + '_' + participant + '_' + session2 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file2_mid5v = open('output_' + trial + '_' + participant + '_' + session2 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file2_last5v = open('output_' + trial + '_' + participant + '_' + session2 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..')  # GOES OUT LEGO
    ##############################################
    os.chdir('..')  # GOES OUT LEGO 0017-55
    os.chdir('..')  # GOES OUT ./0009_LEGO-LOF (EDA) processed_TEST

    # ecg_rawdata_filename = 'output_ECG_' + rawdata_filename
    # PUSH= np.loadtxt(ecg_rawdata_filename, usecols=(0),unpack=True, dtype=float, delimiter='\t')
#############3

    ############3 w system log event mark
    os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./' + session1 + '/')
    createFolder('./' + session2 + '/')
    #################################################session1
    os.chdir('./' + session1 + '/')
    output_files = open('output_' + trial + '_' + participant + '_' + session1 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file_first5s = open('output_' + trial + '_' + participant + '_' + session1 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file_mid5s = open('output_' + trial + '_' + participant + '_' + session1 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file_last5s = open('output_' + trial + '_' + participant + '_' + session1 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..')

    ###############################################session2
    os.chdir('./' + session2 + '/')
    output_file2s = open('output_' + trial + '_' + participant + '_' + session2 + '_EDA.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file2_first5s = open('output_' + trial + '_' + participant + '_' + session2 + '_first5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file2_mid5s = open('output_' + trial + '_' + participant + '_' + session2 + '_mid5_EDA.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file2_last5s = open('output_' + trial + '_' + participant + '_' + session2 + '_last5_EDA.txt', 'w')
    os.chdir('..')

    os.chdir('..')  # GOES OUT LEGO
    ##############################################
    os.chdir('..')  # GOES OUT LEGO 0017-55
    os.chdir('..')  # GOES OUT ./0009_LEGO-LOF (EDA) processed_TEST

    # ecg_rawdata_filename = 'output_ECG_' + rawdata_filename
    # PUSH= np.loadtxt(ecg_rawdata_filename, usecols=(0),unpack=True, dtype=float, delimiter='\t')
    #############3


    for i in range(0, 900 * 500):  # always gets the 15 min from the start

        if i == 0:
            output_file.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
            output_file.write("\n")
            output_file2.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
            output_file2.write("\n")
            output_filev.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
            output_filev.write("\n")
            output_file2v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
            output_file2v.write("\n")
            output_files.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
            output_files.write("\n")
            output_file2s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
            output_file2s.write("\n")

        else:
            output_file.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
            output_file.write("\n")
            output_file2.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
            output_file2.write("\n")
            output_filev.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
            output_filev.write("\n")
            output_file2v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
            output_file2v.write("\n")
            output_files.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
            output_files.write("\n")
            output_file2s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
            output_file2s.write("\n")
        if i <= 300 * 500:

            if i == 0:
                output_file_first5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_first5.write("\n")
                output_file2_first5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_first5.write("\n")
                output_file_first5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_first5v.write("\n")
                output_file2_first5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_first5v.write("\n")
                output_file_first5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_first5s.write("\n")
                output_file2_first5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_first5s.write("\n")
            else:
                output_file_first5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_first5.write("\n")
                output_file2_first5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_first5.write("\n")
                output_file_first5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_first5v.write("\n")
                output_file2_first5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_first5v.write("\n")
                output_file_first5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_first5s.write("\n")
                output_file2_first5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_first5s.write("\n")

            time_data_flag = 1
        elif i > 300 * 500 and i <= 600 * 500:

            if time_data_flag == 1:
                output_file_mid5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_mid5.write("\n")
                output_file2_mid5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_mid5.write("\n")
                output_file_mid5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_mid5v.write("\n")
                output_file2_mid5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_mid5v.write("\n")
                output_file_mid5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_mid5s.write("\n")
                output_file2_mid5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_mid5s.write("\n")
                time_data_flag = 2
            else:
                output_file_mid5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_mid5.write("\n")
                output_file2_mid5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_mid5.write("\n")
                output_file_mid5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_mid5v.write("\n")
                output_file2_mid5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_mid5v.write("\n")
                output_file_mid5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_mid5s.write("\n")
                output_file2_mid5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_mid5s.write("\n")
            time_data_flag = 2

        elif i > 600 * 500 and i <= 900 * 500:
            if time_data_flag == 2:
                output_file_last5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_last5.write("\n")
                output_file2_last5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_last5.write("\n")
                output_file_last5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_last5v.write("\n")
                output_file2_last5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_last5v.write("\n")
                output_file_last5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',22')
                output_file_last5s.write("\n")
                output_file2_last5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',22')
                output_file2_last5s.write("\n")
                time_data_flag = 3
            else:
                output_file_last5.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_last5.write("\n")
                output_file2_last5.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_last5.write("\n")
                output_file_last5v.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_last5v.write("\n")
                output_file2_last5v.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_last5v.write("\n")
                output_file_last5s.write(str(time_data) + ',' + str(EDA[gamestarts + i]) + ',0')
                output_file_last5s.write("\n")
                output_file2_last5s.write(str(time_data) + ',' + str(EDA[gamestarts2 + i]) + ',0')
                output_file2_last5s.write("\n")
            time_data_flag = 3

        time_data = time_data + samplingfreq

    ############## Baseline seperation

    os.chdir('./0010_BASELINE (EDA) processed')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./b1')
    createFolder('./break')
    createFolder('./b2')

    if participant == "44":
        createFolder('./cb1')
        createFolder('./cb2')
        createFolder('./cb3')
        createFolder('./cb4')
    if participant == "55":
        createFolder('./jb1')
        createFolder('./jb2')
        createFolder('./jb3')
        createFolder('./jb4')

    os.chdir('./b1')
    b1 = open('output_' + trial + '_' + participant + '_' + "b1" + '_EDA.txt', 'w')
    os.chdir('..')
    os.chdir('./break')
    b_break = open('output_' + trial + '_' + participant + '_' + "break" + '_EDA.txt', 'w')
    os.chdir('..')
    os.chdir('./b2')
    b2 = open('output_' + trial + '_' + participant + '_' + "b2" + '_EDA.txt', 'w')
    os.chdir('..')

    if participant == "44":
        os.chdir('./cb1')
        cb1 = open('output_' + trial + '_' + participant + '_' + "cb1" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./cb2')
        cb2 = open('output_' + trial + '_' + participant + '_' + "cb2" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./cb3')
        cb3 = open('output_' + trial + '_' + participant + '_' + "cb3" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./cb4')
        cb4 = open('output_' + trial + '_' + participant + '_' + "cb4" + '_EDA.txt', 'w')
        os.chdir('..')
    if participant == "55":
        os.chdir('./jb1')
        jb1 = open('output_' + trial + '_' + participant + '_' + "jb1" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./jb2')
        jb2 = open('output_' + trial + '_' + participant + '_' + "jb2" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./jb3')
        jb3 = open('output_' + trial + '_' + participant + '_' + "jb3" + '_EDA.txt', 'w')
        os.chdir('..')
        os.chdir('./jb4')
        jb4 = open('output_' + trial + '_' + participant + '_' + "jb4" + '_EDA.txt', 'w')
        os.chdir('..')

    for i in range(len(title)):
        if title[i] == "b1":
            baseline1 = total_sec[i] * 500
            print baseline1
        if title[i] == "break":
            baseline_break = total_sec[i] * 500
            print baseline_break
        if title[i] == "b2":
            print i
            print '#####################################333'+str(total_sec[i])
            baseline2 = total_sec[i] * 500
            print baseline2
        if participant == "44":
            if title[i] == "cb1":
                cbaseline1 = total_sec[i] * 500
                print cbaseline1
            if title[i] == "cb2":
                cbaseline2 = total_sec[i] * 500
                print cbaseline2
            if title[i] == "cb3":
                cbaseline3 = total_sec[i] * 500
                print cbaseline3
            if title[i] == "cb4":
                cbaseline4 = total_sec[i] * 500
                print cbaseline4

            if flag_second_session_exist == 1:
                print 'flag_second_session_baseline_exist'
            elif flag_second_session_exist == 0:
                cbaseline3 = 0
                cbaseline4 = 0


        if participant == "55":
            if title[i] == "jb1":
                jbaseline1 = total_sec[i] * 500
                print jbaseline1
            if title[i] == "jb2":
                jbaseline2 = total_sec[i] * 500
                print jbaseline2
            if title[i] == "jb3":
                jbaseline3 = total_sec[i] * 500
                print jbaseline3
            if title[i] == "jb4":
                jbaseline4 = total_sec[i] * 500
                print jbaseline4

            if flag_second_session_exist == 1:
                print 'flag_second_session_baseline_exist'
            elif flag_second_session_exist == 0:

                jbaseline3 = 0
                jbaseline4 = 0

    time_data = 0



    print 'LENGTH OF EDA----------------'+str(len(EDA))
    for i in range(0, 60 * 500):  # always gets the 1 min from the start for the baselines except break

        if i == 0:
            b1.write(str(time_data) + ',' + str(EDA[baseline1 + i]) + ',22')
            b1.write("\n")

            b2.write(str(time_data) + ',' + str(EDA[baseline2 + i]) + ',22')
            b2.write("\n")

            if participant == "44":
                cb1.write(str(time_data) + ',' + str(EDA[cbaseline1 + i]) + ',22')
                cb1.write("\n")
                cb2.write(str(time_data) + ',' + str(EDA[cbaseline2 + i]) + ',22')
                cb2.write("\n")
                cb3.write(str(time_data) + ',' + str(EDA[cbaseline3 + i]) + ',22')
                cb3.write("\n")
                cb4.write(str(time_data) + ',' + str(EDA[cbaseline4 + i]) + ',22')
                cb4.write("\n")
            if participant == "55":
                jb1.write(str(time_data) + ',' + str(EDA[jbaseline1 + i]) + ',22')
                jb1.write("\n")
                jb2.write(str(time_data) + ',' + str(EDA[jbaseline2 + i]) + ',22')
                jb2.write("\n")
                jb3.write(str(time_data) + ',' + str(EDA[jbaseline3 + i]) + ',22')
                jb3.write("\n")
                jb4.write(str(time_data) + ',' + str(EDA[jbaseline4 + i]) + ',22')
                jb4.write("\n")

        else:

            b1.write(str(time_data) + ',' + str(EDA[baseline1 + i]) + ',0')
            b1.write("\n")
            b2.write(str(time_data) + ',' + str(EDA[baseline2 + i]) + ',0')
            b2.write("\n")

            if participant == "44":
                cb1.write(str(time_data) + ',' + str(EDA[cbaseline1 + i]) + ',0')
                cb1.write("\n")
                cb2.write(str(time_data) + ',' + str(EDA[cbaseline2 + i]) + ',0')
                cb2.write("\n")
                cb3.write(str(time_data) + ',' + str(EDA[cbaseline3 + i]) + ',0')
                cb3.write("\n")
                cb4.write(str(time_data) + ',' + str(EDA[cbaseline4 + i]) + ',0')
                cb4.write("\n")
            if participant == "55":
                jb1.write(str(time_data) + ',' + str(EDA[jbaseline1 + i]) + ',0')
                jb1.write("\n")
                jb2.write(str(time_data) + ',' + str(EDA[jbaseline2 + i]) + ',0')
                jb2.write("\n")
                jb3.write(str(time_data) + ',' + str(EDA[jbaseline3 + i]) + ',0')
                jb3.write("\n")
                jb4.write(str(time_data) + ',' + str(EDA[jbaseline4 + i]) + ',0')
                jb4.write("\n")
        time_data = time_data + samplingfreq

    time_data = 0
    for i in range(0, 300 * 500):  # always gets the 5 min from the start for the baselines for break
        if i == 0:
            b_break.write(str(time_data) + ',' + str(EDA[baseline_break + i]) + ',22')
            b_break.write("\n")
        else:

            b_break.write(str(time_data) + ',' + str(EDA[baseline_break + i]) + ',0')
            b_break.write("\n")
        time_data = time_data + samplingfreq

    os.chdir('..') #GOING OUT 0017_55
    os.chdir('..')  # GOING OUT 0010_BASELINE (EDA) processed_TEST
def acc_seperation(rawdata_filename,participant,timeline_filename,trial,text_type,samplingrate,samplingfreq,flag_second_session_exist,EDA,X,Y,Z,ECG  ):

    ############################################# PARAMETERS TO CHANGE ################
    # rawdata_filename = "SCH_opensignals_000780D8AB44_2018-09-15_10-19-48.txt"
    # participant = "44"
    # trial = "0017"
    # timeline_filename = trial + "_Timeline - Experiment_Timeline.csv"
    #
    # samplingrate = 500
    # samplingfreq = 0.002
    #


    time_data = 0
    time_data2 = 0

    print rawdata_filename

    # if text_type == 2:
    #     f = open(rawdata_filename, "r")
    #     lines = f.readlines()
    #     result = []
    #     result2 = []
    #     result3 = []
    #     result4 = []
    #     result5 = []
    #     result6 = []
    #
    #     for x in lines:
    #         a = re.split(',', x)
    #         result.append(a[1])
    #         result2.append(a[2])
    #         result3.append(a[3])
    #         result4.append(a[4])
    #         result5.append(a[5])
    #     f.close()
    #
    #     EDA = result2
    #     X = result3
    #     Y = result4
    #     Z = result5
    #     ECG = result6
    #     # EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
    #     #                                delimiter=',',
    #     #                                skiprows=3)
    #
    # if text_type ==2:
    #     print 'text_type =2'
    # elif text_type ==0:
    # ####use delimiter='\t' for experiments before ....
    #     EDA,X,Y,Z,ECG= np.loadtxt(rawdata_filename, usecols=(2,3,4,5,6),unpack=True, dtype=float, delimiter='\t', skiprows = 3)
    # elif text_type==1:
    # ####use delimiter=' ' for experiments after .... (0012-0016)
    #     EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float, delimiter=' ',
    #                                skiprows=3)

    ##############################################################################

    os.chdir('..') #goes out from ASD folder
    os.chdir('..') #goes out from the experiment folder
    os.chdir('..')  # goes out from the 0000-RAW data folder

    for i in range(len(X)):
        X[i] = (float(X[i]) - 31127) / (34285 - 31127) * 2 - 1
        Y[i] = (float(Y[i]) - 31127) / (34285 - 31127) * 2 - 1
        Z[i] = (float(Z[i]) - 31127) / (34285 - 31127) * 2 - 1

    os.chdir('./0000_TIMELINE')
    title, min, sec = np.loadtxt(timeline_filename, usecols=(0, 1, 2), unpack=True, dtype=str, delimiter=',')
    min_real = min.astype(np.int)
    sec_real = sec.astype(np.int)
    total_sec = min_real * 60 + sec_real
    print total_sec

    os.chdir('..')#goes out from 0000-TIMELINE

    ############## session order description

    if min[3] == "1":
        session1 = "LEGO"
        session2 = "LOF"
    elif min[3] == "2":
        session1 = "LOF"
        session2 = "LEGO"
    else:
        print "session order is not defined!"

    ############## session start time calculation LOF & LEGO

    for i in range(len(title)):
        if title[i] == "1":
            gamestarts = total_sec[i] * 500
        if title[i] == "2":
            gamestarts2 = total_sec[i] * 500

    if flag_second_session_exist == 1:
        print 'flag_second_session_exist'
    elif flag_second_session_exist == 0:
        gamestarts2 = gamestarts #requires mannually removing the data


    os.chdir('./0011_LEGO-LOF (ACC) processed')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./' + session1 + '/')
    createFolder('./' + session2 + '/')
    #################################################session1
    os.chdir('./' + session1 + '/')
    output_file = open('output_' + trial + '_' + participant + '_' + session1 + '_ACC.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file_first5 = open('output_' + trial + '_' + participant + '_' + session1 + '_first5_ACC.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file_mid5 = open('output_' + trial + '_' + participant + '_' + session1 + '_mid5_ACC.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file_last5 = open('output_' + trial + '_' + participant + '_' + session1 + '_last5_ACC.txt', 'w')
    os.chdir('..')

    os.chdir('..')

    ###############################################session2
    os.chdir('./' + session2 + '/')
    output_file2 = open('output_' + trial + '_' + participant + '_' + session2 + '_ACC.txt', 'w')

    createFolder('./first5/')
    os.chdir('./first5/')
    output_file2_first5 = open('output_' + trial + '_' + participant + '_' + session2 + '_first5_ACC.txt', 'w')
    os.chdir('..')

    createFolder('./mid5/')
    os.chdir('./mid5/')
    output_file2_mid5 = open('output_' + trial + '_' + participant + '_' + session2 + '_mid5_ACC.txt', 'w')
    os.chdir('..')

    createFolder('./last5/')
    os.chdir('./last5/')
    output_file2_last5 = open('output_' + trial + '_' + participant + '_' + session2 + '_last5_ACC.txt', 'w')
    os.chdir('..')

    print(os.getcwd())

    os.chdir('..') #GOES OUT LEGO
    ##############################################
    os.chdir('..')#GOES OUT LEGO 0017-55
    os.chdir('..')#GOES OUT ./0009_LEGO-LOF (EDA) processed_TEST

    # ecg_rawdata_filename = 'output_ECG_' + rawdata_filename
    # PUSH= np.loadtxt(ecg_rawdata_filename, usecols=(0),unpack=True, dtype=float, delimiter='\t')

    for i in range(0, 900 * 500):  # always gets the 15 min from the start

        if i == 0:
            output_file.write(','+'time' + ',' +'x'+','+'y'+',' + 'z')
            output_file.write("\n")
            output_file2.write(','+'time' + ',' + 'x'+','+'y'+',' + 'z')
            output_file2.write("\n")
        else:
            output_file.write(','+str(time_data) + ',' +str(X[gamestarts + i])+','+str(Y[gamestarts + i])+',' + str(Z[gamestarts + i]))
            output_file.write("\n")
            output_file2.write(','+str(time_data) + ',' + str(X[gamestarts2 + i])+','+str(Y[gamestarts2 + i])+',' + str(Z[gamestarts2 + i]))
            output_file2.write("\n")


        if i <= 300 * 500:

            if i == 0:
                output_file_first5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file_first5.write("\n")
                output_file2_first5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file2_first5.write("\n")
            else:
                output_file_first5.write(','+str(time_data) + ',' + str(X[gamestarts + i])+','+str(Y[gamestarts + i])+',' + str(Z[gamestarts + i]))
                output_file_first5.write("\n")
                output_file2_first5.write(','+str(time_data) + ',' + str(X[gamestarts2 + i])+','+str(Y[gamestarts2 + i])+',' + str(Z[gamestarts2 + i]))
                output_file2_first5.write("\n")

            time_data_flag = 1
        elif i > 300 * 500 and i <= 600 * 500:

            if time_data_flag ==1 :
                output_file_mid5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file_mid5.write("\n")
                output_file2_mid5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file2_mid5.write("\n")
                time_data_flag = 2
            else:
                output_file_mid5.write(','+str(time_data) + ',' +str(X[gamestarts + i])+','+str(Y[gamestarts + i])+',' + str(Z[gamestarts + i]))
                output_file_mid5.write("\n")
                output_file2_mid5.write(','+str(time_data) + ',' + str(X[gamestarts2 + i])+','+str(Y[gamestarts2 + i])+',' + str(Z[gamestarts2 + i]) )
                output_file2_mid5.write("\n")
            time_data_flag = 2

        elif i > 600 * 500 and i <= 900 * 500:

            if time_data_flag ==2 :
                output_file_last5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file_last5.write("\n")
                output_file2_last5.write(',' + 'time' + ',' + 'x' + ',' + 'y' + ',' + 'z')
                output_file2_last5.write("\n")
                time_data_flag = 3
            else:
                output_file_last5.write(','+str(time_data) + ',' + str(X[gamestarts + i])+','+str(Y[gamestarts + i])+',' + str(Z[gamestarts + i]))
                output_file_last5.write("\n")
                output_file2_last5.write(','+str(time_data) + ',' + str(X[gamestarts2 + i])+','+str(Y[gamestarts2 + i])+',' + str(Z[gamestarts2 + i]) )
                output_file2_last5.write("\n")
            time_data_flag = 3

        time_data = time_data + samplingfreq
def ecg_seperation(rawdata_filename,participant,timeline_filename,trial,text_type,samplingrate,samplingfreq,flag_second_session_exist,EDA,X,Y,Z,ECG  ):
    time_data = 0
    time_data2 = 0

    print rawdata_filename

    # if text_type == 2:
    #     f = open(rawdata_filename, "r")
    #     lines = f.readlines()
    #     result = []
    #     result2 = []
    #     result3 = []
    #     result4 = []
    #     result5 = []
    #     result6 = []
    #
    #     for x in lines:
    #         a = re.split(',', x)
    #         result.append(a[1])
    #         result2.append(a[2])
    #         result3.append(a[3])
    #         result4.append(a[4])
    #         result5.append(a[5])
    #     f.close()
    #
    #     EDA = result2
    #     X = result3
    #     Y = result4
    #     Z = result5
    #     ECG = result6
    #     # EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
    #     #                                delimiter=',',
    #     #                                skiprows=3)
    #
    # if text_type == 2:
    #     print 'text_type =2'
    # elif text_type == 0:
    #     ####use delimiter='\t' for experiments before ....
    #     EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
    #                                    delimiter='\t', skiprows=3)
    # elif text_type == 1:
    #     ####use delimiter=' ' for experiments after .... (0012-0016)
    #     EDA, X, Y, Z, ECG = np.loadtxt(rawdata_filename, usecols=(2, 3, 4, 5, 6), unpack=True, dtype=float,
    #                                    delimiter=' ',
    #                                    skiprows=3)

    ##############################################################################



    os.chdir('..')  # goes out from ASD folder
    os.chdir('..')  # goes out from the experiment folder
    os.chdir('..')  # goes out from the 0000-RAW data folder

    os.chdir('./0002_RAW_DATA_HRV')
    createFolder('./' + trial + '/')
    os.chdir('./' + trial + '/')
    np.savetxt('output_ECG_' + rawdata_filename, ECG, fmt="%s")

    os.chdir('..')
    os.chdir('..')
    os.chdir('./0000_TIMELINE')
    title, min, sec = np.loadtxt(timeline_filename, usecols=(0, 1, 2), unpack=True, dtype=str, delimiter=',')
    min_real = min.astype(np.int)
    sec_real = sec.astype(np.int)
    total_sec = min_real * 60 + sec_real
    print total_sec



    os.chdir('..')  # goes out from 0000-TIMELINE

    ############## session order description

    if min[3] == "1":
        session1 = "LEGO"
        session2 = "LOF"
    elif min[3] == "2":
        session1 = "LOF"
        session2 = "LEGO"
    else:
        print "session order is not defined!"

    ############## session start time calculation LOF & LEGO

    os.chdir('./0003_LEGO-LOF (HRV) processed')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./' + session1 + '/')
    createFolder('./' + session2 + '/')

    os.chdir('./' + session1 + '/')
    output_file = open('output_' + trial + '_' + participant + '_' + session1 + '_ECG.txt', 'w')
    os.chdir('..')
    os.chdir('./' + session2 + '/')
    output_file2 = open('output_' + trial + '_' + participant + '_' + session2 + '_ECG.txt', 'w')

    os.chdir('..')
    os.chdir('..')
    os.chdir('..')


    for i in range(len(title)):
        if title[i] == "1":
            gamestarts = total_sec[i] * 500
        if title[i] == "2":
            gamestarts2 = total_sec[i] * 500

    if flag_second_session_exist == 1:
        print 'flag_second_session_exist'
    elif flag_second_session_exist == 0:
        gamestarts2 = gamestarts  # requires mannually removing the data

    for i in range(0, 900 * 500):  # always gets the 15 min from the start
        output_file.write(str(ECG[gamestarts + i]))
        output_file.write("\n")
        output_file2.write(str(ECG[gamestarts2 + i]))
        output_file2.write("\n")

    ############## Baseline seperation

    os.chdir('./0004_BASELINE (HRV) processed')
    createFolder('./' + trial + '_' + participant + '/')
    os.chdir('./' + trial + '_' + participant + '/')
    createFolder('./b1')
    createFolder('./break')
    createFolder('./b2')

    if participant == "44":
        createFolder('./cb1')
        createFolder('./cb2')
        createFolder('./cb3')
        createFolder('./cb4')
    if participant == "55":
        createFolder('./jb1')
        createFolder('./jb2')
        createFolder('./jb3')
        createFolder('./jb4')

    os.chdir('./b1')
    b1 = open('output_' + trial + '_' + participant + '_' + "b1" + '_ECG.txt', 'w')
    os.chdir('..')
    os.chdir('./break')
    b_break = open('output_' + trial + '_' + participant + '_' + "break" + '_ECG.txt', 'w')
    os.chdir('..')
    os.chdir('./b2')
    b2 = open('output_' + trial + '_' + participant + '_' + "b2" + '_ECG.txt', 'w')
    os.chdir('..')

    if participant == "44":
        os.chdir('./cb1')
        cb1 = open('output_' + trial + '_' + participant + '_' + "cb1" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./cb2')
        cb2 = open('output_' + trial + '_' + participant + '_' + "cb2" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./cb3')
        cb3 = open('output_' + trial + '_' + participant + '_' + "cb3" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./cb4')
        cb4 = open('output_' + trial + '_' + participant + '_' + "cb4" + '_ECG.txt', 'w')
        os.chdir('..')
    if participant == "55":
        os.chdir('./jb1')
        jb1 = open('output_' + trial + '_' + participant + '_' + "jb1" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./jb2')
        jb2 = open('output_' + trial + '_' + participant + '_' + "jb2" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./jb3')
        jb3 = open('output_' + trial + '_' + participant + '_' + "jb3" + '_ECG.txt', 'w')
        os.chdir('..')
        os.chdir('./jb4')
        jb4 = open('output_' + trial + '_' + participant + '_' + "jb4" + '_ECG.txt', 'w')
        os.chdir('..')

    for i in range(len(title)):
        if title[i] == "b1":
            baseline1 = total_sec[i] * 500
            print baseline1
        if title[i] == "break":
            baseline_break = total_sec[i] * 500
            print baseline_break
        if title[i] == "b2":
            baseline2 = total_sec[i] * 500
            print baseline2
        if participant == "44":
            if title[i] == "cb1":
                cbaseline1 = total_sec[i] * 500
                print cbaseline1
            if title[i] == "cb2":
                cbaseline2 = total_sec[i] * 500
                print cbaseline2
            if title[i] == "cb3":
                cbaseline3 = total_sec[i] * 500
                print cbaseline3
            if title[i] == "cb4":
                cbaseline4 = total_sec[i] * 500
                print cbaseline4
        if participant == "55":
            if title[i] == "jb1":
                jbaseline1 = total_sec[i] * 500
                print jbaseline1
            if title[i] == "jb2":
                jbaseline2 = total_sec[i] * 500
                print jbaseline2
            if title[i] == "jb3":
                jbaseline3 = total_sec[i] * 500
                print jbaseline3
            if title[i] == "jb4":
                jbaseline4 = total_sec[i] * 500
                print jbaseline4

    for i in range(0, 60 * 500):  # always gets the 1 min from the start for the baselines except break

        b1.write(str(ECG[baseline1 + i]))
        b1.write("\n")
        b2.write(str(ECG[baseline2 + i]))
        b2.write("\n")

        if participant == "44":
            cb1.write(str(ECG[cbaseline1 + i]))
            cb1.write("\n")
            cb2.write(str(ECG[cbaseline2 + i]))
            cb2.write("\n")
            cb3.write(str(ECG[cbaseline3 + i]))
            cb3.write("\n")
            cb4.write(str(ECG[cbaseline4 + i]))
            cb4.write("\n")
        if participant == "55":
            jb1.write(str(ECG[jbaseline1 + i]))
            jb1.write("\n")
            jb2.write(str(ECG[jbaseline2 + i]))
            jb2.write("\n")
            jb3.write(str(ECG[jbaseline3 + i]))
            jb3.write("\n")
            jb4.write(str(ECG[jbaseline4 + i]))
            jb4.write("\n")

    for i in range(0, 300 * 500):  # always gets the 5 min from the start for the baselines for break
        b_break.write(str(ECG[baseline_break + i]))
        b_break.write("\n")

    os.chdir('..')  # GOING OUT 0017_55
    os.chdir('..')  # GOING OUT 0010_BASELINE (EDA) processed_TEST
def seperation():
    list = []
    for x in os.listdir(physio_raw_data_path):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    os.chdir(physio_raw_data_path)

    for i in range(main_loop_start_count, numberofexperiments):

        if i == skipped_experiment - 1 or i == skipped_experiment2 - 1 or i == skipped_experiment3 - 1 or i == skipped_experiment4 - 1:
            continue
        else:
            # print(os.getcwd())

            os.chdir('./' + list[i])
            os.chdir('./' + 'ASD')  ################## MAIN ENTERANCE TO LEGO

            # to control the sessions which does not have 2nd session
            if i == experiment_number_which_doesnot_have_2nd_session - 1:
                flag_second_session_exist = 0
            else:
                flag_second_session_exist = 1

            # to control plux raw data delimeter issue
            if i + 1 <= 5:  # experiment 0005 and below 0004,0003, since before and after raw datas merged manually
                text_type = 2
            elif i + 1 > 5 and i + 1 <= 11:  # experiment 0011 and below 0010,0009, ....
                text_type = 0
            elif i + 1 > 11:  # experiment 0012 and above 0012,0013, ....
                text_type = 1

            if i <= 11:  # experiment 0011 and below 0010,0009, ....
                rawdata_filename = newest('.')
                participant = "55"
                trial = str(list[i])
                timeline_filename = trial + "_Timeline - Experiment_Timeline.csv"
                print timeline_filename
                print rawdata_filename


                EDA, X, Y, Z, ECG = data_import(text_type, rawdata_filename)
                ########Function Calls-start

                eda_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')

                ecg_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)

                os.chdir('./0000-RAW data')
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')

                acc_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)

                ########Function Calls-end

                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')

                rawdata_filename = newest('.')
                participant = "44"
                trial = str(list[i])
                timeline_filename = trial + "_Timeline - Experiment_Timeline.csv"

                EDA, X, Y, Z, ECG = data_import(text_type, rawdata_filename)
                ########Function Calls-start

                eda_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')

                ecg_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)

                os.chdir('./0000-RAW data')
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')

                acc_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)

                ########Function Calls-end



            elif i > 11:  # experiment 0012 and above 0012,0013, ....

                rawdata_filename = newest('.')
                participant = "55"
                trial = str(list[i])
                timeline_filename = trial + "_Timeline - Experiment_Timeline.csv"

                EDA, X, Y, Z, ECG = data_import(text_type, rawdata_filename)

                ########Function Calls-start
                eda_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')

                ecg_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)

                os.chdir('./0000-RAW data')
                os.chdir('./' + list[i])
                os.chdir('./' + 'ASD')

                acc_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                                samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                ########Function Calls-end

                os.chdir('./' + list[i])

                os.chdir('./' + 'TD')  ##################

                rawdata_filename = newest('.')
                participant = "44"
                trial = str(list[i])
                timeline_filename = trial + "_Timeline - Experiment_Timeline.csv"

                EDA, X, Y, Z, ECG = data_import(text_type, rawdata_filename)

                ########Function Calls-start
                eda_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')

                ecg_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                               samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)

                os.chdir('./0000-RAW data')
                os.chdir('./' + list[i])
                os.chdir('./' + 'TD')

                acc_seperation(rawdata_filename, participant, timeline_filename, trial, text_type, samplingrate,
                                samplingfreq, flag_second_session_exist, EDA, X, Y, Z, ECG)
                os.chdir(physio_raw_data_path)
                ########Function Calls-end

    print(os.getcwd())
    os.chdir('..')

#########stage 2
def preprocessing__batch_EDA_session_seperation():
    os.chdir(data_path)

    directory = directory_batch5_LEGO_LOF
    directory_batch = directory_batch_LEGO_LOF

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0009_LEGO-LOF (EDA) processed')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):
        os.chdir('./' + list[i])

        os.chdir('./' + 'LEGO')  ################## MAIN ENTERANCE TO LEGO

        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename, directory_batch + rawdata_filename)

        ################## MAIN ENTERANCE TO first 5

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')
        ################## MAIN EXIT TO first 5

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LEGO

        os.chdir('./' + 'LOF')  ################## MAIN ENTERANCE TO LOF
        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename,
                 directory_batch + rawdata_filename)

        #################

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LOF

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def preprocessing__batch_EDA_session_seperation_BASELINE():
    os.chdir(data_path)

    directory = directory_batch_baseline_LEGO_LOF
    directory_break = directory_batch_break_baselineLEGO_LOF

    list = []
    for x in os.listdir('./0010_BASELINE (EDA) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0010_BASELINE (EDA) processed')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):

        os.chdir('./' + list[i])

        trial_participant = list[i]

        # print trial_participant[5:7]
        if trial_participant[5:7] == '44':

            os.chdir('./' + 'b1')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename, directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'b2')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'break')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory_break + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'cb1')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'cb2')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'cb3')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'cb4')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')


        elif trial_participant[5:7] == '55':

            os.chdir('./' + 'b1')  ################## MAIN ENTERANCE TO LOF
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            #################

            os.chdir('./' + 'b2')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'break')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory_break + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'jb1')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'jb2')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'jb3')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

            os.chdir('./' + 'jb4')
            rawdata_filename = newest('.')
            copyfile('./' + rawdata_filename,
                     directory + rawdata_filename)
            os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def preprocessing__batch_ACC_session_seperation():
    os.chdir(data_path)

    directory = directory_batch_all_LEGO_LOF_ACC
    directory_batch = directory_batch_all2_LEGO_LOF_ACC

    list = []
    for x in os.listdir('./0011_LEGO-LOF (ACC) processed'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0011_LEGO-LOF (ACC) processed')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):
        os.chdir('./' + list[i])

        os.chdir('./' + 'LEGO')  ################## MAIN ENTERANCE TO LEGO

        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename, directory_batch + rawdata_filename)

        ################## MAIN ENTERANCE TO first 5

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')
        ################## MAIN EXIT TO first 5

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LEGO

        os.chdir('./' + 'LOF')  ################## MAIN ENTERANCE TO LOF
        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename,
                 directory_batch + rawdata_filename)

        #################

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LOF

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def test():##############################################acc feature extraction
    DEBUG = True

    SAMPLING_RATE = 8

    ONE_MINUTE_S = 60
    THIRTY_MIN_S = ONE_MINUTE_S * 30
    SECONDS_IN_DAY = 24 * 60 * 60

    STILLNESS_MOTION_THRESHOLD = .1
    PERCENT_STILLNESS_THRESHOLD = .95

    STEP_DIFFERENCE_THRESHOLD = 0.3

    def computeAllAccelerometerFeatures(data, time_frames):
        if DEBUG: print "\t\tcomputing motion..."
        motion = computeMotion(data['AccelX'], data['AccelY'], data['AccelZ'])

        if DEBUG: print "\t\tcomputing steps..."
        steps = computeSteps(motion)

        if DEBUG: print "\t\tcomputing stillness..."
        stillness = computeStillness(motion)

        features = []

        for time_frame in time_frames:
            start = time_frame[0]
            end = time_frame[1]
            start1Hz = int(start / SAMPLING_RATE)
            end1Hz = int(end / SAMPLING_RATE)
            if DEBUG: print "\t\tcomputing features for time frame. Start index:", start, "end index:", end

            time_frame_feats = computeAccelerometerFeaturesOverOneTimeFrame(motion[start:end],
                                                                            steps[start:end],
                                                                            stillness[start1Hz:end1Hz])
            features.append(time_frame_feats)

        return features, steps, motion

    def computeMotion(acc1, acc2, acc3):
        '''Aggregates 3-axis accelerometer signal into a single motion signal'''
        return np.sqrt(np.array(acc1) ** 2 + np.array(acc2) ** 2 + np.array(acc3) ** 2)

    def computeSteps(motion):
        '''Determines the location of steps from the aggregated accelerometer signal.
        Signal is low-pass filtered, then minimums are located in the signal. For each
        min, if the max absolute derivative (first difference) immediately surrounding
        it is greater than a threshold, it is counted as a step.

        Args:
            motion:		root mean squared 3 axis acceleration
        Returns:
            steps:		binary array at 8Hz which is 1 everywhere there is a step'''

        filtered_signal = filterSignalFIR(motion, 2, 256)
        diff = filtered_signal[1:] - filtered_signal[:-1]

        mins = scisig.argrelextrema(filtered_signal, np.less)[0]

        steps = [0] * len(filtered_signal)
        for m in mins:
            if m <= 4 or m >= len(diff) - 4:
                continue
            if max(abs(diff[m - 4:m + 4])) > STEP_DIFFERENCE_THRESHOLD:
                steps[m] = 1.0

        return steps

    def filterSignalFIR(eda, cutoff=0.4, numtaps=64):
        f = cutoff / (SAMPLING_RATE / 2.0)
        FIR_coeff = scisig.firwin(numtaps, f)

        return scisig.lfilter(FIR_coeff, 1, eda)

    def computeStillness(motion):
        '''Locates periods in which the person is still or motionless.
        Total acceleration must be less than a threshold for 95 percent of one
        minute in order for that minute to count as still

        Args:
            motion:		an array containing the root mean squared acceleration
        Returns:
            A 1Hz array that is 1 for each second belonging to a still period, 0 otherwise
        '''
        diff = motion[1:] - motion[:-1]
        momentary_stillness = diff < STILLNESS_MOTION_THRESHOLD
        np.append(momentary_stillness, 0)  # to ensure list is the same size as the full day signal
        num_minutes_in_day = 24 * 60

        # create array indicating whether person was still or not for each second of the day
        # to be still the momentary_stillness signal must be true for more than 95% of the minute
        # containing that second
        second_stillness = [0] * SECONDS_IN_DAY

        for i in range(num_minutes_in_day):
            hours_start = i / 60
            mins_start = i % 60
            hours_end = (i + 1) / 60
            mins_end = (i + 1) % 60

            start_idx = getIndexFromTimestamp(hours_start, mins_start)
            end_idx = getIndexFromTimestamp(hours_end, mins_end)

            this_minute = momentary_stillness[start_idx:end_idx]
            minute_stillness = sum(this_minute) > PERCENT_STILLNESS_THRESHOLD * (60 * SAMPLING_RATE)

            second_idx = int(start_idx / 8)
            for si in range(second_idx, second_idx + 60):
                second_stillness[si] = float(minute_stillness)

        return second_stillness

    def computeAccelerometerFeaturesOverOneTimeFrame(motion, steps, stillness):
        ''' Computes all available features for a time period. Incoming signals are assumed to be from
        only that time period.

        Args:
            motion:						8Hz		root mean squared 3 axis acceleration
            steps:						8Hz		binary signal that is 1 if there is a step
            stillness:					1Hz		1 if the person was still during this second, 0 otherwise
        Returns:
            A list of features containing (in order):
            -Step count 								number of steps detected
            -mean step time during movement				average number of samples between two steps (aggregated first to 1 minute,
                                                        then we take the mean of only the parts of this signal occuring during movement)
            -percent stillness 							percentage of time the person spent nearly motionless
        '''

        features = []

        features.extend(computeStepFeatures(steps, stillness))
        features.append(countStillness(stillness))

        return features

    def computeStepFeatures(steps, stillness):
        '''Counts the total number of steps over a given period,
        as well as the average time between steps (meant to approximate walking speed)

        Args:
            steps:	an binary array at 8 Hz that is 1 every time there is a step
        Returns:
            sum: 			the number of steps in a period
            median time: 	average number of samples between two steps'''

        sum_steps = float(sum(steps))

        step_indices = np.nonzero(steps)[0]
        diff = step_indices[1:] - step_indices[:-1]

        # ensure length of step difference array is the same so we can get the actual locations of step differences
        timed_step_diff = np.empty(len(steps)) * np.nan
        timed_step_diff[step_indices] = diff

        signal_length_1s = len(stillness)
        signal_length_1min = signal_length_1s / 60

        # if there aren't enough steps during this period, cannot accurately compute mean step diff
        if len(timed_step_diff) < signal_length_1min:
            return [sum_steps, np.nan]

        agg_stillness = aggregateSignal(stillness, signal_length_1min, 'max')
        agg_step_diff = aggregateSignal(timed_step_diff, signal_length_1min, 'mean')

        movement_indices = [i for i in range(len(agg_stillness)) if agg_stillness[i] == 0.0]
        step_diff_during_movement = agg_step_diff[movement_indices]

        return [sum_steps, np.nanmean(step_diff_during_movement)]

    def countStillness(stillness):
        '''Counts the total percentage of time spent still over a period

        Args:
            stillness:	an binary array at 1Hz that is 1 if that second is part of a still period
        Returns:
            the percentage time spent still over a period'''

        return float(sum(stillness)) / float(len(stillness))

    def aggregateSignal(signal, new_signal_length, agg_method='sum'):
        new_signal = np.zeros(new_signal_length)
        samples_per_bucket = len(signal) / new_signal_length

        # the new signal length must be large enough that there is at least 1 sample per bucket
        assert (samples_per_bucket > 0)

        for i in range(new_signal_length):
            if agg_method == 'sum':
                new_signal[i] = np.nansum(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
            elif agg_method == 'percent':
                new_signal[i] = np.nansum(
                    signal[i * samples_per_bucket:(i + 1) * samples_per_bucket]) / samples_per_bucket
            elif agg_method == 'mean':
                new_signal[i] = np.nanmean(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
            elif agg_method == 'max':
                new_signal[i] = np.nanmax(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
        return new_signal

    def getIndexFromTimestamp(hours, mins=0):
        return ((hours * 60) + mins) * 60 * SAMPLING_RATE

    def inputTimeFrames():
        '''Allows user to choose the time frames over which they compute accelerometer features.'''

        time_frames = []
        # print "Accelerometer features can be extracted over different time periods."
        # cont = raw_input(
        #     "If you would like to enter a time period over which to compute features, enter 'y', or press enter to compute features over the entire file.")
        # while cont == 'y' or cont == 'Y':
        #     start = int(raw_input("Enter the starting hour of the time period (hour 0 is when the file starts):"))
        #     end = int(raw_input(
        #         "Enter the ending hour of the time period (hour 0 is when the file starts; use -1 for the end of the file):"))
        #     start = getIndexFromTimestamp(int(start))
        #     if end != -1:
        #         end = getIndexFromTimestamp(int(end))
        #     time_frames.append([start, end])
        #     print "Great! Now computing features for the following time periods:", time_frames
        #     cont = raw_input("To add another time period, enter 'y'. To finish, press enter.")

        if len(time_frames) == 0:
            time_frames = [[0, -1]]  # the whole file

        return time_frames

    def saveFeaturesToFile(features, time_frames, output_file):
        of = open(output_file, 'w')
        of.write(
            "Time period start hour, Time period end hour, Step count, Mean step time during movement, Percent stillness\n")
        tf_i = 0
        for tf in time_frames:
            output_str = str(tf[0]) + ' , ' + str(tf[1])
            for feat in features[tf_i]:
                output_str += ' , ' + str(feat)
            tf_i += 1
            of.write(output_str + '\n')
        of.close()
        print "Saved features to file", output_file

    # draws a graph of the data with the peaks marked on it
    # assumes that 'data' dataframe already contains the 'peaks' column
    def plotSteps(data, x_seconds, sampleRate=SAMPLING_RATE):
        if x_seconds:
            time_m = np.arange(0, len(data)) / float(sampleRate)
            realign = 128 / (sampleRate)
        else:
            time_m = np.arange(0, len(data)) / (sampleRate * 60.)
            realign = 128 / (sampleRate * 60.)

        data_min = data['motion'].min()
        data_max = data['motion'].max()

        # Plot the data with the Peaks marked
        plt.figure(1, figsize=(20, 5))

        plt.plot(time_m, data['motion'])

        for i in range(len(data)):
            if data.iloc[i]["steps"] == 1:
                x_loc = time_m[i] - realign
                plt.plot([x_loc, x_loc], [data_min, data_max], "k")
        step_height = data_max * 1.15
        # data['steps_plot'] = data['steps'] * step_height
        # plt.plot(time_m,data['steps_plot'],'k')

        plt.xlim([0, time_m[-1]])
        plt.ylim([data_min - .1, data_max + .1])
        plt.title('Motion with Detected "Steps" marked')
        plt.ylabel('g')
        if x_seconds:
            plt.xlabel('Time (s)')
        else:
            plt.xlabel('Time (min)')

        plt.show()


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

    list_excel = []

    for i in range(0, len(list)):
        if list[i].endswith('.txt'):
            list_excel.append(list[i])
    os.chdir('./0011_batch_all_LEGO-LOF (ACC) processed')

    # trial = '0017'
    # participant = '55'
    # session = 'ACC'
    # part = 'mid5'

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

        filepath = list_excel[i]
        print list_excel[i]

        data, filepath_confirm = getInputLoadFile(filepath)

        output_path = getOutputPath(trial, participant, session, part)

        time_frames = inputTimeFrames()

        features, steps, motion = computeAllAccelerometerFeatures(data, time_frames)

        data["steps"] = steps
        data["motion"] = motion

        saveFeaturesToFile(features, time_frames, output_path)

    os.chdir('..')


####cut and paste
def cut_and_paste():
    source1 = input_directory_path+'0001_RAW_DATA_EDA/'
    source2 = input_directory_path+'0002_RAW_DATA_HRV/'
    source3 = input_directory_path+'0003_LEGO-LOF (HRV) processed/'
    source4 = input_directory_path+'0004_BASELINE (HRV) processed/'
    source5 = input_directory_path+'0009_LEGO-LOF (EDA) processed/'
    source6 = input_directory_path+'0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED/'
    source7 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED/'
    source8 = input_directory_path+'0010_BASELINE (EDA) processed/'
    source9 = input_directory_path+'0011_LEGO-LOF (ACC) processed/'

    source10 = input_directory_path+'0009_batch_LEGO-LOF (EDA) processed/'
    source11 = input_directory_path+'0009_batch5_LEGO-LOF (EDA) processed/'
    source12 = input_directory_path+'0010_batch_BASELINE (EDA) processed/'
    source13 = input_directory_path+'0010_batch_break_BASELINE (EDA) processed/'
    source14 = input_directory_path+'0011_batch_all_LEGO-LOF (ACC) processed/'
    source15 = input_directory_path+'0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED/'

    source16 = input_directory_path+ "0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH/"
    source17 = input_directory_path+"0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH/"
    source18 = input_directory_path+ "0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH/"
    source19 = input_directory_path + "0015_OUTPUT/"


    destination = output_directory_path

    shutil.move(source1, destination)
    shutil.move(source2, destination)
    shutil.move(source3, destination)
    shutil.move(source4, destination)
    shutil.move(source5, destination)
    shutil.move(source6, destination)
    shutil.move(source7, destination)
    shutil.move(source8, destination)
    shutil.move(source9, destination)

    shutil.move(source10, destination)
    shutil.move(source11, destination)
    shutil.move(source12, destination)
    shutil.move(source13, destination)
    shutil.move(source14, destination)
    shutil.move(source15, destination)

    shutil.move(source16, destination)
    shutil.move(source17, destination)
    shutil.move(source18, destination)
    shutil.move(source19, destination)

#########stage 3
def coders_aggreed_video_coding_feature_extraction2():
# ############################################# FUNCTIONS ################
    os.chdir(output_path_main)
    def count_initiation_response(rawdata_filename, number_of_initiations, number_of_responses,trial,condition,phase):
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

        initiation_time_array = []
        response_time_array= []
        externalization_time_array= []
        # for i in range(0, len(initiation)):
        #     if direction[i] == 'Child':
        #         if initiation[i] == "Initiation":
        #             initiation_count = initiation_count + 1
        #             initiation_time_array.append(T[i])
        #             if type[i] == "STOP":
        #                 initiation_count = initiation_count - 1
        #         elif initiation[i] == "Response":
        #             response_count = response_count + 1
        #             response_time_array.append(T[i])
        #             if type[i] == "STOP":
        #                 response_count = response_count - 1
        #     if direction[i] == 'Externalization':
        #         externalization_count = externalization_count + 1
        #         externalization_time_array.append(T[i])
        #         if type[i] == "STOP":
        #             externalization_count = externalization_count - 1

        for i in range(0, len(initiation)):
            if direction[i] == 'Child':
                if initiation[i] == "Initiation" and type[i] == "POINT":
                    initiation_count = initiation_count + 1
                    initiation_time_array.append(T[i])
                if initiation[i] == "Initiation" and type[i] == "START":
                    initiation_count = initiation_count + 1
                    initiation_time_array.append(T[i])
                if initiation[i] == "Initiation" and type[i] == "STOP":
                    continue

                if initiation[i] == "Response"and type[i] == "POINT":
                    response_count = response_count + 1
                    response_time_array.append(T[i])
                if initiation[i] == "Response"and type[i] == "START":
                    response_count = response_count + 1
                    response_time_array.append(T[i])
                if initiation[i] == "Response"and type[i] == "STOP":
                    continue

            if direction[i] == 'Externalization':
                if type[i] == "START":
                    externalization_count = externalization_count + 1
                    externalization_time_array.append(T[i])
                if type[i] == "POINT":
                    externalization_count = externalization_count + 1
                    externalization_time_array.append(T[i])
                if type[i] == "STOP":
                    continue

            else:
                continue

        output_kubios_time = open('output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_kubios_time2 = open(
            'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt', 'w')

        count1 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(initiation_time_array) - count1) + '\t' + 'initiation')
        output_kubios_time.write("\n")

        output_initiation_time = open('output_initiation_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt',
                                      'w')
        output_initiation_time.write('time' + '\t' + 'nid')
        output_initiation_time.write("\n")
        for i in range(0, len(initiation_time_array)):
            output_initiation_time.write(str(initiation_time_array[i]) + '\t' + '1')
            output_initiation_time.write("\n")


            kubios_time_window = float(initiation_time_array[i]) + 30


            if phase == 'first':
                output_kubios_time.write(
                    str(initiation_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '1')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(initiation_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '1')
                output_kubios_time2.write("\n")

            elif phase == 'last':
                a=kubios_time_window + 600
                if kubios_time_window+600 > 900:
                    a = 900
                output_kubios_time.write(
                    str(float(initiation_time_array[i]) + 600) + '\t' + str(a) + '\t' + '1')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(float(initiation_time_array[i]) + 600) + '\t' + str(a) + '\t' + '1')
                output_kubios_time2.write("\n")

        count2 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(response_time_array) - count2) + '\t' + 'response')
        output_kubios_time.write("\n")

        output_response_time = open('output_response_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_response_time.write('time' + '\t' + 'nid')
        output_response_time.write("\n")
        for i in range(0, len(response_time_array)):
            output_response_time.write(str(response_time_array[i]) + '\t' + '2')
            output_response_time.write("\n")


            kubios_time_window = float(response_time_array[i]) + 30

            if phase == 'first':
                output_kubios_time.write(str(response_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '2')
                output_kubios_time.write("\n")
                output_kubios_time2.write(str(response_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '2')
                output_kubios_time2.write("\n")
            elif phase == 'last':

                a=kubios_time_window + 600
                if kubios_time_window+600 > 900:
                    a = 900

                output_kubios_time.write(
                    str(float(response_time_array[i]) + 600) + '\t' + str(a) + '\t' + '2')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(float(response_time_array[i]) + 600) + '\t' + str(a) + '\t' + '2')
                output_kubios_time2.write("\n")

        count3 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(externalization_time_array) - count3) + '\t' + 'externalization')
        output_kubios_time.write("\n")

        output_externalization_time = open(
            'output_externalization_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_externalization_time.write('time' + '\t' + 'nid')
        output_externalization_time.write("\n")
        for i in range(0, len(externalization_time_array)):
            output_externalization_time.write(str(externalization_time_array[i]) + '\t' + '3')
            output_externalization_time.write("\n")


            kubios_time_window = float(externalization_time_array[i]) + 30

            if phase == 'first':
                output_kubios_time.write(
                    str(externalization_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '3')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(externalization_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '3')
                output_kubios_time2.write("\n")
            elif phase == 'last':
                a=kubios_time_window + 600
                if kubios_time_window+600 > 900:
                    a = 900
                print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' + str(kubios_time_window)

                output_kubios_time.write(str(float(externalization_time_array[i]) + 600) + '\t' + str(
                    a) + '\t' + '3')
                output_kubios_time.write("\n")
                output_kubios_time2.write(str(float(externalization_time_array[i]) + 600) + '\t' + str(
                    a) + '\t' + '3')
                output_kubios_time2.write("\n")

        number_of_initiations = initiation_count
        number_of_responses = response_count
        number_of_externalizations = externalization_count
        return number_of_initiations, number_of_responses, number_of_externalizations

            # FUNTION END &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'),os.listdir('.'))
        print paths
        a =''
        if paths == []:
            a = 'nothing'
        else:
            a = max(paths, key=os.path.getctime)
        return a

    trial_array = []
    initiation_time_array_first5=[]

    number_of_initiation_response_array = np.zeros((numberofexperiments, 12)) # should be carefull with 0 and not exist state

    for i in range (0, numberofexperiments):
        for j in range (0,12):
            number_of_initiation_response_array[i][j] ='-1'

    result_array =[[0,0,0],[0,0,0]]
    number_of_initiations = 0
    number_of_responses = 0

    os.chdir('./0008-VIDEO-CODING')

    for i in range (1,numberofexperiments+1):

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 : # we dont have experiment 10

            trial_array.append(' ')
            continue
        else:
            if i<10:
                trial = "000" + str(i)
            elif i>=10 and i<100:
                trial = "00" + str(i)
            elif i>=100 and i<1000:
                trial = "0" + str(i)
            elif i >= 1000:
                trial = str(i)

            trial_array.append(trial)



            for j in range(1, 3):
                doesnotexistcatch = [0, 0]
                if j == 1:
                    # participant = 44
                    continue
                elif j == 2:
                    participant = 55
                print  './' + trial + '_' + str(participant) + '/'






                if (starting_point<=i):
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    print arr


                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "LEGO":
                            condition = "LEGO"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')
                            prr = os.listdir('.')

                            doesnotexistcatch_condition = [0, 0]
                            doesnotexistcatch_phase = ["first", "last"]

                            output_kubios_time_all = open(
                                'output_kubios_all_' + trial + '_'+'LEGO'+'_'+ 'time2.txt', 'w')
                            output_kubios_time_all2 = open(
                                'output_kubios_all_' + trial + '_'+'LEGO'+'_'+ 'time_WO_headers2.txt', 'w')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    doesnotexistcatch_condition[0] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':
                                        os.chdir('..')
                                        pass

                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses,number_of_externalizations = count_initiation_response(rawdata_filename,
                                                                                                               number_of_initiations,
                                                                                                             number_of_responses,trial,condition,phase)

                                        #
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all2.write(line)


                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")




                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i-1][0]=number_of_initiations
                                        number_of_initiation_response_array[i-1][1] = number_of_responses
                                        number_of_initiation_response_array[i - 1][2] = number_of_externalizations

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    doesnotexistcatch_condition[1] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':
                                        os.chdir('..')
                                        pass

                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses,number_of_externalizations = count_initiation_response(rawdata_filename,
                                                                                                               number_of_initiations,
                                                                                                               number_of_responses,trial,condition,phase)

                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all2.write(line)



                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")


                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i-1][3]=number_of_initiations
                                        number_of_initiation_response_array[i-1][4] = number_of_responses
                                        number_of_initiation_response_array[i - 1][5] = number_of_externalizations


                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                else:

                                    continue
                            # if j == 1:
                            #
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W1'
                            #             # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #             #                doesnotexistcatch_ciera[P]
                            #             # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            #
                            # elif j == 2:
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W2'
                            #             # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #             #                doesnotexistcatch_juan[P]
                            #             # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            output_kubios_time_all2.close()
                            data = pd.read_csv('output_kubios_all_' + trial + '_'+'LEGO'+'_'+ 'time_WO_headers2.txt', sep='\t',names = ['a', 'b','c'],dtype={'High': np.float64, 'Low': np.float64})
                            print data
                            data2 = data.sort_values(by=['a'],ascending=True)

                            data2.to_csv('output_kubios_all_' + trial + '_'+'LEGO'+'_'+ 'time_WO_headers3.txt',  sep='\t', index=False)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "LOF":
                            condition = "LOF"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')

                            prr = os.listdir('.')

                            doesnotexistcatch_condition = [0, 0]
                            doesnotexistcatch_phase = ["first", "last"]
                            output_kubios_time_all = open(
                                'output_kubios_all_' + trial + '_'+'LOF'+'_'+ 'time2.txt', 'w')
                            output_kubios_time_all2 = open(
                                'output_kubios_all_' + trial + '_'+'LOF'+'_'+ 'time_WO_headers2.txt', 'w')
                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    doesnotexistcatch_condition[0] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':

                                        os.chdir('..')
                                        pass
                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses,number_of_externalizations = count_initiation_response(rawdata_filename,
                                                                                                               number_of_initiations,
                                                                                                               number_of_responses,trial,condition,phase)
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]

                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all2.write(line)



                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")

                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i-1][6]=number_of_initiations
                                        number_of_initiation_response_array[i-1][7] = number_of_responses
                                        number_of_initiation_response_array[i - 1][8] = number_of_externalizations

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    doesnotexistcatch_condition[1] = 1
                                    os.chdir('./' + phase + '/')
                                    if newest('.') == 'nothing':

                                        os.chdir('..')
                                        pass
                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses,number_of_externalizations = count_initiation_response(rawdata_filename,
                                                                                                               number_of_initiations,
                                                                                                               number_of_responses,trial,condition,phase)
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]

                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines() :
                                            # write line to output file
                                            output_kubios_time_all2.write(line)


                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")

                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i-1][9]=number_of_initiations
                                        number_of_initiation_response_array[i-1][10] = number_of_responses
                                        number_of_initiation_response_array[i - 1][11] = number_of_externalizations

                                        # extract_ECG_features(trial, participant, condition)

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                else:
                                    continue
                            # if j == 1:
                            #
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W'
                            #         # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #         #                doesnotexistcatch_ciera[P]
                            #         # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            #
                            # elif j == 2:
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W'
                            #         # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #         #                doesnotexistcatch_juan[P]
                            #         # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue

                            output_kubios_time_all2.close()
                            data = pd.read_csv('output_kubios_all_' + trial + '_'+'LOF'+'_'+ 'time_WO_headers2.txt', sep='\t',names = ['a', 'b','c'],dtype={'High': np.float64, 'Low': np.float64})
                            print data
                            data2 = data.sort_values(by=['a'],ascending=True)

                            data2.to_csv('output_kubios_all_' + trial + '_'+'LOF'+'_'+ 'time_WO_headers3.txt',  sep='\t', index=False)

                            os.chdir('..')

                        # elif str(arr[k - 1]) == "ZDOESNOTEXIST":
                        #     print doesnotexistcatch
                        #     print "batu"
                        #     if doesnotexistcatch[0] == 1 and doesnotexistcatch[1] == 0:
                        #         # rawdata_name = 'output_' + trial + ';' + str(
                        #         #     participant) + ';' + "LOF" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                        #         # output_feature.write(rawdata_name + " " + "\n")
                        #         doesnotexistcatch[0] == 0
                        #         doesnotexistcatch[1] == 0
                        #     elif doesnotexistcatch[0] == 0 and doesnotexistcatch[1] == 1:
                        #         # rawdata_name = 'output_' + trial + ';' + str(
                        #         #     participant) + ';' + "LEGO" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                        #         # output_feature.write(rawdata_name + " " + "\n")
                        #         doesnotexistcatch[0] == 0
                        #         doesnotexistcatch[1] == 0
                        #     else:
                        #         continue

                        else:

                            continue
                    os.chdir('..')
                else:
                    continue


    output_feature = open('all_features_video_coding_ASC.txt','w')
    output_all_feature = open('initiation.txt', 'w')
    output_all_feature1 = open('response.txt', 'w')
    output_all_feature2 = open('externalization.txt', 'w')

    print number_of_initiation_response_array
    print trial_array

    for i in range (0,numberofexperiments):

        for k in range (0,2):
            if k == 0:
                phase ='LEGO'

                output_all_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'initiation,')
                output_all_feature.write(str(int(number_of_initiation_response_array[i][0]))+",")
                output_all_feature.write(str(int(number_of_initiation_response_array[i][3]))+",")
                output_all_feature.write("\n")

                output_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'initiation,')
                output_feature.write(str(int(number_of_initiation_response_array[i][0]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][3]))+",")
                output_feature.write("\n")

                output_all_feature1.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'response,')
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][1]))+",")
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][4]))+",")
                output_all_feature1.write("\n")

                output_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'response,')
                output_feature.write(str(int(number_of_initiation_response_array[i][1]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][4]))+",")
                output_feature.write("\n")

                output_all_feature2.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'externalization,')
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][2]))+",")
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][5]))+",")
                output_all_feature2.write("\n")

                output_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'externalization,')
                output_feature.write(str(int(number_of_initiation_response_array[i][2]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][5]))+",")
                output_feature.write("\n")

            elif k == 1:
                phase = 'LOF'

                output_all_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'initiation,')
                output_all_feature.write(str(int(number_of_initiation_response_array[i][6]))+",")
                output_all_feature.write(str(int(number_of_initiation_response_array[i][9]))+",")
                output_all_feature.write("\n")

                output_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'initiation,')
                output_feature.write(str(int(number_of_initiation_response_array[i][6]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][9]))+",")
                output_feature.write("\n")

                output_all_feature1.write('output_' + trial_array[i] + "," + "55" + "," + phase + ',' + 'response,')
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][7])) + ",")
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][10])) + ",")
                output_all_feature1.write("\n")

                output_feature.write('output_'+trial_array[i] + "," +"55" +","+phase + ',' + 'response,')
                output_feature.write(str(int(number_of_initiation_response_array[i][7]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][10]))+",")
                output_feature.write("\n")


                output_all_feature2.write('output_' + trial_array[i] + "," + "55" + "," + phase + ',' + 'externalization,')
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][8])) + ",")
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][11])) + ",")
                output_all_feature2.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "55" + "," + phase + ',' + 'externalization,')
                output_feature.write(str(int(number_of_initiation_response_array[i][8]))+",")
                output_feature.write(str(int(number_of_initiation_response_array[i][11]))+",")
                output_feature.write("\n")

    os.chdir('..')#
def coders_aggreed_video_coding_feature_extraction2_NONASC():
    # ############################################# FUNCTIONS ################
    os.chdir(output_path_main)
    def count_initiation_response(rawdata_filename, number_of_initiations, number_of_responses, trial, condition,
                                  phase):
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
            direction1[i - 1] = str(code_line[i][8])
            # direction2[i - 1] = str(code_line[i][13])
            initiation1[i - 1] = str(code_line[i][9])
            # initiation2[i - 1] = str(code_line[i][7])
            # initiation3[i - 1] = str(code_line[i][6])
            response[i - 1] = str(code_line[i][9])
            type[i - 1] = str(code_line[i][15])
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

        initiation_time_array = []
        response_time_array = []
        externalization_time_array = []
        # for i in range(0, len(initiation)):
        #     if direction[i] == 'Child':
        #         if initiation[i] == "Initiation":
        #             initiation_count = initiation_count + 1
        #             initiation_time_array.append(T[i])
        #             if type[i] == "STOP":
        #                 initiation_count = initiation_count - 1
        #         elif initiation[i] == "Response":
        #             response_count = response_count + 1
        #             response_time_array.append(T[i])
        #             if type[i] == "STOP":
        #                 response_count = response_count - 1
        #     if direction[i] == 'Externalization':
        #         externalization_count = externalization_count + 1
        #         externalization_time_array.append(T[i])
        #         if type[i] == "STOP":
        #             externalization_count = externalization_count - 1

        for i in range(0, len(initiation)):
            if direction[i] == 'Child':
                if initiation[i] == "Initiation" and type[i] == "POINT":
                    initiation_count = initiation_count + 1
                    initiation_time_array.append(T[i])
                if initiation[i] == "Initiation" and type[i] == "START":
                    initiation_count = initiation_count + 1
                    initiation_time_array.append(T[i])
                if initiation[i] == "Initiation" and type[i] == "STOP":
                    continue

                if initiation[i] == "Response" and type[i] == "POINT":
                    response_count = response_count + 1
                    response_time_array.append(T[i])
                if initiation[i] == "Response" and type[i] == "START":
                    response_count = response_count + 1
                    response_time_array.append(T[i])
                if initiation[i] == "Response" and type[i] == "STOP":
                    continue

            if direction[i] == 'Externalization':
                if type[i] == "START":
                    externalization_count = externalization_count + 1
                    externalization_time_array.append(T[i])
                if type[i] == "POINT":
                    externalization_count = externalization_count + 1
                    externalization_time_array.append(T[i])
                if type[i] == "STOP":
                    continue

            else:
                continue

        output_kubios_time = open('output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_kubios_time2 = open(
            'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt', 'w')

        count1 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(initiation_time_array) - count1) + '\t' + 'initiation')
        output_kubios_time.write("\n")

        output_initiation_time = open('output_initiation_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt',
                                      'w')
        output_initiation_time.write('time' + '\t' + 'nid')
        output_initiation_time.write("\n")
        for i in range(0, len(initiation_time_array)):
            output_initiation_time.write(str(initiation_time_array[i]) + '\t' + '1')
            output_initiation_time.write("\n")

            kubios_time_window = float(initiation_time_array[i]) + 30

            if phase == 'first':
                output_kubios_time.write(
                    str(initiation_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '1')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(initiation_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '1')
                output_kubios_time2.write("\n")

            elif phase == 'last':
                a = kubios_time_window + 600
                if kubios_time_window + 600 > 900:
                    a = 900
                output_kubios_time.write(
                    str(float(initiation_time_array[i]) + 600) + '\t' + str(a) + '\t' + '1')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(float(initiation_time_array[i]) + 600) + '\t' + str(a) + '\t' + '1')
                output_kubios_time2.write("\n")

        count2 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(response_time_array) - count2) + '\t' + 'response')
        output_kubios_time.write("\n")

        output_response_time = open('output_response_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_response_time.write('time' + '\t' + 'nid')
        output_response_time.write("\n")
        for i in range(0, len(response_time_array)):
            output_response_time.write(str(response_time_array[i]) + '\t' + '2')
            output_response_time.write("\n")

            kubios_time_window = float(response_time_array[i]) + 30

            if phase == 'first':
                output_kubios_time.write(str(response_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '2')
                output_kubios_time.write("\n")
                output_kubios_time2.write(str(response_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '2')
                output_kubios_time2.write("\n")
            elif phase == 'last':

                a = kubios_time_window + 600
                if kubios_time_window + 600 > 900:
                    a = 900

                output_kubios_time.write(
                    str(float(response_time_array[i]) + 600) + '\t' + str(a) + '\t' + '2')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(float(response_time_array[i]) + 600) + '\t' + str(a) + '\t' + '2')
                output_kubios_time2.write("\n")

        count3 = 0

        output_kubios_time.write(
            'time' + '\t' + 'nid' + '\t' + str(len(externalization_time_array) - count3) + '\t' + 'externalization')
        output_kubios_time.write("\n")

        output_externalization_time = open(
            'output_externalization_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt', 'w')
        output_externalization_time.write('time' + '\t' + 'nid')
        output_externalization_time.write("\n")
        for i in range(0, len(externalization_time_array)):
            output_externalization_time.write(str(externalization_time_array[i]) + '\t' + '3')
            output_externalization_time.write("\n")

            kubios_time_window = float(externalization_time_array[i]) + 30

            if phase == 'first':
                output_kubios_time.write(
                    str(externalization_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '3')
                output_kubios_time.write("\n")
                output_kubios_time2.write(
                    str(externalization_time_array[i]) + '\t' + str(kubios_time_window) + '\t' + '3')
                output_kubios_time2.write("\n")
            elif phase == 'last':
                a = kubios_time_window + 600
                if kubios_time_window + 600 > 900:
                    a = 900
                print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' + str(kubios_time_window)

                output_kubios_time.write(str(float(externalization_time_array[i]) + 600) + '\t' + str(
                    a) + '\t' + '3')
                output_kubios_time.write("\n")
                output_kubios_time2.write(str(float(externalization_time_array[i]) + 600) + '\t' + str(
                    a) + '\t' + '3')
                output_kubios_time2.write("\n")

        number_of_initiations = initiation_count
        number_of_responses = response_count
        number_of_externalizations = externalization_count
        return number_of_initiations, number_of_responses, number_of_externalizations

        # FUNTION END &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.xlsx'), os.listdir('.'))
        print paths
        a = ''
        if paths == []:
            a = 'nothing'
        else:
            a = max(paths, key=os.path.getctime)
        return a

    trial_array = []
    initiation_time_array_first5 = []

    number_of_initiation_response_array = np.zeros(
        (numberofexperiments, 12))  # should be carefull with 0 and not exist state

    for i in range(0, numberofexperiments):
        for j in range(0, 12):
            number_of_initiation_response_array[i][j] = '-1'

    result_array = [[0, 0, 0], [0, 0, 0]]
    number_of_initiations = 0
    number_of_responses = 0

    os.chdir('./0008-VIDEO-CODING - NONASC')

    for i in range(1, numberofexperiments + 1):

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10 or i == 30 or i == 31

            trial_array.append(' ')
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

            trial_array.append(trial)

            for j in range(1, 3):
                doesnotexistcatch = [0, 0]
                if j == 1:
                    # participant = 44
                    continue
                elif j == 2:
                    participant = 44
                print  './' + trial + '_' + str(participant) + '/'

                if (starting_point <= i):
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    print arr

                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "LEGO":
                            condition = "LEGO"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')
                            prr = os.listdir('.')

                            doesnotexistcatch_condition = [0, 0]
                            doesnotexistcatch_phase = ["first", "last"]

                            output_kubios_time_all = open(
                                'output_kubios_all_' + trial + '_' + 'LEGO' + '_' + 'time2.txt', 'w')
                            output_kubios_time_all2 = open(
                                'output_kubios_all_' + trial + '_' + 'LEGO' + '_' + 'time_WO_headers2.txt', 'w')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    doesnotexistcatch_condition[0] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':
                                        os.chdir('..')
                                        pass

                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses, number_of_externalizations = count_initiation_response(
                                            rawdata_filename,
                                            number_of_initiations,
                                            number_of_responses, trial, condition, phase)

                                        #
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all2.write(line)

                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")




                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i - 1][0] = number_of_initiations
                                        number_of_initiation_response_array[i - 1][1] = number_of_responses
                                        number_of_initiation_response_array[i - 1][2] = number_of_externalizations

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    doesnotexistcatch_condition[1] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':
                                        os.chdir('..')
                                        pass

                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses, number_of_externalizations = count_initiation_response(
                                            rawdata_filename,
                                            number_of_initiations,
                                            number_of_responses, trial, condition, phase)

                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all2.write(line)

                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")


                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i - 1][3] = number_of_initiations
                                        number_of_initiation_response_array[i - 1][4] = number_of_responses
                                        number_of_initiation_response_array[i - 1][5] = number_of_externalizations

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                else:

                                    continue
                            # if j == 1:
                            #
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W1'
                            #             # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #             #                doesnotexistcatch_ciera[P]
                            #             # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            #
                            # elif j == 2:
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W2'
                            #             # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #             #                doesnotexistcatch_juan[P]
                            #             # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            output_kubios_time_all2.close()
                            data = pd.read_csv(
                                'output_kubios_all_' + trial + '_' + 'LEGO' + '_' + 'time_WO_headers2.txt', sep='\t',
                                names=['a', 'b', 'c'], dtype={'High': np.float64, 'Low': np.float64})
                            print data
                            data2 = data.sort_values(by=['a'], ascending=True)

                            data2.to_csv('output_kubios_all_' + trial + '_' + 'LEGO' + '_' + 'time_WO_headers3.txt',
                                         sep='\t', index=False)

                            os.chdir('..')

                        elif str(arr[k - 1]) == "LOF":
                            condition = "LOF"
                            doesnotexistcatch[0] = 1
                            os.chdir('./' + condition + '/')

                            prr = os.listdir('.')

                            doesnotexistcatch_condition = [0, 0]
                            doesnotexistcatch_phase = ["first", "last"]
                            output_kubios_time_all = open(
                                'output_kubios_all_' + trial + '_' + 'LOF' + '_' + 'time2.txt', 'w')
                            output_kubios_time_all2 = open(
                                'output_kubios_all_' + trial + '_' + 'LOF' + '_' + 'time_WO_headers2.txt', 'w')
                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    doesnotexistcatch_condition[0] = 1
                                    os.chdir('./' + phase + '/')

                                    # extract_ECG_features(trial, participant, condition)
                                    if newest('.') == 'nothing':

                                        os.chdir('..')
                                        pass
                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses, number_of_externalizations = count_initiation_response(
                                            rawdata_filename,
                                            number_of_initiations,
                                            number_of_responses, trial, condition, phase)
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]

                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all2.write(line)

                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")

                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i - 1][6] = number_of_initiations
                                        number_of_initiation_response_array[i - 1][7] = number_of_responses
                                        number_of_initiation_response_array[i - 1][8] = number_of_externalizations

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    doesnotexistcatch_condition[1] = 1
                                    os.chdir('./' + phase + '/')
                                    if newest('.') == 'nothing':

                                        os.chdir('..')
                                        pass
                                    else:
                                        rawdata_filename = newest('.')
                                        number_of_initiations, number_of_responses, number_of_externalizations = count_initiation_response(
                                            rawdata_filename,
                                            number_of_initiations,
                                            number_of_responses, trial, condition, phase)
                                        rawdata_name4 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]

                                        f = open(rawdata_name4, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all.write(line)

                                        rawdata_name5 = 'output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time_WO_headers2.txt'

                                        f = open(rawdata_name5, 'r+')
                                        for line in f.readlines():
                                            # write line to output file
                                            output_kubios_time_all2.write(line)

                                        # data4 = pd.read_csv(rawdata_name4, sep='\t')
                                        # length_kubios = data4.shape[0]
                                        # print length_kubios
                                        #
                                        # for i in range(0, length_kubios-4):
                                        #     start_kubios = str(data4.iat[i, 0])
                                        #     end_kubios = str(data4.iat[i, 1])
                                        #     output_kubios_time_all.write(start_kubios + '\t' + end_kubios)
                                        #     output_kubios_time_all.write("\n")

                                        print number_of_initiations
                                        print number_of_responses
                                        result_array[1][0] = number_of_initiations
                                        result_array[0][0] = number_of_responses

                                        number_of_initiation_response_array[i - 1][9] = number_of_initiations
                                        number_of_initiation_response_array[i - 1][10] = number_of_responses
                                        number_of_initiation_response_array[i - 1][11] = number_of_externalizations

                                        # extract_ECG_features(trial, participant, condition)

                                        # name = 'output_' + trial + ';' + str(participant) + ';' + condition
                                        # output_feature.write(name + ";" +'initiation' +";" + str(number_of_initiations) + "\n")
                                        # output_feature.write(name + ";" +'response' +";"+ str(number_of_responses) + "\n")
                                        # output_feature.write(name + ";" +'externalization' +";"+ str(number_of_externalizations) + "\n")

                                        print phase

                                        os.chdir('..')
                                else:
                                    continue
                            # if j == 1:
                            #
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W'
                            #         # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #         #                doesnotexistcatch_ciera[P]
                            #         # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue
                            #
                            # elif j == 2:
                            #     for P in range(0, len(doesnotexistcatch_condition) - 1):
                            #         if doesnotexistcatch_condition[P] == 0:
                            #             print 'W'
                            #         # rawdata_name = 'output_' + trial + ';' + str(participant) + ';' + \
                            #         #                doesnotexistcatch_juan[P]
                            #         # output_feature.write(rawdata_name + " " + "\n")
                            #         else:
                            #             continue

                            output_kubios_time_all2.close()
                            data = pd.read_csv(
                                'output_kubios_all_' + trial + '_' + 'LOF' + '_' + 'time_WO_headers2.txt', sep='\t',
                                names=['a', 'b', 'c'], dtype={'High': np.float64, 'Low': np.float64})
                            print data
                            data2 = data.sort_values(by=['a'], ascending=True)

                            data2.to_csv('output_kubios_all_' + trial + '_' + 'LOF' + '_' + 'time_WO_headers3.txt',
                                         sep='\t', index=False)

                            os.chdir('..')

                        # elif str(arr[k - 1]) == "ZDOESNOTEXIST":
                        #     print doesnotexistcatch
                        #     print "batu"
                        #     if doesnotexistcatch[0] == 1 and doesnotexistcatch[1] == 0:
                        #         # rawdata_name = 'output_' + trial + ';' + str(
                        #         #     participant) + ';' + "LOF" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                        #         # output_feature.write(rawdata_name + " " + "\n")
                        #         doesnotexistcatch[0] == 0
                        #         doesnotexistcatch[1] == 0
                        #     elif doesnotexistcatch[0] == 0 and doesnotexistcatch[1] == 1:
                        #         # rawdata_name = 'output_' + trial + ';' + str(
                        #         #     participant) + ';' + "LEGO" + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';' + ';'
                        #         # output_feature.write(rawdata_name + " " + "\n")
                        #         doesnotexistcatch[0] == 0
                        #         doesnotexistcatch[1] == 0
                        #     else:
                        #         continue

                        else:

                            continue
                    os.chdir('..')
                else:
                    continue

    output_feature = open('all_features_video_coding_NONASC.txt', 'w')
    output_all_feature = open('initiation.txt', 'w')
    output_all_feature1 = open('response.txt', 'w')
    output_all_feature2 = open('externalization.txt', 'w')

    print number_of_initiation_response_array
    print trial_array

    for i in range(0, numberofexperiments):

        for k in range(0, 2):
            if k == 0:
                phase = 'LEGO'

                output_all_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'initiation,')
                output_all_feature.write(str(int(number_of_initiation_response_array[i][0])) + ",")
                output_all_feature.write(str(int(number_of_initiation_response_array[i][3])) + ",")
                output_all_feature.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'initiation,')
                output_feature.write(str(int(number_of_initiation_response_array[i][0])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][3])) + ",")
                output_feature.write("\n")

                output_all_feature1.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'response,')
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][1])) + ",")
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][4])) + ",")
                output_all_feature1.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'response,')
                output_feature.write(str(int(number_of_initiation_response_array[i][1])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][4])) + ",")
                output_feature.write("\n")

                output_all_feature2.write(
                    'output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'externalization,')
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][2])) + ",")
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][5])) + ",")
                output_all_feature2.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'externalization,')
                output_feature.write(str(int(number_of_initiation_response_array[i][2])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][5])) + ",")
                output_feature.write("\n")

            elif k == 1:
                phase = 'LOF'

                output_all_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'initiation,')
                output_all_feature.write(str(int(number_of_initiation_response_array[i][6])) + ",")
                output_all_feature.write(str(int(number_of_initiation_response_array[i][9])) + ",")
                output_all_feature.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'initiation,')
                output_feature.write(str(int(number_of_initiation_response_array[i][6])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][9])) + ",")
                output_feature.write("\n")

                output_all_feature1.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'response,')
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][7])) + ",")
                output_all_feature1.write(str(int(number_of_initiation_response_array[i][10])) + ",")
                output_all_feature1.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'response,')
                output_feature.write(str(int(number_of_initiation_response_array[i][7])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][10])) + ",")
                output_feature.write("\n")

                output_all_feature2.write(
                    'output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'externalization,')
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][8])) + ",")
                output_all_feature2.write(str(int(number_of_initiation_response_array[i][11])) + ",")
                output_all_feature2.write("\n")

                output_feature.write('output_' + trial_array[i] + "," + "44" + "," + phase + ',' + 'externalization,')
                output_feature.write(str(int(number_of_initiation_response_array[i][8])) + ",")
                output_feature.write(str(int(number_of_initiation_response_array[i][11])) + ",")
                output_feature.write("\n")

    os.chdir('..')  #

#########stage 4
def systemlog_feature_extraction2():
    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_merge_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_merge_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_merge_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window)+ '\t'  '5')
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):

            #####FEATURE .................find the timestamp for first char creature
            if flag == 0:
                if (action[k] == 'character_creator' and player[k] == 'Player1'):
                    time_of_first_char[i - 1][0] = 1
                    time_of_first_char[i - 1][1] = time[k]
                    sync_time_array[i - 1][0] = 1
                    sync_time_array[i - 1][1] = start_time
                if (action[k] == 'character_creator' and player[k] == 'Player2'):
                    time_of_first_char[i - 1][2] = 2
                    time_of_first_char[i - 1][3] = time[k]
                    sync_time_array[i - 1][2] = 2
                    sync_time_array[i - 1][3] = start_time
            elif flag == 1:

                if (action[k] == 'character_creator' and player[k] == 'Player1'):
                    time_of_first_char2[i - 1][0] = 1
                    time_of_first_char2[i - 1][1] = time[k]
                    sync_time_array2[i - 1][0] = 1
                    sync_time_array2[i - 1][1] = start_time
                if (action[k] == 'character_creator' and player[k] == 'Player2'):
                    time_of_first_char2[i - 1][2] = 2
                    time_of_first_char2[i - 1][3] = time[k]
                    sync_time_array2[i - 1][2] = 2
                    sync_time_array2[i - 1][3] = start_time

                    ####FEATURE .................find the # of merges

            if (action[k] == 'creature_merge' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'creature_merge'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'creature_merge'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'creature_merge'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)

    test = open('0010_real_time_of_first_char_creation.txt', 'w')
    for i in range(0, numberofexperiments):
        for j in range(0, 4):
            test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array[i][j])) + ",")
            # test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array2[i][j]))+",")
        test.write("\n")

    result_merged_creature = open('0009_a_result_#of_merged_creature.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_merged_creature2.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_merged_creature,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_merged_creature,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction_customizable(PLAYER, FEATURE):
    player_var = PLAYER
    feature_var = FEATURE

    def create_merge_time_array_text(merge_time_array, phase):
        print ("create_merge_time_array_text")
        # output_merge_time = open('output_greeting_time_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_merge_time_array_text2(merge_time_array, phase):
        print ("create_merge_time_array_text2")
        # output_merge_time = open('output_greeting_time2_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_kubios_merge_time_array_text(merge_time_array, phase):
        print ("create_kubios_merge_time_array_text")
        # output_merge_time = open('output_kubios_greeting_time_' + trial + '_' + phase + '_3.txt', 'w')
        # # output_merge_time.write('time' + '\t' + 'nid')
        # # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     # if float(merge_time_array[
        #     #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
        #     #     continue
        #     # else:
        #     kubios_time_window = float(merge_time_array[i]) + 30
        #     if kubios_time_window>900:
        #          kubios_time_window=900
        #
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
        #     output_merge_time.write("\n")

    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag, player_var, feature_var):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []


        for k in range(0, len(time)):

            #####FEATURE .................find the timestamp for first char creature
            # if flag == 0:
            #     if (action[k] == 'character_creator' and player[k] == 'Player1'):
            #         time_of_first_char[i - 1][0] = 1
            #         time_of_first_char[i - 1][1] = time[k]
            #         sync_time_array[i - 1][0] = 1
            #         sync_time_array[i - 1][1] = start_time
            #     if (action[k] == 'character_creator' and player[k] == 'Player2'):
            #         time_of_first_char[i - 1][2] = 2
            #         time_of_first_char[i - 1][3] = time[k]
            #         sync_time_array[i - 1][2] = 2
            #         sync_time_array[i - 1][3] = start_time
            # elif flag == 1:
            #
            #     if (action[k] == 'character_creator' and player[k] == 'Player1'):
            #         time_of_first_char2[i - 1][0] = 1
            #         time_of_first_char2[i - 1][1] = time[k]
            #         sync_time_array2[i - 1][0] = 1
            #         sync_time_array2[i - 1][1] = start_time
            #     if (action[k] == 'character_creator' and player[k] == 'Player2'):
            #         time_of_first_char2[i - 1][2] = 2
            #         time_of_first_char2[i - 1][3] = time[k]
            #         sync_time_array2[i - 1][2] = 2
            #         sync_time_array2[i - 1][3] = start_time

            ####FEATURE .................find the # of merges

            # print player_var
            # print feature_var

            if player_var == "manipulateprop":
                if (float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events = count_merge_events + 1
                        print time[k]
                        merge_time_array.append(str(float(time[k]) - float(start_time)))

                if (float(time[k]) <= 300 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_first = count_merge_events_first + 1
                        merge_time_array_first.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_mid = count_merge_events_mid + 1
                        merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_last = count_merge_events_last + 1
                        merge_time_array_last.append(str(float(time[k]) - float(start_time)))
            else:
                if (float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events = count_merge_events + 1
                        print time[k]
                        merge_time_array.append(str(float(time[k]) - float(start_time)))

                if (float(time[k]) <= 300 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_first = count_merge_events_first + 1
                        merge_time_array_first.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_mid = count_merge_events_mid + 1
                        merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_last = count_merge_events_last + 1
                        merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []


    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')
        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag, player_var, feature_var)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)






                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")




                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)







                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)


                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    # test = open('0010_real_time_of_first_char_creation.txt', 'w')
    # for i in range(0, numberofexperiments):
    #     for j in range(0, 4):
    #         test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array[i][j])) + ",")
    #         # test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array2[i][j]))+",")
    #     test.write("\n")

    if player_var == True:
        player_var = "manipulateprop"

    os.chdir(system_log_output_destination)

    if player_var =="Player1" or player_var =="Creature1":
        name="1"
    elif player_var =="Player2" or player_var =="Creature2":
        name = "2"
    elif player_var == "manipulateprop":
        name = "3"

    if feature_var=="greeting":
        result_merged_creature = open("0001_a_"+name+"_"+player_var+"result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open("0001_b_"+name+"_"+player_var+"result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    elif feature_var=="hunted_insect":
        result_merged_creature = open(
            "0002_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open(
            "0002_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    elif feature_var=="creature_changed":
        result_merged_creature = open(
            "0003_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open(
            "0003_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    elif feature_var=="look_up":
        result_merged_creature = open(
            "0004_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open(
            "0004_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    elif feature_var=="point_at":
        result_merged_creature = open(
            "0005_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open(
            "0005_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    elif feature_var=="manipulate_prop":
        result_merged_creature = open(
            "0006_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
        result_merged_creature2 = open(
            "0006_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')


    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + "#of_" + feature_var + "_" + player_var + ",")
        result_merged_creature2.write(
            'output_' + trial_array[i] + "," + "#of_2_" + feature_var + "_" + player_var + ",")
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction_customizable_event(PLAYER, FEATURE):
    player_var = PLAYER
    feature_var = FEATURE
    nid =""

    def create_merge_time_array_text(merge_time_array, phase,player_var,feature_var):
        system_event_type = feature_var


        if player_var == "Creature1" or player_var == "Player1":
            participant_no = "Participant1"
        elif player_var == "Creature2" or player_var == "Player2":
            participant_no = "Participant2"


        if system_event_type == "greeting":
            nid = "7"
        elif system_event_type == "creature_changed":
            nid = "8"
        elif system_event_type == "point_at":
            nid = "9"
        elif system_event_type == "look_up":
            nid = "10"
        elif system_event_type == "character_creator":
            nid = "11"


        os.chdir(system_log_output_destination + trial)
        output_merge_time = open("output_"+system_event_type+"_" + trial + '_' + phase + "_"+participant_no+'.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + nid)
            output_merge_time.write("\n")
        os.chdir(system_log_output_destination + trial)

    def create_merge_time_array_text2(merge_time_array, phase,player_var,feature_var):
        system_event_type = feature_var
        if player_var == "Creature1" or player_var == "Player1":
            participant_no = "Participant1"
        elif player_var == "Creature2" or player_var == "Player2":
            participant_no = "Participant2"

        if system_event_type == "greeting":
            nid = "7"
        elif system_event_type == "creature_changed":
            nid = "8"
        elif system_event_type == "point_at":
            nid = "9"
        elif system_event_type == "look_up":
            nid = "10"
        elif system_event_type == "character_creator":
            nid = "11"


        os.chdir(system_log_output_destination + trial)
        output_merge_time = open("output_"+system_event_type+"_" + trial + '_' + phase +"_"+participant_no +'.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + nid)
            output_merge_time.write("\n")
        os.chdir(system_log_output_destination + trial)

    def create_kubios_merge_time_array_text(merge_time_array, phase,player_var,feature_var):


        system_event_type = feature_var
        if player_var == "Creature1" or player_var == "Player1":
            participant_no = "Participant1"
        elif player_var == "Creature2" or player_var == "Player2":
            participant_no = "Participant2"


        if system_event_type == "greeting":
            nid = "7"
        elif system_event_type == "creature_changed":
            nid = "8"
        elif system_event_type == "point_at":
            nid = "9"
        elif system_event_type == "look_up":
            nid = "10"
        elif system_event_type == "character_creator":
            nid = "11"

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open("output_kubios_"+system_event_type+"_" + trial + '_' + phase +"_"+participant_no + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window>900:
                 kubios_time_window=900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window)+ '\t'+ nid)
            output_merge_time.write("\n")
        os.chdir(system_log_output_destination + trial)

    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag, player_var, feature_var):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []


        for k in range(0, len(time)):

            #####FEATURE .................find the timestamp for first char creature
            # if flag == 0:
            #     if (action[k] == 'character_creator' and player[k] == 'Player1'):
            #         time_of_first_char[i - 1][0] = 1
            #         time_of_first_char[i - 1][1] = time[k]
            #         sync_time_array[i - 1][0] = 1
            #         sync_time_array[i - 1][1] = start_time
            #     if (action[k] == 'character_creator' and player[k] == 'Player2'):
            #         time_of_first_char[i - 1][2] = 2
            #         time_of_first_char[i - 1][3] = time[k]
            #         sync_time_array[i - 1][2] = 2
            #         sync_time_array[i - 1][3] = start_time
            # elif flag == 1:
            #
            #     if (action[k] == 'character_creator' and player[k] == 'Player1'):
            #         time_of_first_char2[i - 1][0] = 1
            #         time_of_first_char2[i - 1][1] = time[k]
            #         sync_time_array2[i - 1][0] = 1
            #         sync_time_array2[i - 1][1] = start_time
            #     if (action[k] == 'character_creator' and player[k] == 'Player2'):
            #         time_of_first_char2[i - 1][2] = 2
            #         time_of_first_char2[i - 1][3] = time[k]
            #         sync_time_array2[i - 1][2] = 2
            #         sync_time_array2[i - 1][3] = start_time

            ####FEATURE .................find the # of merges

            # print player_var
            # print feature_var

            if player_var == "manipulateprop":
                if (float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events = count_merge_events + 1
                        print time[k]
                        merge_time_array.append(str(float(time[k]) - float(start_time)))

                if (float(time[k]) <= 300 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_first = count_merge_events_first + 1
                        merge_time_array_first.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_mid = count_merge_events_mid + 1
                        merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var):
                        count_merge_events_last = count_merge_events_last + 1
                        merge_time_array_last.append(str(float(time[k]) - float(start_time)))
            else:
                if (float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events = count_merge_events + 1
                        print time[k]
                        merge_time_array.append(str(float(time[k]) - float(start_time)))

                if (float(time[k]) <= 300 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_first = count_merge_events_first + 1
                        merge_time_array_first.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_mid = count_merge_events_mid + 1
                        merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

                elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                    if (action[k] == feature_var and player[k] == player_var):
                        count_merge_events_last = count_merge_events_last + 1
                        merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []


    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')
        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag, player_var, feature_var)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase,player_var,feature_var)
                create_kubios_merge_time_array_text(merge_time_array, phase,player_var,feature_var)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase,player_var,feature_var)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase,player_var,feature_var)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase,player_var,feature_var)






                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")




                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase,player_var,feature_var)
                    create_kubios_merge_time_array_text(merge_time_array, phase,player_var,feature_var)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase,player_var,feature_var)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase,player_var,feature_var)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase,player_var,feature_var)







                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase,player_var,feature_var)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase,player_var,feature_var)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase,player_var,feature_var)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase,player_var,feature_var)


                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase,player_var,feature_var)
                    create_kubios_merge_time_array_text(merge_time_array, phase,player_var,feature_var)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase,player_var,feature_var)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase,player_var,feature_var)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase,player_var,feature_var)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase,player_var,feature_var)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase,player_var,feature_var)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase,player_var,feature_var)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase,player_var,feature_var)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    # test = open('0010_real_time_of_first_char_creation.txt', 'w')
    # for i in range(0, numberofexperiments):
    #     for j in range(0, 4):
    #         test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array[i][j])) + ",")
    #         # test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array2[i][j]))+",")
    #     test.write("\n")

    if player_var == True:
        player_var = "manipulateprop"

    os.chdir(system_log_output_destination)

    if player_var =="Player1" or player_var =="Creature1":
        name="1"
    elif player_var =="Player2" or player_var =="Creature2":
        name = "2"
    elif player_var == "manipulateprop":
        name = "3"

    # if feature_var=="greeting":
    #     result_merged_creature = open("0001_a_"+name+"_"+player_var+"result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open("0001_b_"+name+"_"+player_var+"result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    # elif feature_var=="hunted_insect":
    #     result_merged_creature = open(
    #         "0002_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open(
    #         "0002_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    # elif feature_var=="creature_changed":
    #     result_merged_creature = open(
    #         "0003_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open(
    #         "0003_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    # elif feature_var=="look_up":
    #     result_merged_creature = open(
    #         "0004_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open(
    #         "0004_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    # elif feature_var=="point_at":
    #     result_merged_creature = open(
    #         "0005_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open(
    #         "0005_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')
    # elif feature_var=="manipulate_prop":
    #     result_merged_creature = open(
    #         "0006_a_" + name + "_" + player_var + "result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    #     result_merged_creature2 = open(
    #         "0006_b_" + name + "_" + player_var + "result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')


    # for i in range(0, numberofexperiments):
    #     result_merged_creature.write('output_' + trial_array[i] + "," + "#of_" + feature_var + "_" + player_var + ",")
    #     result_merged_creature2.write(
    #         'output_' + trial_array[i] + "," + "#of_2_" + feature_var + "_" + player_var + ",")
    #     for j in range(0, 4):
    #         result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
    #         result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
    #     result_merged_creature.write("\n")
    #     result_merged_creature2.write("\n")
    os.chdir('..')
def define_ASC_NONASC():
    trial_array = []
    lof_2_stages = []
    #####################################
    experiment_order_system_log = pd.read_csv(input_directory_path+ "experiment_order_systemlog.csv")

    #print experiment_order_system_log

    def change_name_system(player_var_Player,player_var_Creature):
        ###############################START OF FEATURE EXTRACTION
        list = []
        for x in os.listdir('.'):
            list.append(str(x))

        list3 = []
        list4 = []

        for t in range(0, len(list)):
            name_kubious = list[t]
            is_name_kubious = name_kubious[0:7]
            end_kubious = name_kubious[-7:]
            end_kubious2 = name_kubious[-5:]

            if is_name_kubious == "output_" and end_kubious == "1_3.txt":
                list3.append(list[t])
            if is_name_kubious == "output_" and end_kubious == "2_3.txt":
                list4.append(list[t])

            if is_name_kubious == "output_" and end_kubious2 == "1.txt":
                list3.append(list[t])
            if is_name_kubious == "output_" and end_kubious2 == "2.txt":
                list4.append(list[t])

        print list3
        print list4

        def copy_text_system(input, output,participant_name):

            shutil.copyfile(input, output + "_" + participant_name + ".txt")

        for t in range(0, len(list3)):
            name_kubious = list3[t]
            name_kubious_wo_txt = name_kubious[:-4]

            result7 = name_kubious.find('greeting')
            result8 = name_kubious.find('creature_changed')
            result9 = name_kubious.find('point_at')
            result10 = name_kubious.find('look_up')
            result11 = name_kubious.find('character_creator')

            if result7 != -1:

                #print "player_var_Creature: " +str(player_var_Creature[-1:])
                if player_var_Creature[-1:]== "1":
                    participant_name = "ASC"
                elif player_var_Creature[-1:]== "2":
                    participant_name = "NONASC"
                copy_text_system (name_kubious,name_kubious_wo_txt,participant_name)
            elif result8 != -1:
                if player_var_Player[-1:]== "1":
                    participant_name = "ASC"
                elif player_var_Player[-1:]== "2":
                    participant_name = "NONASC"
                copy_text_system (name_kubious,name_kubious_wo_txt,participant_name)

            elif result9 != -1:
                if player_var_Creature[-1:] == "1":
                    participant_name = "ASC"
                elif player_var_Creature[-1:] == "2":
                    participant_name = "NONASC"
                copy_text_system(name_kubious, name_kubious_wo_txt, participant_name)

            elif result10 != -1:
                if player_var_Creature[-1:] == "1":
                    participant_name = "ASC"
                elif player_var_Creature[-1:] == "2":
                    participant_name = "NONASC"
                copy_text_system(name_kubious, name_kubious_wo_txt, participant_name)

            elif result11 != -1:
                if player_var_Player[-1:] == "1":
                    participant_name = "ASC"
                elif player_var_Player[-1:] == "2":
                    participant_name = "NONASC"
                copy_text_system(name_kubious, name_kubious_wo_txt, participant_name)

        for t in range(0, len(list4)):
            name_kubious2 = list4[t]
            name_kubious_wo_txt2 = name_kubious2[:-4]


            result7 = name_kubious2.find('greeting')
            result8 = name_kubious2.find('creature_changed')
            result9 = name_kubious2.find('point_at')
            result10 = name_kubious2.find('look_up')
            result11 = name_kubious2.find('character_creator')

            if result7 != -1:
                if player_var_Creature[-1:]== "1":
                    participant_name = "NONASC"
                elif player_var_Creature[-1:]== "2":
                    participant_name = "ASC"
                copy_text_system (name_kubious2,name_kubious_wo_txt2,participant_name)
            elif result8 != -1:
                if player_var_Player[-1:]== "1":
                    participant_name = "NONASC"
                elif player_var_Player[-1:]== "2":
                    participant_name = "ASC"
                copy_text_system (name_kubious2,name_kubious_wo_txt2,participant_name)

            elif result9 != -1:
                if player_var_Creature[-1:] == "1":
                    participant_name = "NONASC"
                elif player_var_Creature[-1:] == "2":
                    participant_name = "ASC"
                copy_text_system(name_kubious2, name_kubious_wo_txt2, participant_name)

            elif result10 != -1:
                if player_var_Creature[-1:] == "1":
                    participant_name = "NONASC"
                elif player_var_Creature[-1:] == "2":
                    participant_name = "ASC"
                copy_text_system(name_kubious2, name_kubious_wo_txt2, participant_name)

            elif result11 != -1:
                if player_var_Player[-1:] == "1":
                    participant_name = "NONASC"
                elif player_var_Player[-1:] == "2":
                    participant_name = "ASC"
                copy_text_system(name_kubious2, name_kubious_wo_txt2, participant_name)







    for i in range(1, numberofexperiments + 1):
        os.chdir(output_directory_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10

            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            index_system = int(trial)

            print trial
            print experiment_order_system_log.experiment[index_system-1]

            player_var_Player=  experiment_order_system_log.iloc[index_system-1]['Player']
            player_var_Creature =experiment_order_system_log.iloc[index_system - 1]['Creature']
            #experiment_order_system_log.loc[experiment_order_system_log['experiment'] == some_value]
            change_name_system(player_var_Player,player_var_Creature)


            os.chdir('..')



def systemlog_feature_extraction_total_area(PLAYER, FEATURE):
    player_var = PLAYER
    feature_var = FEATURE

    def create_merge_time_array_text(merge_time_array, phase):
        print ("create_merge_time_array_text")
        # output_merge_time = open('output_greeting_time_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_merge_time_array_text2(merge_time_array, phase):
        print ("create_merge_time_array_text2")
        # output_merge_time = open('output_greeting_time2_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_kubios_merge_time_array_text(merge_time_array, phase):
        print ("create_kubios_merge_time_array_text")
        # output_merge_time = open('output_kubios_greeting_time_' + trial + '_' + phase + '_3.txt', 'w')
        # # output_merge_time.write('time' + '\t' + 'nid')
        # # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     # if float(merge_time_array[
        #     #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
        #     #     continue
        #     # else:
        #     kubios_time_window = float(merge_time_array[i]) + 30
        #     if kubios_time_window>900:
        #          kubios_time_window=900
        #
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
        #     output_merge_time.write("\n")

    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag, player_var, feature_var,dataframe):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        dataframe_pos = dataframe[dataframe.action == "pos"]

        dataframe_pos_player = dataframe_pos[dataframe_pos.actor == player_var]

        threshold = dataframe_pos["time"].iloc[-1] + start_time

        print dataframe_pos_player

        def find_total_area_traveled(dataframe_player,phase_type):

            if phase_type == "total":
                dataframe_player = dataframe_player[dataframe_player["time"]<= 900 + start_time]

            elif phase_type == "first":
                dataframe_player = dataframe_player[dataframe_player["time"]<= 300 + start_time]

            elif phase_type == "mid":

                if (600 + start_time) <= threshold:
                    dataframe_player = dataframe_player[dataframe_player["time"]> 300 + start_time]
                    dataframe_player = dataframe_player[dataframe_player["time"] <= 600 + start_time]

                else:
                    dataframe_player = dataframe_player[
                        dataframe_player["time"] > 300 + start_time]
                    dataframe_player = dataframe_player[dataframe_player["time"] <= threshold]


            elif phase_type == "last":

                if (900 + start_time) <= threshold:
                    dataframe_player = dataframe_player[dataframe_player["time"]> 600 + start_time]
                    dataframe_player = dataframe_player[dataframe_player["time"] <= 900 + start_time]

                else:
                    dataframe_player = dataframe_player[
                        dataframe_player["time"] > 600 + start_time]
                    dataframe_player = dataframe_player[dataframe_player["time"] <= threshold]


            dataframe_player_just_pos = dataframe_player[["x", "y"]]
            dataframe_player_diff = dataframe_player_just_pos.diff()
            dataframe_player_square = np.square(dataframe_player_diff)
            dataframe_player_square["total"] = dataframe_player_square["x"] + dataframe_player_square["y"]
            dataframe_player_square["sqrt"] = np.sqrt((dataframe_player_square['total']))
            Total = dataframe_player_square['sqrt'].sum()
            return Total

        player_total_area = find_total_area_traveled(dataframe_pos_player,"total")
        player_first_area = find_total_area_traveled(dataframe_pos_player,"first")
        player_mid_area = find_total_area_traveled(dataframe_pos_player,"last")
        player_last_area = find_total_area_traveled(dataframe_pos_player,"mid")

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,player_total_area,player_first_area,player_mid_area,player_last_area

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []


    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')
        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3  or i == skipped_experiment4 :  # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)

                    dataset_name = rawdata_filename
                    colnames = ['time', 'actor', 'action', 'x', 'y']
                    dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)
                    dataset_name = rawdata_filename
                    colnames = ['time', 'actor', 'action', 'x', 'y']
                    dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag, player_var, feature_var,dataframe)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)


                count_merge_array[i - 1][0] = first_area
                count_merge_array[i - 1][1] = mid_area
                count_merge_array[i - 1][2] = last_area
                count_merge_array[i - 1][3] = total_area


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)







                    count_merge_array[i - 1][0] = first_area
                    count_merge_array[i - 1][1] = mid_area
                    count_merge_array[i - 1][2] = last_area
                    count_merge_array[i - 1][3] = total_area

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)


                    count_merge_array[i - 1][0] = first_area
                    count_merge_array[i - 1][1] = mid_area
                    count_merge_array[i - 1][2] = last_area
                    count_merge_array[i - 1][3] = total_area

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first_area
                    count_merge_array[i - 1][1] = mid_area
                    count_merge_array[i - 1][2] = last_area
                    count_merge_array[i - 1][3] = total_area

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area2,first_area2,mid_area2,last_area2 = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first_area2
                    count_merge_array2[i - 1][1] = mid_area2
                    count_merge_array2[i - 1][2] = last_area2
                    count_merge_array2[i - 1][3] = total_area2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    # test = open('0010_real_time_of_first_char_creation.txt', 'w')
    # for i in range(0, numberofexperiments):
    #     for j in range(0, 4):
    #         test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array[i][j])) + ",")
    #         # test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array2[i][j]))+",")
    #     test.write("\n")

    if player_var == True:
        player_var = "manipulateprop"



    if player_var =="Player1" or player_var =="Creature1":
        name="1"
    elif player_var =="Player2" or player_var =="Creature2":
        name = "2"

    os.chdir(system_log_output_destination)

    result_merged_creature = open("0007_a_"+name+"_"+player_var+"result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    result_merged_creature2 = open("0007_b_"+name+"_"+player_var+"result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')


    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + "#of_" + feature_var + "_" + player_var + ",")
        result_merged_creature2.write(
            'output_' + trial_array[i] + "," + "#of_2_" + feature_var + "_" + player_var + ",")
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction_calculate_distance_between():
    player_var = 'distance'
    feature_var = "between"

    def create_merge_time_array_text(merge_time_array, phase):
        print ("create_merge_time_array_text")
        # output_merge_time = open('output_greeting_time_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_merge_time_array_text2(merge_time_array, phase):
        print ("create_merge_time_array_text2")
        # output_merge_time = open('output_greeting_time2_' + trial + '_' + phase + '_.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
        #     output_merge_time.write("\n")

    def create_kubios_merge_time_array_text(merge_time_array, phase):
        print ("create_kubios_merge_time_array_text")
        # output_merge_time = open('output_kubios_greeting_time_' + trial + '_' + phase + '_3.txt', 'w')
        # # output_merge_time.write('time' + '\t' + 'nid')
        # # output_merge_time.write("\n")
        # for i in range(0, len(merge_time_array)):
        #     # if float(merge_time_array[
        #     #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
        #     #     continue
        #     # else:
        #     kubios_time_window = float(merge_time_array[i]) + 30
        #     if kubios_time_window>900:
        #          kubios_time_window=900
        #
        #     output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
        #     output_merge_time.write("\n")

    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag, player_var, feature_var,dataframe):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []




        dataframe_pos = dataframe[dataframe.action == "pos"]
        dataframe_pos_player1 = dataframe_pos[dataframe_pos.actor == "Player1"]
        dataframe_pos_player2 = dataframe_pos[dataframe_pos.actor == "Player2"]

        dataframe_pos_player1['caseno'] = np.arange(len(dataframe_pos_player1))
        dataframe_pos_player2['caseno'] = np.arange(len(dataframe_pos_player2))
        dataframe_player_just_pos_1 = dataframe_pos_player1[["caseno", "time","x", "y"]]
        dataframe_player_just_pos_2 = dataframe_pos_player2[["caseno", "time","x", "y"]]
        dataframe_player_just_pos_1 = dataframe_player_just_pos_1.set_index("caseno")
        dataframe_player_just_pos_2 = dataframe_player_just_pos_2.set_index("caseno")


        threshold = dataframe_pos["time"].iloc[-1] + start_time

        def calculate_distance_between(dataframe_player_just_pos_1, dataframe_player_just_pos_2,phase_type):


            if phase_type == "total":
                dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"]<= 900 + start_time]
                dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"]<= 900 + start_time]
            elif phase_type == "first":
                dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"]<= 300 + start_time]
                dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"]<= 300 + start_time]
            elif phase_type == "mid":

                if (600 + start_time) <= threshold:
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"]> 300 + start_time]
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"] <= 600 + start_time]

                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] > 300 + start_time]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] <= 600 + start_time]
                else:
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[
                        dataframe_player_just_pos_1["time"] > 300 + start_time]
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"] <= threshold]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[
                        dataframe_player_just_pos_2["time"] > 300 + start_time]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] <= threshold]

            elif phase_type == "last":

                if (900 + start_time) <= threshold:
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"]> 600 + start_time]
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"] <= 900 + start_time]

                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] > 600 + start_time]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] <= 900 + start_time]
                else:
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[
                        dataframe_player_just_pos_1["time"] > 600 + start_time]
                    dataframe_player_just_pos_1 = dataframe_player_just_pos_1[dataframe_player_just_pos_1["time"] <= threshold]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[
                        dataframe_player_just_pos_2["time"] > 600 + start_time]
                    dataframe_player_just_pos_2 = dataframe_player_just_pos_2[dataframe_player_just_pos_2["time"] <= threshold]


            dataframe_player_just_substract = dataframe_player_just_pos_1 - dataframe_player_just_pos_2
            dataframe_player_just_substract_square = np.square(dataframe_player_just_substract)
            dataframe_player_just_substract_square["total"] = dataframe_player_just_substract_square["x"] + \
                                                              dataframe_player_just_substract_square["y"]
            dataframe_player_just_substract_square["sqrt"] = np.sqrt((dataframe_player_just_substract_square['total']))
            Total = dataframe_player_just_substract_square['sqrt'].sum()
            Average = float (Total / float(len(dataframe_pos_player1)))

            print "Average___" + str(Average)

            return Average



        player_total_area = calculate_distance_between(dataframe_player_just_pos_1, dataframe_player_just_pos_2,"total")
        player_first_area = calculate_distance_between(dataframe_player_just_pos_1, dataframe_player_just_pos_2,"first")
        player_mid_area = calculate_distance_between(dataframe_player_just_pos_1, dataframe_player_just_pos_2,"mid")
        player_last_area = calculate_distance_between(dataframe_player_just_pos_1, dataframe_player_just_pos_2,"last")


        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,player_total_area,player_first_area,player_mid_area,player_last_area

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []


    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')
        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4 :  # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)

                    dataset_name = rawdata_filename
                    colnames = ['time', 'actor', 'action', 'x', 'y']
                    dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)
                    dataset_name = rawdata_filename
                    colnames = ['time', 'actor', 'action', 'x', 'y']
                    dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)


                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag, player_var, feature_var,dataframe)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)


                count_merge_array[i - 1][0] = float(first_area)
                count_merge_array[i - 1][1] = float(mid_area)
                count_merge_array[i - 1][2] = float(last_area)
                count_merge_array[i - 1][3] = float(total_area)


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)







                    count_merge_array[i - 1][0] = float(first_area)
                    count_merge_array[i - 1][1] = float(mid_area)
                    count_merge_array[i - 1][2] = float(last_area)
                    count_merge_array[i - 1][3] = float(total_area)

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)


                    count_merge_array[i - 1][0] = float(first_area)
                    count_merge_array[i - 1][1] = float(mid_area)
                    count_merge_array[i - 1][2] = float(last_area)
                    count_merge_array[i - 1][3] = float(total_area)

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area,first_area,mid_area,last_area = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = float(first_area)
                    count_merge_array[i - 1][1] = float(mid_area)
                    count_merge_array[i - 1][2] = float(last_area)
                    count_merge_array[i - 1][3] = float(total_area)

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=';',skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)
                        dataset_name = rawdata_filename
                        colnames = ['time', 'actor', 'action', 'x', 'y']
                        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep='\t',skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last,total_area2,first_area2,mid_area2,last_area2 = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag, player_var, feature_var,dataframe)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first_area2
                    count_merge_array2[i - 1][1] = mid_area2
                    count_merge_array2[i - 1][2] = last_area2
                    count_merge_array2[i - 1][3] = total_area2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    # test = open('0010_real_time_of_first_char_creation.txt', 'w')
    # for i in range(0, numberofexperiments):
    #     for j in range(0, 4):
    #         test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array[i][j])) + ",")
    #         # test.write(str(datetime.timedelta(seconds=real_time_of_first_char_array2[i][j]))+",")
    #     test.write("\n")

    if player_var == True:
        player_var = "manipulateprop"

    name=""
    if player_var =="Player1" or player_var =="Creature1":
        name="1"
    elif player_var =="Player2" or player_var =="Creature2":
        name = "2"

    os.chdir(system_log_output_destination)
    result_merged_creature = open("0008_a_"+name+"_"+player_var+"result_#of_" + feature_var + "_" + player_var + ".txt", 'w')
    result_merged_creature2 = open("0008_b_"+name+"_"+player_var+"result_#of_" + feature_var + "_2_" + player_var + ".txt", 'w')


    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + "#of_" + feature_var + "_" + player_var + ",")
        result_merged_creature2.write(
            'output_' + trial_array[i] + "," + "#of_2_" + feature_var + "_" + player_var + ",")
        for j in range(0, 4):
            result_merged_creature.write(str(float(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(float(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def create_system_log_summary_dataframes(participant,type_of_phase):
    os.chdir(system_log_output_destination)

    list = []
    for x in os.listdir('.'):
        if x.endswith(".txt"):
            list.append(str(x))
    print list

    def naming(list, i, action, stage, player,type_of_phase):
        dataset_name = list[i]
        colnames = ["trialno", "action", 'first', 'mid', 'last', 'total', 'idle']
        dataframe = pd.read_csv(dataset_name, names=colnames, header=None, sep=',')
        print type_of_phase
        print dataframe

        if type_of_phase=='total':
            dataframe = dataframe[['total']]
            dataframe = dataframe.rename(columns={'total': action + "_" + stage + "_" + player})
        elif type_of_phase=='first':
            dataframe = dataframe[['first']]
            dataframe = dataframe.rename(columns={'first': action + "_" + stage + "_" + player})
        elif type_of_phase=='mid':
            dataframe = dataframe[['mid']]
            dataframe = dataframe.rename(columns={'mid': action + "_" + stage + "_" + player})
        elif type_of_phase=='last':
            dataframe = dataframe[['last']]
            dataframe = dataframe.rename(columns={'last': action + "_" + stage + "_" + player})


        return dataframe

    for i in range(0, len(list)):
        file_text = list[i]
        action = file_text[:4]
        stage = file_text[5:6]
        player = file_text[7:8]
        name = action + "_" + stage + "_" + player
        if action == "0001":
            if stage == "a":
                if player == "1":
                    main_dataframe = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0002":

            if stage == "a":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0003":
            if stage == "a":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0004":
            if stage == "a":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0005":
            if stage == "a":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0006":
            if stage == "a":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0007":
            if stage == "a":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                if player == "1":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
                elif player == "2":
                    main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0008":
            if stage == "a":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0009":
            if stage == "a":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
            elif stage == "b":
                main_dataframe[name] = naming(list, i, action, stage, player,type_of_phase)
        if action == "0010":
            char_find_name = list[i]

    colnames = ["player1_idle", "player1", 'player_2_idle', 'player2', 'idle']
    dataframe = pd.read_csv(char_find_name, names=colnames, header=None, sep=',')
    dataframe_player1 = dataframe[['player1']]
    dataframe_player2 = dataframe[['player2']]

    print char_find_name
    print dataframe_player1.iloc[:, 0]
    print dataframe_player2.iloc[:, 0]
    main_dataframe["0010__1"] = dataframe_player1['player1']
    main_dataframe["0010__2"] = dataframe_player2['player2']

    main_dataframe.to_csv("main_dataframe_"+type_of_phase+".csv")

    print main_dataframe

    ################SECOND PART
    main_dataframe["0001_1"] = main_dataframe["0001_a_1"] + main_dataframe["0001_b_1"]
    main_dataframe["0001_2"] = main_dataframe["0001_a_2"] + main_dataframe["0001_b_2"]
    main_dataframe.drop(labels=['0001_a_1', "0001_b_1", "0001_a_2", "0001_b_2"], axis=1, inplace=True)

    main_dataframe["0002_1"] = main_dataframe["0002_a_1"] + main_dataframe["0002_b_1"]
    main_dataframe["0002_2"] = main_dataframe["0002_a_2"] + main_dataframe["0002_b_2"]
    main_dataframe.drop(labels=['0002_a_1', "0002_b_1", "0002_a_2", "0002_b_2"], axis=1, inplace=True)

    main_dataframe["0003_1"] = main_dataframe["0003_a_1"] + main_dataframe["0003_b_1"]
    main_dataframe["0003_2"] = main_dataframe["0003_a_2"] + main_dataframe["0003_b_2"]
    main_dataframe.drop(labels=['0003_a_1', "0003_b_1", "0003_a_2", "0003_b_2"], axis=1, inplace=True)

    main_dataframe["0004_1"] = main_dataframe["0004_a_1"] + main_dataframe["0004_b_1"]
    main_dataframe["0004_2"] = main_dataframe["0004_a_2"] + main_dataframe["0004_b_2"]
    main_dataframe.drop(labels=['0004_a_1', "0004_b_1", "0004_a_2", "0004_b_2"], axis=1, inplace=True)

    main_dataframe["0005_1"] = main_dataframe["0005_a_1"] + main_dataframe["0005_b_1"]
    main_dataframe["0005_2"] = main_dataframe["0005_a_2"] + main_dataframe["0005_b_2"]
    main_dataframe.drop(labels=['0005_a_1', "0005_b_1", "0005_a_2", "0005_b_2"], axis=1, inplace=True)

    main_dataframe["0006_"] = main_dataframe["0006_a_3"] + main_dataframe["0006_b_3"]
    main_dataframe.drop(labels=['0006_a_3', "0006_b_3"], axis=1, inplace=True)

    main_dataframe["0007_1"] = main_dataframe["0007_a_1"] + main_dataframe["0007_b_1"]
    main_dataframe["0007_2"] = main_dataframe["0007_a_2"] + main_dataframe["0007_b_2"]
    main_dataframe.drop(labels=['0007_a_1', "0007_b_1", "0007_a_2", "0007_b_2"], axis=1, inplace=True)

    main_dataframe["0008_"] = main_dataframe["0008_a__"] + main_dataframe["0008_b__"]
    main_dataframe.drop(labels=['0008_a__', "0008_b__"], axis=1, inplace=True)

    main_dataframe["0009_"] = main_dataframe["0009_a_r"] + main_dataframe["0009_b_r"]
    main_dataframe.drop(labels=['0009_a_r', "0009_b_r"], axis=1, inplace=True)

    main_dataframe["0010_1"] = main_dataframe["0010__1"]
    main_dataframe["0010_2"] = main_dataframe["0010__2"]
    a = main_dataframe["0010_1"]
    for i in range(0, len(a)):
        b = str(a[i])
        c = b.split(':')
        d = float(c[0]) * 60 * 60 + float(c[1]) * 60 + float(c[2])
        a[i] = d
    main_dataframe["0010_1"] = a

    a = main_dataframe["0010_2"]
    for i in range(0, len(a)):
        b = str(a[i])
        c = b.split(':')
        d = float(c[0]) * 60 * 60 + float(c[1]) * 60 + float(c[2])
        a[i] = d
    main_dataframe["0010_2"] = a
    main_dataframe.drop(labels=['0010__1', "0010__2"], axis=1, inplace=True)

    main_dataframe.to_csv("main_dataframe_modified_"+type_of_phase+".csv")

    # ################THIRD PART
    #
    dataset_name = "main_dataframe_modified_"+type_of_phase+".csv"
    dataframe = pd.read_csv(dataset_name, sep=',')
    dataframe.iloc[:, 0] = dataframe.iloc[:, 0] + 1
    dataframe.head()
    dataframe_modified = dataframe

    #

    current_path =os.getcwd()
    os.chdir(data_path)
    experiment_order_w = 'experiment_order_w_creature_v2.csv'
    experiment_order = pd.read_csv(experiment_order_w, sep=',')
    os.chdir(current_path)
    print experiment_order


    def for_ASC(experiment_order,dataframe_modified):
        i = 0
        for index, row in experiment_order.iterrows():

            if experiment_order.at[i, 'Player'] == "Player1":
                if experiment_order.at[i, 'Creature'] == "Creature1":
                    dataframe_modified.at[i, '0001_2'] = 0
                    dataframe_modified.at[i, '0002_2'] = 0
                    dataframe_modified.at[i, '0003_2'] = 0
                    dataframe_modified.at[i, '0004_2'] = 0
                    dataframe_modified.at[i, '0005_2'] = 0
                    dataframe_modified.at[i, '0007_2'] = 0
                    dataframe_modified.at[i, '0010_2'] = 0
                    # dataframe.at[i,'Creature']
                elif experiment_order.at[i, 'Creature'] == "Creature2":
                    dataframe_modified.at[i, '0001_1'] = 0
                    dataframe_modified.at[i, '0002_2'] = 0
                    dataframe_modified.at[i, '0003_2'] = 0
                    dataframe_modified.at[i, '0004_1'] = 0
                    dataframe_modified.at[i, '0005_1'] = 0
                    dataframe_modified.at[i, '0007_2'] = 0
                    dataframe_modified.at[i, '0010_2'] = 0
            elif experiment_order.at[i, 'Player'] == "Player2":
                if experiment_order.at[i, 'Creature'] == "Creature1":
                    dataframe_modified.at[i, '0001_2'] = 0
                    dataframe_modified.at[i, '0002_1'] = 0
                    dataframe_modified.at[i, '0003_1'] = 0
                    dataframe_modified.at[i, '0004_2'] = 0
                    dataframe_modified.at[i, '0005_2'] = 0
                    dataframe_modified.at[i, '0007_1'] = 0
                    dataframe_modified.at[i, '0010_1'] = 0
                elif experiment_order.at[i, 'Creature'] == "Creature2":
                    dataframe_modified.at[i, '0001_1'] = 0
                    dataframe_modified.at[i, '0002_1'] = 0
                    dataframe_modified.at[i, '0003_1'] = 0
                    dataframe_modified.at[i, '0004_1'] = 0
                    dataframe_modified.at[i, '0005_1'] = 0
                    dataframe_modified.at[i, '0007_1'] = 0
                    dataframe_modified.at[i, '0010_1'] = 0
            if i == 9 or i == 29 or i == 30:
                dataframe_modified.at[i, '0001_2'] = -1
                dataframe_modified.at[i, '0002_2'] = -1
                dataframe_modified.at[i, '0003_2'] = -1
                dataframe_modified.at[i, '0004_2'] = -1
                dataframe_modified.at[i, '0005_2'] = -1
                dataframe_modified.at[i, '0007_2'] = -1
                dataframe_modified.at[i, '0010_2'] = -1
                dataframe_modified.at[i, '0001_1'] = -1
                dataframe_modified.at[i, '0002_1'] = -1
                dataframe_modified.at[i, '0003_1'] = -1
                dataframe_modified.at[i, '0004_1'] = -1
                dataframe_modified.at[i, '0005_1'] = -1
                dataframe_modified.at[i, '0007_1'] = -1
                dataframe_modified.at[i, '0010_1'] = -1
                dataframe_modified.at[i, '0006_'] = -1
                dataframe_modified.at[i, '0008_'] = -1
                dataframe_modified.at[i, '0009_'] = -1
            i = i + 1

        dataframe_modified["0001"] = dataframe_modified["0001_1"] + dataframe_modified["0001_2"]
        dataframe_modified.drop(labels=['0001_1', "0001_2"], axis=1, inplace=True)

        dataframe_modified["0002"] = dataframe_modified["0002_1"] + dataframe_modified["0002_2"]
        dataframe_modified.drop(labels=['0002_1', "0002_2"], axis=1, inplace=True)

        dataframe_modified["0003"] = dataframe_modified["0003_1"] + dataframe_modified["0003_2"]
        dataframe_modified.drop(labels=['0003_1', "0003_2"], axis=1, inplace=True)

        dataframe_modified["0004"] = dataframe_modified["0004_1"] + dataframe_modified["0004_2"]
        dataframe_modified.drop(labels=['0004_1', "0004_2"], axis=1, inplace=True)

        dataframe_modified["0005"] = dataframe_modified["0005_1"] + dataframe_modified["0005_2"]
        dataframe_modified.drop(labels=['0005_1', "0005_2"], axis=1, inplace=True)

        dataframe_modified["0007"] = dataframe_modified["0007_1"] + dataframe_modified["0007_2"]
        dataframe_modified.drop(labels=['0007_1', "0007_2"], axis=1, inplace=True)

        dataframe_modified["0010"] = dataframe_modified["0010_1"] + dataframe_modified["0010_2"]
        dataframe_modified.drop(labels=['0010_1', "0010_2"], axis=1, inplace=True)

        dataframe_modified["0006"] = dataframe_modified["0006_"]
        dataframe_modified.drop(labels=["0006_"], axis=1, inplace=True)

        dataframe_modified["0008"] = dataframe_modified["0008_"]
        dataframe_modified.drop(labels=["0008_"], axis=1, inplace=True)

        dataframe_modified["0009"] = dataframe_modified["0009_"]
        dataframe_modified.drop(labels=["0009_"], axis=1, inplace=True)

        dataframe_modified_ASC = dataframe_modified


        return dataframe_modified_ASC

    def for_TD(experiment_order, data):
        i = 0
        for index, row in experiment_order.iterrows():

            if experiment_order.at[i, 'Player'] == "Player1":
                if experiment_order.at[i, 'Creature'] == "Creature1":
                    data.at[i, '0001_1'] = 0
                    data.at[i, '0002_1'] = 0
                    data.at[i, '0003_1'] = 0
                    data.at[i, '0004_1'] = 0
                    data.at[i, '0005_1'] = 0
                    data.at[i, '0007_1'] = 0
                    data.at[i, '0010_1'] = 0
                    # dataframe.at[i,'Creature']
                elif experiment_order.at[i, 'Creature'] == "Creature2":
                    data.at[i, '0001_2'] = 0
                    data.at[i, '0002_1'] = 0
                    data.at[i, '0003_1'] = 0
                    data.at[i, '0004_2'] = 0
                    data.at[i, '0005_2'] = 0
                    data.at[i, '0007_1'] = 0
                    data.at[i, '0010_1'] = 0
            elif experiment_order.at[i, 'Player'] == "Player2":
                if experiment_order.at[i, 'Creature'] == "Creature1":
                    data.at[i, '0001_1'] = 0
                    data.at[i, '0002_2'] = 0
                    data.at[i, '0003_2'] = 0
                    data.at[i, '0004_1'] = 0
                    data.at[i, '0005_1'] = 0
                    data.at[i, '0007_2'] = 0
                    data.at[i, '0010_2'] = 0
                elif experiment_order.at[i, 'Creature'] == "Creature2":
                    data.at[i, '0001_2'] = 0
                    data.at[i, '0002_2'] = 0
                    data.at[i, '0003_2'] = 0
                    data.at[i, '0004_2'] = 0
                    data.at[i, '0005_2'] = 0
                    data.at[i, '0007_2'] = 0
                    data.at[i, '0010_2'] = 0
            if i == 9 or i == 29 or i == 30:
                data.at[i, '0001_2'] = -1
                data.at[i, '0002_2'] = -1
                data.at[i, '0003_2'] = -1
                data.at[i, '0004_2'] = -1
                data.at[i, '0005_2'] = -1
                data.at[i, '0007_2'] = -1
                data.at[i, '0010_2'] = -1
                data.at[i, '0001_1'] = -1
                data.at[i, '0002_1'] = -1
                data.at[i, '0003_1'] = -1
                data.at[i, '0004_1'] = -1
                data.at[i, '0005_1'] = -1
                data.at[i, '0007_1'] = -1
                data.at[i, '0010_1'] = -1
                data.at[i, '0006_'] = -1
                data.at[i, '0008_'] = -1
                data.at[i, '0009_'] = -1
            i = i + 1

        data["0001"] = data["0001_1"] + data["0001_2"]
        data.drop(labels=['0001_1', "0001_2"], axis=1, inplace=True)

        data["0002"] = data["0002_1"] + data["0002_2"]
        data.drop(labels=['0002_1', "0002_2"], axis=1, inplace=True)

        data["0003"] = data["0003_1"] + data["0003_2"]
        data.drop(labels=['0003_1', "0003_2"], axis=1, inplace=True)

        data["0004"] = data["0004_1"] + data["0004_2"]
        data.drop(labels=['0004_1', "0004_2"], axis=1, inplace=True)

        data["0005"] = data["0005_1"] + data["0005_2"]
        data.drop(labels=['0005_1', "0005_2"], axis=1, inplace=True)

        data["0007"] = data["0007_1"] + data["0007_2"]
        data.drop(labels=['0007_1', "0007_2"], axis=1, inplace=True)

        data["0010"] = data["0010_1"] + data["0010_2"]
        data.drop(labels=['0010_1', "0010_2"], axis=1, inplace=True)

        data["0006"] = data["0006_"]
        data.drop(labels=["0006_"], axis=1, inplace=True)

        data["0008"] = data["0008_"]
        data.drop(labels=["0008_"], axis=1, inplace=True)

        data["0009"] = data["0009_"]
        data.drop(labels=["0009_"], axis=1, inplace=True)

        dataframe_modified_TD = data


        return dataframe_modified_TD


    if participant == "ASC":
        dataframe_modified_ASC =dataframe_modified
        dataframe_A = for_ASC(experiment_order, dataframe_modified_ASC)
        dataframe_A.to_csv("dataframe_modified_ASC_"+type_of_phase+".csv")
    elif  participant == "NONASC":

        dataframe_modified_TD=dataframe_modified
        dataframe_B = for_TD(experiment_order, dataframe_modified_TD)
        dataframe_B.to_csv("dataframe_modified_NONASC_"+type_of_phase+".csv")


    os.chdir('..')
def systemlog_feature_extraction6():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_manipulate_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '6')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_manipulate_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '6')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_manipulate_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window)+ '\t' '6')
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'manipulate_prop' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'manipulate_prop'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'manipulate_prop'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'manipulate_prop'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)


    result_merged_creature = open('0009_a_result_#of_manipulate_prop.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_manipulate_prop.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_manipulate_prop,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_manipulate_prop,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction7():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_greeting_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '7')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_greeting_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '7')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_greeting_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'greeting' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'greeting'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'greeting'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'greeting'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)



    result_merged_creature = open('0009_a_result_#of_greeting.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_greeting.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_greeting,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_greeting,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction8():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_creature_changed_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '8')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_creature_changed_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '8')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_creature_changed_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'creature_changed' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'creature_changed'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'creature_changed'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'creature_changed'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)


    result_merged_creature = open('0009_a_result_#of_creature_changed.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_creature_changed.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_creature_changed,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_creature_changed,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction9():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_point_at_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '9')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_point_at_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '9')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_point_at_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'point_at' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'point_at'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'point_at'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'point_at'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)


    result_merged_creature = open('0009_a_result_#of_point_at.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_poin_at.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_point_at,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_point_at,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction10():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_look_up_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '10')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_look_up_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '10')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_look_up_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'look_up' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'look_up'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'look_up'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'look_up'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)


    result_merged_creature = open('0009_a_result_#of_look_up.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_look_up.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_look_up,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_look_up,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def systemlog_feature_extraction11():

    def create_merge_time_array_text(merge_time_array, phase):

        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_character_creator_time_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '11')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination+ trial)
    def create_merge_time_array_text2(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_character_creator_time2_' + trial + '_' + phase + '_.txt', 'w')
        output_merge_time.write('time' + '\t' + 'nid')
        output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            output_merge_time.write(str(merge_time_array[i]) + '\t' + '11')
            output_merge_time.write("\n")
        os.chdir(system_log_input_destination + trial)
    def create_kubios_merge_time_array_text(merge_time_array, phase):
        os.chdir(system_log_output_destination + trial)
        output_merge_time = open('output_kubios_character_creator_time_' + trial + '_' + phase + '_3.txt', 'w')
        # output_merge_time.write('time' + '\t' + 'nid')
        # output_merge_time.write("\n")
        for i in range(0, len(merge_time_array)):
            # if float(merge_time_array[
            #              i]) > 870:  # we dont include the last 30 sec because kubios window can not e less than 30 sec
            #     continue
            # else:
            kubios_time_window = float(merge_time_array[i]) + 30
            if kubios_time_window > 900:
                kubios_time_window = 900

            output_merge_time.write(str(merge_time_array[i]) + '\t' + str(kubios_time_window))
            output_merge_time.write("\n")

        os.chdir(system_log_input_destination + trial)
    def find_start_time(rawdata_filename):

        with open(rawdata_filename) as f:
            reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)

        print num_cols
        if num_cols == 1:
            print rawdata_filename
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter=';', skiprows=1)
        elif num_cols == 5:
            time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True, dtype=str,
                                                    delimiter='\t', skiprows=1)

        print rawdata_filename
        biometrics_start_cutpoint = 0
        start_time = 0
        for i in range(0, len(time)):
            if (action[i] == 'start_biometrics'):
                start_time = float(time[i])
                break
            biometrics_start_cutpoint = biometrics_start_cutpoint + 1

        return start_time, biometrics_start_cutpoint

    def calculate_merge_events_and_char_creature(action, time, start_time, i, flag):

        count_merge_events = 0
        count_merge_events_first = 0
        count_merge_events_mid = 0
        count_merge_events_last = 0

        merge_time_array = []
        merge_time_array_first = []
        merge_time_array_mid = []
        merge_time_array_last = []

        for k in range(0, len(time)):



                    ####FEATURE .................find the # of merges

            if (action[k] == 'character_creator' and float(time[k]) <= 900 + start_time):
                count_merge_events = count_merge_events + 1
                print time[k]
                merge_time_array.append(str(float(time[k]) - float(start_time)))

            if (float(time[k]) <= 300 + start_time):
                if (action[k] == 'character_creator'):
                    count_merge_events_first = count_merge_events_first + 1
                    merge_time_array_first.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 300 + start_time and float(time[k]) <= 600 + start_time):
                if (action[k] == 'character_creator'):
                    count_merge_events_mid = count_merge_events_mid + 1
                    merge_time_array_mid.append(str(float(time[k]) - float(start_time)))

            elif (float(time[k]) > 600 + start_time and float(time[k]) <= 900 + start_time):
                if (action[k] == 'character_creator'):
                    count_merge_events_last = count_merge_events_last + 1
                    merge_time_array_last.append(str(float(time[k]) - float(start_time)))

        return count_merge_events_first, count_merge_events_mid, count_merge_events_last, count_merge_events, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last

    count_merge_array = np.zeros((numberofexperiments, 4))
    count_merge_array2 = np.zeros((numberofexperiments, 4))
    time_of_first_char = np.zeros((numberofexperiments, 4))
    time_of_first_char2 = np.zeros((numberofexperiments, 4))
    sync_time_array = np.zeros((numberofexperiments, 4))
    sync_time_array2 = np.zeros((numberofexperiments, 4))
    trial_array = []

    lof_2_stages = []



    #####################################

    for i in range(1, numberofexperiments + 1):
        os.chdir(data_path)
        os.chdir('./0007-SYSTEM_LOGS')

        if i == skipped_experiment  or i == skipped_experiment2  or i == skipped_experiment3  or i == skipped_experiment4 :   # we dont have experiment 10
            count_merge_array[i - 1][0] = 0
            count_merge_array[i - 1][1] = 0
            count_merge_array[i - 1][2] = 0
            count_merge_array[i - 1][3] = 0
            count_merge_array2[i - 1][0] = 0
            count_merge_array2[i - 1][1] = 0
            count_merge_array2[i - 1][2] = 0
            count_merge_array2[i - 1][3] = 0
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))
            if len(list) == 1:

                #####sync data according to start time
                rawdata_filename = list[0]
                start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                print start_time
                flag = 0

                with open(rawdata_filename) as f:
                    reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

                print num_cols
                if num_cols == 1:
                    print rawdata_filename
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter=';',
                                                            skiprows=biometrics_start_cutpoint)
                elif num_cols == 5:
                    time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                            dtype=str, delimiter='\t',
                                                            skiprows=biometrics_start_cutpoint)

                first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                    action, time, start_time, i, flag)

                phase = 'total'
                create_merge_time_array_text(merge_time_array, phase)
                create_kubios_merge_time_array_text(merge_time_array, phase)

                phase = 'first'
                create_merge_time_array_text(merge_time_array_first, phase)
                phase = 'mid'
                create_merge_time_array_text(merge_time_array_mid, phase)
                phase = 'last'
                create_merge_time_array_text(merge_time_array_last, phase)

                # print len(merge_time_array)
                # print merge_time_array
                # output_merge_time = open('output_merge_time_' + trial + '_.txt', 'w')
                # output_merge_time.write('time' + '\t' + 'nid')
                # output_merge_time.write("\n")
                # for i in range(0, len(merge_time_array)):
                #     output_merge_time.write(str(merge_time_array[i]) + '\t' + '5')
                #     output_merge_time.write("\n")

                count_merge_array[i - 1][0] = first
                count_merge_array[i - 1][1] = mid
                count_merge_array[i - 1][2] = last
                count_merge_array[i - 1][3] = total


            elif len(list) == 2:
                lof_2_stages.append(str(trial))
                x = list[0]
                hour = int(x[11:13])
                min = int(x[14:16])
                sec = int(x[17:19])
                total_sec = hour * 60 * 60 + min * 60 + sec
                y = list[1]
                hour2 = int(y[11:13])
                min2 = int(y[14:16])
                sec2 = int(y[17:19])
                total_sec2 = hour2 * 60 * 60 + min2 * 60 + sec2

                print total_sec
                print total_sec2
                #
                #
                if (total_sec < total_sec2):

                    #####sync data according to start time
                    rawdata_filename = list[0]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    # second file processing

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True, dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0

                elif (total_sec > total_sec2):
                    #####sync data according to start time
                    rawdata_filename = list[1]
                    start_time, biometrics_start_cutpoint = find_start_time(rawdata_filename)
                    flag = 0
                    a = start_time

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter=';',
                                                                skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time, player, action, x, y = np.loadtxt(rawdata_filename, usecols=(0, 1, 2, 3, 4), unpack=True,
                                                                dtype=str, delimiter='\t',
                                                                skiprows=biometrics_start_cutpoint)

                    first, mid, last, total, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action, time, start_time, i, flag)

                    phase = 'total'
                    create_merge_time_array_text(merge_time_array, phase)
                    create_kubios_merge_time_array_text(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text(merge_time_array_last, phase)

                    count_merge_array[i - 1][0] = first
                    count_merge_array[i - 1][1] = mid
                    count_merge_array[i - 1][2] = last
                    count_merge_array[i - 1][3] = total

                    rawdata_filename2 = list[1]
                    print rawdata_filename
                    start_time2, biometrics_start_cutpoint2 = find_start_time(rawdata_filename2)
                    flag = 1

                    print a + start_time
                    print len(time)

                    with open(rawdata_filename) as f:
                        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
                        first_row = next(reader)
                        num_cols = len(first_row)

                    print num_cols
                    if num_cols == 1:
                        print rawdata_filename
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter=';',
                                                                     skiprows=biometrics_start_cutpoint)
                    elif num_cols == 5:
                        time2, player2, action2, x2, y2 = np.loadtxt(rawdata_filename2, usecols=(0, 1, 2, 3, 4),
                                                                     unpack=True,
                                                                     dtype=str, delimiter='\t',
                                                                     skiprows=biometrics_start_cutpoint)

                    first2, mid2, last2, total2, merge_time_array, merge_time_array, merge_time_array_first, merge_time_array_mid, merge_time_array_last = calculate_merge_events_and_char_creature(
                        action2, time2, start_time2, i, flag)

                    phase = 'total'
                    create_merge_time_array_text2(merge_time_array, phase)
                    phase = 'first'
                    create_merge_time_array_text2(merge_time_array_first, phase)
                    phase = 'mid'
                    create_merge_time_array_text2(merge_time_array_mid, phase)
                    phase = 'last'
                    create_merge_time_array_text2(merge_time_array_last, phase)

                    count_merge_array2[i - 1][0] = first2
                    count_merge_array2[i - 1][1] = mid2
                    count_merge_array2[i - 1][2] = last2
                    count_merge_array2[i - 1][3] = total2

                    flag = 0
                flag = 0
            else:
                continue

            os.chdir('..')

    print lof_2_stages
    print count_merge_array
    print count_merge_array2
    print time_of_first_char
    print time_of_first_char2
    print sync_time_array
    print sync_time_array2

    real_time_of_first_char_array = time_of_first_char - sync_time_array
    real_time_of_first_char_array2 = time_of_first_char2 - sync_time_array2

    os.chdir(system_log_output_destination)


    result_merged_creature = open('0009_a_result_#of_character_creator.txt', 'w')
    result_merged_creature2 = open('0009_b_result_#of_character_creator.txt', 'w')
    for i in range(0, numberofexperiments):
        result_merged_creature.write('output_' + trial_array[i] + "," + '#of_character_creator,')
        result_merged_creature2.write('output_' + trial_array[i] + "," + '#of_character_creator,')
        for j in range(0, 4):
            result_merged_creature.write(str(int(count_merge_array[i][j])) + ",")
            result_merged_creature2.write(str(int(count_merge_array2[i][j])) + ",")
        result_merged_creature.write("\n")
        result_merged_creature2.write("\n")
    os.chdir('..')
def create_kubios_system_log_files():

    trial_array = []
    lof_2_stages = []
    ####################################
    for i in range(1, numberofexperiments + 1):
        os.chdir(output_directory_path)
        os.chdir('./0007-SYSTEM_LOGS')
        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4 :  # we dont have experiment 10
            trial_array.append(' ')
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
            trial_array.append(trial)
            print  './' + trial + '/'
            os.chdir('./' + trial + '/')

            ###############################START OF FEATURE EXTRACTION
            list = []
            for x in os.listdir('.'):
                list.append(str(x))


            print trial
            print list
            list2 = []
            list3 = []
            list4 = []
            list5 = []


            for t in range (0,len(list)):
                name_kubious = list[t]
                is_name_kubious = name_kubious[0:13]
                end_kubious_ASC = name_kubious[-7:]
                end_kubious_NONASC = name_kubious[-10:]
                print "end_kubious_ASC : " + end_kubious_ASC
                print "end_kubious_NONASC : " + end_kubious_NONASC
                end_kubious2 = name_kubious[-11:]
                # output_merge= name_kubious[0:12]
                # output_manipulate = name_kubious[0:17]



                # if is_name_kubious == "output_kubios" or output_merge == "output_merge" or output_manipulate == "output_manipulate":
                #     list2.append(list[t])
                if is_name_kubious == "output_kubios" :
                    list2.append(list[t])
                if is_name_kubious == "output_kubios" and end_kubious_ASC == "ASC.txt" and end_kubious_NONASC != "NONASC.txt":
                    list3.append(list[t])
                if is_name_kubious == "output_kubios" and  end_kubious_NONASC == "NONASC.txt":
                    list4.append(list[t])
                if is_name_kubious == "output_kubios" and  end_kubious2 == "total_3.txt":
                    list5.append(list[t])

            list3 = list3+ list5
            list4 = list4 + list5
            #print list2
            print list2
            print list3
            print list4
            # filenames = ['file1.txt', 'file2.txt', ...]
            with open("kubious_all_"+trial+".txt", 'w') as outfile:
                outfile.write("start"+"\t"+"end"+"\t"+"nid\n")
                for fname in list2:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            with open("kubious_all_"+trial+"_ASC.txt", 'w') as outfile:
                outfile.write("start"+"\t"+"end"+"\t"+"nid\n")
                for fname in list3:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            with open("kubious_all_"+trial+"_NONASC.txt", 'w') as outfile:
                outfile.write("start"+"\t"+"end"+"\t"+"nid\n")
                for fname in list4:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            kubious_all = pd.read_csv("kubious_all_"+trial+".txt",sep="\t")
            kubious_all=kubious_all.sort_values(by=["start"])
            kubious_all.to_csv("kubious_all_new_"+trial+".txt",sep="\t",index=False)

            kubious_all_p1 = pd.read_csv("kubious_all_"+trial+"_ASC.txt",sep="\t")
            kubious_all_p1=kubious_all_p1.sort_values(by=["start"])
            kubious_all_p1.to_csv("kubious_all_new_"+trial+"_ASC.txt",sep="\t",index=False)

            kubious_all_p2 = pd.read_csv("kubious_all_"+trial+"_NONASC.txt",sep="\t")
            kubious_all_p2=kubious_all_p2.sort_values(by=["start"])
            kubious_all_p2.to_csv("kubious_all_new_"+trial+"_NONASC.txt",sep="\t",index=False)

            # print len(kubious_all)
            # print len(kubious_all_p1)
            # print len(kubious_all_p2)

            os.chdir('..')

def systemlog_function_calls():

    # number of greetings---------OK
    systemlog_feature_extraction_customizable("Creature1","greeting")
    systemlog_feature_extraction_customizable("Creature2","greeting")
    # number of hunted insects---------OK
    systemlog_feature_extraction_customizable("Player1","hunted_insect")
    systemlog_feature_extraction_customizable("Player2","hunted_insect")
    # number of prop manipulations---------OK
    systemlog_feature_extraction_customizable("manipulateprop","manipulate_prop")
    # number of creature color changed, must be correlated to hunted insects---------OK
    systemlog_feature_extraction_customizable("Player1","creature_changed")
    systemlog_feature_extraction_customizable("Player2","creature_changed")
    # number of creature color changed, must be correlated to hunted insects---------OK
    systemlog_feature_extraction_customizable("Creature1","look_up")
    systemlog_feature_extraction_customizable("Creature2","look_up")
    # number of point_at---------OK
    systemlog_feature_extraction_customizable("Creature1","point_at")
    systemlog_feature_extraction_customizable("Creature2","point_at")
    ## total area traveled---------OK
    systemlog_feature_extraction_total_area("Player1","total_area_traveled")
    systemlog_feature_extraction_total_area("Player2","total_area_traveled")
    # calculate distance between
    systemlog_feature_extraction_calculate_distance_between()

    systemlog_feature_extraction2() # >870 version included and more ...
    systemlog_feature_extraction6()

    ################event based tagging

    systemlog_feature_extraction_customizable_event("Creature1","greeting")
    systemlog_feature_extraction_customizable_event("Creature2","greeting")

    systemlog_feature_extraction_customizable_event("Player1","creature_changed")
    systemlog_feature_extraction_customizable_event("Player2","creature_changed")

    # number of point_at---------OK
    systemlog_feature_extraction_customizable_event("Creature1","point_at")
    systemlog_feature_extraction_customizable_event("Creature2","point_at")

    # number of creature color changed, must be correlated to hunted insects---------OK
    systemlog_feature_extraction_customizable_event("Creature1","look_up")
    systemlog_feature_extraction_customizable_event("Creature2","look_up")

    systemlog_feature_extraction_customizable_event("Player1","character_creator")
    systemlog_feature_extraction_customizable_event("Player2","character_creator")


    create_system_log_summary_dataframes("ASC","total")
    create_system_log_summary_dataframes ("NONASC","total")
    create_system_log_summary_dataframes("ASC","first")
    create_system_log_summary_dataframes ("NONASC","first")
    create_system_log_summary_dataframes("ASC","mid")
    create_system_log_summary_dataframes ("NONASC","mid")
    create_system_log_summary_dataframes("ASC","last")
    create_system_log_summary_dataframes ("NONASC","last")




#########stage 5
def eda_video_code_marking_ASC():
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    def video_code_timestamping(trial, participant, condition, phase, samplingrate):
        rawdata_name = 'output_initiation_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name2 = 'output_response_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name3 = 'output_externalization_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name4='output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'

        data = pd.read_csv(rawdata_name, sep='\t')
        length_initiation = data.shape[0]

        data2 = pd.read_csv(rawdata_name2, sep='\t')
        length_response = data2.shape[0]

        data3 = pd.read_csv(rawdata_name3, sep='\t')
        length_externalization = data3.shape[0]

        # data4 = pd.read_csv(rawdata_name4, sep='\t')
        # length_kubios = data4.shape[0]

        # for i in range (0,length_initiation):
        #     print round(data.iat[i, 0])

        #### going out from Video coding folder and entering new EDA folder
        os.chdir('..')  # going out first
        os.chdir('..')  # going out LEGO

        # output_kubios_time_all = open(
        #     'output_kubios_all_' + trial + '_' + condition + '_' + phase + '_' + 'time.txt', 'w')
        # for i in range(0, length_kubios):
        #     start_kubios = str(data4.iat[i, 0])
        #     end_kubios = str(data4.iat[i, 1])
        #
        # output_kubios_time_all.write(start_kubios + '\t' + end_kubios )
        # output_kubios_time_all.write("\n")


        os.chdir('..')  # going out 0017-55
        os.chdir('..')  # going out 0008-VIDEO-CODING

        os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED')

        os.chdir('./' + trial + '_' + str(participant))
        os.chdir('./' + condition)
        os.chdir('./' + phase + '5')

        rawdata_filename = newest('.')

        eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

        for i in range(0, length_initiation):
            timestamp = round(data.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)
            print timestamp
            print "HOOOOOOOOO: "+ str(real_timestamp)
            eda_filetobe_timestaped.iat[real_timestamp, 2] = '1'

        for i in range(0, length_response):
            timestamp = round(data2.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)

            eda_filetobe_timestaped.iat[real_timestamp, 2] = '2'

        for i in range(0, length_externalization):
            timestamp = round(data3.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)
            print timestamp
            eda_filetobe_timestaped.iat[real_timestamp, 2] = '3'

        eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
        print rawdata_filename

        os.chdir('..')  # going out first
        os.chdir('..')  # going out LEGO
        os.chdir('..')  # going out 0017-55
        os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

        os.chdir('./0008-VIDEO-CODING')
        os.chdir('./' + trial + '_' + str(participant) + '/')
        os.chdir('./' + condition + '/')
        os.chdir('./' + phase + '/')


    trial_array = []
    initiation_time_array_first5 = []
    number_of_initiation_response_array = np.zeros(
        (numberofexperiments, 12))  # should be carefull with 0 and not exist state

    for i in range(0, numberofexperiments):
        for j in range(0, 12):
            number_of_initiation_response_array[i][j] = '-1'

    result_array = [[0, 0, 0], [0, 0, 0]]
    number_of_initiations = 0
    number_of_responses = 0

    ##################################### MAIN BODY

    os.chdir (output_path_main)
    os.chdir('./0008-VIDEO-CODING')

    for i in range(starting_point, numberofexperiments + 1):

        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4 :  # we dont have experiment 10

            trial_array.append(' ')
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
            print trial
            trial_array.append(trial)

            for j in range(1, 3):
                if j == 1:
                    # participant = 44
                    continue
                elif j == 2:
                    participant = 55
                print  './' + trial + '_' + str(participant) + '/'

                if (starting_point <= i):
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    print arr

                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "LEGO":
                            condition = "LEGO"
                            os.chdir('./' + condition + '/')
                            prr = os.listdir('.')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                    # extract_ECG_features(trial, participant, condition)


                                        ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends


                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                    ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends





                                        os.chdir('..')
                                else:

                                    continue

                            os.chdir('..')

                        elif str(arr[k - 1]) == "LOF":
                            condition = "LOF"

                            os.chdir('./' + condition + '/')

                            prr = os.listdir('.')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                        ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends




                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    os.chdir('./' + phase + '/')
                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")
                                    ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends



                                        os.chdir('..')
                                else:
                                    continue

                            os.chdir('..')



                        else:

                            continue
                    os.chdir('..')
                else:
                    continue

    os.chdir('..')
def eda_video_code_marking_NONASC():
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    def video_code_timestamping(trial, participant, condition, phase, samplingrate):
        rawdata_name = 'output_initiation_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name2 = 'output_response_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name3 = 'output_externalization_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'
        rawdata_name4='output_kubios_' + trial + '_' + condition + '_' + phase + '_' + 'time2.txt'

        data = pd.read_csv(rawdata_name, sep='\t')
        length_initiation = data.shape[0]

        data2 = pd.read_csv(rawdata_name2, sep='\t')
        length_response = data2.shape[0]

        data3 = pd.read_csv(rawdata_name3, sep='\t')
        length_externalization = data3.shape[0]

        # data4 = pd.read_csv(rawdata_name4, sep='\t')
        # length_kubios = data4.shape[0]

        # for i in range (0,length_initiation):
        #     print round(data.iat[i, 0])

        #### going out from Video coding folder and entering new EDA folder
        os.chdir('..')  # going out first
        os.chdir('..')  # going out LEGO

        # output_kubios_time_all = open(
        #     'output_kubios_all_' + trial + '_' + condition + '_' + phase + '_' + 'time.txt', 'w')
        # for i in range(0, length_kubios):
        #     start_kubios = str(data4.iat[i, 0])
        #     end_kubios = str(data4.iat[i, 1])
        #
        # output_kubios_time_all.write(start_kubios + '\t' + end_kubios )
        # output_kubios_time_all.write("\n")


        os.chdir('..')  # going out 0017-55
        os.chdir('..')  # going out 0008-VIDEO-CODING

        os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED')

        os.chdir('./' + trial + '_' + str(participant))
        os.chdir('./' + condition)
        os.chdir('./' + phase + '5')

        rawdata_filename = newest('.')

        eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

        for i in range(0, length_initiation):
            timestamp = round(data.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)
            eda_filetobe_timestaped.iat[real_timestamp, 2] = '1'

        for i in range(0, length_response):
            timestamp = round(data2.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)
            eda_filetobe_timestaped.iat[real_timestamp, 2] = '2'

        for i in range(0, length_externalization):
            timestamp = round(data3.iat[i, 0])
            if timestamp == 300:
                timestamp = 299
            real_timestamp = int(timestamp * samplingrate)
            print timestamp
            eda_filetobe_timestaped.iat[real_timestamp, 2] = '3'

        eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
        print rawdata_filename

        os.chdir('..')  # going out first
        os.chdir('..')  # going out LEGO
        os.chdir('..')  # going out 0017-55
        os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST
        if participant == 55:
            os.chdir('./0008-VIDEO-CODING')
        elif participant == 44:
            os.chdir('./0008-VIDEO-CODING - NONASC')
        os.chdir('./' + trial + '_' + str(participant) + '/')
        os.chdir('./' + condition + '/')
        os.chdir('./' + phase + '/')


    trial_array = []
    initiation_time_array_first5 = []
    number_of_initiation_response_array = np.zeros(
        (numberofexperiments, 12))  # should be carefull with 0 and not exist state

    for i in range(0, numberofexperiments):
        for j in range(0, 12):
            number_of_initiation_response_array[i][j] = '-1'

    result_array = [[0, 0, 0], [0, 0, 0]]
    number_of_initiations = 0
    number_of_responses = 0

    ##################################### MAIN BODY

    os.chdir (output_path_main)
    os.chdir('./0008-VIDEO-CODING - NONASC')

    for i in range(starting_point, numberofexperiments + 1):

        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4 :  # we dont have experiment 10

            trial_array.append(' ')
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
            print trial
            trial_array.append(trial)

            for j in range(1, 3):
                if j == 1:
                    participant = 44

                elif j == 2:
                    #participant = 55
                    continue
                print  './' + trial + '_' + str(participant) + '/'

                if (starting_point <= i):
                    os.chdir('./' + trial + '_' + str(participant) + '/')
                    arr = os.listdir('.')
                    print arr

                    for k in range(1, len(arr) + 1):

                        if str(arr[k - 1]) == "LEGO":
                            condition = "LEGO"
                            os.chdir('./' + condition + '/')
                            prr = os.listdir('.')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                    # extract_ECG_features(trial, participant, condition)


                                        ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends


                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                    ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends





                                        os.chdir('..')
                                else:

                                    continue

                            os.chdir('..')

                        elif str(arr[k - 1]) == "LOF":
                            condition = "LOF"

                            os.chdir('./' + condition + '/')

                            prr = os.listdir('.')

                            for t in range(1, len(prr) + 1):

                                if str(prr[t - 1]) == "first":
                                    phase = "first"
                                    os.chdir('./' + phase + '/')

                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")

                                        ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends




                                        os.chdir('..')
                                elif str(prr[t - 1]) == "last":

                                    phase = "last"
                                    os.chdir('./' + phase + '/')
                                    if len(os.listdir('./')) == 0:
                                        print("Directory is empty")
                                        os.chdir('..')
                                    else:
                                        print("Directory is not empty")
                                    ############################# marking video coding timestamps start
                                        video_code_timestamping(trial, participant, condition, phase, samplingrate)
                                        ############################# marking video coding timestamps ends



                                        os.chdir('..')
                                else:
                                    continue

                            os.chdir('..')



                        else:

                            continue
                    os.chdir('..')
                else:
                    continue

    os.chdir('..')

#########stage 6
def eda_system_log_marking():
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    def system_log_timestamping(trial, participant, condition, phase, samplingrate):

        rawdata_name = 'output_merge_time_' + trial + '_' + phase + '_' + '.txt'

        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            #print 'batuuuuuu' + str()
            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'
    def manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate):

        rawdata_name = 'output_manipulate_time_' + trial + '_' + phase + '_' + '.txt'

        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            #print 'batuuuuuu' + str()
            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'
    def event_timestamping(trial, participant, condition, phase, samplingrate,system_event_type,person_type):



        list = []
        list2 = []
        list3 = []
        list4 = []
        for x in os.listdir('.'):
            list.append(str(x))

        for t in range(0, len(list)):
            name_kubious = list[t]
            is_name_kubious = name_kubious[0:7]
            end_kubious = name_kubious[-7:]
            end_kubious2= name_kubious[-10:]

            if is_name_kubious == "output_" and end_kubious =="ASC.txt" and end_kubious2 != "NONASC.txt":
                list2.append(list[t])
            elif is_name_kubious == "output_" and  end_kubious2 == "NONASC.txt":
                list3.append(list[t])

        if person_type == "ASC":
            tag_person = "ASC"
            list4 = list2
        elif person_type == "NONASC":
            tag_person = "NONASC"
            list4 = list3



        def find_rawdata(feature_type,list):

            list_result =[]

            for t in range (0,len(list)):

                name_kubious = list[t]

                result = name_kubious.find(feature_type)

                if result != -1:
                    list_result.append(list[t])

            return list_result

        def find_rawdata_name(list,phase):

            list_result = []

            for t in range(0, len(list)):

                name_kubious = list[t]

                result_phase = name_kubious.find(phase)

                if result_phase != -1:
                    rawdata_name = name_kubious

            return rawdata_name



        if system_event_type == "greeting":
            nid = "7"
            list_result = find_rawdata("greeting", list4)
            rawdata_name=  find_rawdata_name(list_result, phase)
        elif system_event_type == "creature_changed":
            nid = "8"
            list_result = find_rawdata("creature_changed", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "point_at":
            nid = "9"
            list_result = find_rawdata("point_at", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "look_up":
            nid = "10"
            list_result = find_rawdata("look_up", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "character_creator":
            nid = "11"
            list_result = find_rawdata("character_creator", list4)
            rawdata_name = find_rawdata_name(list_result, phase)

        print rawdata_name


        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            #print 'batuuuuuu' + str()
            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'

    # ############################################# PARAMETERS TO CHANGE ################

    # if there is participant 44 , the comment should be removed # participant = 44


    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []
    number_of_initiation_response_array = np.zeros(
        (numberofexperiments, 12))  # should be carefull with 0 and not exist state

    for i in range(0, numberofexperiments):
        for j in range(0, 12):
            number_of_initiation_response_array[i][j] = '-1'

    result_array = [[0, 0, 0], [0, 0, 0]]
    number_of_initiations = 0
    number_of_responses = 0

    ##################################### MAIN BODY

    os.chdir(output_path_main)
    os.chdir('./0007-SYSTEM_LOGS')

    for i in range(starting_point, numberofexperiments + 1):

        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4 :  # we dont have experiment 10

            trial_array.append(' ')
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

            trial_array.append(trial)

            os.chdir('./' + trial + '/')

            for i in range(0, 2):
                if i == 0:
                    participant = '44'
                    for k in range(0, 2):
                        if k == 0:
                            condition = 'LEGO'
                        elif k == 1:
                            condition = 'LOF'
                        for t in range(0, 3):
                            if t == 0:
                                phase = 'first'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                            if t == 1:
                                phase = 'mid'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                            if t == 2:
                                phase = 'last'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                   "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                elif i == 1:
                    participant = '55'

                    for k in range(0, 2):
                        if k == 0:
                            condition = 'LEGO'
                        elif k == 1:
                            condition = 'LOF'
                        for t in range(0, 3):
                            if t == 0:
                                phase = 'first'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")

                            if t == 1:
                                phase = 'mid'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")

                            if t == 2:
                                phase = 'last'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")


            os.chdir('..')

    os.chdir('..')

#########stage 7 video & system log marking together
def eda_system_log_marking2():
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    def system_log_timestamping(trial, participant, condition, phase, samplingrate):

        rawdata_name = 'output_merge_time_' + trial + '_' + phase + '_' + '.txt'
        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '5'

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'
    def manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate):

        rawdata_name = 'output_manipulate_time_' + trial + '_' + phase + '_' + '.txt'

        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            #print 'batuuuuuu' + str()
            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = '6'

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'

    def event_timestamping(trial, participant, condition, phase, samplingrate, system_event_type, person_type):

        list = []
        list2 = []
        list3 = []
        list4 = []
        for x in os.listdir('.'):
            list.append(str(x))

        for t in range(0, len(list)):
            name_kubious = list[t]
            is_name_kubious = name_kubious[0:7]
            end_kubious = name_kubious[-7:]
            end_kubious2 = name_kubious[-10:]

            if is_name_kubious == "output_" and end_kubious == "ASC.txt" and end_kubious2 != "NONASC.txt":
                list2.append(list[t])
            elif is_name_kubious == "output_" and end_kubious2 == "NONASC.txt":
                list3.append(list[t])

        if person_type == "ASC":
            tag_person = "ASC"
            list4 = list2
        elif person_type == "NONASC":
            tag_person = "NONASC"
            list4 = list3

        def find_rawdata(feature_type,list):

            list_result =[]

            for t in range (0,len(list)):

                name_kubious = list[t]

                result = name_kubious.find(feature_type)

                if result != -1:
                    list_result.append(list[t])

            return list_result

        def find_rawdata_name(list,phase):

            list_result = []

            for t in range(0, len(list)):

                name_kubious = list[t]

                result_phase = name_kubious.find(phase)

                if result_phase != -1:
                    rawdata_name = name_kubious

            return rawdata_name



        if system_event_type == "greeting":
            nid = "7"
            list_result = find_rawdata("greeting", list4)
            rawdata_name=  find_rawdata_name(list_result, phase)
        elif system_event_type == "creature_changed":
            nid = "8"
            list_result = find_rawdata("creature_changed", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "point_at":
            nid = "9"
            list_result = find_rawdata("point_at", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "look_up":
            nid = "10"
            list_result = find_rawdata("look_up", list4)
            rawdata_name = find_rawdata_name(list_result, phase)
        elif system_event_type == "character_creator":
            nid = "11"
            list_result = find_rawdata("character_creator", list4)
            rawdata_name = find_rawdata_name(list_result, phase)

        print rawdata_name

        if condition == 'LEGO':
            pass
        elif condition == 'LOF':
            data = pd.read_csv(rawdata_name, sep='\t')
            length_merge = data.shape[0]
            print length_merge

            # for i in range (0,length_initiation):
            #     print round(data.iat[i, 0])

            #### going out from system log folder and entering new EDA folder
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0008-VIDEO-CODING

            os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')
            os.chdir('./' + trial + '_' + str(participant))
            os.chdir('./' + condition)
            os.chdir('./' + phase + '5')

            rawdata_filename = newest('.')
            print rawdata_filename
            eda_filetobe_timestaped = pd.read_csv(rawdata_filename)

            # print 'batuuuuuu' + str()
            if phase == 'first':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0])
                    print round(data.iat[i, 0])
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid
            if phase == 'mid':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 300
                    print round(data.iat[i, 0]) - 300
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid
            if phase == 'last':
                for i in range(0, length_merge):
                    timestamp = round(data.iat[i, 0]) - 600
                    print round(data.iat[i, 0]) - 600
                    if timestamp == 300:
                        timestamp = 299
                    real_timestamp = int(timestamp * samplingrate)
                    eda_filetobe_timestaped.iat[real_timestamp, 2] = nid

            eda_filetobe_timestaped.to_csv(rawdata_filename, index=False)
            print rawdata_filename

            os.chdir('..')  # going out first
            os.chdir('..')  # going out LEGO
            os.chdir('..')  # going out 0017-55
            os.chdir('..')  # going out 0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_TEST

            os.chdir('./0007-SYSTEM_LOGS')
            os.chdir('./' + trial + '/')

            print phase + '_finished'

    # ############################################# PARAMETERS TO CHANGE ################

    # if there is participant 44 , the comment should be removed # participant = 44


    # ############################################# VARIABLE DEFINITIONS ################

    trial_array = []
    initiation_time_array_first5 = []
    number_of_initiation_response_array = np.zeros(
        (numberofexperiments, 12))  # should be carefull with 0 and not exist state

    for i in range(0, numberofexperiments):
        for j in range(0, 12):
            number_of_initiation_response_array[i][j] = '-1'

    result_array = [[0, 0, 0], [0, 0, 0]]
    number_of_initiations = 0
    number_of_responses = 0

    ##################################### MAIN BODY
    os.chdir(output_path_main)

    os.chdir('./0007-SYSTEM_LOGS')

    for i in range(starting_point, numberofexperiments + 1):

        if i == skipped_experiment or i == skipped_experiment2 or i == skipped_experiment3 or i == skipped_experiment4:  # we dont have experiment 10

            trial_array.append(' ')
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

            trial_array.append(trial)

            os.chdir('./' + trial + '/')

            for i in range(0, 2):
                if i == 0:
                    participant = '44'
                    for k in range(0, 2):
                        if k == 0:
                            condition = 'LEGO'
                        elif k == 1:
                            condition = 'LOF'
                        for t in range(0, 3):
                            if t == 0:
                                phase = 'first'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                            if t == 1:
                                phase = 'mid'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                            if t == 2:
                                phase = 'last'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "creature_changed",  "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at",
                                                    "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up",
                                                   "NONASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate,
                                                   "character_creator",  "NONASC")

                elif i == 1:
                    participant = '55'

                    for k in range(0, 2):
                        if k == 0:
                            condition = 'LEGO'
                        elif k == 1:
                            condition = 'LOF'
                        for t in range(0, 3):
                            if t == 0:
                                phase = 'first'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")

                            if t == 1:
                                phase = 'mid'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")

                            if t == 2:
                                phase = 'last'
                                system_log_timestamping(trial, participant, condition, phase, samplingrate)
                                manipulate_prop_timestamping(trial, participant, condition, phase, samplingrate)
                                event_timestamping(trial, participant, condition, phase, samplingrate, "greeting","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "creature_changed","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "point_at","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "look_up","ASC")
                                event_timestamping(trial, participant, condition, phase, samplingrate, "character_creator","ASC")

            os.chdir('..')

    os.chdir('..')

#########stage 8 eda batch processing preparation
def preprocessing__batch_EDA_session_seperation_MARKED_system_log():

    os.chdir(output_path_main)
    directory = output_directory_path + '0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH/'
    directory_batch = output_directory_path + '0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH/'

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0009_LEGO-LOF (EDA) processed_SYSTEMLOG_EVENT_MARKED')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):
        os.chdir('./' + list[i])

        os.chdir('./' + 'LEGO')  ################## MAIN ENTERANCE TO LEGO

        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename, directory_batch + rawdata_filename)

        ################## MAIN ENTERANCE TO first 5

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')
        ################## MAIN EXIT TO first 5

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LEGO

        os.chdir('./' + 'LOF')  ################## MAIN ENTERANCE TO LOF
        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename,
                 directory_batch + rawdata_filename)

        #################

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LOF

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def preprocessing__batch_EDA_session_seperation_MARKED_video_code():

    os.chdir(output_path_main)
    directory = output_directory_path + '0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH/'
    directory_batch = output_directory_path + '0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH/'

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):
        os.chdir('./' + list[i])

        os.chdir('./' + 'LEGO')  ################## MAIN ENTERANCE TO LEGO

        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename, directory_batch + rawdata_filename)

        ################## MAIN ENTERANCE TO first 5

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')
        ################## MAIN EXIT TO first 5

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LEGO

        os.chdir('./' + 'LOF')  ################## MAIN ENTERANCE TO LOF
        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename,
                 directory_batch + rawdata_filename)

        #################

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LOF

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def preprocessing__batch_EDA_session_seperation_MARKED_system_log_video_code():

    os.chdir(output_path_main)
    directory = output_directory_path + '0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH/'
    directory_batch = output_directory_path + '0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH/'

    list = []
    for x in os.listdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED'):
        if os.path.isfile(x):
            print 'f-', x
        elif os.path.isdir(x):
            print 'd-', x
        elif os.path.islink(x):
            print 'l-', x
        else:
            list.append(str(x))

    print list

    os.chdir('./0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED')

    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        paths = filter(lambda x: x.endswith('.txt'), os.listdir('.'))
        return max(paths, key=os.path.getctime)

    for i in range(0, len(list)):
        os.chdir('./' + list[i])

        os.chdir('./' + 'LEGO')  ################## MAIN ENTERANCE TO LEGO

        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename, directory_batch + rawdata_filename)

        ################## MAIN ENTERANCE TO first 5

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')
        ################## MAIN EXIT TO first 5

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LEGO

        os.chdir('./' + 'LOF')  ################## MAIN ENTERANCE TO LOF
        rawdata_filename = newest('.')

        copyfile('./' + rawdata_filename,
                 directory_batch + rawdata_filename)

        #################

        os.chdir('./' + 'first5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'mid5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('./' + 'last5')
        rawdata_filename = newest('.')
        copyfile('./' + rawdata_filename,
                 directory + rawdata_filename)
        os.chdir('..')

        os.chdir('..')  #################MAIN EXIT TO LOF

        os.chdir('..')  #################MAIN EXIT TO 0017

    os.chdir('..')
def remove_noisy_eda_for_ledalab(path_to_noisy_eda_folder):
    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove("output_0013_44_LEGO_EDA.txt")
    os.remove("output_0013_44_LEGO_first5_EDA.txt")
    os.remove("output_0013_44_LEGO_last5_EDA.txt")
    os.remove("output_0013_44_LEGO_mid5_EDA.txt")
    os.remove("output_0013_44_LOF_EDA.txt")
    os.remove("output_0013_44_LOF_first5_EDA.txt")
    os.remove("output_0013_44_LOF_last5_EDA.txt")
    os.remove("output_0013_44_LOF_mid5_EDA.txt")

    os.remove("output_0014_55_LEGO_EDA.txt")
    os.remove("output_0014_55_LEGO_first5_EDA.txt")
    os.remove("output_0014_55_LEGO_last5_EDA.txt")
    os.remove("output_0014_55_LEGO_mid5_EDA.txt")
    os.remove("output_0014_55_LOF_EDA.txt")
    os.remove("output_0014_55_LOF_first5_EDA.txt")
    os.remove("output_0014_55_LOF_last5_EDA.txt")
    os.remove("output_0014_55_LOF_mid5_EDA.txt")
def remove_noisy_eda_for_ledalab_system_batch(path_to_noisy_eda_folder):
    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove("output_0019_44_LEGO_mid5_EDA.txt")
    os.remove("output_0019_44_LOF_EDA.txt")
    os.remove("output_0019_44_LOF_first5_EDA.txt")
    os.remove("output_0019_44_LOF_last5_EDA.txt")
    os.remove("output_0019_44_LOF_mid5_EDA.txt")

    os.remove("output_0032_44_LEGO_EDA.txt")
    os.remove("output_0032_44_LEGO_first5_EDA.txt")
    os.remove("output_0032_44_LEGO_last5_EDA.txt")
    os.remove("output_0032_44_LEGO_mid5_EDA.txt")

def remove_noisy_eda_for_ledalab_break(path_to_noisy_eda_folder):
    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove("output_0013_44_break_EDA.txt")
    os.remove("output_0013_55_break_EDA.txt")
    os.remove("output_0014_55_break_EDA.txt")
def remove_noisy_eda_for_ledalab_batch5(path_to_noisy_eda_folder):
    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove('output_0002_44_LOF_mid5_EDA.txt')

    os.remove("output_0013_44_LEGO_first5_EDA.txt")
    os.remove("output_0013_44_LEGO_last5_EDA.txt")
    os.remove("output_0013_44_LEGO_mid5_EDA.txt")

    os.remove("output_0013_44_LOF_first5_EDA.txt")
    os.remove("output_0013_44_LOF_last5_EDA.txt")
    os.remove("output_0013_44_LOF_mid5_EDA.txt")

    os.remove("output_0013_55_LEGO_first5_EDA.txt")
    os.remove("output_0013_55_LEGO_last5_EDA.txt")
    os.remove("output_0013_55_LEGO_mid5_EDA.txt")

    os.remove("output_0013_55_LOF_first5_EDA.txt")
    os.remove("output_0013_55_LOF_last5_EDA.txt")
    os.remove("output_0013_55_LOF_mid5_EDA.txt")

    os.remove("output_0014_55_LEGO_first5_EDA.txt")
    os.remove("output_0014_55_LEGO_last5_EDA.txt")
    os.remove("output_0014_55_LEGO_mid5_EDA.txt")

    os.remove("output_0014_55_LOF_first5_EDA.txt")
    os.remove("output_0014_55_LOF_last5_EDA.txt")
    os.remove("output_0014_55_LOF_mid5_EDA.txt")
def remove_noisy_eda_for_ledalab_batch_baseline(path_to_noisy_eda_folder):
    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove("output_0013_44_b1_EDA.txt")
    os.remove("output_0013_44_b2_EDA.txt")
    os.remove("output_0013_44_cb1_EDA.txt")
    os.remove("output_0013_44_cb2_EDA.txt")
    os.remove("output_0013_44_cb3_EDA.txt")
    os.remove("output_0013_44_cb4_EDA.txt")
    os.remove("output_0013_55_b1_EDA.txt")
    os.remove("output_0013_55_b2_EDA.txt")
    os.remove("output_0013_55_jb1_EDA.txt")
    os.remove("output_0013_55_jb2_EDA.txt")
    os.remove("output_0013_55_jb3_EDA.txt")
    os.remove("output_0013_55_jb4_EDA.txt")
    os.remove("output_0014_44_cb4_EDA.txt")
    os.remove("output_0014_55_b1_EDA.txt")
    os.remove("output_0014_55_b2_EDA.txt")
    os.remove("output_0014_55_jb1_EDA.txt")
    os.remove("output_0014_55_jb2_EDA.txt")
    os.remove("output_0014_55_jb3_EDA.txt")
    os.remove("output_0014_55_jb4_EDA.txt")
def remove_noisy_eda_for_ledalab_batch(path_to_noisy_eda_folder):

    os.chdir(output_directory_path+ path_to_noisy_eda_folder)

    os.remove("output_0013_44_LEGO_EDA.txt")
    os.remove("output_0013_44_LOF_EDA.txt")
    os.remove("output_0013_55_LEGO_EDA.txt")
    os.remove("output_0013_55_LOF_EDA.txt")

    os.remove("output_0014_55_LEGO_EDA.txt")
    os.remove("output_0014_55_LOF_EDA.txt")

#9--------- Questionnaire data extraction
def extract_questionnaire():
    import pandas as pd
    import numpy as np
    import glob, os
    os.chdir(qst_input_destination)
    src_file = input_directory_path + "experiment_order.csv"



    list = []
    experiment_order = pd.read_csv(src_file, sep=',')

    def generate_dataframe(dataframe_size):
        column_names = ["pre_LEGO", "post_LEGO", "pre_LOF", "post_LOF"]
        index = np.array([np.arange(dataframe_size)])
        generated_dataframe = pd.DataFrame(index=index[0], columns=column_names)
        generated_dataframe = generated_dataframe.fillna("")
        return generated_dataframe

    for file in glob.glob("*.csv"):
        if file == "experiment_order.csv":
            continue
        else:
            list.append(file)

    length_of_the_list = len(list)
    dataframe_size = length_of_the_list / 2
    name_of_the_file = ""

    arousal_AS_ASC = generate_dataframe(dataframe_size)
    valence_AS_ASC = generate_dataframe(dataframe_size)
    social_status_ASC = generate_dataframe(dataframe_size)
    desiretoknowmore_ASC = generate_dataframe(dataframe_size)
    staic_ASC = generate_dataframe(dataframe_size)

    arousal_AS_TDC = generate_dataframe(dataframe_size)
    valence_AS_TDC = generate_dataframe(dataframe_size)
    social_status_TDC = generate_dataframe(dataframe_size)
    desiretoknowmore_TDC = generate_dataframe(dataframe_size)
    staic_TDC = generate_dataframe(dataframe_size)

    def feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, target_dataframe, flag_value):

        a = questionnoare_no['flag']
        count = 0
        step = 3

        for i in range(0, len(a)):

            if a[i] == flag_value:
                step = 1
                break
            elif a[i] != flag_value:
                count = count + 1

        if (step == 3):
            print ("flag_value is not in the list")

        elif (step == 1):
            target_dataframe_value_index = questionnoare_no.index[questionnoare_no['flag'] == flag_value]
            target_dataframe_value = questionnoare_no.iloc[target_dataframe_value_index, 6]
            target_dataframe_value_real = target_dataframe_value.iloc[0]
            a = int(trial_no - 1)

            trial_turn = experiment_order.iloc[a, 2]
            trial_turn_real = trial_turn

            if flag_value < 5.0:

                if trial_turn_real == "LEGO":
                    target_dataframe.iloc[(trial_no - 1), 0] = target_dataframe_value_real
                elif trial_turn_real == "LOF":
                    target_dataframe.iloc[(trial_no - 1), 2] = target_dataframe_value_real

            elif flag_value > 4.0 and flag_value < 11.0:
                if trial_turn_real == "LEGO":
                    target_dataframe.iloc[(trial_no - 1), 1] = target_dataframe_value_real
                elif trial_turn_real == "LOF":
                    target_dataframe.iloc[(trial_no - 1), 3] = target_dataframe_value_real

            elif flag_value > 10.0 and flag_value < 55.0:
                if trial_turn_real == "LEGO":
                    target_dataframe.iloc[(trial_no - 1), 2] = target_dataframe_value_real
                elif trial_turn_real == "LOF":
                    target_dataframe.iloc[(trial_no - 1), 0] = target_dataframe_value_real

            elif flag_value > 44.0 and flag_value < 99.0:
                if trial_turn_real == "LEGO":
                    target_dataframe.iloc[(trial_no - 1), 3] = target_dataframe_value_real
                elif trial_turn_real == "LOF":
                    target_dataframe.iloc[(trial_no - 1), 1] = target_dataframe_value_real

    for i in range(0, length_of_the_list):
        name_of_the_file = list[i]
        trial_no = int(name_of_the_file[:4])
        type_of = name_of_the_file[5:8]
        questionnoare_no = pd.read_csv(name_of_the_file, sep=',')
        print (name_of_the_file)

        if type_of == "ASC":

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_ASC, 1.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_ASC, 2.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_ASC, 3.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_ASC, 4.0)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_ASC, 5.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_ASC, 6.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_ASC, 7.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_ASC, 8.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, staic_ASC, 6.6)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_ASC, 11.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_ASC, 22.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_ASC, 33.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_ASC, 44.0)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_ASC, 55.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_ASC, 66.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_ASC, 77.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_ASC, 88.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, staic_ASC, 66.6)


        elif type_of == "TDC":

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_TDC, 1.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_TDC, 2.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_TDC, 3.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_TDC, 4.0)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_TDC, 5.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_TDC, 6.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_TDC, 7.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_TDC, 8.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, staic_TDC, 6.6)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_TDC, 11.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_TDC, 22.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_TDC, 33.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_TDC, 44.0)

            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, arousal_AS_TDC, 55.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, valence_AS_TDC, 66.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, social_status_TDC, 77.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, desiretoknowmore_TDC, 88.0)
            feed_dataframe(name_of_the_file, trial_no, type_of, questionnoare_no, staic_TDC, 66.6)
    def modify_dataframe(dataframe):
        dataframe['trial_no'] = np.arange(1, len(dataframe) + 1)
        dataframe = dataframe[["trial_no", "pre_LEGO", "post_LEGO", "pre_LOF", "post_LOF"]]
        #     dataframe["pre_LEGO"]= dataframe["pre_LEGO"].astype(float)
        #     dataframe["pre_LOF"]=dataframe["pre_LOF"].astype(float)
        #     dataframe["post_LEGO"]=dataframe["post_LEGO"].astype(float)
        #     dataframe["post_LOF"]= dataframe["post_LOF"].astype(float)

        #     dataframe["postLEGO-preLEGO"]=dataframe ["post_LEGO"]-dataframe ["pre_LEGO"]
        #     dataframe["postLOF-preLOF"]=dataframe ["post_LOF"]-dataframe ["pre_LOF"]

        return dataframe



    os.chdir(qst_output_destination)
    dirpath = os.getcwd()
    print (dirpath)
    createFolder("Questionnaires")

    os.chdir("./Questionnaires")

    arousal_AS_ASC = modify_dataframe(arousal_AS_ASC)
    arousal_AS_ASC.to_csv('arousal_AS_ASC.csv', index=False)
    valence_AS_ASC = modify_dataframe(valence_AS_ASC)
    valence_AS_ASC.to_csv('valence_AS_ASC.csv', index=False)
    social_status_ASC = modify_dataframe(social_status_ASC)
    social_status_ASC.to_csv('social_status_ASC.csv', index=False)
    desiretoknowmore_ASC = modify_dataframe(desiretoknowmore_ASC)
    desiretoknowmore_ASC.to_csv('desiretoknowmore_ASC.csv', index=False)

    staic_ASC = modify_dataframe(staic_ASC)
    staic_ASC.to_csv('staic_ASC.csv', index=False)

    arousal_AS_TDC = modify_dataframe(arousal_AS_TDC)
    arousal_AS_TDC.to_csv('arousal_AS_TDC.csv', index=False)
    valence_AS_TDC = modify_dataframe(valence_AS_TDC)
    valence_AS_TDC.to_csv('valence_AS_TDC.csv', index=False)
    social_status_TDC = modify_dataframe(social_status_TDC)
    social_status_TDC.to_csv('social_status_TDC.csv', index=False)
    desiretoknowmore_TDC = modify_dataframe(desiretoknowmore_TDC)
    desiretoknowmore_TDC.to_csv('desiretoknowmore_TDC.csv', index=False)

    staic_TDC = modify_dataframe(staic_TDC)
    staic_TDC.to_csv('staic_TDC.csv', index=False)

    os.chdir("..")

#0--------
datafolder_preparation()

#1---------
seperation()
clean_eda()

#2---------

preprocessing__batch_EDA_session_seperation()
preprocessing__batch_EDA_session_seperation_BASELINE()
preprocessing__batch_ACC_session_seperation()
test()

#3--------- VIDEO CODING FEATURE EXTRACTION
coders_aggreed_video_coding_feature_extraction2()
coders_aggreed_video_coding_feature_extraction2_NONASC()

#4--------- SYSTEM LOG FEATURE EXTRACTION
systemlog_function_calls()
define_ASC_NONASC()
create_kubios_system_log_files()

# CUT AND PASTE THE FOLDERS TO OUTPUT FOLDER
cut_and_paste()
#
# ####################################################################
#
# # #5--------- EDA VIDEO CODE MARKING EVENT MARKING
eda_video_code_marking_ASC()
eda_video_code_marking_NONASC()
#
# #6--------- EDA SYSTEM LOG MARKING EVENT MARKING
eda_system_log_marking()

#7--------- EDA VIDEO AND SYSTEM LOG  MARKING EVENT MARKING
source = output_directory_path+ "0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED/"
destination=output_directory_path+ "0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED/"
copytree(source,destination)
eda_system_log_marking2()

#8--------- BATCH EDA DATA preparation before preprocesing
preprocessing__batch_EDA_session_seperation_MARKED_system_log()
preprocessing__batch_EDA_session_seperation_MARKED_video_code()
preprocessing__batch_EDA_session_seperation_MARKED_system_log_video_code()
remove_noisy_eda_for_ledalab("0009_LEGO-LOF (EDA) processed_VIDEO_EVENT_MARKED_BATCH")
remove_noisy_eda_for_ledalab('0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH')
remove_noisy_eda_for_ledalab('0009_LEGO-LOF (EDA) processed_VIDEO_SYSTEM_EVENT_MARKED_BATCH')
remove_noisy_eda_for_ledalab_system_batch("0009_LEGO-LOF (EDA) processed_SYSTEM_EVENT_MARKED_BATCH")
remove_noisy_eda_for_ledalab_break('0010_batch_break_BASELINE (EDA) processed')
remove_noisy_eda_for_ledalab_batch5('0009_batch5_LEGO-LOF (EDA) processed')
remove_noisy_eda_for_ledalab_batch_baseline('0010_batch_BASELINE (EDA) processed')
remove_noisy_eda_for_ledalab_batch('0009_batch_LEGO-LOF (EDA) processed')


#9--------- Questionnaire data extraction

extract_questionnaire()
#
#
#
#
#
#
#

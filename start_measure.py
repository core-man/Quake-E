
#from E_function import *
import numpy as np
import glob
import os
import sys
from E_function import *


# input
channel = "HH"                                          # station info
station = "GIMEL"
network = "CH"

#k = 1.4                                                         # not used, commented by Jiayuan
periods = [10, 12.5, 15, 20, 25, 30, 35, 40, 50, 60, 80, 100]   # periods
#periods = [10, 12.5, 15, 20]   # periods

cmtpath = "./CMTSOLUTIONS"                              # catalog folder
database_path = "./Data/" + station + "/"               # data folder
folder_list = os.listdir(database_path)                 # data list (events)

# output
results_folder = "Results/"                             # result folder
os.system("mkdir "+ results_folder + station)           # output folder
os.system("touch " + results_folder + "log_file.txt")   # output log file
log = open(results_folder + "log_file.txt", "a")


#### begin to measure ellipticity ####
# loop: each period
print ("Measuring " + station)
for T0 in periods:
    out = open(results_folder +  station + "/results_T"+str(T0)+".txt", "w")
    out.write("event" + "\t" + "E" + "\t" + "sd" + "\t" + "signal/noise" +"\t"+ "char_func_max" + "\n")
    n = 0   # event counter
    m = 0   # succeed ellipticity counter
#   loop: each event
    for i in range(0,len(folder_list)):
#    for i in range(0,2):
        n += 1
        event = folder_list[i]
        print ("Event: ", event, i+1, "/", len(folder_list))
        Z_file = glob.glob(database_path + folder_list[i] + "/" + network + ".*Z*.SAC.corr")
        R_file = glob.glob(database_path + folder_list[i] + "/" + network + ".*R*.SAC.corr")

        if Z_file != [] and R_file != []:
            #try:
            #R path, Z path, period, "no", event name, station name, catalog folder
            T, E, sd, snr, char_func_max = E_function(R_file[0], Z_file[0], T0, "no", event, station, cmtpath)
            #T, E, sd, snr, char_func_max = E_function(R_file[0], Z_file[0], T0, "yes", event, station, cmtpath)
            #sys.exit()
            out.write(event + "\t" + str(E) + "\t" + str(sd) + "\t" + str(snr)+ "\t" + str(char_func_max) + "\n")
            print ("Period: ", T0, "s Ellipticity: ", E)
            print ("----------------------")
            if isinstance(E, float):
                m += 1
            #except:
            #   E = "Error"
            #   sd = "Error"
            #   snr = "Error"
            #   char_func_max = "Error"
            #   out.write(event + "\t" + E + "\t" + sd + "\t" + snr +"\t"+ char_func_max + "\n")
            #   pass


# some output info
print ("\n\n\n\n--------------------------------")
print ("Tot. events number: ", n)
print ("Measurements performed: ", m)
perc = 100 * m / n
print ("Percentage: ", perc, "%")
print ("--------------------------------\n")
log.write("Station: " + station + " Done correctly!\n")
#except:
#       log.write("Station: " + station + " had some problem :( \n")
#       pass



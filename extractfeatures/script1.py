from scapy.all import *
import numpy as np
import pandas as pd
import argparse


parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
args = parser.parse_args()

inputfile = args.i
outputfile = args.o



results = []
all_packets = rdpcap(inputfile)
for packet in all_packets:
    size =  len(packet)
    try:
        proto = packet.proto
    except AttributeError:
        proto = 0
    try:
        sport = packet.sport
        dport = packet.dport
    except AttributeError:
        sport = 0
        dport = 0

    difference = abs(sport - dport)
    metric = [proto,sport,dport,size,difference]
    results.append(metric)
results = (np.array(results)).T
dataframe = pd.DataFrame({'protocl':results[0],'src':results[1],'dst':results[2],'size':results[3],'difference':results[4]})
columns = ['protocl','src','dst','size','difference']

dataframe.to_csv(outputfile,index=False,sep=',',columns = columns)

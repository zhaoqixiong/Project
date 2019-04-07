# Read me
## feature.py
usage: ./feature.py -i [input pcap file] -o [output csv file] 
>eg : ./feature.py -i /Users/xiongzhaoqi/Cambridge/Project/framework/traces/iperf.pcap  -o /Users/xiongzhaoqi/Cambridge/Project/framework/iperf.csv

It read the pcap file and convert to csv file. It extracts features: proto, srouce and destination.

## decision tree
usage: ./decision.py -i [csv file with label] -o [output txt file] 
>eg :./decisiontree.py -i /Users/xiongzhaoqi/Cambridge/Project/framework/csv/machinelearning.csv   -o /Users/xiongzhaoqi/Cambridge/Project/framework/tree.txt

It read the csv file and output the rules of the  decision tree in txt file.

## runtime.py
usage:  ./runtime.py -i [input txt file] -o [output json file]
> eg :  ./runtime.py -i /Users/xiongzhaoqi/Cambridge/Project/framework/tree.txt  -o /Users/xiongzhaoqi/Cambridge/Project/framework/runtime.json

It read the text file which describes the rule of decision tree and output the written json file which defines the table entries.

# MAKE FILE 
## make clean: 
remove the results file
## make build:
build the results file
## make class0-4 (M= input file)
## make tree
## make runtime


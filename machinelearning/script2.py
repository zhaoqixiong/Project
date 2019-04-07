from scapy.all import *
import numpy as np
import pandas as pd
import argparse
import tensorflow as tf
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i1', required=True, help='path to dataset')
parser.add_argument('-i2', required=True, help='path to dataset')
parser.add_argument('-i3', required=True, help='path to dataset')
parser.add_argument('-i4', required=True, help='path to dataset')
parser.add_argument('-i5', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
args = parser.parse_args()

input1 = args.i1
input2 = args.i2
input3 = args.i3
input4 = args.i4
input5 = args.i5
outputfile = args.o



iperf1 = pd.read_csv(input1)
iperf = iperf1.values.tolist()
a =len(iperf)

memcached1 = pd.read_csv(input2)
memcached = memcached1.values.tolist()
b =len(memcached)

ping1 = pd.read_csv(input3)
ping = ping1.values.tolist()
c =len(ping)

sparkglm1 = pd.read_csv(input4)
sparkglm = sparkglm1.values.tolist()
d =len(sparkglm)

sparkkmeans1 = pd.read_csv(input5)
sparkkmeans = sparkkmeans1.values.tolist()
e =len(sparkkmeans)

X = iperf + memcached + ping + sparkglm + sparkkmeans
Y = a*[0] + b*[1] + c*[2] + d*[3] + e* [4]


# prepare training and testing set
X = np.array(X)
Y = np.array(Y)
indices = np.random.permutation(len(X))
Training_X = X[indices[:-400]]
Training_Y = Y[indices[:-400]]
Testing_X = X[indices[-400:]]
Testing_Y = Y[indices[-400:]]


# decision tree fit

dt = DecisionTreeClassifier(max_depth = 5)
dt.fit(Training_X, Training_Y)
Predict_Y = dt.predict(Testing_X)
print(accuracy_score(Testing_Y, Predict_Y))

# output decision tree
dot_data = export_graphviz(dt, out_file=None,
                           feature_names=['proto','src','dst','size','difference'],
                           class_names=['iperf','memcached','ping','sparkglm','sparkkmeans'])
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf(outputfile)

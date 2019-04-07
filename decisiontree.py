#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
import pydotplus



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
args = parser.parse_args()

input = args.i
outputfile = args.o


def get_lineage(tree, feature_names, file):
    proto = []
    src = []
    dst = []
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value
    le = '<='
    g = '>'
    # get ids of child nodes
    idx = np.argwhere(left == -1)[:, 0]
    
    def recurse(left, right, child, lineage=None):
        if lineage is None:
            lineage = [child]
        if child in left:
            parent = np.where(left == child)[0].item()
            split = 'l'
        else:
            parent = np.where(right == child)[0].item()
            split = 'r'
        
        lineage.append((parent, split, threshold[parent], features[parent]))
        if parent == 0:
            lineage.reverse()
            return lineage
        else:
            return recurse(left, right, parent, lineage)

    for j, child in enumerate(idx):
        clause = ' when '
        for node in recurse(left, right, child):
                if len(str(node)) < 3:
                    continue
                i = node
                
                if i[1] == 'l':
                    sign = le
                else:
                    sign = g
                clause = clause + i[3] + sign + str(i[2]) + ' and '

        a = list(value[node][0])
        ind = a.index(max(a))
        clause = clause[:-4] + ' then ' + str(ind)
        file.write(clause)
        file.write(";\n")


Set1 = pd.read_csv(input)
Set = Set1.values.tolist()
X = [i[0:3] for i in Set]
Y =[i[3] for i in Set]
class_names=['iperf','memcached','ping','sparkglm','sparkkmeans']
feature_names=['proto','src','dst']


# prepare training and testing set
X = np.array(X)
Y = np.array(Y)

# decision tree fit

dt = DecisionTreeClassifier(max_depth = 5)
dt.fit(X, Y)
Predict_Y = dt.predict(X)
print(accuracy_score(Y, Predict_Y))

# output
threshold = dt.tree_.threshold
features  = [feature_names[i] for i in dt.tree_.feature]
proto = []
src = []
dst = []
for i, fe in enumerate(features):
    
    if fe == 'proto':
        proto.append(threshold[i])
    elif fe == 'src':
        if threshold[i] != -2.0:
            src.append(threshold[i])
    else:
        dst.append(threshold[i])
proto = [int(i) for i in proto]
src = [int(i) for i in src]
dst = [int(i) for i in dst]
proto.sort()
src.sort()
dst.sort()
tree = open(outputfile,"w+")
tree.write("proto = ")
tree.write(str(proto))
tree.write(";\n")
tree.write("src = ")
tree.write(str(src))
tree.write(";\n")
tree.write("dst = ")
tree.write(str(dst))
tree.write(";\n")
get_lineage(dt,feature_names,tree)
tree.close()

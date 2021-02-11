"""
Prepare some KG files with random relations dropped
in order to assess the impact of sparsity on 
model performance.
"""

import random
import networkx as nx
import pandas as pd
import numpy as np
from pathlib import Path

file_path = 'raw_data/kegg/train2id.txt'
file_template = 'raw_data/kegg/train2id_ablation'

def make_ablation_file(random_sample):
    writer = open(f'{file_template}{random_sample}.txt','w',encoding='utf8')
    
    with open(file_path, encoding='utf8') as reader:
        count=0
        for line in reader:
            if count==0: #First row is metadata(?) to keep
                writer.write(line)
                count += 1
            #Generate a random number on [0,1] and keep row only if 
            #that number is below the threshold/fraction to keep
            elif random.random() < random_sample:
                writer.write(line)
            else:
                pass
    writer.close()

def drop_nodes_on_degree():
    """Function generates 
    """
    df = pd.read_csv(file_path, sep=' ', index_col=False, header=None, skiprows=1)
    df.columns = ['node1','node2','edge_label']
    G = nx.from_pandas_edgelist(df, 'node1','node2','edge_label')
    degree_df = pd.DataFrame([(n, G.degree(n)) for n in G.nodes()], columns=['node','degree'])
    degree_df['bin'] = pd.cut(degree_df['degree'], [0,10,100,1000,1000000], labels=['bin0_10','bin10_100','bin100_1000','bin1000_n'])
    for frac in [0.1, 0.2, 0.3, 0.5, 0.8]:
        for b in degree_df['bin'].drop_duplicates().values.tolist():
            frac_nodes = degree_df[degree_df['bin'] == b].sample(frac=frac, random_state=42)['node'].values.tolist()
            df[~(df['node1'].isin(frac_nodes)) | (df['node2'].isin(frac_nodes))].to_csv(f'{file_template}_{b}_frac{frac}.txt', sep=' ')
    
    
for r in [0.001,0.01,0.1,0.2,0.3,0.5,0.7,0.9,0.95]:
    make_ablation_file(r)
drop_nodes_on_degree()

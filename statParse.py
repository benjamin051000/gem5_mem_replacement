import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from caches import *


gem5_path = "~/Tools/gem5/build/X86"
results_folder = "results"
rawout = results_folder+"/raw.txt"
grepout = results_folder+"/grep.txt"
stats = "./m5out/stats.txt"
statsout = results_folder+"/stats.txt"
tokens = [
          "Exit tick #",
          "icache.overallHits::total",               # number of overall hits (Count)
          "icache.overallMisses::total",             # number of overall misses (Count)
          "icache.overallMissLatency::total",        # number of overall miss ticks (Tick)
          "icache.overallAvgMissLatency::total",      # average overall miss latency ((Tick/Count))
          "icache.overallAccesses::total",              # number of overall (read+write) accesses (Count)
          "icache.overallMissRate::total" ,            # miss rate for overall accesses (Ratio)
          "icache.replacements",                      # number of replacements (Count)

          "dcache.overallHits::total",               # number of overall hits (Count)
          "dcache.overallMisses::total",             # number of overall misses (Count)
          "dcache.overallMissLatency::total",        # number of overall miss ticks (Tick)
          "dcache.overallAvgMissLatency::total",      # average overall miss latency ((Tick/Count))
          "dcache.overallAccesses::total",              # number of overall (read+write) accesses (Count)
          "dcache.overallMissRate::total" ,            # miss rate for overall accesses (Ratio)
          "dcache.replacements",                       # number of replacements (Count)
        ]
    
policy_list = ["FIFO","LRU","MRU","LFU","NRU","RAND"]
# policy_list = ["RAND"]

token_dict = {key : [key] for key in tokens}

def get_num(token,lines):
    for line in lines:
        if token in line:
            return line.split()[1]

    return 0
    
try:
    os.mkdir(results_folder)
except:
    pass

#clear file out 
os.system(f"echo \"\" > {rawout}")

for policy in policy_list:
    os.system(f'''{gem5_path}/gem5.opt test_bench.py \
           --rp=\'{policy}\' \
           --binary=\"./mat_mult_000.bin\" \
        >> {rawout}''')

    os.system(f"rm -f {statsout}")
    os.system(f"mv {stats} {statsout}")
    with open(statsout,"r") as f:
        lines = f.readlines()
        for token in tokens:
            num = get_num(token,lines)
            print(token,num)
            token_dict[token] += [num]

os.system(f"cat {rawout} | grep \'Exiting @ tick\' > {grepout}")
ticks = ["Exit tick #"]
with open(grepout,"r") as f:
    lines = f.readlines()
    for line in lines:
        ticks += [line.split(" ")[3]]

#ticks += [int(i) for i in ticks[1:]]
token_dict[tokens[0]] = ticks

# populate dataframe and dump to csv
df = pd.DataFrame()
df["replacement policy="] = [val[0] for key,val in token_dict.items()]
for i in range(1,len(policy_list)):
    df[policy_list[i]] = [val[i] for key,val in token_dict.items()]

df.to_csv(results_folder+"/stats.csv")


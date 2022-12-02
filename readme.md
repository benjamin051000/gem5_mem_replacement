# Cache Performance Analysis Code 

## Goals
Perform a performance analysis of several difference caching policies. 

## Tutorials Involved/Project Type

### Project Type
We technically did a Type 2 project where we chose to do a replacement policy analysis. We did the Simple Cache Tutorial and added the anaylsis of replacement policies. 

### Tutorials 
Simple Memory Objects (prereq to Simple Cache): https://www.gem5.org/documentation/learning_gem5/part2/memoryobject/
Creating Simple Cache: https://www.gem5.org/documentation/learning_gem5/part2/simplecache/

## Our Extension
The way we ended the tutorial is by doing analyzing several of the available replacement policies. The way the tutorial was involved was that we used the ```SimpleCache``` tutorial as one our test cases to demonstrate random replacement. 

## Scripts

### test_bench.py 
This is the gem5 script that gets run by statParse. This can be left alone, only thing to note is the architecture that we used to demonstate our system. We used a single level of cache and used multiple policies.

#### Architecture
* dcache size = 512B
* icache size = 512B
* single level of cache

#### Policies Tested Out
```
policy_list = ["FIFO","LRU","MRU","LFU","NRU","RAND"]
```

Where ```RAND``` is the tutorial SimpleCache that has a random replacement policy

### statsParse.py

This will automatically run our several use cases and parse the terminal output + stats.txt file for each case 

### results folder 
This has all the results. We care mostly aobut the ```stats.csv``` file that consolidates all the stats for each case. 

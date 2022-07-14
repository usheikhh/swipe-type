import os
from numpy import int32 
from tqdm import tqdm


timestamps = 0
files = 0

def count_timestamps(header_present = True):
    file_count = 0
    timestamps = []
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        file_count+=1
        f = open(os.path.join(os.getcwd(), "data", file))
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(file)
            pass
            
        for line in lines: 
            res = list(line.split(" "))[1]
            timestamps.append(res)
    if header_present == True:
        print(len(timestamps[1:]))
            
    
        

print(count_timestamps())



def extract_timestamps_from_file(path: str, header_present=True):
    file = open(path, "r")
    lines = file.readlines()
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        word = list(line.split(" "))[10]
        timestamps.append((res))
    if header_present == True:
        return sum(timestamps[1:])
    elif header_present == False:
        return sum(timestamps)


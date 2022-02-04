from itertools import groupby
scan_list = [False,False,10,1,1,False,1,2,3,False,4]
print(scan_list)
grouping = [list(g) for k, g in groupby(scan_list, lambda x: x != False) if k]
print(grouping)
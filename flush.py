from glob import glob
import os
files = glob('*.csv')
files1 = glob('*.mov')
files2 = glob('*.jpg')
if len(files) == 0:
    print("No .CSV files")
else:
    count =0
    for file in files:
        os.remove(file)
        count=count+1
    print("{} temporary files deleleted.".format(count))
if len(files1) == 0:
    print("No .MOV files")
else:
    count1 =0
    for fileD in files1:
        os.remove(fileD)
        count1=count1+1
    print("{} temporary files deleleted.".format(count1))
if len(files2) == 0:
    print("No .JPG files")
else:
    count2 =0
    for fileJ in files2:
        os.remove(fileJ)
        count2=count2+1
    print("{} temporary files deleleted.".format(count2))

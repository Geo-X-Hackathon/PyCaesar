from osgeo import gdal
import os

f = open('files.txt', 'r')

numlist=[]
for line in f:
	num=line[8:].split('.')[0],
	if num[0]=='0' or num[0]=='':
		continue
	numlist.append(int(num[0]))
f.close()
sortedlist=sorted(numlist)

for num in sortedlist:
	filename='../CAESAR_data/D4/elev.dat'+str(num)+'.txt'
	dataset=gdal.Open(filename, gdal.GA_ReadOnly)	
	print("Size is {} x {} x {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
	dataset = None



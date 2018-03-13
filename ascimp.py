from osgeo import gdal
import numpy as np

f = open('files.txt', 'r')

numlist=[]
for line in f:
	num=line[8:].split('.')[0],
	if num[0]=='0' or num[0]=='':
		continue
	numlist.append(int(num[0]))
f.close()
sortedlist=sorted(numlist)

first=True

#Get First Image and check dimensions
filename='../CAESAR_data/D4/elev.dat'+str(sortedlist[0])+'.txt'
dataset=gdal.Open(filename, gdal.GA_ReadOnly)
print("Size of one DTM is {} x {} x {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("There are {} time steps".format(len(sortedlist)))
#Build n-dimensional array (currently 3)
array=np.empty([dataset.RasterYSize,dataset.RasterXSize,len(sortedlist)],dtype=np.float)
print("Array size is {}".format(array.shape))

#Cycle through all images and append to array
for i in range(0,len(sortedlist)):
	num=sortedlist[i]
	name='../CAESAR_data/D4/elev.dat'+str(num)+'.txt'
	ds=gdal.Open(name, gdal.GA_ReadOnly)	
	a=ds.GetRasterBand(1).ReadAsArray()
	array[:,:,i]=a
	array[:,:,i][a<-999]=np.nan
	ds = None



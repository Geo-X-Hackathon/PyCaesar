from osgeo import gdal
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import QCaesarTemplate as QCaesarTemplate


app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('QCaesar')
ui = QCaesarTemplate.Ui_MainWindow()
ui.setupUi(win)
win.show()

f = open('files.txt', 'r')
numlist=[]
for line in f:
	num=line[8:].split('.')[0],
	if num[0]=='0' or num[0]=='':
		continue
	numlist.append(int(num[0]))
f.close()
sortedlist=sorted(numlist)

#Make smaller for testing
numImages=240

#Get First Image and check dimensions
filename='../CAESAR_data/D4/elev.dat'+str(sortedlist[0])+'.txt'
dataset=gdal.Open(filename, gdal.GA_ReadOnly)
print("Size of one DTM is {} x {} x {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("There are {} time steps".format(len(sortedlist)))
ns=dataset.RasterXSize
nl=dataset.RasterYSize
array=np.empty([nl,ns,numImages],dtype=np.float)
print("Array size is {}".format(array.shape))
dataset=None

#Cycle through all images and append to array
#for i in range(0,len(sortedlist)):
if True: #set to false after first run to speed up
  for i in range(0,numImages):
	num=sortedlist[i]
	name='../CAESAR_data/D4/elev.dat'+str(num)+'.txt'
	ds=gdal.Open(name, gdal.GA_ReadOnly)	
	a=ds.GetRasterBand(1).ReadAsArray()
	array[:,:,i]=a
	array[:,:,i][a<-999]=np.nan
	ds = None
  np.save('elev.npy',array)
else:
  array = np.load('elev.npy')

min=np.nanmin(array)
max=np.nanmax(array)
heightFactor=1.
normarray=(array-min)*heightFactor/(max-min)
min=np.nanmin(normarray)
max=np.nanmax(normarray)

diff=np.absolute(np.diff(array,axis=2))
diff[diff > .001] = np.log10(diff[diff > .001])-np.nanmin(np.log10(diff[diff > .001]))
diff=diff/np.nanmax(diff)
diff[diff < .001] = 0.

colors=np.zeros([nl,ns,4],dtype=float)

a=np.squeeze(diff[:,:,0])
colors[:,:,1]=a
colors[:,:,0]=a
colors[colors<0.001]=1.

ui.diffView.plot(y=diff[:,:,0].flatten())

ui.dtmView.setCameraPosition(distance=25)

g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
ui.dtmView.addItem(g)

z = np.squeeze(normarray[:,:,0])
p1 = gl.GLSurfacePlotItem(z=z, shader='shaded', colors=colors.reshape(ns*nl,4), computeNormals=True, smooth=False)
p1.scale(1./50., 1./50., 2.)
ui.dtmView.addItem(p1)

ui.horizontalSlider.setMaximum(len(sortedlist)-2)
index = 0
def update():
	global colors,normarray, p1, z, index
	if index<numImages-2:
		index += 1
	else:
		index=0
	#print index
	a=np.squeeze(diff[:,:,index])
	colors[...]=0.
	colors[:,:,1]=a
	colors[:,:,0]=a
	colors[colors<0.001]=1.
	#p1.setData(z=np.squeeze(normarray[:,:,index]), colors=colors.reshape(ns*nl,4))
	if ui.diffBox.isChecked():
		p1.setData(z=np.squeeze(diff[:,:,index]), colors=colors.reshape(ns*nl,4))
	else:
		p1.setData(z=np.squeeze(normarray[:,:,index]), colors=colors.reshape(ns*nl,4))
	ui.diffView.plot(y=diff[:,:,index].flatten())
	ui.frameNumber.display(index)
	ui.horizontalSlider.setProperty("value", index)

def sliderChange():
	val=ui.horizontalSlider.value()
	#print "val",val
	#ui.timeSlider.setProperty("value", val)
	a=np.squeeze(diff[:,:,val])
	colors[...]=0.
	colors[:,:,1]=a
	colors[:,:,0]=a
	colors[colors<0.001]=1.
	p1.setData(z=np.squeeze(normarray[:,:,val]), colors=colors.reshape(ns*nl,4))
	ui.diffView.plot(y=diff[:,:,val].flatten())
	ui.frameNumber.display(val)
	
#ui.horizontalSlider.sliderMoved.connect(sliderChange)
ui.horizontalSlider.sliderReleased.connect(sliderChange)
toggled=0
def timeMovie():
	global toggled
	if toggled==0:
		toggled=1
		timer.start(30)
	else:
		toggled=0
		timer.stop()

timer = QtCore.QTimer()
timer.timeout.connect(update)
ui.checkBox.toggled.connect(timeMovie)




QtGui.QApplication.instance().exec_()

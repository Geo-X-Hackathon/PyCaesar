from osgeo import gdal
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import QCaesarTemplate as QCaesarTemplate


app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
ui = QCaesarTemplate.Ui_MainWindow()
ui.setupUi(win)
win.show()

#try:
#    from pyqtgraph.opengl.RawImageWidget import GLGraphicsItem
#except ImportError:
#    ui.rawGLRadio.setEnabled(False)
#    ui.rawGLRadio.setText(ui.rawGLRadio.text() + " (OpenGL not available)")
#else:
#    ui.rawGLImg = RawImageGLWidget()
#    ui.stack.addWidget(ui.rawGLImg)

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
if False: #run only once
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

#plot diffs
#win = pg.GraphicsWindow(title="Basic plotting examples")
#win.resize(1000,600)
#win.setWindowTitle('pyqtgraph example: Plotting')
#p1 = win.addPlot(title="Basic array plotting", y=diff[:,:,0].flatten())

ui.diffView.plot(y=diff[:,:,0].flatten())











QtGui.QApplication.instance().exec_()
"""
这个软件最大的作用是同时展现多条trace，是加载trace.mat的最佳选择。同时还可以标注感兴趣的时间区间；
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTextCodec

from PyQt5 import uic
import pyqtgraph as pg
import os
import scipy.io as scio
import math

class TVWindow(QMainWindow):
    plotList = []
    lastChoosePath = r'D:\Data\SanChaShenJingTong\fzh-TN-CalciumSignal\2021-04-04--0030-P1\CellVideo1'
    l = 0
    r = 0
    SOFTWAREVERSION = r'Trace.mat Visualization V0.0.2'
    SOFTWARECOPYRIGHT = r' 2021-2023 FengZhiheng'
    SOFTWAREAUTHOR = r'Feng Zhiheng'
    SOFTWAREEMAIL = r'zhihengfeng5371@163.com'
    WELCOMEMESSAGE = 'Welcom to use ' + SOFTWAREVERSION + "!"
    def __init__(self):
        super(TVWindow, self).__init__()#调用父类的构造函数
        uic.loadUi(r'./GUI/TraceVisualization.ui', self)

        self.btnOpenTraceMat.clicked.connect(self.slotOpenTraceMat)
        self.btnOpenTraceMat.installEventFilter(self)

        self.btnCloseAll.clicked.connect(self.slotCloseAll)

        self.setWindowTitle(self.SOFTWAREVERSION)
        self.statusBar().showMessage(self.WELCOMEMESSAGE)

        print(self.WELCOMEMESSAGE)

    def slotOpenTraceMat(self, tracefilePath = ""):

        if tracefilePath == "" or tracefilePath is False:
            traceMatPath, filetype = QFileDialog.getOpenFileName(self,
                                                                 "载入Neurons",
                                                                 self.lastChoosePath,
                                                                 "Trace(*.mat)")  # 设置文件扩展名过滤,注意用双分号间隔
        else:
            traceMatPath = tracefilePath


        if traceMatPath == '':
            self.statusBar().showMessage("取消")
            return

        self.lastChoosePath = traceMatPath

        mat = scio.loadmat(traceMatPath)
        NeuronSig = mat['dff']

        #加一个施加疼痛刺激的range
        #这里来一个对话框，支持用户把range给输入进来最好了；
        noteDialog = QInputDialog(self)
        noteDialog.setWindowTitle("输入Range")
        noteDialog.setLabelText("格式：1000-2000")
        if noteDialog.exec_() == QDialog.Accepted:
            try:
                rangeInfo = noteDialog.textValue()
                self.l = int(rangeInfo.split('-')[0])
                self.r = int(rangeInfo.split('-')[1])
            except:
                self.l = 0
                self.r = 0

        if NeuronSig.shape[0] > 20:
            curveNum = 20
            figNum = math.ceil(NeuronSig.shape[0] / curveNum)
        else:
            figNum = 1
            curveNum = NeuronSig.shape[0]

        for i in range(figNum):
            start = i*curveNum
            if (i+1)*curveNum > NeuronSig.shape[0]:
                end = NeuronSig.shape[0]
            else:
                end = (i+1)*curveNum
            textLabel = range(start, end)
            tmpData = NeuronSig[start:end]
            plotName = "Gourp"+str(i+1)
            position = [(i%7)*500,(i//7)*1000]
            pen = (i*3, 20*1.3)  #创建颜色的方法请参考： https://pyqtgraph.readthedocs.io/en/latest/functions.html#pyqtgraph.intColor
            self.createPlotWindowAndPlot(tmpData, plotName, position, pen,textLabel)

        self.statusBar().showMessage("Load trace.mat finished!")
        print("load trace.mat finished")

    def createPlotWindowAndPlot(self, NeuronSig, plotName, position, pen,textLabel):
        # 在原始界面上刷新有点卡。所以再来一个plot界面，看看。
        # 结论是，依然很卡
        plot = pg.plot(title = plotName)
        self.plotList.append(plot.parent())
        plot.resize(500,1000) #对plot窗口的大小进行设置
        plot.parent().move(position[0], position[1]) #对plot窗口在显示器上的相对位置进行设置
        # plot.setWindowTitle('MultiPlotTest')
        plot.setLabel('bottom', plotName)
        


        lr = pg.LinearRegionItem([self.l, self.r])
        plot.addItem(lr)

        nPlots = NeuronSig.shape[0]
        for idx in range(nPlots):
            curve = pg.PlotCurveItem(pen=pen)
            curve.setData(NeuronSig[idx,:])
            plot.addItem(curve)
            curve.setPos(0,idx*3)

            label = textLabel[idx]
            text = pg.TextItem(text=str(label+1))
            text.setPos(0, idx*3)
            plot.addItem(text)

    def eventFilter(self, object, event):
        if (object is self.btnOpenTraceMat):
            if (event.type() == QtCore.QEvent.DragEnter):

                if event.mimeData().text().endswith(".mat") and event.mimeData().hasUrls():
                    path = event.mimeData().urls()[0].toLocalFile()
                    self.lastChoosePath = path
                    event.accept()
                    print("accept")

                else:
                    event.ignore()
                    print("ignore")

            if (event.type() == QtCore.QEvent.Drop):
                self.slotOpenTraceMat(tracefilePath=self.lastChoosePath)
                print("droped")

            return False
        return False

    def slotCloseAll(self):

        for p in self.plotList:
            p.close()
        self.plotList = []
        self.statusBar().showMessage("Close all plot finished!")
        print("Close all plot finished!")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = TVWindow()

    ui.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
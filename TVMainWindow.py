from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from PyQt5 import uic
import pyqtgraph as pg


SOFTWAREVERSION = r'Trace.mat Visualization V0.0.1'
SOFTWARECOPYRIGHT = r' 2021-2023 FengZhiheng'
SOFTWAREAUTHOR = r'Feng Zhiheng'
SOFTWAREEMAIL = r'zhihengfeng5371@163.com'
WELCOMEMESSAGE = 'Welcom to use ' + SOFTWAREVERSION + "!"

#这个软件最大的作用是，可以标注index。


class TVWindow(QMainWindow):
    plotList = []
    def __init__(self):
        super(TVWindow, self).__init__()#调用父类的构造函数
        uic.loadUi(r'./GUI/TraceVisualization.ui', self)
        self.btnOpenTraceMat.clicked.connect(self.slotOpenTraceMat)
        self.btnCloseAll.clicked.connect(self.slotCloseAll)
        self.setWindowTitle(SOFTWAREVERSION)
        print(WELCOMEMESSAGE)

    def slotOpenTraceMat(self):

        self.lastChoosePath = r'D:\Data\SanChaShenJingTong\fzh-TN-CalciumSignal\2021-04-04--0030-P1\CellVideo1'
        traceMatPath, filetype = QFileDialog.getOpenFileName(self,
                                                             "载入Neurons",
                                                             self.lastChoosePath,
                                                             "Trace(*.mat)")  # 设置文件扩展名过滤,注意用双分号间隔
        if traceMatPath == '':
            self.statusBar().showMessage("取消")
            return

        self.lastChoosePath = traceMatPath
        import scipy.io as scio
        mat = scio.loadmat(traceMatPath)
        NeuronSig = mat['dff']

        curveNum = 20
        figNum = NeuronSig.shape[0] // curveNum - 1
        # figNum = 3

        for i in range(figNum):
            textLabel = range(i*curveNum,(i+1)*curveNum)
            tmpData = NeuronSig[i*curveNum:(i+1)*curveNum]
            plotName = "Gourp"+str(i)
            position = [(i%7)*500,(i//7)*1000]
            pen = (i*3, 20*1.3)  #创建颜色的方法请参考： https://pyqtgraph.readthedocs.io/en/latest/functions.html#pyqtgraph.intColor
            self.createPlotWindowAndPlot(tmpData, plotName, position, pen,textLabel)



        print("slotOpenTraceMat")


    def createPlotWindowAndPlot(self, NeuronSig, plotName, position, pen,textLabel):
        # 在原始界面上刷新有点卡。所以再来一个plot界面，看看。
        # 结论是，依然很卡
        plot = pg.plot(title = plotName)
        self.plotList.append(plot.parent())
        plot.resize(500,1000) #对plot窗口的大小进行设置
        plot.parent().move(position[0], position[1]) #对plot窗口在显示器上的相对位置进行设置
        # plot.setWindowTitle('MultiPlotTest')
        plot.setLabel('bottom', plotName)

        nPlots = NeuronSig.shape[0]
        for idx in range(nPlots):
            curve = pg.PlotCurveItem(pen=pen)
            curve.setData(NeuronSig[idx,:])
            plot.addItem(curve)
            curve.setPos(0,idx*3)

            label = textLabel[idx]
            text = pg.TextItem(text=str(label))
            text.setPos(0, idx*3)
            plot.addItem(text)

    def slotCloseAll(self):
        print("slotCloseAll")
        for p in self.plotList:
            p.close()
        self.plotList = []


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = TVWindow()

    ui.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
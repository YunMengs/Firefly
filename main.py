import ctypes
import json
import subprocess
import threading
import time

from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide2.QtUiTools import QUiLoader
from Dnconsole import Dnconsole
from model.func import stop_thread
from task.FriendTask import FriendTask
from task.TestTask import TestTask


class MainModel:
    # 当前控制的vm index
    index = None
    # 当前控制的vm index
    setupUI = None
    # 当前控制的VM
    vm = None
    # 启动的列表
    startList = {}
    # 启动的线程列表
    threadingtList = {}

    def screenshotButtonHandle(self):
        """
        截图
        :return:
        """
        self.getVM()
        # ' + str(int(time.time())) + '
        Dnconsole.dnld(self.index, 'screencap -p /mnt/shared/Pictures/' + str(self.index) + 'screencap.png')

    def setupButtonHandle(self):
        """
        打开设置
        :return:
        """
        self.setupUI = QUiLoader().load('setup.ui')
        self.setupUI.show()

    def pauseButtonHandle(self):
        """
        暂停 继续 处理
        :return:
        """
        dn = Dnconsole
        self.getVM()
        self.startList[self.index].pause()
        arr = ["未开始", "暂停", "继续"]
        self.ui.pauseButton.setText(arr[self.startList[self.index].status])

    def stopButtonHandle(self):
        """
        游戏结束
        :return:
        """
        self.getVM()
        # 停止所有子线程
        self.startList[self.index].game_over()
        # 停止主线程
        stop_thread(self.threadingtList[self.index])
        print("停止游戏")

    def StartUpSimulatorButtonHandle(self):
        dn = Dnconsole
        """
        启动模拟器处理事件
        :return: None
        """
        item = self.ui.tableWidget.selectedItems()
        index = int(item[0].text())
        dn.set_screen_size(index)
        dn.launch(index)
        self.vm = dn.get_one_list(index)

    def StartUpScriptButtonHandle(self):
        """
        启动脚本处理事件
        :return: None
        """
        dn = Dnconsole
        self.getVM()
        index = self.ui.comboBoxTask.currentIndex()
        print("index：" + str(index))
        if index == 1:
            start = FriendTask(self.vm, self.index)
        else:
            start = TestTask(self.vm, self.index)

        self.startList[self.index] = start
        # 创建线程
        self.threadingtList[self.index] = threading.Thread(target=start.start_game(), args=())
        # 启动线程
        self.threadingtList[self.index].start()

    def getVM(self):
        """
        获取VM模拟器
        :return:
        """
        dn = Dnconsole
        item = self.ui.tableWidget.selectedItems()
        if len(item) <= 0:
            self.index = 0
        else:
            self.index = int(item[0].text())
        self.vm = dn.get_one_list(self.index)

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit

        self.ui = QUiLoader().load('main.ui')

        self.ui.tableWidget.setStyleSheet(
            '''QWidget{min-height: 20px; font-size:10pt;border-radius:3px;background-color:rgb(240,248,255);color: 
            rgb(0,0,0)}''')

        # self.ui.pushButton_3.clicked.connect(lambda: self.add_timer(self.ui.pushButton_3))

        dn = Dnconsole
        vmlist = dn.get_list()
        # 遍历模拟器
        for index in range(len(vmlist)):
            item = vmlist[index]
            col_1 = QtWidgets.QTableWidgetItem(str(item.index))
            col_2 = QtWidgets.QTableWidgetItem(item.name)
            if item.is_in_android:
                openStatus = "打开"
            else:
                openStatus = "关闭"
            col_3 = QtWidgets.QTableWidgetItem(openStatus)
            self.ui.tableWidget.insertRow(int(self.ui.tableWidget.rowCount()))
            self.ui.tableWidget.setItem(index, 0, col_1)
            self.ui.tableWidget.setItem(index, 1, col_2)
            self.ui.tableWidget.setItem(index, 2, col_3)
            self.ui.tableWidget.update()

        # 自动拉升最后一列
        # self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 每一列都拉伸, 使用QHeaderView的setSectionResizeMode函数，将resizemode设置为QHeaderView::Stretch。
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 禁止编辑
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 只允许单行选中
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 为按钮绑定事件
        self.ui.StartUpSimulatorButton.clicked.connect(self.StartUpSimulatorButtonHandle)
        self.ui.StartUpScriptButton.clicked.connect(self.StartUpScriptButtonHandle)
        self.ui.pauseButton.clicked.connect(self.pauseButtonHandle)
        self.ui.stopButton.clicked.connect(self.stopButtonHandle)
        self.ui.setupButton.clicked.connect(self.setupButtonHandle)
        self.ui.screenshotButton.clicked.connect(self.screenshotButtonHandle)


app = QApplication([])
# 加载 icon
app.setWindowIcon(QIcon('./img/logo.ico'))
stats = MainModel()
stats.ui.show()
app.exec_()

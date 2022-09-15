#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：TFTBrother
@File    ：TFTStartModel.py
@Author  ：织梦行云
@Date    ：2021/9/18 23:12
"""
import random
from Dnconsole import Dnconsole
import threading
import time

from model.func import stop_thread


class TFTStartModel:
    # 当前控制的VM
    vm = None
    # 当前控制的VM index
    index = None
    # 阵容选择 0. 随机 1.黎明使者 2.小恶魔
    lineup = 0

    # 游戏线程
    GameThreading = []

    # 每步操作间隔时间
    sleep = 1
    # 游戏中处理间隔时间
    setup = 60 * 15
    # 0.结束 1.游戏中 2.暂停中
    status = 0
    # 当前阶段 0未开始 11 为 1-1 22 为 2-2 以此类推
    stage = 0
    # 当前D牌次数
    dnum = 20
    # 设定的D牌频率
    frequency = 60

    # 棋盘战场的最大最小坐标
    minX = 645
    minY = 212
    maxX = 1300
    maxY = 700

    # 装备栏坐标
    EquipmentX = [346, 400, 337, 390, 445, 355, 320, 341, 305]
    EquipmentY = [619, 619, 660, 660, 656, 685, 714, 746, 775]

    # 空白坐标
    spaceX = 900
    spaceY = 40

    # 场上英雄坐标(加入部分观众席英雄坐标)
    heroPosX = [963, 898, 964, 1092, 1017, 1084, 1225, 1152] + [446, 555, 674, 790, 906, 1022]
    heroPosY = [645, 563, 492, 636, 571, 488, 631, 555] + [744, 739, 742, 743, 743, 744]
    # 观众席坐标
    watcherPosX = [446, 555, 674, 790, 906, 1022, 1137, 1253, 1366]
    watcherPosY = [744, 739, 742, 743, 743, 744, 743, 744, 743]

    def CheckState(self):
        """
        确认当前状态
        :return: int 返回状态码 0.模拟器主界面 1.云游戏APP内
        """
        dn = Dnconsole
        # ok, xy = dn.wait_picture(self.index, 10, r".\img\TXStartAPP.png")
        # if not ok:
        #     return
        # dn.touch(self.index, xy[0], xy[1])
        ok, xy = dn.wait_picture(self.index, 10, r".\img\zuijinzaiwanTFT.png")
        # if not ok:
        #     return
        # dn.touch(self.index, xy[0], xy[1])

    def StartGame(self):
        """
        开始游戏
        :return:
        """
        dn = Dnconsole
        # 设置操作模式
        # dn.touch(self.index, 60, 144)
        # time.sleep(self.sleep)
        # # 判断虚拟键是否存在 不存在就开启虚拟键
        # ok, xy = dn.wait_picture(self.index, 1, r".\img\ESC.png")
        # if not ok:
        #     dn.touch(self.index, 255, 114)
        # time.sleep(self.sleep)
        # # 打开操作模式选择
        # dn.touch(self.index, 109, 182)
        # time.sleep(self.sleep)
        # # 选择触屏
        # dn.touch(self.index, 1083, 395)
        # time.sleep(self.sleep)
        # # 确定操作模式
        # dn.touch(self.index, 960, 774)
        self.StartUp()

    def StartUp(self):
        """
        开始游戏
        :return:
        """
        dn = Dnconsole
        # 每步操作间隔时间
        self.sleep = 1
        # 游戏中处理间隔时间
        self.setup = 60 * 15
        # 0.结束 1.游戏中 2.暂停中
        self.status = 0
        # 设定的D牌频率
        self.frequency = 60

        print("开始游戏")
        # # 打开左键键
        # ok, xy = dn.wait_picture(self.index, 1, r".\img\左键虚拟键.png")
        # if not ok:
        #     # 开的右键就改成左键
        #     dn.touch(self.index, 44, 262)

        # 开始匹配
        time.sleep(self.sleep)
        dn.touch(self.index, 824, 1035)
        # 再点一次匹配防止未点击
        time.sleep(self.sleep)
        dn.touch(self.index, 824, 1035)
        # 等待匹配
        self.GameMatching()
        self.status = 1
        # 判断游戏是否结束了
        self.GameThreading.insert(0, threading.Timer(720, self.GameOverCheck))
        self.GameThreading[0].start()
        # 每个阶段的操作
        self.GameThreading.insert(1, threading.Timer(10, self.stageHandle))
        self.GameThreading[1].start()
        # 每隔一段时间买牌
        self.GameThreading.insert(2, threading.Timer(30, self.BuyCards))
        self.GameThreading[2].start()
        # 捡取战利品、上装备
        # self.GameThreading.insert(3, threading.Timer(20, self.UpperEquipment))
        # self.GameThreading[3].start()

    def test(self):
        # 每步操作间隔时间
        self.sleep = 1
        # 游戏中处理间隔时间
        self.setup = 60 * 15
        # 0.结束 1.游戏中 2.暂停中
        self.status = 1
        # 判断游戏是否结束了
        self.GameThreading.insert(0, threading.Timer(10, self.GameOverCheck))
        self.GameThreading[0].start()
        # 每个阶段的操作
        self.GameThreading.insert(1, threading.Timer(1, self.stageHandle))
        self.GameThreading[1].start()
        # 每隔一段时间买牌
        self.GameThreading.insert(2, threading.Timer(1, self.BuyCards))
        self.GameThreading[2].start()
        # self.CheckIsDawnMessenger(self.watcherPosX, self.watcherPosY)
        # self.CheckIsDawnMessenger(self.heroPosX, self.heroPosY)

    def GameMatching(self, needmatching: bool = True):
        """
        检测匹配状态
        :param needmatching:为False时跳过检测匹配直接检测是否被拒绝
        :return:
        """
        dn = Dnconsole
        # 等待匹配
        if needmatching:
            while True:
                # 鼠标移动到空闲位置防止遮挡识别
                dn.touch(self.index, 900, 40)
                ok, xy = dn.wait_picture(self.index, 10, r".\img\accept.png", 1)
                if ok:
                    # 点击确认匹配
                    dn.touch(self.index, 960, 839)
                    # 鼠标移动到空闲位置防止遮挡识别
                    dn.touch(self.index, 900, 40)
                    break

        # 是否被拒绝了
        while True:
            # 鼠标移动到空闲位置防止遮挡识别
            dn.touch(self.index, 900, 40)
            template = [
                r"./img/InQueue.png",
                r"./img/accept.png",
                r"./img/阶段/1-1.png",
            ]
            i, xy = dn.check_picture(self.index, template, 1, threshold=0.01)

            if i == 0:
                # 被人拒绝了重新匹配
                self.GameMatching()
                return 1
            elif i == 1:
                # 点击确认匹配
                dn.touch(self.index, 960, 839)
                self.GameMatching(False)
                return 1
            elif i == 2:
                self.stage = 11
                print("已进入游戏")
                return 1

    def OpenSpace(self):
        """
        鼠标移动到空闲位置防止遮挡识别
        :return:
        """
        # 鼠标移动到空闲位置防止遮挡识别
        Dnconsole.touch(self.index, 900, 40)

    def GameOverCheck(self):
        """
        游戏状态检测 游戏是否结束了
        :return:
        """
        dn = Dnconsole
        while True:
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            # 有可能被打死了 点击退出
            dn.touch(self.index, 845, 554)
            # 点两次防止把棋子点起来
            dn.touch(self.index, 845, 554)
            # 鼠标移动到空闲位置防止遮挡识别
            dn.touch(self.index, 900, 40)
            time.sleep(2)
            template = [
                r".\img\LingJiangLiOk.png",
                r".\img\RestartGame.png",
                r".\img\LookingMatch.png",
            ]

            i, xy = dn.check_picture(self.index, template, 1, threshold=0.1, shareimg='GameOver.png')
            if i == 0:
                # 点击ok 领取 多点几次把奖励领完
                self.OpenLeftKey()
                for i in range(5):
                    dn.touch(self.index, xy[0] + 15, xy[1] + 5)
                    time.sleep(self.sleep)
                continue
            elif i == 1:
                self.OpenLeftKey()
                # 游戏结束了 点击再来一次
                dn.touch(self.index, 824, 1035)
                self.GameRestart()
                return 1
            elif i == 2:

                # 游戏可能退出在房间里了 继续游戏
                self.GameRestart()
                return 1

            # 间隔
            time.sleep(28)

    def UpperEquipment(self):
        """
        捡取战利品、上装备
        :return:
        """
        dn = Dnconsole
        # 捡取战利品
        # 左键是否打开了 True 打开 False 未打开
        OpenLeftKey = True
        # 鼠标移动到空闲位置防止遮挡识别
        dn.touch(self.index, 900, 40)
        template = [
            r"./img/战利品/金色战利品.png",
            r"./img/战利品/蓝色战利品.png",
            r"./img/战利品/白色战利品.png",
        ]
        for index in range(10):
            i, xy = dn.check_picture(self.index, template, 1, threshold=0.1)
            if i >= 0:
                # 打开右键
                if OpenLeftKey:
                    self.OpenLeftKey(False)
                    OpenLeftKey = False
                dn.touch(self.index, xy[0] + 10, xy[1] + 10)
            else:
                # 没有检测到就break不用浪费时间继续检测了
                break

        # 恢复左键 如果没有打开就打开左键
        if not OpenLeftKey:
            self.OpenLeftKey(True)

            # 先暂停其他操作
            # self.status = 2
            # time.sleep(self.sleep)

            # 上装备
            # print("上装备")
            # # 点击空白
            # dn.touch(self.index, self.spaceX, self.spaceY)
            # for i in range(len(self.EquipmentX)):
            #     # 拿装备
            #     dn.touch(self.index, self.EquipmentX[i], self.EquipmentY[i])
            #     time.sleep(1)
            #     # 放在观众席第一个棋子上
            #     dn.touch(self.index, self.SpectatorSeatsX[0], self.SpectatorSeatsY[0])
            #     time.sleep(0.5)
            #     # 点击空白
            #     dn.touch(self.index, self.spaceX, self.spaceY)
            #     time.sleep(0.5)

    def stageHandle(self):
        """
        每个阶段的操作
        :return:
        """
        dn = Dnconsole
        while True:
            # 判断游戏状态
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            Dnconsole.dnld(self.index, 'screencap -p /sdcard/Pictures/stage.png')
            time.sleep(1)
            """
            2-1 查4块 升级1次
            2-5 差8块 升级2次
            3-2 差16块 升级4次
            4-1 差28块 升级 7次
            5-1 差44块 升级 11次
            6-1 差68块 升级 11次
            """
            if self.stage < 22:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/2-2.png", 0.01)
                if ok:
                    print("进入2-2")
                    # 先暂停其他操作
                    self.status = 2
                    # 先拿装备
                    dn.touch(self.index, 783, 932)
                    # 卖掉选秀棋子
                    dn.touch(self.index, 960, 660)
                    # 34是F 32是D 33是E
                    Dnconsole.dnld(self.index, "input keyevent 33")
                    # 升级
                    self.UpgradeDo()
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    self.stage = 22
            if self.stage < 25:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/2-5.png", 0.01)
                if ok:
                    print("进入2-5")
                    # 先暂停其他操作
                    self.status = 2
                    # 升级
                    self.UpgradeDo(2)
                    self.stage = 25
            if self.stage < 32:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/3-2.png", 0.01)
                if ok:
                    print("进入3-2")
                    # 先暂停其他操作
                    self.status = 2
                    # 升级
                    self.UpgradeDo(4)
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    self.stage = 32
            # if self.stage < 33:
            #     ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/3-3.png", 0.01)
            #     if ok:
            #         print("进入3-3")
            #         # 先暂停其他操作
            #         self.status = 2
            #         # 卖棋子
            #         self.CheckIsDawnMessenger(self.watcherPosX, self.watcherPosY)
            #         self.stage = 33
            # if self.stage < 35:
            #     ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/3-5.png", 0.02)
            #     if ok:
            #         print("进入3-5")
            #         # 先暂停其他操作
            #         self.status = 2
            #         # 卖棋子
            #         self.CheckIsDawnMessenger(self.heroPosX, self.heroPosY)
            #         self.stage = 35
            if self.stage < 36:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/3-6.png", 0.02)
                if ok:
                    print("进入3-6")
                    # 先暂停其他操作
                    self.status = 2
                    # 拿光明装备
                    dn.touch(self.index, 888, 938)
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    self.stage = 36
            if self.stage < 41:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/4-1.png", 0.02)
                if ok:
                    print("进入4-1")
                    # 先暂停其他操作
                    self.status = 2
                    # 升级
                    self.UpgradeDo(7)
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    # 设定的D牌频率
                    self.frequency = 20
                    self.stage = 41
            # if self.stage < 43:
            #     ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/4-3.png", 0.02)
            #     if ok:
            #         print("进入4-3")
            #         # 先暂停其他操作
            #         self.status = 2
            #         # 卖棋子
            #         self.CheckIsDawnMessenger(self.watcherPosX, self.watcherPosY)
            #         self.stage = 43
            # if self.stage < 46:
            #     ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/4-6.png", 0.02)
            #     if ok:
            #         print("进入4-6")
            #         # 先暂停其他操作
            #         self.status = 2
            #         # 卖棋子
            #         self.CheckIsDawnMessenger(self.heroPosX, self.heroPosY)
            #         self.stage = 46
            if self.stage < 51:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/5-1.png", 0.02)
                if ok:
                    print("进入5-1")
                    # 先暂停其他操作
                    self.status = 2
                    # 升级
                    self.UpgradeDo(11)
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    # 设定的D牌频率
                    self.frequency = 10
                    self.stage = 51
            # if self.stage < 53:
            #     ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/5-3.png", 0.02)
            #     if ok:
            #         print("进入5-3")
            #         # 先暂停其他操作
            #         self.status = 2
            #         # 卖棋子
            #         self.CheckIsDawnMessenger(self.watcherPosX, self.watcherPosY)
            #         self.stage = 53
            if self.stage < 61:
                ok, xy = Dnconsole.find_pic(Dnconsole.share_path + '/stage.png', r"./img/阶段/6-1.png", 0.02)
                if ok:
                    print("进入6-1")
                    # 先暂停其他操作
                    self.status = 2
                    # 升级
                    self.UpgradeDo(17)
                    # 捡取战利品上装备
                    self.UpperEquipment()
                    # 设定的D牌频率
                    self.frequency = 3
                    self.stage = 61

            # 恢复操作
            self.status = 1
            time.sleep(10)

    def RefreshCard(self):
        """
        D牌
        :return:
        """
        # D牌
        # 34是F 32是D 33是E
        Dnconsole.dnld(self.index, "input keyevent 32")
        # Dnconsole.touch(self.index, 430, 1040)

    def UpgradeDo(self, num=1):
        """
        升级
        :return:
        """
        for i in range(num):
            # 升级
            # 34是F 32是D 33是E
            Dnconsole.dnld(self.index, "input keyevent 34")
            # Dnconsole.touch(self.index, 414, 965)

    def upgrade(self):
        """
        升级
        :return:
        """
        dn = Dnconsole
        while True:
            # 判断游戏状态
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            # D牌
            # dn.touch(self.index, 430, 1040)

            # 每隔一段时间升级
            for i in range(20):
                # dn.touch(self.index, 414, 965)
                # 34是F 32是D 33是E
                self.UpgradeDo()

            # 走动一番
            # minX = 645
            # minY = 212
            # maxX = 1300
            # maxY = 700
            # # 点一下右键虚拟键
            # dn.touch(self.index, 44, 262)
            # x = random.randint(minX, maxX)
            # y = random.randint(minY, maxY)
            # # 走动
            # dn.touch(self.index, x, y)
            # time.sleep(self.sleep)
            # # 点一下右键虚拟键
            # dn.touch(self.index, 44, 262)
            # # 再次走动
            # x = random.randint(minX, maxX)
            # y = random.randint(minY, maxY)
            # # 走动
            # dn.touch(self.index, x, y)
            #
            # # 打开左键键
            # ok, xy = dn.wait_picture(self.index, 1, r".\img\左键虚拟键.png")
            # if not ok:
            #     # 开的右键就改成左键
            #     dn.touch(self.index, 44, 262)

            # 休息间隔
            self.setup -= 60 * 5
            if self.setup <= 60 * 10:
                self.setup = 60 * 10
            time.sleep(self.setup)

    def BuyCards(self):
        """
        购买卡片
        :return:
        """
        dn = Dnconsole

        while True:
            # 判断游戏状态
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            # 阵容选择
            if self.lineup == 1:
                self.DawnMessenger()
            elif self.lineup == 2:
                self.LittleDevil()
            else:
                # 随机拿卡
                x = 600
                y = 950
                # 拿卡片 5张
                for i in range(5):
                    dn.touch(self.index, x + (i * 200), y)
                    time.sleep(self.sleep)

            # 间隔时间
            time.sleep(8)

    def LittleDevil(self):
        """
        小恶魔阵容
        :return:
        """
        dn = Dnconsole
        # 检测英雄
        ok, xy = dn.wait_picture(self.index, 1, r"./img/hero/小恶魔/小恶魔.png", threshold=0.08, shareimg='lineup.png')
        if ok:
            dn.touch(self.index, xy[0], xy[1])
            # 鼠标移动到空闲位置防止遮挡识别
            self.OpenSpace()
            self.LittleDevil()

        self.dnum += 1
        # D牌
        if self.dnum >= self.frequency:
            # 34是F 32是D 33是E
            self.RefreshCard()
            self.dnum = 0
            self.LittleDevil()

    def DawnMessenger(self):
        """
        黎明使者阵容
        :return:
        """
        dn = Dnconsole
        # 检测英雄
        template = [
            r"./img/hero/黎明使者/黎明使者.png",
            r"./img/hero/黎明使者/复生亡魂.png",
        ]
        i, xy = dn.check_picture(self.index, template, 1, threshold=0.08, shareimg='lineup.png')
        if i >= 0:
            dn.touch(self.index, xy[0], xy[1])
            # 鼠标移动到空闲位置防止遮挡识别
            self.OpenSpace()
            self.DawnMessenger()

        self.dnum += 1
        # D牌
        if self.dnum >= self.frequency:
            # 34是F 32是D 33是E
            self.RefreshCard()
            self.dnum = 0
            self.DawnMessenger()

    def CheckIsDawnMessenger(self, x, y):
        """
        检查是否是黎明使者
        :param x: 检查单位 x坐标
        :param y: 检查单位 y坐标
        :return:
        """
        dn = Dnconsole
        return 0
        # 检测英雄
        template = [
            r"./img/hero/黎明使者/介绍/黎明使者.png",
            r"./img/hero/黎明使者/介绍/复生亡魂.png",
        ]
        self.OpenLeftKey(False)
        # 先回到座位上去
        dn.touch(self.index, 486, 662)
        time.sleep(1.5)
        for i in range(len(x)):
            dn.touch(self.index, x[i], y[i])
            li, xy = dn.check_picture(self.index, template, 1, threshold=0.08, shareimg='checklineup.png')
            if li < 0:
                # 不是黎明使者 卖掉
                print("不是阵容内所需英雄 卖掉")
                self.ClickLeftKey()
                dn.touch(self.index, x[i], y[i])
                # 34是F 32是D 33是E
                Dnconsole.dnld(self.index, "input keyevent 33")
                self.ClickLeftKey()
            else:
                print("是阵容内所需英雄")
            # 鼠标移动到空闲位置防止遮挡识别
            # self.OpenSpace()

        # 结束 恢复左键
        self.OpenLeftKey(True)
        print("结束大清扫")

    def OpenLeftKey(self, left=True):
        """
        打开左右键
        :return:
        """
        dn = Dnconsole
        # 打开左键键
        ok, xy = dn.wait_picture(self.index, 1, r".\img\左键虚拟键.png")
        if left:
            if not ok:
                # 开的右键就改成左键
                self.ClickLeftKey()
        else:
            if ok:
                # 开的左键就改成右键
                self.ClickLeftKey()

    def ClickLeftKey(self):
        """
        打开左右键 - 点击操作
        :return:
        """
        Dnconsole.touch(self.index, 44, 262)

    def GameRestart(self):
        """
        游戏结束回调 再来一局
        :return:
        """
        try:
            self.GameOver()
        except SystemError as e:
            print("停止成功")
        except ValueError as e:
            print("该进程已经不存在了")
        finally:
            time.sleep(2)
            self.StartUp()

    def GameOver(self):
        """
       停止游戏
       :return:
       """
        print("结束游戏")
        self.status = 0
        for thread in self.GameThreading:
            stop_thread(thread)

    def Pause(self):
        """
        暂停游戏
        :return:
        """
        if self.status == 2:
            self.status = 1
        elif self.status == 1:
            self.status = 2

    def __init__(self, vms, indexnum: int):
        self.vm = vms
        self.index = indexnum
        print("当前index:" + str(self.index))

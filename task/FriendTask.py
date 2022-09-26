#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from Dnconsole import Dnconsole
import threading
import time

from model.func import stop_thread


class FriendTask:
    # 当前控制的VM
    vm = None
    # 当前控制的VM index
    index = None

    # 游戏线程
    GameThreading = []

    # 每步操作间隔时间
    sleep = 1
    # 游戏中处理间隔时间
    setup = 60 * 15
    # 0.结束 1.游戏中 2.暂停中
    status = 0

    def start_game(self):
        """
        开始游戏
        :return:
        """
        dn = Dnconsole
        self.start_up()

    def start_up(self):
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
        self.status = 1

        print("开始好友对战")

        # 开始执行任务
        self.GameThreading.insert(0, threading.Timer(0, self.doFight))
        self.GameThreading[0].setDaemon(True)
        self.GameThreading[0].start()

    def doFight(self):
        """
        开始好友对战
        :return:
        """
        dn = Dnconsole

        while True:
            # 判断游戏状态
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            # 点菜单
            dn.touch(self.index, 63, 644)
            time.sleep(self.sleep)
            # 点好友菜单
            dn.touch(self.index, 160, 556)
            for i in range(3):
                time.sleep(self.sleep)
                print(210 + (135 * i))
                # 点好友
                dn.touch(self.index, 667, 210 + (135 * i))
                time.sleep(self.sleep)
                # 拜访
                dn.touch(self.index, 970, 439)
                time.sleep(self.sleep)
                # 点小人
                dn.touch(self.index, 1155, 561)
                time.sleep(self.sleep)
                # 好友演习
                dn.touch(self.index, 1175, 400)
                time.sleep(self.sleep)
                # 挑战
                dn.touch(self.index, 1108, 537)
                time.sleep(self.sleep * 2)
                # 点击第二队
                dn.touch(self.index, 300, 117)
                # 开始出征
                time.sleep(self.sleep)
                dn.touch(self.index, 1121, 669)
                # 开始战斗界面检测（索敌不够会不显示）
                self.startBattle()
                # 选择阵型
                for j in range(3):
                    dn.touch(self.index, 976, 527)
                # 等待战斗完成
                self.battleEnd()
                # 点返回
                time.sleep(self.sleep)
                dn.touch(self.index, 67, 54)
                time.sleep(self.sleep)

            return

    def battleEnd(self):
        """
        战斗结束检测
        :return:
        """
        dn = Dnconsole
        time.sleep(self.sleep * 3)
        # 等待
        while True:
            ok, xy = dn.wait_picture(self.index, 10, r".\img\interface\click_continue.png", 1)
            if ok:
                for i in range(2):
                    # 点击继续
                    dn.touch(self.index, 1170, 659)
                    time.sleep(self.sleep)
                return

    def startBattle(self):
        """
        开始战斗界面检测（索敌不够会不显示）
        :return:
        """
        dn = Dnconsole
        time.sleep(self.sleep * 2)
        # 等待
        ok, xy = dn.wait_picture(self.index, 3, r".\img\interface\start_battle.png", 1)
        if ok:
            # 点击开始战斗
            dn.touch(self.index, 1157, 666)
            time.sleep(self.sleep)

    def game_over(self):
        """
       停止游戏
       :return:
       """
        dn = Dnconsole
        print("结束游戏")
        self.status = 0
        for thread in self.GameThreading:
            stop_thread(thread)

    def pause(self):
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

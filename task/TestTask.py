#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from Dnconsole import Dnconsole
import threading
import time

from model.func import stop_thread


class TestTask:
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

        print("开始游戏")

        # 每隔31分钟重新点开始
        self.GameThreading.insert(0, threading.Timer(0, self.restart))
        self.GameThreading[0].setDaemon(True)
        self.GameThreading[0].start()

    def restart(self):
        """
        每隔31分钟重新点开始
        :return:
        """
        dn = Dnconsole

        while True:
            # 判断游戏状态
            if self.status == 2:
                continue
            if self.status == 0:
                return 1

            dn.touch(self.index, 1275, 215)
            time.sleep(self.sleep)
            # dn.touch(self.index, 928, 260)
            dn.touch(self.index, 835, 220)

            # 间隔时间 31分钟
            time.sleep(2100)

    def game_over(self):
        """
       停止游戏
       :return:
       """
        dn = Dnconsole
        print("结束游戏")
        dn.touch(self.index, 1275, 215)
        time.sleep(self.sleep)
        # dn.touch(self.index, 928, 260)
        dn.touch(self.index, 835, 220)
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

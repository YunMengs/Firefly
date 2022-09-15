import os
import shutil
import time
from xml.dom.minidom import parseString
import cv2 as cv


# 注意pc下的C:/Users/Administrator/Documents/雷电模拟器/Pictures/和安卓上面的/sdcard/Pictures/文件夹是相通的
# D:\Lily\document\leidian\Pictures

class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)


class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
            # 用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)
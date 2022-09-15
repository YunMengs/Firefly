import os
import shutil
import subprocess
import time

import numpy as np
import win32gui
import win32con
import win32api
from typing import Tuple, Any

import cv2 as cv

from DnPlayer import DnPlayer, UserInfo
from File import getDocuments


class Dnconsole:
    # 请根据自己电脑配置
    console = r'D:/Program/Phone/LDPlayer64/ldconsole.exe '
    ld = r'D:/Program/Phone/LDPlayer64/ld.exe '
    # console = r'D:\Program\phone\LDPlayer4/ldconsole.exe '
    # ld = r'D:\Program\phone\LDPlayer4/ld.exe '
    share_path = getDocuments() + r"/leidian64/Pictures"

    # 获取模拟器列表
    @staticmethod
    def get_list():
        cmd = os.popen(Dnconsole.console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result

    # 获取单个模拟器列表
    @staticmethod
    def get_one_list(index: int):
        cmd = os.popen(Dnconsole.console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        for line in info:
            if len(line) > 1:
                dnplayer = DnPlayer(line.split(','))
                if dnplayer.index == index:
                    return dnplayer

    # 获取正在运行的模拟器列表
    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    # 检测指定序号的模拟器是否正在运行
    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()

    # 执行shell命令
    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d %s' % (index, command)
        if silence:
            subprocess.call(cmd, shell=True)
            return ''
        process = subprocess.Popen(cmd)
        result = process.stdout.read()
        process.stdout.close()
        return result

    # 执行adb命令,不建议使用,容易失控
    # @staticmethod
    # def adb(index: int, command: str, silence: bool = False) -> str:
    #     cmd = Dnconsole.console + 'adb --index %d --command "%s"' % (index, command)
    #     if silence:
    #         subprocess.call(cmd, shell=True)
    #         return ''
    #     process = subprocess.Popen(cmd)
    #     result = process.read()
    #     process.close()
    #     return result

    # 安装apk 指定模拟器必须已经启动
    @staticmethod
    def install(index: int, path: str):
        shutil.copy(path, Dnconsole.share_path + str(index) + '/update.apk')
        time.sleep(1)
        Dnconsole.dnld(index, 'pm install /sdcard/Pictures/update.apk')

    # 卸载apk 指定模拟器必须已经启动
    @staticmethod
    def uninstall(index: int, package: str):
        cmd = Dnconsole.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 启动App  指定模拟器必须已经启动
    @staticmethod
    def invokeapp(index: int, package: str):
        cmd = Dnconsole.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        print(result)
        return result

    # 停止App  指定模拟器必须已经启动
    @staticmethod
    def stopapp(index: int, package: str):
        cmd = Dnconsole.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 输入文字
    @staticmethod
    def input_text(index: int, text: str):
        cmd = Dnconsole.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取安装包列表
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    # 检测是否安装指定的应用
    @staticmethod
    def has_install(index: int, package: str):
        if Dnconsole.is_running(index) is False:
            return False
        return package in Dnconsole.get_package_list(index)

    # 启动模拟器
    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 关闭模拟器
    @staticmethod
    def quit(index: int):
        cmd = Dnconsole.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 复制模拟器,被复制的模拟器不能启动
    @staticmethod
    def reboot(index: int = 0):
        cmd = Dnconsole.console + 'reboot --index %s' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置窗口位置大小
    @staticmethod
    def set_window_size(top_win_handler: int):
        title = win32gui.GetWindowText(top_win_handler)
        clssname = win32gui.GetClassName(top_win_handler)
        win = win32gui.FindWindow(clssname, title)
        # 参数1：控制的窗体
        # 参数2：大致方位,HWND_TOPMOST上方
        # 参数3：位置x
        # 参数4：位置y
        # 参数5：长度
        # 参数6：宽度
        win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 0, 0, 1120, 620, win32con.SWP_SHOWWINDOW)

    # 设置屏幕分辨率 下次启动时生效
    @staticmethod
    def set_screen_size(index: int, x: int = 720, y: int = 1280, dpi: int = 320):
        cmd = Dnconsole.console + 'modify --index %d --resolution %d,%d,%d' % (index, x, y, dpi)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 点击或者长按某点
    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input touch %d %d %d' % (x, y, delay))

    # 滑动
    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # 复制模拟器,被复制的模拟器不能启动
    @staticmethod
    def copy(name: str, index: int = 0):
        cmd = Dnconsole.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 添加模拟器
    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置自动旋转
    @staticmethod
    def auto_rate(index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = Dnconsole.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变设备信息 imei imsi simserial androidid mac值
    @staticmethod
    def change_device_data(index: int):
        # 改变设备信息
        cmd = Dnconsole.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变CPU数量
    @staticmethod
    def change_cpu_count(index: int, number: int):
        # 修改cpu数量
        cmd = Dnconsole.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    @staticmethod
    def get_cur_activity_xml(index: int):
        # 获取当前activity的xml信息
        Dnconsole.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(Dnconsole.share_path + '/activity.xml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    @staticmethod
    def get_user_info(index: int) -> UserInfo:
        xml = Dnconsole.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    # 获取当前activity名称
    @staticmethod
    def get_activity_name(index: int):
        text = Dnconsole.dnld(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    # 等待某个activity出现
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if Dnconsole.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    # 找图
    @staticmethod
    def find_pic(screen: str, template: str, threshold: float):
        try:
            scr = cv.imdecode(np.fromfile(screen, dtype=np.uint8), cv.IMREAD_COLOR)
            tp = cv.imdecode(np.fromfile(template, dtype=np.uint8), cv.IMREAD_COLOR)
            result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
        except cv.error:
            print('文件错误：', screen, template, cv.error.msg)
            time.sleep(1)
            try:
                scr = cv.imread(screen)
                tp = cv.imread(template)
                result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if min_val > threshold:
            print(template, min_val, max_val, min_loc, max_loc)
            return False, None
        print(template, min_val, min_loc)
        return True, min_loc

    # 等待某个图片出现
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str, sleep: float = 1, threshold: float = 0.001
                     , shareimg: str = 'apk_scr.png') -> Tuple[bool, Any]:
        count = 0
        while count < timeout:
            Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/' + shareimg)
            time.sleep(sleep)
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/' + shareimg, template, threshold)
            if ret is False:
                print(loc)
                count += 2
                continue
            print(loc)
            return True, loc
        return False, None

    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    @staticmethod
    def check_picture(index: int, templates: list, sleep: float = 1, threshold: float = 0.001
                      , shareimg: str = 'apk_scr.png'):
        Dnconsole.dnld(index, 'screencap -p /sdcard/Pictures/' + shareimg)
        time.sleep(sleep)
        for i, t in enumerate(templates):
            ret, loc = Dnconsole.find_pic(Dnconsole.share_path + '/' + shareimg, t, threshold)
            if ret is True:
                return i, loc
        return -1, None

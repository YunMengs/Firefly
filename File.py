#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：TFTBrother 
@File    ：File.py
@Author  ：织梦行云
@Date    ：2021/9/19 0:16 
"""
import ctypes

from win32con import MAX_PATH


def getDocuments():
    foundError = 'NoFound'
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        return foundError

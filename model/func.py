#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：TFTBrother 
@File    ：func.py
@Author  ：织梦行云
@Date    ：2021/10/1 0:58 
"""
import ctypes
import inspect


def _async_raise(tid, exctype):
    """引发异常，根据需要执行清理，此函数作用是抛出异常来终止某一个线程"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        """
        如果返回的数字大于1，则说明您遇到了麻烦，您应该使用exc=NULL再次调用它以恢复效果
        """
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

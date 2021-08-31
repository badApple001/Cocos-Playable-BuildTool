import json
import os
import sys
import time
import traceback
import IUtils

DEBUG = True if sys.gettrace() else False
class Debug:
    __log = ''
    __time = dict()
    
    
    @staticmethod
    def Init():
        '''
            初始化操作
        '''
        Debug.Log("$$$$$$$$$当前处于DEBUG模式" if DEBUG else "$$$$$$$$$当前处于RELEASE模式")
        if not os.path.exists('log'):
            os.makedirs('log')

    @staticmethod
    def Log(str1:str):
        '''
            输出日志 DEBUG模式下 同时输出编辑器显示
        '''
        str1 = '%s: %s\n' % ( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str1 )
        if DEBUG:
            print(str1)
        Debug.__log += str1

    @staticmethod
    def LogExcept():
        '''
            输出堆栈信息 一般用于捕获异常报错后调用
        '''
        Debug.Log(traceback.format_exc())

    
    @staticmethod
    def TimeEnd(str1):
        '''
            输出两次打印间程序的运行时间
            成双成对的方式出现

            第一次调用并不会打印任何信息
            仅在第二次调用后 返回与第一调用间的间隔
        '''
        if(str1 in Debug.__time.keys()):
            runtime = time.time() - Debug.__time[str1]
            del Debug.__time[str1]
            Debug.Log("%s%f秒"%(str1,runtime))
        else:
            Debug.__time[str1] = time.time()


    @staticmethod
    def Export():
        '''
            导出日志
        '''
        t = time.strftime('%m%d',time.localtime(time.time()))
        IUtils.writeInFile(f'./log/{t}.txt', Debug.__log)

Debug.Init()

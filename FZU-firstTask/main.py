import sys
import time
import re
import copy
from pypinyin import lazy_pinyin
import hanziBreaker
import cProfile


needExamineFile = './example/org.txt'
theSensitiveVoc = './example/words.txt'
theResultFile = './result.txt'

class SensitiveProcess:

    def __init__(self, sensitive):  #读入敏感词的文档
        self.sensitiveTxt = sensitive  #敏感词文档路径
        self.SenTxt = []
        self.pianpan = {}
        self.pianpanCnt = 0
        self.pinyinPart = {}
        self.sensitiveTree = []
        self.dealSensitive=[]


    def punctuations(self,str):
        pun = '''········ \n　　￣o╯□╰o|╭☆!()-[]{};:……'"\,<>./?@#$%^&*_~，。.：”“""、=？！'''
        no_punct = ""
        for char in str:
            if char not in pun:
             no_punct = no_punct + char

        # 显示未加标点的字符串
        return no_punct



    def read_theSensitiveTxt(self):
        try:
            with open(self.sensitiveTxt, 'r+', encoding='utf-8') as sen:
                lines = sen.readlines()
                for line in lines:
                    line = line.replace('\r\n', '')
                    self.SenTxt.append(line)
                    line.lower()
                    line = self.punctuations(line)   #文本处理，除去所有奇怪字符

                    self.sensitivePro(line)
        except IOError:
            raise IOError("fail to read the file ")


    def sensitivePro(self,vocal):
        sen=list(vocal)
        for i in range(len(vocal)):
            c=sen[i]    #依次读取敏感词，如果是汉字就把它拆分成拼音，拼音首字母，和单词组合 和偏旁部首
            if(u'\u4e00' <= c <= u'\u9fa5') or (u'\u3400' <= c <= u'\u4db5'):
                li = []
                pin = lazy_pinyin(c)
                pin=pin[0]
                li.append(pin)
                li.append(list[pin])
                li.append((pin[0]))

                if hanziBreaker.is_breakable(c):
                    hanziPart = hanziBreaker.get(c)
                    part = []
                    for i in hanziPart:
                        if i not in self.pianpan:
                            self.pianpan[i]=self.pianpanCnt
                            self.pianpanCnt+=1  #对偏旁进行编码
                        part.append(i) #li数组里面包含着全部的中文拆分对象 包括拼音组合和各种偏旁部首
                    li.append(part)

                # vocal[i]=li  #把原来的词汇文本替换成 中文改版成 拼音和偏旁部首 的模式

        for c in vocal: #ac状态机，进行塞选
            if not isinstance(c,list):
                if len(self.sensitiveTree)==0:
                    self.sensitiveTree.append([c])
                else:
                    for i in self.sensitiveTree:
                        i.append(c)
            else:
                if len(self.sensitiveTree)==0:
                    for i in c:
                        if not isinstance(i,list):
                            self.sensitiveTree.append([i])
                        else:
                            self.sensitiveTree.append(i)
                else:
                    pre = self.sensitiveTree
                    new_confuse_enum = []
                    for one_confuse in c:
                        new_confuse = copy.deepcopy(pre)
                        # print(new_confuse)
                        if not isinstance(one_confuse, list):
                            for existed_confuse in new_confuse:
                                existed_confuse.append(one_confuse)
                        else:
                            for existed_confuse in new_confuse:
                                for x in one_confuse:
                                    existed_confuse.append(x)
                        new_confuse_enum = new_confuse_enum + new_confuse

                    self.sensitiveTree = new_confuse_enum

        return self.sensitiveTree


def main():
    file = SensitiveProcess('./example/org.txt')
    file.read_theSensitiveTxt()


if __name__ == '__main__':
    main()
    cProfile.run('re.compile("main")')

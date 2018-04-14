# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 16:48
# @Author  : houtianba(549145583@qq.com)
# @FileName: tokenization.py
# @Software: PyCharm
# @Blog    ：http://blog.csdn.net/worryabout/
import jieba.posseg as pseg

def tokenization(doc,stopwords,stopflags):
    # 结巴分词，去掉停用词
    result = []
    text = doc
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stopflags and word not in stopwords:
            result.append(word)
    return result

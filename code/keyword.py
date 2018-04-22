# -*- coding: utf-8 -*-
# @Time    : 2017/4/22 10:31
# @Author  : houtianba(549145583@qq.com)
# @FileName: keyword.py
# @Software: PyCharm
# @Blog    ：http://blog.csdn.net/worryabout/

import jieba.analyse
import jieba.posseg as pseg
from bs4 import BeautifulSoup
import pandas as pd

wordmodel = jieba.analyse


def genkeyword(doc, W=5, K=5):
    """
    取关键词
    :param doc:             文本内容
    :param stop_flag:       停用词属性
    :param W:               textrank窗口磊小
    :param K:               topK取词
    :return:                2个关键词列表， tfidf, textrank
    """
    # tfidf
    tfidfwords = wordmodel.extract_tags(doc, topK=K, withWeight=False)

    # textrank
    wordmodel.TextRank().span = W
    textrankwords = wordmodel.textrank(doc, topK=K, withWeight=False)
    return tfidfwords, textrankwords

def tokenization(doc,sw):
    """
    分词
    :param doc:         文本内容
    :param sw:          停用词列表
    :return:            分词后的列表
    """
    #     结巴分词，去掉停用词
    result = []
    text = doc
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in sw:
            result.append(word)
    return result


if __name__ == '__main__':
    out = pd.read_table('../jupyter/csdn_blog_100.csv', sep='\t',
                        engine='python', index_col=['_id'], header=None,
                        names=['_id', '标题', '标签', '时间', 'pv', '作者', '原创', 'c'])

    out['tfkey'] = ''
    out['trkey'] = ''
    out['nlp'] = ''

    # 加停用词库
    wordmodel.set_stop_words(stop_words_path='../words/CNstop_words_zh.txt')
    import codecs
    stopwords = codecs.open('../words/CNstop_words_zh.txt', 'r', encoding='utf8').readlines()
    stopwordlist = [w.strip() for w in stopwords]
    # 结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']


    ids = []
    dockeys = []
    # 100篇文档分词，保存
    for row in out.itertuples():
        soup = BeautifulSoup(row.c,'html5lib').getText().strip()
        ids.append(row.Index)
        word_list = tokenization(soup,stopwordlist)
        dockeys.append(word_list)
        out.loc[out.index == row[0], ['nlp']] = ' '.join([w for w in word_list])
        tfwords,trwords = genkeyword(soup, W=5, K=8)
        out.loc[out.index == row[0], ['tfkey']] = ' '.join([w for w in tfwords])
        out.loc[out.index == row[0], ['trkey']] = ' '.join([w for w in trwords])
        print('||'.join([out.index, row.标签,' '.join([w for w in tfwords]),' '.join([w for w in trwords])]))

    out.to_csv('../jupyter/csdn_blog_100_nlp_tf_tr_keyword.csv', sep='\t')


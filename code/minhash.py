# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 15:33
# @Author  : houtianba(549145583@qq.com)
# @FileName: minhash.py
# @Software: PyCharm
# @Blog    ：http://blog.csdn.net/worryabout/

import random
from operator import itemgetter

import numpy as np


class MinHash:

    def __init__(self, corpus, k=5):
        # 文档数量
        self.num_docs = corpus.num_docs
        # 词数量
        self.num_terms = corpus.num_terms
        self.k = k
        # 生成 term-doc-shuffle 字典 {term:{'docs':[doc1,doc2,doc3],'fp':[shuffle1,shuffle2,....]}}
        self.tds = dict()
        for ck, cv in enumerate(corpus):
            for c in cv:
                self.tds.setdefault(c[0], {'docs': [], 'fp': []})
                self.tds[c[0]]['docs'].append(ck)
        # 生成随机数列
        shuffled = []
        for i in range(self.k):
            base = [i for i in range(0, len(self.tds))]
            shuffle = list(map(lambda x:(x*(i+1) +(i+1)*int(len(self.tds)/(i+1)))%len(self.tds),base)) #random.shuffle(shuffle)
            for sk, sv in enumerate(shuffle):
                self.tds[sk]['fp'].append(sv)
        # 签名矩阵
        self.fprets  = [[float("inf") for x in range(self.k)] for docnum in range(len(corpus))]

        # 计算所有doc hash
        for tk, tv in self.tds.items():
            for d in tv['docs']:
                for vk, vv in enumerate(tv['fp']):
                    if vv < self.fprets[d][vk]:
                        self.fprets[d][vk] = vv
        print(self.fprets)
        # 最终结果
        self.rets = dict()
        for k1,v1 in enumerate(self.fprets):
            self.rets.setdefault(k1,{})
            for k2,v2 in enumerate(self.fprets):
                if k1 == k2:
                    continue
                self.rets[k1][k2]=len(set(v1)&set(v2))/len(set(v1)|set(v2))
        print(self.rets)

    def __getitem__(self, key):
        return self.rets.get(key)


    # words = {}
    # for word in corpus:
    #     words[word] = []
    # for i in range(k):
    #     shuffled = list(corpus)
    #     random.shuffle(shuffled)
    #     for j in range(len(shuffled)):
    #         words[shuffled[j]].append(j)
    #
    # def hash(document):
    #     total = 0.
    #
    #     # for each hash function, find the lowest value word in the
    #     # document.
    #
    #     #sum(min(h_k(w) over words in doc)
    #
    #     vals = [-1] * k
    #     for word in document:
    #         if word in words:
    #             m = words[word]
    #             for i in range(k):
    #                 if vals[i] == -1 or m[i] < vals[i]:
    #                     vals[i] = m[i]
    #     return sum(vals) / k
    #
    # return hash

if __name__ == '__main__':
    from gensim import corpora, models, similarities
    import pickle

    ids = None
    try:
        f = open("../jupyter/csdn_blog_ids_100.dat", "rb")
        ids = pickle.load(f)
        f.close()
    except Exception as e:
        print('../jupyter/csdn_blog_ids_100.dat文件出错')
    dockeys = None
    try:
        f = open("../jupyter/csdn_blog_dockeys_100.dat", "rb")
        dockeys = pickle.load(f)
        f.close()
    except Exception as e:
        print('../jupyter/csdn_blog_dockeys_100.dat文件出错')

    corpus = corpora.MmCorpus('../jupyter/csdn_blog_100.mm')

    mhret = MinHash(corpus,30)
    # mhret[0]
    print(sorted(mhret[0].items(),key=itemgetter(1),reverse=True))
    print(sorted(mhret[10].items(), key=itemgetter(1), reverse=True))
    print(sorted(mhret[20].items(), key=itemgetter(1), reverse=True))
    print(sorted(mhret[30].items(), key=itemgetter(1), reverse=True))

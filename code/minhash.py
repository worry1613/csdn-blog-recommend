# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 15:33
# @Author  : houtianba(549145583@qq.com)
# @FileName: minhash.py
# @Software: PyCharm
# @Blog    ：http://blog.csdn.net/worryabout/

class MinHash:
    def __init__(self, corpus, k=5):
        # 文档数量
        self.__num_docs = corpus.num_docs
        # 词数量
        self.__num_terms = corpus.num_terms
        self.__k = k
        self.__rets = dict()
        self.__fastrets = dict()
        # 生成 term-doc-shuffle 字典 {term:{'docs':[doc1,doc2,doc3],'fp':[shuffle1,shuffle2,....]}}
        self.__tds = dict()
        for ck, cv in enumerate(corpus):
            for c in cv:
                self.__tds.setdefault(c[0], {'docs': [], 'fp': []})
                self.__tds[c[0]]['docs'].append(ck)
        # 生成 doc-term 字典 {'doc':[term1,term2,term3]}
        self.__dt = dict()
        for ck, cv in enumerate(corpus):
            for c in cv:
                self.__dt.setdefault(ck, set())
                self.__dt[ck].add(c[0])
        # 生成随机数列
        for i in range(self.__k):
            base = [i for i in range(0, len(self.__tds))]
            shuffle = list(map(lambda x: (x * (i + 1) + (i + 1) * int(len(self.__tds) / (i + 1))) % len(self.__tds), base))
            for sk, sv in enumerate(shuffle):
                self.__tds[sk]['fp'].append(sv)
        # 签名矩阵
        self.__signrets = [[float("inf") for x in range(self.__k)] for docnum in range(len(corpus))]

        # 计算所有doc hash
        for tk, tv in self.__tds.items():
            for d in tv['docs']:
                for vk, vv in enumerate(tv['fp']):
                    if vv < self.__signrets[d][vk]:
                        self.__signrets[d][vk] = vv
        print(self.__signrets)

    def cal(self,key):
        # 根据签名矩阵，计算最终结果
        if len(self.__rets) == 0:
            for k1, v1 in enumerate(self.__signrets):
                self.__rets.setdefault(k1, {})
                for k2, v2 in enumerate(self.__signrets):
                    if k1 == k2:
                        continue
                    self.__rets[k1][k2] = len(set(v1) & set(v2)) / len(set(v1) | set(v2))
            print(self.__rets)
        return self.__rets.get(key)

    # def calfast(self,key):
    #     # 根据签名矩阵，计算最终结果
    #     if len(self.__fastrets) == 0:
    #         for doc, terms in self.__dt.items():
    #             rdoc = set()#相关doc
    #             self.__fastrets.setdefault(doc, {})
    #             for term in terms:
    #                 rdoc |=set(self.__tds[term]['docs'])
    #             print(len(rdoc))
    #             for d in rdoc:
    #                 if doc == d:
    #                     continue
    #                 self.__fastrets[doc][d] = len(set(self.__signrets[doc]) & set(self.__signrets[d])) / \
    #                                       len(set(self.__signrets[doc]) | set(self.__signrets[d]))
    #         print(self.__fastrets)
    #     return self.__fastrets.get(key)


if __name__ == '__main__':
    import datetime
    from operator import itemgetter
    from gensim import corpora
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

    start = datetime.datetime.now()
    print('start==', start)
    mhret = MinHash(corpus, 50)
    ok = datetime.datetime.now()
    print('ok==', ok)
    print('times==', ok - start)
    print(0, sorted(mhret.cal(0).items(), key=itemgetter(1), reverse=True))
    print(10, sorted(mhret.cal(10).items(), key=itemgetter(1), reverse=True))
    print(20, sorted(mhret.cal(20).items(), key=itemgetter(1), reverse=True))
    print(30, sorted(mhret.cal(30).items(), key=itemgetter(1), reverse=True))
    print('=============')
    end = datetime.datetime.now()
    print('end==', end)
    print('times==', end - start)



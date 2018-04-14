# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 15:25
# @Author  : houtianba(549145583@qq.com)
# @FileName: simhash.py
# @Software: PyCharm
# @Blog    ：http://blog.csdn.net/worryabout/
import hashlib
import collections
import tokenization
import operator


class simhash:
    def __init__(self, content, stopwords, stopflags=['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r'],f=64):
        self.value = None
        self.stopwords = stopwords
        self.stopflags = stopflags
        self.f = f
        if isinstance(content,simhash):
            self.value = content
        elif isinstance(content,str):
            #一段文字，切分词
            self.value = self.build_by_text(content)
        elif isinstance(content, list):
            # 已经切分好词的列表
            keys = self.build_by_list(content)
            self.value = self.build_by_dict(keys)
        elif isinstance(content, dict):
            # 已经统计好词频的字典 {'key':10,'key2':2}
            self.value = self.build_by_dict(content)
        else:
            raise Exception('参数类型错误 {}'.format(type(content)))

    def __str__(self):
        return str(int(self.value,2))

    def build_by_text(self,content):
        keys = tokenization.tokenization(content,self.stopwords,self.stopflags)
        keystf = dict(collections.Counter(keys))
        value = self.build_by_dict(keystf)
        return value

    def build_by_list(self, content):
        keystf = dict(collections.Counter(content))
        value = self.build_by_dict(keystf)
        return value

    def build_by_dict(self, content):
        c20 = sorted(content.items(),key=operator.itemgetter(1),reverse=True)[:20]
        v = [0] * self.f
        masks = [1 << i for i in range(self.f)]
        for fw in c20:
            feature_hash = self.string_hash(fw[0])
            weight = fw[1]
            for i in range(self.f):
                v[i] += weight if feature_hash & masks[i] else -weight
        value = ''
        for i in v:
            value += '1' if i > 0 else '0'
        print(value)
        return int('0b'+value,2)

    def string_hash(self,source):
        if source == "":
            return 0
        else:
            return int(hashlib.md5(source.encode("utf8")).hexdigest(), 16)

    def hammingDis(self,o):
        n=self.value ^ o.value
        i=0
        while n:
            n &= (n-1)
            i+=1
        return i


if __name__ == '__main__':
    import codecs
    # 加停用词库
    stopwords = codecs.open('../words/CNstop_words_zh.txt', 'r', encoding='utf8').readlines()
    stopwordlist = [w.strip() for w in stopwords]
    # 结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

    s1 = """我们知道，在文本去重的时候，有很多方式，在文本与文本之间对比，如果是整篇对比，费时费力，有人就想到用什么东西代表每篇文章，如摘要，当然，对计算机来说，摘要和整篇的区别只是缩小了篇幅，所以又有人想到了采用关键字来对比。这样确实可以大大缩减我们对比的复杂性。那我们怎么得到一篇文章的关键字呢？一般采用词频（TF），但是只用词频，如中文出现类似“的”、“我们”之类的词语很多，应该怎么去掉这些词语呢，手动去掉实在是麻烦，于是可以结合逆向词频（IDF)，这就是著名的TD-IDF，一种提取一个文章的关键词的算法。词频我们很好理解，一个词语在整篇文章中出现的次数与词语总个数之比。IDF又怎么算呢，假如一个词语，在我们所有文章中出现的频率都非常高（例如“的”在我们多个文本中出现的次数很多），我们就认为，这个词语不具有代表性，就可以降低其作用，也就是赋予其较小的权值。
那这个权重，我们怎么计算呢，（这里敲公式比较麻烦，直接找来图片），如下图，分子代表文章总数，分母表示该词语在这些文章（|D|）出现的篇数。一般我们还会采取分母加一的方法，防止分母为0的情况出现，在这个比值之后取对数，就是IDF了。
simhash是一种局部敏感hash。我们都知道什么是hash。那什么叫局部敏感呢，假定A、B具有一定的相似性，在hash之后，仍然能保持这种相似性，就称之为局部敏感hash。
在上文中，我们得到一个文档的关键词，取得一篇文章关键词集合，又会降低对比效率，我们可以通过hash的方法，把上述得到的关键词集合hash成一串二进制，这样我们直接对比二进制数，看其相似性就可以得到两篇文档的相似性，在查看相似性的时候我们采用海明距离，即在对比二进制的时候，我们看其有多少位不同，就称海明距离为多少。在这里，我是将文章simhash得到一串64位的二进制，一般取海明距离为3作为阈值，即在64位二进制中，只有三位不同，我们就认为两个文档是相似的。当然了，这里可以根据自己的需求来设置阈值。
就这样，我们把一篇文档用一个二进制代表了，也就是把一个文档hash之后得到一串二进制数的算法，称这个hash为simhash。
具体simhash步骤如下：
（1）将文档分词，取一个文章的TF-IDF权重最高的前20个词（feature）和权重（weight）。即一篇文档得到一个长度为20的（feature：weight）的集合。
（2）对其中的词（feature），进行普通的哈希之后得到一个64为的二进制，得到长度为20的（hash : weight）的集合。
（3）根据（2）中得到一串二进制数（hash）中相应位置是1是0，对相应位置取正值weight和负值weight。例如一个词进过（2）得到（010111：5）进过步骤（3）之后可以得到列表[-5,5,-5,5,5,5]，即对一个文档，我们可以得到20个长度为64的列表[weight，-weight...weight]。
（4）对（3）中20个列表进行列向累加得到一个列表。如[-5,5,-5,5,5,5]、[-3,-3,-3,3,-3,3]、[1,-1,-1,1,1,1]进行列向累加得到[-7，1，-9，9，3，9]，这样，我们对一个文档得到，一个长度为64的列表。
（5）对（4）中得到的列表中每个值进行判断，当为负值的时候去0，正值取1。例如，[-7，1，-9，9，3，9]得到010111，这样，我们就得到一个文档的simhash值了。
（6）计算相似性。连个simhash取异或，看其中1的个数是否超过3。超过3则判定为不相似，小于等于3则判定为相似。
呼呼呼，终于写完大致的步骤，可参考下图理解步骤。"""
    s2 = """我们知道，在文本去重的时候，有很多方式，在文本与文本之间对比，如果是整篇对比，费时费力，有人就想到用什么东西代表每篇文章，如摘要，当然，对计算机来说，摘要和整篇的区别只是缩小了篇幅，所以又有人想到了采用关键字来对比。这样确实可以大大缩减我们对比的复杂性。那我们怎么得到一篇文章的关键字呢？一般采用词频（TF），但是只用词频，如中文出现类似“的”、“我们”之类的词语很多，应该怎么去掉这些词语呢，手动去掉实在是麻烦，于是可以结合逆向词频（IDF)，这就是著名的TD-IDF，一种提取一个文章的关键词的算法。词频我们很好理解，一个词语在整篇文章中出现的次数与词语总个数之比。IDF又怎么算呢，假如一个词语，在我们所有文章中出现的频率都非常高（例如“的”在我们多个文本中出现的次数很多），我们就认为，这个词语不具有代表性，就可以降低其作用，也就是赋予其较小的权值。
那这个权重，我们怎么计算呢，（这里敲公式比较麻烦，直接找来图片），如下图，分子代表文章总数，分母表示该词语在这些文章（|D|）出现的篇数。一般我们还会采取分母加一的方法，防止分母为0的情况出现，在这个比值之后取对数，就是IDF了。
simhash是一种局部敏感hash。我们都知道什么是hash。那什么叫局部敏感呢，假定A、B具有一定的相似性，在hash之后，仍然能保持这种相似性，就称之为局部敏感hash。
在上文中，我们得到一个文档的关键词，取得一篇文章关键词集合，又会降低对比效率，我们可以通过hash的方法，把上述得到的关键词集合hash成一串二进制，这样我们直接对比二进制数，看其相似性就可以得到两篇文档的相似性，在查看相似性的时候我们采用海明距离，即在对比二进制的时候，我们看其有多少位不同，就称海明距离为多少。在这里，我是将文章simhash得到一串64位的二进制，一般取海明距离为3作为阈值，即在64位二进制中，只有三位不同，我们就认为两个文档是相似的。当然了，这里可以根据自己的需求来设置阈值。
就这样，我们把一篇文档用一个二进制代表了，也就是把一个文档hash之后得到一串二进制数的算法，称这个hash为simhash。
具体simhash步骤如下：
（1）将文档分词，取一个文章的TF-IDF权重最高的前20个词（feature）和权重（weight）。即一篇文档得到一个长度为20的（feature：weight）的集合。
（2）对其中的词（feature），进行普通的哈希之后得到一个64为的二进制，得到长度为20的（hash : weight）的集合。
（3）根据（2）中得到一串二进制数（hash）中相应位置是1是0，对相应位置取正值weight和负值weight。例如一个词进过（2）得到（010111：5）进过步骤（3）之后可以得到列表[-5,5,-5,5,5,5]，即对一个文档，我们可以得到20个长度为64的列表[weight，-weight...weight]。
"""
    a1 = simhash(s1,stopwordlist,stopflags=stop_flag)
    a2 = simhash(s2,stopwordlist,stopflags=stop_flag)
    ret = a1.hammingDis(a2)
    print(ret)




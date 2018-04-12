==========================================================================================
百度网盘下载地址     https://pan.baidu.com/s/1qzJDmpzAMe1vmtvuCXSfIw
==========================================================================================

++++csdn_blog_100.csv
100条博文数据，格式
_id\t标题\t标签\t时间戳\t浏览量\t作者\t是否原创\t内容
标签:多个标签中间用 空格 分开
内容:html格式内容，文字内容需要自己提取，用BeautifulSoup就行
//+++++++++++++++++++++++++++++++++++//
import pandas as pd
out=pd.read_table('csdn_blog_10000.csv',sep='\t',
                engine='python',index_col=['_id'],header=None,names=['_id','标题','标签','时间','pv','作者','原创','内容'])
//+++++++++++++++++++++++++++++++++++//


++++csdn_blog_10000.csv
10000条博文数据，其它同上


++++csdn_blog.csv
30W+博文数据，格式同上
注意：用pandas处理时会出现 ParserError: field larger than field limit (131072)    


++++csdn_[0_ai_1_cloud_2_blockchain_3_db_4_career_5_engineering_6_arch_7_fund]文本分类训练语料库.txt
22k条博文数据，每类数据2k到3k条，格式
类别id___label_____内容
内容是纯文本内容，不带html格式标签。
ft=pd.read_table('csdn_[0_ai_1_cloud_2_blockchain_3_db_4_career_5_engineering_6_arch_7_fund]文本分类训练语料库.txt',
                 sep="___label_____",engine='python',header=None)

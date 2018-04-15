#!/usr/bin/python
# -*- coding:UTF-8 -*-


import os
import sys
import time
from collections import Counter
import xml.dom.minidom
from xml.dom import Node

def parse_result_file(filename):

    if not os.path.isfile(filename):
        raise SystemExit(filename + " does not exist")
    print filename
    dirname = os.path.dirname(filename)

    #获取文件扩展名
    expand_type=os.path.basename(filename).split('.')[1]
    print expand_type

    output_path = dirname + os.sep + 'loadtime_' + str(time.time()) + '.txt'
    print output_path

    # 从jmeter察看结果树组件到输出文件中过滤需要到数据
    with open(filename) as rf, open(output_path, 'w') as of:
        #通过文件扩展名来选择不同到解析方式
        if expand_type == 'jtl' or expand_type == 'txt':
            #解析非xml格式内容
            for line in rf:
                sr = line.strip().split(',')
                if sr[0].isdigit():
                    print sr[0]
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(sr[0]) / 1000))
                    print start_time
                    sample_name = sr[2]
                    of.write(start_time + ',' + sr[1] + ',' + sample_name)
                    of.write("\n")
        elif expand_type == 'xml':
            # 解析xml格式内容
            dom = xml.dom.minidom.parse(rf)
            root = dom.documentElement

            for child in root.childNodes:
                if child.nodeType == Node.ELEMENT_NODE and child.nodeName=='sample':
                    for key in child.attributes.keys():
                        if key=='ts':
                            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(child.attributes[key].value) / 1000))
                        if key=='t':
                            loadtime=child.attributes[key].value
                        if key=='lb':
                            lb=child.attributes[key].value
                    of.write(start_time + ',' + loadtime + ',' + lb)
                    of.write("\n")





    # 根据label统计加总loadtime
    times=0
    c = Counter()
    if not os.path.isfile(output_path):
        raise SystemExit(output_path + " does not exist")
    else:
        with open(output_path) as ds:
            for line in ds:
                data = line.split(',')
                lt = data[1]
                lb = data[2]
                c[lb] += int(lt)
                times+=1
            #计算迭代次数
            times=float(times)/c.__len__()
            print times
            print c

    # 对loadtime取平均值并输出到结果文件中
    result_path = dirname + os.sep + 'result_' + str(time.time()) + '.txt'

    with open(result_path, 'w') as rf:
        for key in c.keys():
            rf.write('SampleName:' + key + '\tTotalLoadTime:' + str(c[key]) + 'ms AverageLoadTime:' + str(
                c[key] / float(times)) + 'ms\n')






if __name__  == "__main__":
    if not sys.argv:
        raise SystemExit("please input filename as parameter for command")
    filename=sys.argv[1]
    parse_result_file(filename)

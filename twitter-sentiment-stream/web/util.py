#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import pickle
import threading
import time

#host = '35.243.211.34', port = 5070
def getData(host = 'localhost', port = 5070):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg = s.recv(10240)
    data = pickle.loads(msg)

    sentiment = data['count']
    throughput = data['throughput']
    twitter_before = data['original']
    twitter_after = data['text']
    session = data['session']
    #[time, sentiment: dict]

    # print("sentiment: ", sentiment)
    # print("throughput", throughput)
    # print("twitter_after", twitter_after)
    # print("twitter_before", twitter_before)
    # print("Get: session time", session[0])
    # print("Get: session count", session[1])



    return data;


def convertime(timenow):
    timenow = time.gmtime(timenow)
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", timenow)
    return timenow

def PieOneData(values, labels, domain):
        return {
          "values": values,
          "labels": labels,
          "domain": {"column": domain},
          "name": "GHG Emissions",
          "hoverinfo":"label+percent+name",
          "hole": .4,
          "type": "pie"
        }

def PieAllData(data, layout):
    return {"data": data,
             "layout": layout}

def subtitle(name, x):
    return {
        "font": {
            "size": 20
        },
        "showarrow": False,
        "text": " ",
        "x": None,
        "y": 0.5
    }

def layout(annotations, column, title):
    return {"title":"Latest Session: " + title,
        "grid": {"rows": 1, "columns": column},
        "annotations": annotations}

if __name__ == '__main__':
    for i in range(10):
        data = getData()

        sentiment = data['count']
        throughput = data['throughput']
        twitter_before = data['original']
        twitter_after = data['text']
        session = data['session']
        #[time, sentiment: dict]

        print("sentiment: ", sentiment)
        print("throughput", throughput)
        print("twitter_after", twitter_after)
        print("twitter_before", twitter_before)
        print("session time", session[0])
        print("session count", session[1])

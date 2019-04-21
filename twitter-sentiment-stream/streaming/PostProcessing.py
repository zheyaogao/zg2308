import socket
import sys
import pickle
import threading
import time
import numpy as np
import tensorflow as tf


class myThread_2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 获取本地主机名
        host = 'localhost'#socket.gethostname()
        port = 5070
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定端口号
        serversocket.bind((host, port))

        # 设置最大连接数，超过后排队
        serversocket.listen(5)
        global message

        while True:
            clientsocket,addr = serversocket.accept()
            pic = pickle.dumps(message)
            clientsocket.send(pic)
            print("Send", message)

class myThread_1 (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pred = 0
        self.count = {}
        self.session = [[time.time(),{}]]
        self.past = time.time()

    def run(self):
        host = 'localhost'
        port = 5050
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        global message

        while True :
            msg = s.recv(10240)
            message = pickle.loads(msg)
            print('received',message)
            self.window()
            self.predict()
            self.counting()
            self.throughput()
            print("Read", message['count'])

    def predict(self):
        # Parse Data

        tweet_text = message['text']
        sequence = tokenizer.texts_to_sequences([tweet_text])
        pad_seq = [0]*(40-len(sequence[0])) + sequence[0]
        self.pred = int(np.argmax(model.predict(np.array([pad_seq]))))

    def counting(self):
        # count
        for n in message['name'].split():
            if n in self.count.keys():
                self.count[n][self.pred] += 1
            else:
                self.count[n] = [0]*2
                self.count[n][self.pred] += 1
        message['count'] = self.count

    def throughput(self):
       end = time.time()
       message['throughput'] = 1/(end-message['time'])

    def window(self):
        if message['time']-self.session[-1][0] >60*3 or message['time']-self.past>60:
            self.session.append([self.past,self.count])
            self.count = {}
            if len(self.session)>5:
                self.session = self.session[1:]
        message['session'] = self.session
        self.past = message['time']


global message
message = {}

model = tf.keras.models.load_model('../model/model.h5')
with open('../model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

thread1 = myThread_1()
thread2 = myThread_2()

thread1.start()
thread2.start()

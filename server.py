import socket
import random
import time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
b_ip = "10.61.39.230"
user_ip = "10.105.246.123"
user_port = 31412
buffer = 5600
b_port = 31413
s.bind((user_ip,user_port))
s.listen(5)
conn,addr = s.accept()
current_content = [['msg0', 0], ['msg1', 1], ['msg2', 2], ['msg3', 3], ['msg4', 4], ['msg5', 5], ['msg6', 6], ['msg7', 7], ['msg8', 8], ['msg9', 9], ['msg10', 10], ['msg11', 11], ['msg12', 12], ['msg13', 13], ['msg14', 14], ['msg15', 15], ['msg16', 16], ['msg17', 17], ['msg18', 18], ['msg19', 19], ['msg20', 20], ['msg21', 21], ['msg22', 22], ['msg23', 23], ['msg24', 24], ['msg25', 25], ['msg26', 26], ['msg27', 27], ['msg28', 28], ['msg29', 29], ['msg30', 30], ['msg31', 31], ['msg32', 32], ['msg33', 33], ['msg34', 34], ['msg35', 35], ['msg36', 36], ['msg37', 37], ['msg38', 38], ['msg39', 39], ['msg40', 40], ['msg41', 41], ['msg42', 42], ['msg43', 43], ['msg44', 44], ['msg45', 45], ['msg46', 46], ['msg47', 47], ['msg48', 48], ['msg49', 49]]
with open("toLike.txt","w") as rq:
    rq.write("")
    rq.close()
with open("toRT.txt","w") as rt:
    rt.write("")
    rt.close()
    
with open("tweet_stream.txt", "r") as m:
    current_content = m.readlines()[-30:]

def refresh():
    with open("tweet_stream.txt", "r") as m:
        current_content = m.readlines()[-30:]
    print len(current_content)
    
while True:
    data = conn.recv(buffer)
    if len(data) > 0:
        print data
    if data == "r":
        # They need content!
        print "Getting Content."
        last_tweets = [current_content[:-30]]
        mk = []
        '''
        for i in current_content:
            mk.append(i[0]+"="+str(i[1]))
        '''
        tosend = '&'.join(current_content)
        #print tosend
        conn.send(tosend)
        refresh()
    elif len(data) > 0 and "l" == data[0]:
        # Retweet this boi.
        with open("toLike.txt","a") as mk:
            mk.write(data[1:])
            mk.close()
        refresh()
    elif len(data)> 0 and "r" == data[0]:
        with open("toRT.txt","a") as mk:
            mk.write(data[3:-1])
            mk.close()
        refresh()

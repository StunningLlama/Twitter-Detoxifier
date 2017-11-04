from twython import Twython
import twython,string,time
APP_KEY = 	"6n6ZhfANLhIpsrjvAAupolale"
APP_SECRET = "S4KnRU7o4COKOlmGjvuqIwVonN4I8z9EUycwFyMbXi0WEjxTiQ"
CONSUMER_KEY = "761588524441300992-yvelAFUgzX3qa8uTsB8hMB2k6AiN3MU"
CONSUMER_SEC = "6HQiGOoVVmI81lEeNUptkIIE8RlbUhUsoBWJW9rXoQiul"
last = None
with open("tweet_stream.txt","w") as k:
    k.write("")
    k.close()
def fr(k):
    new = ""
    for i in k:
        if i in string.ascii_lowercase + string.ascii_uppercase + string.digits+" ":
            new += i
    return new.replace("RT","")
class myTwitter(twython.TwythonStreamer):
    def on_success(self,data):
        global last
        print "New Tweet Added: %s"%(data["id"])
        last = data
        with open("tweet_stream.txt","a") as k:
            k.write("\n"+fr(data[u'text'])+"="+str(data["id"]))
            k.close()
        v = []
        with open("toLike.txt","r") as r:
            v = r.readlines()
            r.close()
        with open("toLike.txt","w") as r:
            r.close()
        for i in v:
            if len(i) > 2:
                time.sleep(2)
                i = int(i)
                
                myT.create_favorite(id = i)
        v = []
        with open("toRT.txt","r") as r:
            v = r.readlines()
            r.close()
        with open("toRT.txt","w") as r:
            r.close()
        for i in v:
            if len(i) > 2:
                print "Retweeting:",i
                i = int(i)
                time.sleep(2)
                myT.retweet(id = i)
myT = Twython("NNgDBY28ungDWKNEDbUNzX1i3","lQx2k5Pm8SSp8338cPteShZzlCiyL6STCmvUnbMHMGZuo66VPX","926821791581872129-fRA9pmIJL4diUmTvNj4wba2AdEheGcP","VcLky5zTRMH9qVcUToPFM5olR8Lj6bE9Nn8sy40Y0tuLR")
time.sleep(10)
my_twython = myTwitter(APP_KEY,APP_SECRET,CONSUMER_KEY,CONSUMER_SEC)
#my_twython.statuses.filter()
my_twython.statuses.filter(track = ["pokemon","minecraft","apple","samsung","bloomberg","dell"])

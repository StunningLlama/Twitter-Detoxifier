import RPi.GPIO as GPIO
from time import sleep
import socket
from lcd import HD44780

GPIO.setmode(GPIO.BCM)
lcd = HD44780()
lcd.clear()
lcd.message('Welcome to' + chr(10) + 'Twitter-DT')
sleep(1)
GPIO.setup(7, GPIO.OUT) # mmusic output
GPIO.setup(9,GPIO.IN)
global LIKE_STATE
LIKE_STATE = False
GPIO.setup(11,GPIO.IN)
global RT_STATE
RT_STATE = False
GPIO.setup(17,GPIO.IN)
GPIO.setup(22,GPIO.IN)
global REFRESH_STATE
REFRESH_STATE = False

lcd.clear()
#sleep(1)
#lcd.message('LOADING')
#sleep(1)
#lcd.message('LOADING'+chr(10)+chr())
#drawLoading(0)
last_rt_id = -1
last_like_id = -1

def writeMessage(tweet):
	lcd.clear()
	lcd.message(tweet[:16]+chr(10)+tweet[16:32])

def toBool(n):
	if (n):
		return True
	return False

def drawLoading(k):

	lcd.message('LOADING'+chr(10)+''.join([chr(35) for i in range(0,k)]))
def playTone(s):
	GPIO.output(7,True)
	sleep(s)
	GPIO.output(7,False)

def buttonUp():
	if GPIO.input(17):
		return True
	else:
		return False
def buttonDown():
	if GPIO.input(22):
		return True
	else:
		return False
def buttonRetweet():
	global LIKE_STATE, RT_STATE, REFRESH_STATE
	val = toBool(GPIO.input(11))
	if (not val and RT_STATE and not LIKE_STATE and not REFRESH_STATE):
		RT_STATE = False
		return True, True
	RT_STATE = val
	return False, val
def buttonLike():
	global LIKE_STATE
	global RT_STATE, REFRESH_STATE
	val = toBool(GPIO.input(9))
	if (not val and LIKE_STATE and not RT_STATE and not REFRESH_STATE):
		LIKE_STATE = False
		return True, True
	LIKE_STATE = val
	return False, val

def buttonRefresh():
	global LIKE_STATE, RT_STATE, REFRESH_STATE
	val = LIKE_STATE and RT_STATE
	val2 = not LIKE_STATE and not RT_STATE
	if (val and not REFRESH_STATE):
		REFRESH_STATE = True
		return True
	if (val2 and REFRESH_STATE):
		REFRESH_STATE = False
	return False


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
drawLoading(1)
target_ip = '10.105.246.123'
target_port = 31412
s.connect((target_ip, target_port))
lcd.clear()
drawLoading(2)
s.send('r')
data = s.recv(5600)
lcd.clear()
drawLoading(3)
tweetlist = data.split('&')
previndex = -1
index = 0
lcd.clear()
drawLoading(16)
while True:
# 	print buttonLike
	likeSt, likeButDown = buttonLike()
	rtSt, rtButDown = buttonRetweet()
	refreshSt = buttonRefresh()
	c = buttonUp() or buttonDown() or likeButDown or rtButDown
	if c:
		GPIO.output(7, True)
	else:
		GPIO.output(7, False)
	if buttonUp():
		if (index < 29):
			index += 1
	if buttonDown():
		if (index > 0):
			index -= 1
	if likeSt:
		tweetid = tweetlist[index].split('=')[1]
		if (tweetid != last_like_id):
			last_like_id = tweetid
			lcd.clear()
			lcd.message('  Liking!  '+chr(10)+'   Please Wait!  ')
			s.send('l ' + tweetid)
			sleep(1)
			previndex = -1
	if rtSt:
		tweetid = tweetlist[index].split('=')[1]
		if (tweetid != last_rt_id):
			last_rt_id = tweetid
			lcd.clear() 
			lcd.message('  Retweeting!  '+chr(10)+'   Please Wait!  ')
			s.send('rt ' + tweetid)
			sleep(1)
			previndex = -1
			
	if refreshSt:
		lcd.clear()
		drawLoading(0)
		s.send('r')
		lcd.clear()
		drawLoading(5)
		data = s.recv(5600)
		tweetlist = data.split('&')
		lcd.clear()
		drawLoading(16)
		previndex = -1
		index = 0
	if (previndex != index):
		lcd.clear()
		previndex = index
		print 'going to ',index
		try:
			tweet = tweetlist[index].split('=')[0]
		except:
			print tweetlist[index], 'is invalid'
		writeMessage(tweet)

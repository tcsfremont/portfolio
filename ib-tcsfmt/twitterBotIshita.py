import tweepy, markovify
from time import sleep


    
CONSUMER_KEY = 'zhXI0pCXXXNBm5FuIRZccpYwf'
CONSUMER_SECRET =  'bsKxw0v4YrRxqgjkWtDxDuDsM0NQalJsmllVxHKU9P5DJpKLy1'
ACCESS_KEY =  '951987145710931969-xz4ZQwPghCxCUVxjbAgx4Q6ZuRhjVaC'
ACCESS_SECRET =  'NjUx0qSXdstGKhkriROPVZbXGQOAtmVpqcHs3rGZ2kOBN'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

with open("poems.txt") as f:
    text = f.read()
tModel = markovify.Text(text)
sent = tModel.make_short_sentence(200)

'''
class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            print(status.text)

        def on_error(self, status_code):
            if status_code == 420:
                return False


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

myStream.filter(track=['cat'])
'''   


while True:        
    api.update_status(status = sent)
    print sent
    sleep(900)
    


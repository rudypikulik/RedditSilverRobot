# Written by Rudy Pikulik 07/17

import praw
import pickle
import time
from Structures.Queue import Queue
import RedditSilverRobot
from datetime import datetime

print("Starting up the bots!")

reddit = praw.Reddit(client_id='client_id',
                  client_secret='client_secret',
                  user_agent='raspberrypi:com.rudypikulik.redditsilverrobot:v1.1.1',
                  username=‘**********’,
                  password=‘**********’)


# This defines the domain from which to collect comments. "all" for all comments.
sub = reddit.subreddit("all")


bots = [RedditSilverRobot]


def start_stream():
    comments = sub.stream.comments()
    for comment in comments:
        for bot in bots:
            if bot.validate_comment(comment):
                queue = pickle.load(open(bot.file, 'rb'))
                if queue:
                    queue.enqueue(comment.id)
                else:
                    queue = Queue()
                    queue.enqueue(comment.id)
                pickle.dump(queue, open(bot.file, 'wb'))
                timestr = str(time.localtime()[3]) + ":" + str(time.localtime()[4])
                print("> %s - Added comment to queue! Queue length: %s" % (timestr, len(queue)))


while True:
    try:
        print('Starting comment stream at %s' % (datetime.now()))
        start_stream()
    except Exception as e:
        print("> %s - Connection lost. Restarting in 3 seconds... %s" % (datetime.now(), e))
        time.sleep(3)
        continue

# Created by Rudy Pikulik 04/17
import praw
import pickle
import time
from datetime import datetime
import socket
import requests

#Initializes account instance from praw.
reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='raspberrypi:com.rudypikulik.redditsilverrobot:v1.2.1',
                     username='xxxxxxxx',
                     password='xxxxxxxx')

# Initializes used_comments, give_counts, and receive_counts from files.
try:
    used_comments = pickle.load(open("comments.p", "rb"))
except:
    used_comments = []
try:
    give_counts = pickle.load(open("givers.p", "rb"))
except:
    give_counts = {}
try:
    receive_counts = pickle.load(open("receivers.p", "rb"))
except:
    receive_counts = {}

running = True
sub = reddit.subreddit("all")
comments = sub.stream.comments()

# Updates logs for how many times someone has given/received silver.
def register_comment(comment):
    giver = comment.author.name
    receiver = get_receiver(comment)

    if giver in give_counts.keys():
        give_counts[giver] += 1
    else:
        give_counts[giver] = 1
    if receiver in receive_counts.keys():
        receive_counts[receiver] += 1
    else:
        receive_counts[receiver] = 1
    # Saves data in case of crash.
    used_comments.append(comment)
    pickle.dump(used_comments, open("comments.p", "wb"))
    pickle.dump(receive_counts, open("receivers.p", 'wb'))
    pickle.dump(give_counts, open("givers.p", 'wb'))


# Decides whether or not to reply to a given comment.
#    - Must contain command
#    - Must not have already replied
#    - Must not reply to self
def validate_comment(comment):
    if comment in used_comments:
        return False
    if comment.author.name == "RedditSilverRobot":
        return False
    if "!redditsilver" in comment.body.lower():
        return True
    return False


# Figures out who should be the recipiant of silver.
#    - If no one is specified, it should be the author of the parent post.
#    - Otherwise, it should be the person specified. Bot strips /u/ if present.
def get_receiver(comment):
    text = comment.body.lower().split()
    try:
        receiver = text[text.index("!redditsilver")+1]
    except IndexError:
        receiver = comment.parent().author.name
    if '/u/' in receiver:
        receiver = receiver.replace('/u/', '')
    if 'u/' in receiver:
        receiver = receiver.replace('u/', '')
    if '/' in receiver:
        receiver = receiver.replace('/', '')
    return receiver


# Creates the message to be posted.
# Calls get_receiver
def make_message(comment):
    message = "###[Here's your Reddit Silver, kind stranger!](http://i.imgur.com/x0jw93q.png \"Reddit Silver\")"
    message += "\n***\n"
    message += "/u/" + str(comment.author.name) + " has given silver " + "" + str(give_counts[comment.author.name])
    message += " time(s). | /u/" + get_receiver(comment) + " has received silver "
    message += "" + str(receive_counts[get_receiver(comment)]) + " time(s). | [info](http://reddit.com/r/RedditSilverRobot)"
    return message

# The main body of the bot.
#    - Checks all comments with validate comment
#    - Replies to correct messages using make_message
def startStreaming():
    comments = sub.stream.comments()
    for comment in comments:
        text = comment.body
        user = comment.author
        if validate_comment(comment):
            register_comment(comment)
            time.sleep(.5)
            message = make_message(comment)
            try:
                if get_receiver(comment) == comment.parent().author.name:
                    comment.parent().reply(message)
                else:
                    comment.reply(message)
                print("Posted: " + user.name + " -> " + get_receiver(comment))
                time.sleep(2)
            except:
                print("There was an error.")
                continue
        time.sleep(.0001)


# Calls startStreaming().
# Does most exception handling for the bot, including connection errors.
# Automatically restarts the stream if it crashes.
count = 0
for giver in give_counts.values():
    count+= giver
print("Silver has been given a total of %s times." % count)

while True:
    try:
        print('Starting stream at %s' %(datetime.now()))
        startStreaming()
    except Exception as e:
        print("> %s - Connection lost. Restarting in 10 seconds... %s" % (datetime.now(), e))
        time.sleep(10)
        continue


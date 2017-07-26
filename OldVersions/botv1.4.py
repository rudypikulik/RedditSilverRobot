# Created by Rudy Pikulik 04/17
# Last updated 06/17
import praw
import pickle
import time
from datetime import datetime
import socket
import requests

#Initializes account instance from praw.
reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='raspberrypi:com.rudypikulik.redditsilverrobot:v1.4.1',
                     username='xxxxxxxxxx',
                     password='xxxxxxxxxx')


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


# The main body of the bot.
#    - Checks all comments with validate comment
#    - Replies to correct messages using make_message
def start_streaming():
    comments = sub.stream.comments()
    for comment in comments:
        user = comment.author
        if validate_comment(comment) and get_receiver(comment) is not None:
            register_comment(comment)
            message = make_message(comment)
            try:
                # if get_receiver(comment) == comment.parent().author.name:
                    # comment.parent().reply(message)
                # else:
                comment.reply(message)

                timestr = str(time.localtime()[3]) + ":" + str(time.localtime()[4])
                print("> %s - Posted: %s -> " % (timestr, user.name) + get_receiver(comment))
                time.sleep(2)
            except:
                print("Ran into an error while commenting... Maybe I'm banned?")
                continue


# Decides whether or not to reply to a given comment.
#    - Must contain command
#    - Must not have already replied
#    - Must not reply to self
def validate_comment(comment):
    if '!redditsilver' in comment.body.lower():
        comment.refresh()
        for child_comment in comment.replies:
            if child_comment.author.name == "RedditSilverRobot":
                return False
        return True
    return False


# Although these files are no longer used while the bot is running,
# They have been kept for statistical reasons.
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


# Figures out who should be the recipient of silver.
#    - If no one is specified, it should be the author of the parent post.
#    - Otherwise, it should be the person specified. Bot strips /u/ if present.
def get_receiver(comment):
    text = comment.body.lower().split()
    try:
        # Kind of gross looking code below. Splits the comment exactly once at '!RedditSilver',
        # then figures out if the very next character is a new line. If it is, respond to parent.
        # If it is not a new line, either respond to the designated person or the parent.

        split = comment.body.lower().split('!redditsilver', 1)[1].replace(' ', '')
        if split[0] is "\n":
            receiver = comment.parent().author.name
        else:
            receiver = text[text.index('!redditsilver') + 1]
    # An IndexError is thrown if the user did not specify a recipient.
    except IndexError:
        receiver = comment.parent().author.name
    # A ValueError is thrown if '!RedditSilver' is not found. Example: !RedditSilverTest would throw this.
    except ValueError:
        return None
    if '/u/' in receiver:
        receiver = receiver.replace('/u/', '')
    if 'u/' in receiver:
        receiver = receiver.replace('u/', '')
    if '/' in receiver:
        receiver = receiver.replace('/', '')
    # This line is to change the name from all lowercase.
        receiver = reddit.redditor(receiver).name
    return receiver

# This method finds out how many times the receiver has been given silver.
# In version 1.4, this method replaced using the receiver.p file.
def silver_counter(comment):
    rsr = reddit.redditor('RedditSilverRobot')
    rsr_comments = rsr.comments.new()
    count = 0
    for silver_comment in rsr_comments:
        str = '/u/' + get_receiver(comment).lower() + ' has received'
        if str in silver_comment.body.lower():
            count += 1
    # Returns count+1 to include this instance of silver too.
    return count+1


# Creates the message to be posted.
# Calls get_receiver
def make_message(comment):
    message = "###[Here's your Reddit Silver, " + get_receiver(comment) + "!](http://i.imgur.com/x0jw93q.png \"Reddit Silver\")"
    message += "\n***\n"
    message += "/u/" + get_receiver(comment) + " has received silver " + str(silver_counter(comment))
    message += " times this month! (given by /u/"
    message += comment.author.name + ") "
    message += "__[info](http://reddit.com/r/RedditSilverRobot)__"
    return message



# Calls startStreaming().
# Does most exception handling for the bot, including connection errors.
# Automatically restarts the stream if it crashes.

count = 0
for giver in give_counts.values():
    count += giver
print("Silver has been given a total of %s times." % count)

while True:
    try:
        print('Starting stream at %s' % (datetime.now()))
        start_streaming()
    except Exception as e:
        print("> %s - Connection lost. Restarting in 10 seconds... %s" % (datetime.now(), e))
        time.sleep(10)
        continue


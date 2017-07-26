import pickle
import time
import RedditSilverRobot

comments = pickle.load(open('comments.p', 'rb'))

try:
    data = pickle.load(open('RSRData.p', 'rb'))
except FileNotFoundError:
    data = []

for comment in comments:
    try:
        tup = (comment.id, (comment.author.name, RedditSilverRobot.get_receiver(comment), time.localtime(), "Legacy"))
        data.append(tup)
    except Exception as e:
        # This exception is intentionally weak because I'm not too worried about losing one or two entries.
        print("Error: " + str(e))

pickle.dump(data, open('RSRData.p', 'wb'))

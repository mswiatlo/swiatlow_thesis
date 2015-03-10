# thanks to tunasauraus for a great start to this script
# changed it to show only one point per day though (bit busy with how often I compile)
# todo: generalize details like start date as arguments so that others can more easily use it
# note: requires pdfinfo to be installed (from the amusingly sketchy http://www.foolabs.com/xpdf/)

import datetime, time
import sys

spd = float(60*60*24)

start = "2015-02-23-00h00m00s"
start = datetime.datetime.strptime(start, "%Y-%m-%d-%Hh%Mm%Ss")
last = ""

dayssince = []
pages = []
words =[]

first = True

with open("pages.md") as file:
    # read in reverse, to make it easier to take just the latest compile for a day
    for line in reversed(file.readlines()):

        line = line.strip()
        if not line:
            continue
        if not line.count(" ") == 3:
            sys.exit("what the fuck")

        _, date, pagecount, wordcount = line.split(" ")
        date = date.replace("[", "")
        date = date.replace("]", "")

        current = datetime.datetime.strptime(date, "%Y-%m-%d-%Hh%Mm%Ss")
        delta = current - start
        # print delta.days
        if not delta.days in dayssince:
            # print "adding to the array"
            dayssince.append(delta.days)
            pages.append(int(pagecount))
            words.append(int(wordcount))
        
        if first:
            lasttime, lastpages, lastwords = current, pagecount, wordcount
            # print lasttime, lastpages
            first = False

# the template already has 12 pages. thx stanford.
# this has to go at the end because we read the file in reverse order.
dayssince.append(0)
pages.append(12)
words.append(53)


# dayssince = reversed(dayssince)
# pages = reversed(pages)
# print 'first time'
print 'Your progress is:'
print dayssince
print pages
print words

# small module to better include flat days
for i in xrange(len(dayssince) - 1):
    # print i, dayssince[i], dayssince[i+1]
    if dayssince[i] - dayssince[i+1] > 1:
        # print 'i am true' 
        dayssince.insert(i+1, dayssince[i] - 1)
        pages.insert(i+1, pages[i+1])
        words.insert(i+1, words[i+1])
        # print dayssince
        # print pages
    i = i - 1

# print dayssince, pages

import numpy as np
dayssince = np.array(dayssince)
pages     = np.array(pages)
words     = np.array(words)

if len(dayssince) > 1:
    print str(pages[0] - pages[1]) + ' pages today!'
    print str(words[0] - words[1]) + ' words today!'

from matplotlib import rcParams
# rcParams["font.family"] = "sans-serif"
# rcParams["font.sans-serif"] = ["Helvetica"]
rcParams["font.size"] = "16"
import matplotlib.pyplot as plt

now = datetime.datetime.now()
# maxdayssince = (now - start).days + (now - start).seconds/spd
maxdayssince = (now - start).days

ax = plt.gca()
fig, ax1 = plt.subplots()
ax1.xaxis.set_label_coords(0.74, -0.07)
ax1.yaxis.set_label_coords(-0.10, 0.9)

ax1.set_xlabel("Days since start (Feb. 23)")
ax1.set_ylabel("Pages",color='b')
ax1.set_title("")
ax1.text(0.6*maxdayssince, 1.12*max(pages), r"%s pages"   % (lastpages), color='blue')
ax1.text(0.8*maxdayssince, 1.12*max(pages), r"%s words"   % (lastwords), color='red')
ax1.text(0,                1.12*max(pages), r"Updated %s" % (lasttime))
# plt.axis([0, maxdayssince, 0, 1.1*max(pages)])
ax1.axis([-1, maxdayssince+1, 0, 1.1*max(pages)])
ax1.grid(False)
ax1.plot(dayssince, pages, "-")
# plt.plot(dayssince, pages, "rd")
ax1.fill_between(dayssince, 0, pages, facecolor='blue', interpolate=True)

ax2 = ax1.twinx()
ax2.set_ylabel('Words',color='r')
ax2.yaxis.set_label_coords(1.1, 0.9)
# print dayssince, words
ax2.plot(dayssince, words, "r-",linewidth=2)

plt.autoscale()
plt.savefig("pages.png",bbox_inches='tight')
plt.savefig("pages.pdf",bbox_inches='tight')


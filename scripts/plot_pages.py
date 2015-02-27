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

first = True

with open("pages.md") as file:
    # read in reverse, to make it easier to take just the latest compile for a day
    for line in reversed(file.readlines()):

        line = line.strip()
        if not line:
            continue
        if not line.count(" ") == 2:
            sys.exit("what the fuck")

        _, date, pagecount = line.split(" ")
        date = date.replace("[", "")
        date = date.replace("]", "")

        current = datetime.datetime.strptime(date, "%Y-%m-%d-%Hh%Mm%Ss")
        delta = current - start
        # print delta.days
        if not delta.days in dayssince:
            # print "adding to the array"
            dayssince.append(delta.days)
            pages.append(int(pagecount))
        
        if first:
            lasttime, lastpages = current, pagecount
            # print lasttime, lastpages
            first = False

# the template already has 12 pages. thx stanford.
# this has to go at the end because we read the file in reverse order.
dayssince.append(0)
pages.append(12)


# dayssince = reversed(dayssince)
# pages = reversed(pages)
# print 'first time'
print 'Your progress is:'
print dayssince
print pages

# small module to better include flat days
for i in xrange(len(dayssince) - 1):
    # print i, dayssince[i], dayssince[i+1]
    if dayssince[i] - dayssince[i+1] > 0:
        # print 'i am true' 
        dayssince.insert(i+2, dayssince[i+1] - 1)
        pages.insert(i+2, pages[i+2])
    i = i - 1

# print dayssince, pages

import numpy as np
dayssince = np.array(dayssince)
pages     = np.array(pages)

from matplotlib import rcParams
# rcParams["font.family"] = "sans-serif"
# rcParams["font.sans-serif"] = ["Helvetica"]
rcParams["font.size"] = "16"
import matplotlib.pyplot as plt

now = datetime.datetime.now()
# maxdayssince = (now - start).days + (now - start).seconds/spd
maxdayssince = (now - start).days

ax = plt.gca()
ax.xaxis.set_label_coords(0.74, -0.07)
ax.yaxis.set_label_coords(-0.10, 0.9)

plt.xlabel("Days since start (Feb. 23)")
plt.ylabel("Pages")
plt.title("")
plt.text(1.1*maxdayssince, 1.12*max(pages), r"%s pages"   % (lastpages))
plt.text(0,                1.12*max(pages), r"Updated %s" % (lasttime))
# plt.axis([0, maxdayssince, 0, 1.1*max(pages)])
plt.axis([-1, maxdayssince+1, 0, 1.1*max(pages)])
plt.grid(False)
plt.plot(dayssince, pages, "-")
# plt.plot(dayssince, pages, "rd")
plt.fill_between(dayssince, 0, pages, facecolor='blue', interpolate=True)
plt.savefig("pages.png")
plt.savefig("pages.pdf")


# todo: add a point at the end of a streak of days with no compiles (or figure out how to interpolate better)

import datetime, time
import sys

spd = float(60*60*24)

start = "2015-02-23-00h00m00s"
start = datetime.datetime.strptime(start, "%Y-%m-%d-%Hh%Mm%Ss")
last = ""

dayssince = []
pages = []

# the template already has 8 pages. thx reecer.
dayssince.append(0)
pages.append(12)

first = True

with open("pages.md") as file:
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

# dayssince = reversed(dayssince)
# pages = reversed(pages)

# small module to better include flat days
for i in xrange(len(dayssince) - 1):
    if dayssince[i+1] - dayssince[i] > 0:
        dayssince.insert(i+1, dayssince[i] + 1)
        pages.insert(i+1, pages[i])
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
maxdayssince = (now - start).days + (now - start).seconds/spd

ax = plt.gca()
ax.xaxis.set_label_coords(0.74, -0.07)
ax.yaxis.set_label_coords(-0.10, 0.9)

plt.xlabel("Days since start (Feb. 23)")
plt.ylabel("Pages")
plt.title("")
plt.text(1.1*maxdayssince, 1.12*max(pages), r"%s pages"   % (lastpages))
plt.text(0,                1.12*max(pages), r"Updated %s" % (lasttime))
plt.axis([-1, maxdayssince+1, 0, 1.1*max(pages)])
plt.grid(False)
plt.plot(dayssince, pages, "-")
# plt.plot(dayssince, pages, "rd")
plt.fill_between(dayssince, 0, pages, facecolor='blue', interpolate=True)
plt.savefig("pages.png")
plt.savefig("pages.pdf")


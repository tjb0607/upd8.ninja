#!/usr/bin/python3
import urllib.request
import re
import time
import json
import sys
from datetime import datetime, date
from platform import python_version

upd8ninja_user_agent = 'upd8 ninja - Homestuck update notifier running on python ' + python_version() + ' via urllib for tjb0607.me/upd8'

#Print with timestamp
def tsPrint(message):
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%H:%M:%S ')
    print(st + message)
    sys.stdout.flush()

#Print & log with timestamp
def tsPrintLog(message):
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S ')
    print(st + message)
    sys.stdout.flush()
    f = open("upd8ninja.log", "a")
    f.write(st + message + "\n")
    f.close()

#Gets the adventure log
def getPageList():
#    link = "https://www.homestuck.com/log/" + adventure
    link = "https://www.homestuck2.com/log?refresh=" + str(int(time.time()))
    response = None
    while response is None:
        try:
            req = urllib.request.Request(link, headers={'User-Agent': upd8ninja_user_agent})
            response = urllib.request.urlopen(req)
        except Exception as e:
            tsPrintLog("[ERROR] Error while fetching " + link + ": " + str(e))
            time.sleep(5)
    html = response.read().decode('utf-8')

    #tsPrint("[DEBUG] matches: " + str(html))
    #matches = re.findall('(?<=href="/)' + adventure + '[^<]+(?=<)', html)
    matches = re.findall('(?<=href="/)story[^<]+(?=<)', html)
    output = []
    #tsPrint("[DEBUG] matches: " + str(matches))
    for match in reversed(matches):
        output += [{
            "parturl": match.split("\"")[0],
            "title": match.split(">")[1][1:-1]
        }]
    return output

if __name__ == '__main__':
    #adventure = "epilogues"
    upd8ninjadir = "/var/www/html/upd8/"
    sleeptime = 20

    #upd8ninjadir = "C:/Users/tjb06/upd8/new/"
    f = open(upd8ninjadir + "latestupd8", "r")
    latestupd8 = {"parturl": f.readline(), "title": ""}
    f.close()
    f = open(upd8ninjadir + "totalpages", "r")
    totalpages = int(f.readline())
    f.close()

    while True:
        tsPrint("[ INFO] Checking adventure log...")
        pagelist = getPageList()
        upd8index = -1
        for index, page in enumerate(pagelist):
            if latestupd8["parturl"] == page["parturl"]:
                upd8index = index
                break

        if upd8index < 0:
            tsPrintLog("[ WARN] latest upd8 (" + latestupd8["parturl"] + ") is not found in page list: " + str(pagelist))
#        else:
#            tsPrintLog("[DEBUG] Current update index is " + str(upd8index) + " out of " + str(len(pagelist)))

        if (len(pagelist) > totalpages):
            latestupd8 = pagelist[totalpages]
            upd8pages = len(pagelist) - totalpages
            totalpages = len(pagelist)
            tsPrint("[ INFO] Upd8 found! " + str(upd8pages) + " pages: https://www.homestuck.com/" + latestupd8["parturl"])
            f = open(upd8ninjadir + "latestupd8", "w")
            f.write(latestupd8["parturl"])
            f.close()
            f = open(upd8ninjadir + "latestupd8.json", "w")
            f.write(json.dumps({"parturl": latestupd8["parturl"], "title": latestupd8["title"], "pages": upd8pages}))
            f.close()
            f = open(upd8ninjadir + "totalpages", "w")
            f.write(str(totalpages))
            f.close()
        elif (len(pagelist) == 0):
            tsPrintLog("[ERROR] Did not find any pages listed on the adventure log!")
        elif (len(pagelist) < totalpages):
            tsPrintLog("[ERROR] There are fewer pages listed (" + str(len(pagelist)) + ") compared to last time (" + str(totalpages) + "). Page list is: " + str(pagelist))
        else:
            tsPrint("[ INFO] No new pages found.")
        tsPrint("[SLEEP] Sleeping " + str(sleeptime) + "s...")
        time.sleep(sleeptime)

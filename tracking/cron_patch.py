import requests
import time
import re

def update_data():
    start = time.time()
    response2 = requests.get("http://www.browngirlonabike.com/proc_data/24")
    response_list2 = re.findall('<h3>(.*?)</h3>', response2.text)
    time1 = time.time() - start
    print("Process data with 24h cap response:")
    print("_________________________________")
    print("Time taken: {0:.2f}s".format(time1))
    print("_________________________________")
    for place in response_list2:
        print(place)
    print("_________________________________")
    print("Raw html:")
    print("_________________________________")
    print(response2.text)

    start = time.time()
    response1 = requests.get("http://www.browngirlonabike.com/proc_data/0")
    response_list1 = re.findall('<h3>(.*?)</h3>', response1.text)
    time2 = time.time() - start
    print("Process data with no cap response:")
    print("_________________________________")
    print("Time taken: {0:.2f}s".format(time2))
    print("_________________________________")
    for place in response_list1:
        print(place)
    print("_________________________________")
    print("Raw html:")
    print("_________________________________")
    print(response1.text)

loop = 0
while True:
    print("This is loop no {}".format(loop))
    print("_________________________________")
    sleep_time = 420
    mins = loop*(sleep_time/60)
    update_data()
    time.sleep(420)
    loop += 1
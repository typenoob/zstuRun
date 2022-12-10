import json
import time
import requests
import random
from divide import Region
from person import Person
from distance import get_distance_wgs84
import gzip

if __name__ == '__main__':
    def getLocation():
        global dic
        now = int(dic['begintime'])
        region = Region(config['region'])
        person = Person(config['speed']['init'],
                        config['speed']['ave'], config['speed']['step'])
        target = config['target']
        dis_total = 0
        wait_total = 0
        previous = config['region'][0]
        while True:
            record = region.getDivision(config['divide_num'])
            point = record[0]
            location = '{lat},{lon};{time};null;null;0.0;null'.format(
                lat=point[0], lon=point[1], time=time.time())   # gettime
            for point in record:
                dis = get_distance_wgs84(
                    previous[1], previous[0], point[1], point[0])
                dis_total += dis
                wait = dis/person.speed
                now += int(wait)
                wait_total += wait
                previous = (point[0], point[1])
                location += '@{lat},{lon};{time};null;null;0.0;null'.format(
                    lat=point[0], lon=point[1], time=now)
                person.changeSpeed(dis_total/wait_total)
                if dis_total >= target:
                    break
            if dis_total >= target:
                break
        dic['speed'] = str(wait_total/60/dis_total*1000)
        dic['endtime'] = str(now)
        dic['usetime'] = str(int(dic['endtime'])-int(dic['begintime']))
        return location
    # input a YYYY-MM-DD return the timestamp

    def getTimeStamp(date):
        date = date.split('-')
        return int(time.mktime(time.strptime(date[0]+'-'+date[1]+'-'+date[2], '%Y-%m-%d')))

    # return today in YYYY-MM-DD

    def getToday():
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))
    while(1):
        with open('./config.json', 'r', encoding='utf8')as fp:
            config = json.load(fp)
        day = int(input())
        if day == -1:
            break
        dic = {}
        dic['begintime'] = getTimeStamp(
            getToday())+20*3600+random.randint(0, 3600)-day*24*3600  # starttime
        dic['uid'] = r'd6220f10-d208-43cd-a53e-2aa53685323fb88f31121e714f3da11c9e5c6bb2c87f1622117480$a98bcd3166022036e4ed7d2585d84e2c'
        dic['schoolno'] = '10338'
        dic['distance'] = str(config['target'])
        dic['studentno'] = '{sno}'
        dic['atttype'] = '3'
        dic['eventno'] = '801'
        dic['location'] = getLocation()
        url = 'http://10.11.246.182:8029/DragonFlyServ/Api/webserver/uploadRunData'
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "Keep-Alive", "Charset": "UTF-8",
                   "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; TAS-AN00 Build/TAS-AN00)",
                   "Host": "10.11.246.182:8029", "Accept-Encoding": "gzip"}
        data = gzip.compress(str(dic).encode('utf-8'))
        requ = requests.post(url=url, headers=headers, data=data)
        print(requ.text)

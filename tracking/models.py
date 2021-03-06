from django.db import models
import datetime
from .coords import haversine
from colorful.fields import RGBColorField
from django.forms import ModelForm
import requests
import re
import datetime

# Create your models here

class type(models.Model):
    name = models.CharField(max_length=20)
    color = RGBColorField(default = '#004080')

    def __str__(self):
        return self.name

class section(models.Model):
    name = models.CharField(max_length=200, default = "unnamed")

    startPlace = models.ForeignKey('place',
                                   related_name="start",
                                   on_delete=models.SET_NULL,
                                   null=True)

    type = models.ForeignKey(type,
                             related_name="transportType",
                             on_delete= models.SET_NULL,
                             null= True)

    endPlace = models.ForeignKey('place',
                                 related_name="end",
                                 on_delete=models.SET_NULL,
                                 null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_startEnd(self.startPlace, self.endPlace, self)

class place(models.Model):
    name = models.CharField(max_length=200, default = "nowhere")
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    order = models.FloatField()

    section = models.ManyToManyField(section,blank = True)

    def __str__(self):
        return self.name + ": " + str(self.lat) + ", " + str(self.lon)

    def save(self, *args, **kwargs):
        # Tries to get a sample section, might not work as section might not
        # be assigned yet
        try:
            selfSec = list(self.section.objects.all())[0]
            if not (selfSec.startPlace == self or selfSec.endPlace == self):
                print("Assigning order...")
                order_set = get_order(self.lat,self.lon,selfSec.id, self.id)
                print ("order set: " + str(order_set))
                self.order = order_set
            super().save(*args, **kwargs)
        except:
            super().save(*args,**kwargs)

class meetUp(models.Model):
    name = models.CharField(max_length=200)
    info = models.TextField(max_length=1000)

    place = models.ForeignKey(place,
                              related_name= "meetUpPlace",
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    #+ ": @" + self.place.name + ", in section: " + self.section.name

class pastData(models.Model):
    time = models.DateTimeField(default = '2018-04-15 14:30:59')
    timeIn = models.DateTimeField(auto_now= True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    elevation = models.FloatField(default = 0)
    deltaT = models.FloatField(default=0)
    distanceAB = models.FloatField(default = 0, null=True)
    distanceGoogle = models.FloatField(default=0, null=True)
    speed = models.FloatField(default = 0, null=True)
    movingTime = models.IntegerField(default=0, null=True)
    totalMovingTime = models.IntegerField(default=0, null=True)
    totalDistance = models.FloatField(default=0,null=True)
    totalElevation = models.FloatField(default=0, null=True)

    lastGetTime = models.DateTimeField(default="2018-06-28T12:00:00-0000")

    def __str__(self):
        return str(self.lat) + "," + str(self.lon) + " : " + str(self.time)

    def get_pastDay(self):
        today = datetime.now().date()
        tomorrow = today + datetime.timedelta(1)
        today_start = datetime.combine(today, datetime.time())
        today_end = datetime.combine(tomorrow, datetime.time())
        return self.filter(start__lte=today_end, end__gte=today_start)

'''
class extrapolated_data(models.Model):
    time = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    stopped = models.IntegerField(max_length=20)
    deltaT = models.IntegerField(max_length=20)
    velocity = models.FloatField
'''

class post(models.Model):
    image = models.ImageField()
    time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    show = models.BooleanField(default=True)

    place = models.ForeignKey(place,
                              related_name= "postPlace",
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

        #+ ":" + , in section: " + self.section.name

class resolved_coord(models.Model):
    section = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()

class capped_resolved_coord(models.Model):
    section = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()

def get_past_data():
    '''
    Requests latest data from tracker website.
    '''
    data = []
    with open("tracking/data.txt", "r") as f:
        for line in f:
            split_line = line.split(':')
            data.append([split_line[0], split_line[1][:-1]])
    return data

def parse_data():
    '''
    Parses XML data into a list of dicts which contain model keys.
    '''

def add_data(data_in):
    print(len(data_in[0]))
    for row in data_in:
        x = pastData(time = datetime.datetime.now(), lat = row[0],
                     lon = row[1])
        x.save()

def save_startEnd(start,end,sec):
    start.section.add(sec)
    end.section.add(sec)
    start.save()
    end.save()

def get_order(lat,lon,section_id, selfId):
    '''
    :param lat: Place lat.
    :param lon: Place lon.
    :param section_id: id of route section.
    :param selfId: id of place object.

    Function - finds the order, which is defined as the average of the order of
    the two closest places.

    :return: Float -  represents an approximation of the places location
    where the startPlace is eqal to 0 and the endPlace is equal to 0
    '''
    #print("Running get_order...")

    # Function below returns all Place objects in the given section.

    query = get_all_section(section_id,selfId)

    # get_all_sections returns 0/1 if the place is a start or end place.

    if query == 0.0 or query == 1.0:
        #print("Query should be 1 or 0: ".format(query))
        return query

    # Below inits first closest and second closest.

    firstClosest = [1000000,None]
    secondClosest = [1000000,None]

    # Loops through places in section, replaces closest[0] with
    # distance if lower, and replaces closest[1] with the order:

    for key,value in query.items():
        distance = haversine((lat,lon),(value[0],value[1]))
        #print(distance)
        if distance < firstClosest[0]:
            secondClosest = list(firstClosest)
            firstClosest = [distance, value[2]]
        elif distance < secondClosest[0]:
            secondClosest = [distance, value[2]]

    # Returns the average of the two closest places:

    return (firstClosest[1] + secondClosest[1])/2

def get_all_section(id, selfId):
    '''
    :param id: id of place.
    :param selfId:
    :return:
    '''
    #print("Running get_all_sections...")
    sec = section.objects.all().filter(pk = id)
    places = sec[0].place_set.all()

    # Checks if parent section has a startPlace, if so loads relevant vars:

    if sec[0].startPlace:

        startLat = sec[0].startPlace.lat
        startLon = sec[0].startPlace.lon
        startId = sec[0].startPlace.id

        if startId == selfId:
            #print("Returning 0...")
            return 0.0

    # Returns 0 if no startPlace, as required to sort locations

    else:
        print("returning 0 because no startPlace")
        return 0.0

    # Same as above, but with endPlace

    if sec[0].endPlace:

        endLat = sec[0].endPlace.lat
        endLon = sec[0].endPlace.lon
        endId = sec[0].endPlace.id

        if endId == selfId:
            #print("Returning 1...")
            return 1.0

    else:
        return 0.0

    # Builds a dictionary containing relavant data, the ifs prevent
    # duplication of data

    place_dict = {}
    for place in places:
        if place.id != selfId:
            place_dict[place.id] = (place.lat,place.lon,place.order)
    if not startId in place_dict.keys():
        place_dict[startId] = (startLat,startLon, 0)
    if not endId in place_dict.keys():
        place_dict[endId] = (endLat,endLon,1)
    return place_dict


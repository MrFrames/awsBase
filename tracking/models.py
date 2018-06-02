from django.db import models
import datetime

# Create your models here


class place(models.Model):
    name = models.CharField(max_length=200, default = "nowhere")
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name + ": " + str(self.lat) + ", " + str(self.lon)

class type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class section(models.Model):
    name = models.CharField(max_length=200, default = "unnamed")
    order = models.IntegerField()

    type = models.ForeignKey(type,
                             related_name="transportType",
                             on_delete= models.SET_NULL,
                             null= True)

    startPlace = models.ForeignKey(place,
                                   related_name="sectionStart",
                                   on_delete= models.SET_NULL, null=True)

    endPlace = models.ForeignKey(place,
                                 related_name="sectionEnd",
                                 on_delete= models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name) + ": " + str(self.order)

class subSection(models.Model):
    name = models.CharField(max_length=200, default="unnamed")
    order = models.IntegerField()

    section = models.ForeignKey(section,
                                related_name="insideSection",
                                on_delete=models.SET_NULL,
                                null = True)

    type = models.ForeignKey(type,
                             related_name="subTransportType",
                             on_delete=models.SET_NULL,
                             null=True)

    startPlace = models.ForeignKey(place,
                                   related_name="subSectionStart",
                                   on_delete=models.SET_NULL, null=True)

    endPlace = models.ForeignKey(place,
                                 related_name="subSectionEnd",
                                 on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name) + ": " + str(self.order)

class meetUp(models.Model):
    name = models.CharField(max_length=200)
    info = models.TextField(max_length=1000)

    place = models.ForeignKey(place,
                              related_name= "meetUpPlace",
                              on_delete= models.SET_NULL,
                              null=True)

    section = models.ForeignKey(section,
                                related_name="meetUpSection",
                                on_delete= models.SET_NULL,
                                null= True)

    def __str__(self):
        return self.name + ": @" + self.place.name + ", in section: " + \
               self.section.name

class pastData(models.Model):
    time = models.DateTimeField(default = '2018-04-15 14:30:59')
    timeIn = models.DateTimeField(auto_now= True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)

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

    place = models.ForeignKey(place,
                              related_name= "postPlace",
                              on_delete=models.SET_NULL,
                              null=True)

    section = models.ForeignKey(section,
                                related_name= "postSection",
                                on_delete=models.SET_NULL,
                                null=True)

    def __str__(self):
        return self.title + ": @" + self.place.name + ", in section: " + \
               self.section.name

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

def get_closestPoint():
    '''
    Returns closest section.
    '''


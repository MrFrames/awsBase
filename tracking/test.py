from django.test import TestCase
from .models import type, section, place

class sectionPlaceTestCase(TestCase):
    def setUp(self):

        cycling = type.objects.create(name = "Cycling")

        type.objects.create(name = "Boat")

        london = place.objects.create(name = "London",
                                      lat = 51.5285578,
                                      lon = -0.2420243,
                                      order = 0)

        rochester = place.objects.create(name= "Rochester",
                                         lat=51.3811167,
                                         lon=0.4165043,
                                         order=0)

        dover = place.objects.create(name= "Dover",
                                     lat=51.1263712,
                                     lon=1.2309496,
                                     order=0)

        section.objects.create(name = "London to Dover",
                                 order = 1,
                                 startPlace = None,
                                 endPlace = None,
                                 type = cycling)

        section.objects.create(name="London to Dover2",
                               order=1,
                               startPlace=london,
                               endPlace=dover,
                               type=cycling)

    def test_setup(self):
        cycling = type.objects.get(name = "Cycling")
        london = place.objects.get(name="London")
        rochester = place.objects.get(name = "Rochester")
        dover = place.objects.get(name = "Dover")
        englandSection = section.objects.get(name = "London to Dover")
        assert(cycling.name == "Cycling")
        print("1Type: Cycling created successfully.")
        assert (london.name == "London")
        print("2place: London created successfully.")
        assert (englandSection.name == "London to Dover")
        print("3Section: englandSection created successfully.")

    def test_assignMiddleFail(self):
        print ("4This test is to check if the sorting algorithm tries to set "
               "an intermediary place to some value other than 0 if the "
               "startPlace and endPlace of the section are not defined" )
        englandSection = section.objects.get(name="London to Dover")

        rochester = place.objects.get(name="Rochester")
        rochester.section.add(englandSection)
        rochester.save()

        newRochester = place.objects.get(name="Rochester")
        assert (newRochester.order == 0.0)

    def tests_setStartEnd(self):
        print ("5Testing set section start and end point...")
        london = place.objects.get(name="London")
        dover = place.objects.get(name="Dover")
        cycling = type.objects.get(name="Cycling")

        newEnglandSection = section.objects.get(name = "London to Dover")
        newEnglandSection.startPlace = london
        newEnglandSection.endPlace = dover

        newEnglandSection.save()

        testEnglandSection = section.objects.get(name = "London to Dover")
        assert testEnglandSection.startPlace.name == "London"

    def test_assignInter1(self):
        print("8Testing order assigning to Rochester.")
        englandSection = section.objects.get(name="London to Dover2")

        rochester = place.objects.get(name="Rochester")
        rochester.section.add(englandSection)
        rochester.save()

        newRochester = place.objects.get(name="Rochester")
        print ("Rochester order: ".format(newRochester.order))
        assert (newRochester.order == 0.5)



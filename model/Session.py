from model import maps
from datetime import datetime
from dateutil import tz

class Session():
    #appointmentType: str = "PROXY_BAPTISM"
    #sessionTime: str = ""
    #seatsAvailable: int = 0
    #templeOrgId = 0
    def __init__(self, appointmentType="PROXY_BAPTISM", sessionTime='', arrivalDateTime='', seatsAvailable=0, templeOrgId=0):
        self.appointmentType = appointmentType
        self.sessionTime = sessionTime

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.strptime(arrivalDateTime, '%Y-%m-%dT%H:%M:%S.000Z')
        utc = utc.replace(tzinfo=from_zone)
        self.arrivalDateTime = utc.astimezone(to_zone)
        self.seatsAvailable = seatsAvailable
        self.templeOrgId = templeOrgId
    def __str__(self):
        return f"{maps.idToTempleMap[self.templeOrgId]}: {self.appointmentType}, {self.arrivalDateTime.date()}, {self.sessionTime}, {self.seatsAvailable}"

    def __eq__(self, other):
        if isinstance(other, Session):
            if self.appointmentType == other.appointmentType and self.arrivalDateTime.year == other.arrivalDateTime.year and self.arrivalDateTime.month == other.arrivalDateTime.month and self.arrivalDateTime.day == other.arrivalDateTime.day and self.arrivalDateTime.hour == other.arrivalDateTime.hour and self.arrivalDateTime.minute == other.arrivalDateTime.minute and self.templeOrgId == other.templeOrgId:
                return True
        return False
    '''
    {"sessionTime":"06:00",
    "arrivalDateTime":"2024-09-17T11:50:00.000Z",
    "arrivalMinutesOffset":10,
    "appointmentTimeId":78221386,
    "time":"2024-09-17T06:00:00",
    "details":{"capacity":8,
    "onlineCapacity":0,
    "onlineCapacityFromSchedule":0,
    "roomFull":false,
    "patrons":[],
    "livingEndowmentAppointmentsCount":0,
    "malePatronCountMap":{"35803314":3,
    "36423647":1,
    "35793061":1,
    "36256241":0},
    "femalePatronCountMap":{"35803314":1,
    "36423647":0,
    "35793061":1,
    "36256241":1},
    "totalGuestCountMap":{},
    "onlineMaleReservedCount":{"35803314":3,
    "36423647":1,
    "35793061":1,
    "36256241":0},
    "onlineFemaleReservedCount":{"35803314":1,
    "36423647":0,
    "35793061":1,
    "36256241":1},
    "onlineNeutralReservedCount":{},
    "sealingAppointments":[],
    "maleCapacity":0,
    "femaleCapacity":0,
    "markAsFullFlag":false,
    "sessionLength":15,
    "maleSeatsAvailable":-5,
    "femaleSeatsAvailable":-3,
    "totalMalePatronCount":5,
    "reserved":8,
    "remainingOnlineSeatsAvailable":-8,
    "totalOnlineFemalePatronCount":3,
    "reservedLiving":0,
    "onlineSeatsAvailable":-8,
    "totalFemalePatronCount":3,
    "totalOnlineMalePatronCount":5,
    "neutralOnlinePatronCount":0,
    "seatsAvailable":0},
    "appointmentType":"PROXY_BAPTISM",
    "scheduleSubType":"APPOINTMENTS_PREFERRED",
    "scheduleGroupType":"REGULAR",
    "templeOrgId":4012416}
    '''

import WebInterface
from model import *
import sendMail
import datetime
import jsonpickle
from dateutil import tz


interface = WebInterface.WebInterface()

def f(session: Session.Session):
    if (session.seatsAvailable >= 2 and ((session.arrivalDateTime.weekday() == 2 and session.sessionTime >= "00:00") or (session.arrivalDateTime.weekday() == 5))):# and session.sessionTime >= "18:00"):
        return 2
    if (session.seatsAvailable >= 2 and ((session.arrivalDateTime.weekday() == 1 and session.sessionTime >= "18:00") or (session.arrivalDateTime.weekday() == 4 and session.sessionTime >= "17:00"))):
        return 1
    if (session.arrivalDateTime.day >= 26 and session.arrivalDateTime.day <= 29 and session.arrivalDateTime.day != 28 and session.seatsAvailable >= 3 and session.sessionTime <= "18:00" and session.arrivalDateTime.month == 11):
        return 3
    #if (session.seatsAvailable > 0):
    #    return 1
    return 0
    

prioritySessions = []
workableSessions = []
breakSessions = []

base_date = datetime.datetime.today()
for date in [base_date + datetime.timedelta(days=x) for x in range(7*4)]: # for every date within 4 weeks
    print(date.year, date.month, date.day)
    for temple in maps.templeMap:
        print(temple)
        sessionResponse = interface.getSessionInfo(SessionRequest.SessionRequest(date.year,date.month,date.day,"PROXY_BAPTISM",maps.templeMap[temple]))
        for session in sessionResponse.getSessions():
            if f(session) == 2:
                prioritySessions.append(session)
                print(session)
            if f(session) == 1:
                workableSessions.append(session)
                print(session)
            if f(session) == 3:
                breakSessions.append(session)
                print(session)
        #print(str(sessionResponse))

with open('spencer_data/output_'+str(datetime.datetime.today()), "w") as f:
    f.write(str([interface.getSessionInfo(SessionRequest.SessionRequest(date.year, date.month, date.day, s_type, maps.templeMap["Provo"])).sessionList for date in [base_date + datetime.timedelta(days=x) for x in range(7*4)] for s_type in ["PROXY_BAPTISM","PROXY_INITIATORY", "PROXY_ENDOWMENT", "PROXY_SEALING"]]))

#load previously sent sessions
sentSessions = []
try:
    with open('sentSessions', 'r') as f:
        content = f.read()
        if content != '':
            sentSessions = jsonpickle.decode(content)
except Exception as e:
    print(repr(e))
    sentSessions = []

#get rid of all previously sent sessions
for session in sentSessions:
    if session in prioritySessions:
        i = 0
        while i < len(prioritySessions):
            if session == prioritySessions[i]:
                print("deleting ", str(prioritySessions[i]), str(session), "from prioritySessions")
                del prioritySessions[i]
                continue
            i += 1
    if session in workableSessions:
        i = 0
        while i < len(workableSessions):
            if session == workableSessions[i]:
                print("deleting ", str(workableSessions[i]), "from workableSessions")
                del workableSessions[i]
                continue
            i += 1
        print("deleting ", str(session), "from workableSessions")
    if session in breakSessions:
        i = 0
        while i < len(breakSessions):
            if session == breakSessions[i]:
                print("deleting ", str(breakSessions[i]), "from breakSessions")
                del breakSessions[i]
                continue
            i += 1
        print("deleting ", str(session), "from breakSessions")


#for session in sentSessions:


#get rid of sessions older than a day. Sorry for the nasty line
sentSessions = [s for s in sentSessions if s.arrivalDateTime > (base_date.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()) - datetime.timedelta(days=1))]
#display old sessions
print("\nOld Sessions:")
print('\n'.join([str(s) for s in sentSessions]))

#display new sessions
print("\nPriority Sessions:")
print('\n'.join([str(s) for s in prioritySessions]))

print("\nWorkable Sessions:")
print('\n'.join([str(s) for s in workableSessions]))

print("\nBreak Sessions:")
print('\n'.join([str(s) for s in breakSessions]))

#email new sessions
if (prioritySessions or workableSessions):
    sendMail.sendEmail('ckhiggins@pm.me', 'New temple appointments!', 'Priority Sessions:\n'+('\n'.join([str(s) for s in prioritySessions]))+'\nWorkable Sessions:\n'+('\n'.join([str(s) for s in workableSessions])))
if (breakSessions):
    sendMail.sendEmail('ckhiggins@pm.me', '+tfhappts', 'Break Sessions:\n'+('\n'.join([str(s) for s in breakSessions])))

#write new and old sent sessions to disk
sentSessions.extend(prioritySessions+workableSessions+breakSessions)
with open('sentSessions', 'w') as f:
    f.write(jsonpickle.encode(sentSessions))


#while True:
#    exec(input('>'))


        #json = {"sessionYear":2024,"sessionMonth":8,"sessionDay":17,"appointmentType":"PROXY_BAPTISM","templeOrgId":4012416,"isGuestConfirmation":False}

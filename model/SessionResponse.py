from model import Session
class SessionResponse():
    def __init__(self, response):
        self.sessions = []
        self.sessionList = response['sessionList']
        for session in self.sessionList:
            self.sessions.append(Session.Session(session['appointmentType'], session['sessionTime'], session['arrivalDateTime'], session['details']['seatsAvailable'], session['templeOrgId']))

    def __str__(self):
        return '\n'.join([str(s) for s in self.sessions])

    def getSessions(self):
        return self.sessions

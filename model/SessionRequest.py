class SessionRequest():
    sessionYear: int = 0
    sessionMonth: int = 0
    sessionDay: int = 0
    appointmentType: str = "PROXY_BAPTISM"
    templeOrgId: int = 0
    isGuestConfirmation: bool = False
    def __init__(self, sessionYear: int, sessionMonth: int, sessionDay: int, appointmentType: str, templeOrgId: int):
        self.sessionYear = sessionYear
        self.sessionMonth = sessionMonth-1
        self.sessionDay = sessionDay
        self.appointmentType = appointmentType
        self.templeOrgId = templeOrgId

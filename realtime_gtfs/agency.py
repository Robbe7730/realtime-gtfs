from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError
import pytz

class Agency(object):
    def __init__(self):
        self.agency_id = None
        self.agency_name = None
        self.agency_url = None
        self.agency_timezone = None
        self.agency_lang = None
        self.agency_phone = None
        self.agency_fare_url = None
        self.agency_email = None

    @staticmethod
    def from_dict(data):
        ret = Agency()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        ret = Agency()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret
    
    def verify(self):
        # TODO: verify agency_id
        if (self.agency_name == None):
            raise MissingKeyError("agency_name")
        if (self.agency_url == None):
            raise MissingKeyError("agency_url")
        if (self.agency_timezone == None):
            raise MissingKeyError("agency_timezone")
        return True

    def setkey(self, key, value):
        if (key == "agency_id"):
            self.agency_id = value
        elif (key == "agency_name"):
            self.agency_name = value
        elif (key == "agency_url"):
            self.agency_url = value
        elif (key == "agency_timezone"):
            self.agency_timezone = pytz.timezone(value)
        elif (key == "agency_lang"):
            self.agency_lang = value
        elif (key == "agency_phone"):
            self.agency_phone = value
        elif (key == "agency_fare_url"):
            self.agency_fare_url = value
        elif (key == "agency_email"):
            self.agency_email = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Agency {self.agency_name}]"
    
    def __eq__(self, other):
        if (type(self) != type(other)):
            return False
        return (self.agency_id == other.agency_id and
                self.agency_name == other.agency_name and
                self.agency_url == other.agency_url and
                self.agency_timezone == other.agency_timezone and
                self.agency_phone == other.agency_phone and
                self.agency_lang == other.agency_lang and
                self.agency_fare_url == other.agency_fare_url and
                self.agency_email == other.agency_email)
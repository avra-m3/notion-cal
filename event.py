from datetime import datetime

from ics import Event as RawEvent


class Event:
    name: str
    start_at: datetime
    end_at: datetime
    created_at: datetime
    location: str
    url: str
    alarms: list

    def __init__(self, **kwargs):
        kwargs = {key: val for key, val in kwargs.items() if val}
        self.event_id = kwargs.get("event_id", "?")
        self.cal_id = kwargs.get("cal_id", "?")
        self.prod_id = kwargs.get("prod_id", "?")
        self.name = kwargs.get("name",
                               "Untitled Event ({})".format(self.event_id))
        self.start_at = kwargs.get("start_at")
        self.end_at = kwargs.get("end_at")
        self.created_at = kwargs.get("created_at")
        self.location = kwargs.get("location", "N/A")
        self.url = kwargs.get("url", None)
        self.alarms = kwargs.get("alarms", [])
        self.all_day = kwargs.get("all_day", False)
        self.description = kwargs.get("description", "")

    def create_row(self, collection):
        print("Create Mode: {}".format(self.unique_id))
        row = collection.add_row()
        for key in row.get_all_properties():
            if hasattr(self, key):
                setattr(row, key, getattr(self, key))

    @property
    def unique_id(self):
        return "{}/{}/{}({})".format(self.prod_id, self.cal_id, self.event_id,
                                     self.name)

    @classmethod
    def from_notion_row(cls, row):
        result = row.get_all_properties()
        return cls(**result)

    @classmethod
    def from_calendar(cls, event: RawEvent, calendar):
        result = {
            "event_id": event.uid,
            "cal_id": calendar.title,
            "prod_id": calendar.creator,
            "name": event.name,
            "start_at": event.begin.datetime,
            "end_at": event.end.datetime,
            "created_at": event.created.datetime,
            "location": event.location,
            "url": event.url,
            "alarms": event.alarms,
            "all_day": event.all_day,
            "description": event.description
        }

        return cls(**result)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def get_event_schema():
        return {
            "title": {"name": "Name", "type": "title"},
            "0001": {"name": "event_id", "type": "text"},
            "0002": {"name": "cal_id", "type": "text"},
            "0003": {"name": "prod_id", "type": "text"},
            "0004": {"name": "start_at", "type": "date"},
            "0005": {"name": "end_at", "type": "date"},
            "0006": {"name": "created_at", "type": "date"},
            "0007": {"name": "location", "type": "text"},
            "0008": {"name": "url", "type": "url"},
            "0009": {"name": "all_day", "type": "checkbox"},
            "0010": {"name": "description", "type": "text"},
        }

        # a = {"title": {"name": "Name", "type": "title"},
        #      "l/xP": {"name": "event_id", "type": "text"},
        #      "Xpw>": {"name": "cal_id", "type": "text"},
        #      "tr*<": {"name": "prod_id", "type": "text"},
        #      "vKIZ": {"name": "start_at", "type": "date"},
        #      "Kmox": {"name": "end_at", "type": "date"},
        #      ".,G(": {"name": "created_at", "type": "date"},
        #      "_}|l": {"name": "location", "type": "text"},
        #      "9>gd": {"name": "url", "type": "url"},
        #      "s&)-": {"name": "all_day", "type": "checkbox"},
        #      "lZ8K": {"name": "description", "type": "text"}}

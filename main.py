import os
from datetime import datetime

from notion.client import NotionClient

from ics_calendar import Calendar
from database import CalendarDatabase

__HOME__ = "https://www.notion.so/Get-Started-ccc857dcaab04948a66554fc2a09b4f7"
__CALENDARS__ = "https://www.notion.so/6d96f527eae44188b87b653899ea6552?v=35592a53b5554541851ad8f1636a38c9"


def get_reg_calendars(block) -> list:
    return [
        {"name": "Test", "values": []}
    ]


def main():
    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN_V2"))
    calendar_view = notion.get_collection_view(__CALENDARS__)

    for record in calendar_view.default_query().execute():
        name = ""
        calendar = None

        if record.caldav_url:
            print("Connect CalDav/ICS; {}".format(record.caldav_url))
            calendar = Calendar.from_remote(record.caldav_url, record.auth)
            name = calendar.title

        database = CalendarDatabase.find_or_create(record, name, notion)

        database.synchronize(calendar)


if __name__ == "__main__":
    main()

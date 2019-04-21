import argparse
import os

from notion.client import NotionClient

from database import CalendarDatabase
from ics_calendar import Calendar


def get_args():
    parser = argparse.ArgumentParser(
        description="Sync calendars from CalDav format into notion")
    parser.add_argument("notion_database",
                        help="A url pointing to a notion database with a caldav_url, and auth field")
    parser.add_argument("--token_v2", help="The notion token_v2, you can obtain this by looking at cookies while logged in.")
    return parser.parse_args()


def main():
    args = get_args()

    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN_V2", args.token_v2))
    calendar_view = notion.get_collection_view(args.notion_database)

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

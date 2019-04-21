import datetime

from notion.block import CollectionViewBlock

from event import Event


class CalendarDatabase:
    _events = []

    def __init__(self, block: CollectionViewBlock, parent):
        self.view = block.views[0]
        self.block = block
        self.parent = parent
        self.set_sync_status("Running")

    @classmethod
    def search_in_block(cls, block, name):
        for child in block.children.filter(CollectionViewBlock):
            if child.collection is not None:
                if child.title == name:
                    return CalendarDatabase(child, parent=block)
        return None

    @classmethod
    def create_in_block(cls, parent, name, notion):
        block = parent.children.add_new(CollectionViewBlock)
        target = notion.get_collection(
            notion.create_record("collection", parent=block,
                                 schema=Event.get_event_schema()))
        view = notion.get_collection_view(
            notion.create_record("collection_view", parent=block,
                                 type="table"), collection=target)
        view.set("collection_id", target.id)
        block.set("collection_id", target.id)
        block.set("view_ids", [view.id])
        block.title = name

        return CalendarDatabase(block, parent=parent)

    @classmethod
    def find_or_create(cls, block, name, notion):
        result = cls.search_in_block(block, name)
        if result is None:
            result = cls.create_in_block(block, name, notion)
        return result

    @property
    def events(self):
        if not self._events:
            self.refresh_events()
        return self._events

    def set_sync_status(self, status):
        print("Sync status set to {} for table {}".format(status, self.parent.title))
        self.parent.last_sync = datetime.datetime.now()
        self.parent.sync_result = status

    def refresh_events(self):
        self._events.clear()
        for row in self.view.default_query().execute():
            self._events.append(Event.from_notion_row(row))

    def synchronize(self, calendar):
        if calendar is None:
            self.set_sync_status("Error (No calendar located)")
            return

        count = 0

        for ev in calendar.events:
            cal_event = Event.from_calendar(ev, calendar)
            if cal_event not in self.events:
                cal_event.create_row(self.view.collection)
                count += 1

        self.refresh_events()
        self.set_sync_status("Success ({} rows added)".format(count))

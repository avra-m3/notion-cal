from notion.client import NotionClient
import os

client = NotionClient(token_v2=os.getenv("NOTION_TOKEN_V2"))
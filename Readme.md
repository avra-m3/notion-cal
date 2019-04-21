Notion-Cal
===============
**What is this bizarre script?**

Notion is a database trello like thing, learn more here: https://notion.so

The aim of this script is to pull events out of a calendar in ICS format and into a notion database.


Installation
-------------------

1. Install python > 3.6
2. Install dependencies; `pip install -r requirements.txt`


Setup
------------------

In order to run this script successfully, some work needs to be done.

1. Create a new table in notion, add the following properties;
    - Caldav URL
    - Auth
    - Last Sync
    - Sync Result

    You should have a table that looks like the one below.
    
    (insert image)
    
    Copy the link to this table, it'll be important in a second.
    
2. Find your notion token_v2 (up to date guide here: https://github.com/jamalex/notion-py)

Usage
------------------

To run the script execute the following command;

```
python main.py "<insert_link_to_table>" --token_v2 <insert token_v2>
```
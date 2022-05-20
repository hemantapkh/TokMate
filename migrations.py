import os
import json
import sqlite3

config = json.load(open('src/config.json'))
videoDatabase = config['videoDatabase']
database = config['database']

input1 = input('Do you want to run migration for video database? Y/[n]: ')
if input1 == 'y':
    if os.path.exists(videoDatabase):
        os.remove(videoDatabase)
        print('[-] Database already exists. Deleting it.')

    conn = sqlite3.connect(videoDatabase)
    print('[+] Magnetlink Database opened successfully.')

    conn.execute('''CREATE TABLE URL
            (url   TEXT PRIMARY KEY,
            rc     TEXT NOT NULL
            );''')

    conn.execute('''CREATE TABLE RC
            (rc       TEXT PRIMARY KEY,
            description  TEXT,
            duration     TEXT,
            videoId      TEXT,
            id           TEXT
            );''')

    print('[+] Table url created successfully.')
    print('[+] Table rc created successfully.')

    conn.close()

input1 = input('Do you want to run migration for bot database? Y/[n]: ')
if input1 == 'y':
    if os.path.exists(database):
        os.remove(database)
        print('[-] Database already exists. Deleting it.')

    conn = sqlite3.connect(database)
    print('[+] Database opened successfully.')

    conn.execute('''CREATE TABLE users
            (UserId       INTEGER PRIMARY KEY,
            date          STRING  NOT NULL,
            token TEXT UNIQUE NOT NULL
            );''')

    print('[+] Table users created successfully.')

    conn.execute('''CREATE TABLE groups
            (UserId       INTEGER PRIMARY KEY,
            date          STRING  NOT NULL
            );''')

    print('[+] Table groups created successfully.')

    conn.execute('''CREATE TABLE settings
            (userId       INTEGER PRIMARY KEY,
            language       TEXT DEFAULT "english"
            );''')

    print('[+] Table settings created successfully.')

    conn.execute('''CREATE TABLE flood
         (userId       INTEGER PRIMARY KEY,
         warned         INTEGER DEFAULT 0,
         lastMessage   INTEGER DEFAULT 0,
         blockTill     INTEGER DEFAULT 0
         );''')

    print('[+] Table flood created successfully.')

    conn.execute('''CREATE TABLE stats
        (messageRequest INT DEFAULT 0,
        messageRequestCached INT DEFAULT 0,
        inlineRequest  INT DEFAULT 0,
        inlineRequestCached  INT DEFAULT 0,
        deepLinkRequest INT DEFAULT 0,
        );''')

    conn.execute('INSERT INTO stats VALUES(0,0,0,0)')
    conn.commit()

    print('[+] Table Stats created successfully.')

    conn.close()

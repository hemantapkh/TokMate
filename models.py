import sqlite3
import secrets
from datetime import datetime


class dbQuery():
    def __init__(self, db, vdb):
        self.db = db
        self.vdb = vdb

    #: Add the user into the database if not registered
    def setUser(self, userId):
        chatType = 'users' if userId > 0 else 'groups'
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        isRegistered = cur.execute(f'SELECT * FROM {chatType} WHERE userId={userId}').fetchone()
        con.commit()

        isRegistered = True if isRegistered else False

        if not isRegistered:
            if chatType == 'users':
                cur.execute(f"Insert into users (userId, date, token) values ({userId}, \"{datetime.today().strftime('%Y-%m-%d')}\", \"{secrets.token_hex(50)}\")")
                cur.execute(f'Insert into settings (userId) values ({userId})')
                cur.execute(f'Insert into flood (userId) values ({userId})')
                con.commit()

            else:
                cur.execute(f"Insert into groups (userId, date) values ({userId}, \"{datetime.today().strftime('%Y-%m-%d')}\")")
                cur.execute(f'Insert into settings (userId) values ({userId})')
                con.commit()

        return isRegistered

    #: Get users Id from token
    def getUserFromToken(self, token):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute('SELECT userId FROM users WHERE token=?',(token,)).fetchone()
        con.commit()

        return users if users else None

    #: Get all the registered users
    def getAllUsers(self):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT userId FROM users').fetchall()
        con.commit()

        return users if users else None

    #: Get all the users with date
    def getAllUsersDate(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        users = cur.execute(f'SELECT * FROM users').fetchall()
        con.commit()

        return users if users else None

    #: Get users of particular language
    def getUsers(self, language):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT userId FROM settings WHERE language="{language}"').fetchall()
        con.commit()

        return users if users else None

    #: Get all users exclude certain languages
    #: languages must be of list type
    def getUsersExcept(self, languages):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT * FROM users WHERE userId NOT NULL').fetchall()
        con.commit()

        for language in languages:
            users = [item for item in users if item not in self.getUsers(language)] if self.getUsers(language) else users

        return users if users else None

    #: Get the user's settings
    def getSetting(self, userId, var, table='settings'):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        setting = cur.execute(f'SELECT {var} FROM {table} WHERE userId={userId} limit 1').fetchone()
        con.commit()

        return setting[0] if setting else None

    #: Set the user's settings
    def setSetting(self, userId, var, value, table='settings'):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        #!? If value is None, put value as NULL else "{string}"
        value = f'"{value}"' if value else 'NULL'
        cur.execute(f'INSERT OR IGNORE INTO {table} (userId, {var}) VALUES ({userId}, {value})')
        cur.execute(f'UPDATE {table} SET {var}={value} WHERE userId={userId}')
        con.commit()


    #: Set video_id in the database
    def setVideo(self, url, rc, videoId=None, description=None, duration=None, setRc=True, id=None):
        con = sqlite3.connect(self.vdb)
        cur = con.cursor()

        cur.execute('Insert into URL (url, rc) VALUES (?, ?)', (url, rc))
        if setRc:
            cur.execute(f'Insert into RC (rc, description, duration, videoId, id) VALUES ("{rc}", "{description}", "{duration}", "{videoId}", "{id}")')

        con.commit()

    #: Get the video data
    def getVideo(self, url=None, rc=None, id=None):
        con = sqlite3.connect(self.vdb)
        con.row_factory = dict_factory
        cur = con.cursor()

        if url:
            rc = cur.execute('SELECT rc FROM URL WHERE url=?', (url,)).fetchone()
            rc = rc['rc'] if rc else None
            video = cur.execute(f'SELECT * FROM RC WHERE rc=?', (rc, )).fetchone() if rc else None

        elif rc:
            video = cur.execute(f'SELECT * FROM RC WHERE rc=?', (rc,)).fetchone()

        else:
            video = cur.execute(f'SELECT * FROM URL INNER JOIN RC ON URL.rc=RC.rc WHERE RC.id=?', (id,)).fetchone()

        con.commit()

        return video

    #: Increase stats count
    def increaseCounter(self, type):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(f'UPDATE stats SET {type}={type}+1')
        con.commit()


#: Return query as dictionary
# https://stackoverflow.com/a/3300514/13987868
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d

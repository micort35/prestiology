#!usr/bin/env/python
import sys
import time
from enum import Enum
from datetime import timedelta, date
import psycopg2
from psycopg2 import sql, pool
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
import auth
import log
import scraper_lib

times = []

def parse_and_input(score, connection, gameday):
    start = time.time()
    #create object and cursor for pSQL processing
    cur = connection.cursor()
    curr_player = log.Log(score, gameday)

    #if player doesn't exist, must create log table, else update tables
    if not (curr_player.exists(cur)):
        curr_player.add_player(cur)
    else:
        player_id = curr_player.get_pid(cur)
        curr_player.ins_log(player_id, cur)
    end = time.time()
    times.append((end-start))
    print(gameday, (end-start))

def update(connection, gameday=(date.today()-timedelta(1))):
    #convert to string and split to individual date elements
    gameday = str(gameday)
    year, month, day = gameday.split('-', 2)

    #grab all scores on given date
    scores = client.player_box_scores(day, month, year)

    #input each score to DB
    for score in scores:
        parse_and_input(score, connection, gameday)

def pull(connection, start=None):
    #use season start if not specified
    if start is None:
        sched = client.season_schedule(2019)
        start = sched[0].get('start_time').date()
    current = date.today()
    global times
    #loop through start of season to current day, update
    for gameday in scraper_lib.daterange(start, current):
        update(connection, gameday)
    avg = sum(times)/len(times)
    print('AVG:', avg)

def clear(connection):
    #double-check for table deletions
    check = input('Are you sure you want to clear the DB? Y/N\n')
    if check is 'Y':
        print('Dropping tables, clearing league_roster...')
    elif check is 'N':
        print('Clear aborted.')
        return
    else:
        print('Please answer with Y or N')

    #drop all game log tables, delete entries in roster
    cur = connection.cursor()
    query = 'SELECT name FROM league_roster'
    cur.execute(query)
    names = cur.fetchall()
    drop = 'DROP TABLE {}'
    for name in names:
        cur.execute(sql.SQL(drop).format(sql.Identifier(name[0])))
    delete = 'DELETE FROM league_roster'
    cur.execute(delete)

def main():
    #attempt to establish connection
    try:
        connection = psycopg2.connect(**auth.connectParams)
    except (Exception, psycopg2.Error) as error:
        print("Error: Failed to connect,", error)
        return

    #execution option handling
    if '--clear' in sys.argv:
        clear(connection)
    elif '--boot' in sys.argv:
        pull(connection)
    elif '--reboot' in sys.argv:
        clear(connection)
        pull(connection)
    elif '--advance' in sys.argv:
        year, month, day = (sys.argv[2]).split('-', 2)
        start = date(int(year), int(month), int(day))
        pull(connection, start)
    else:
        update(connection)
        
    #make all changes permanent
    connection.commit()

if __name__ == "__main__":
    main()
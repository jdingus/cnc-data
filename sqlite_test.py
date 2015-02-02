#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys

def main():
    # drop_data_table()
    create_data_table()
    


def write_list_data(list_data):
    ''' Take a list of data entry lists and write to a table '''


def drop_data_table():
    con = lite.connect('test.db')

    with con:
        
        cur = con.cursor()    

        cur.execute("DROP TABLE IF EXISTS [data]")

def create_data_table():
    con = lite.connect('test.db')

    with con:
        
        cur = con.cursor()    

        cur.execute("\
        CREATE TABLE [data] (\
        [start_time] DATETIME NOT NULL ON CONFLICT ROLLBACK, \
        [stop_time] DATETIME NOT NULL ON CONFLICT ROLLBACK, \
        [cnc_id] text NOT NULL ON CONFLICT ROLLBACK, \
        [prog_num] text, \
        [part1_num] TEXT, \
        [part1_suf] integer, \
        [part1_qty] integer, \
        [part2_num] TEXT, \
        [part2_suf] integer, \
        [part2_qty] integer, \
        [ref_input] float, \
        [pc_time] float, \
        [tc_time] float, \
        [prog_ct] float, \
        [ref_output] float)")

if __name__ == '__main__':
    main()

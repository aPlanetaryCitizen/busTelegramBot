import asyncio
from typing import Final, List


from fermata import Fermata
from utility import Utility
from trip import Trip
from telegram.ext import *
from geopy import *
import difflib
import datetime
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater, filters
from telegram.ext import CallbackQueryHandler
from queue import Queue
from line import Line
import traceback
import common
from utility import Utility
import time
import sys
import threading
import sqlite3
from datetime import *
from telegram import ReplyKeyboardMarkup, KeyboardButton
from math import radians, cos, sin, asin, sqrt
import uuid
from flask import Flask, request

# from aiogram import Dispatcher, Bot, executor, types
# from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN: Final = '6239455143:AAEfAT9erm_VVUcK8Pu18RFILHOlAHdfji0'
BOT_USERNAME: Final = '@sienaBus_bot'
default_time_range = 50
default_search_radius = 100
default_search_radius_increment = 100
default_num_of_stops_to_show_on_search = 5
callback_main_divider = '__'
callback_command_divider = '::'
callback_arg_divider = ';;'
SIMILARITY_THRESHOLD = 0.7
update_queue = Queue()
# dp = Dispatcher(Bot(TOKEN))

to_print = []

print('starting up...')


def test():
    with open('errori codici fermata.txt', 'r') as file:
        content = file.read()
        results = []
        righe_divise = file_to_righe_divise(content)
        for riga in righe_divise:
            print(riga)
        for riga1 in righe_divise:
            for riga2 in righe_divise:
                if riga1 == riga2:
                    pass
                else:
                    if riga1[0] == riga2[2]:
                        if riga1[0].replace('@', '').isdigit():
                            results.append(riga1)
                        elif Utility.contains_symbols(riga1[0].replace('@', '')):
                            results.append(riga1)
                        elif len(riga1[0]) < len(riga1[2]):
                            results.append(riga1)

        #
        # results = Utility.remove_duplicates(results)
        # for result in results:
        #     print(f"\"{result[0]}\",\"{result[1]}\",\"{result[2]}\",\"{result[3]}\"")

    # with open('errori codici fermata.txt', 'r') as file:
    #     content = file.read()
    #     lines = content.splitlines()
    #     for line in lines:
    #         if line.count('","') > 3:
    #             print(line)
    #     error_tuples = []
    #     for line in lines:
    #         error_tuples.append(line.split(', '))
    #     for tuple in error_tuples:
    #         if tuple[0].replace('@', '').isdigit():
    #             temp_id = tuple[0]
    #             temp_name = tuple[1]
    #             tuple[0] = tuple[2]
    #             tuple[1] = tuple[3]
    #             tuple[2] = temp_id
    #             tuple[3] = temp_name
    #         # print(f"\"{tuple[0]}\",\"{tuple[1]}\",\"{tuple[2]}\",\"{tuple[3]}\"")
    # with open('errori codici fermata.txt', 'r') as file:
    #     content = file.read()
    #     lines = content.splitlines()
    #     lines = Utility.remove_duplicates(lines)
    #     for line in lines:
    #         line = line.replace(', ', '","')
    #         line = f"\"{line}\""
    #         print(line)
    #
    # with open('errori codici fermata.txt', 'r') as file:
    #     content = file.read()
    #     error_tuples = file_to_righe_divise(content)
    #     with open('zone\linee regionali\stops.txt', 'r') as file2:
    #         content2 = file2.read()
    #         stops_tuples = file_to_righe_divise(content)
    #         for error in error_tuples:
    #             if not error[2].replace('@', '').isdigit():
    #                 for stop in stops_tuples:
    #                     if error[0] == stop[0]:
    #                         temp_id = error[0]
    #                         temp_name = error[1]
    #                         error[0] = error[2]
    #                         error[1] = error[3]
    #                         error[2] = temp_id
    #                         error[3] = temp_name
    #     for tuple in error_tuples:
    #         print(f"\"{tuple[0]}\",\"{tuple[1]}\",\"{tuple[2]}\",\"{tuple[3]}\"")


def start():
    test()
    print('importing stops...')
    # import_stops()

    # riusa dopo per cercare le robe nei dictionary
    # test_id = 's0123'
    # if test_id in stops_dict:
    #     fermata = stops_dict[test_id]
    #     print(fermata.to_text())

    print('importing trips...')
    print(Utility.get_now_at_timezone().time())
    # import_trips()

    data_file_path = "data.pickle"

    # if not os.path.isfile(data_file_path):
    #     import_files()
    #
    #
    #     data = {
    #         "liste": [common.stops, common.trips, common.lines],
    #         "dizionari": [common.regional_stops_dict]
    #     }
    #     save_data_thread(data_file_path, data)
    import_files()
    lines = []
    for line in to_print:
        lines.append(line)
    lines = Utility.remove_duplicates(lines)
    for line in lines:
        print(line)

    # import_files()

    # else:
    #     data = Utility.load_data(data_file_path)
    #     fermate, trips, lines = data["liste"]
    #     stops_dict, trips_dict, lines_dict, regional_stops_dict = data["dizionari"]

    # if os.path.isfile("data.pickle"):
    #     with open("data.pickle", "rb") as file:
    #         loaded_data = dill.load(file)
    #         loaded_liste = loaded_data["liste"]
    #         fermate, trips, lines = loaded_liste
    #         loaded_dizionari = loaded_data["dizionari"]
    #         stops_dict, trips_dict, lines_dict, regional_stops_dict = loaded_dizionari

    # if not os.path.isfile("data.pickle"):
    #     import_files()
    #     data = {
    #         "liste": [fermate, trips, lines],
    #         "dizionari": [stops_dict, trips_dict, lines_dict, regional_stops_dict]
    #     }
    #     with open("data.pickle", "wb") as file:
    #         dill.dump(data, file)

    # if os.path.isfile("data.pickle"):
    #     loaded_data = Utility.load_objects("data.pickle")
    #     loaded_liste = loaded_data["liste"]
    #     fermate, trips, lines = loaded_liste
    #     loaded_dizionari = loaded_data["dizionari"]
    #     stops_dict, trips_dict, lines_dict, regional_stops_dict = loaded_dizionari
    # if not os.path.isfile("data.pickle"):
    #     import_files()
    #     data = {
    #         "liste": [fermate, trips, lines],
    #         "dizionari": [stops_dict, trips_dict, lines_dict, regional_stops_dict]
    #     }
    #     Utility.save_objects("data.pickle", data)

    # print('building timetables...')
    # for trip in trips:
    #     for stop_time in trip.stops_times:
    #         stop = stop_time[0]
    #         time = stop_time[1]
    #         for date in trip.dates:
    #             stop.add_arrival(datetime.datetime.combine(date, time), trip)
    #
    # print('timetables built and assigned.')

    # test vari
    # print('running tests...')
    # for id1 in common.regional_stops_dict.keys():
    #     for id2 in common.stops_dict.keys():
    #         stop1 = common.regional_stops_dict[id1]
    #         stop2 = common.stops_dict[id2]
    #         dist = stop1.dist_to(stop2)
    #         # if not (stop1.id == stop2.id) and stop1.id[-3:] == stop2.id[-3:] and dist < 50:
    #         #     print(f"{stop1.id}, {stop1.name}, {stop2.id}, {stop2.name}")
    crea_tabelle()
    build_DB()

    print('tests starting.')

    print('montluc')
    print(common.stops_dict['9@s0067'].passing_lines())
    print('lombardi')
    print(common.stops_dict['9@s2405'].passing_lines())

    # for trip in common.trips:
    #     if trip.line == '130':
    #         print(f"130 {trip.headsign}")
    #         for stop_time in trip.stops_times():
    #             print(f"{stop_time[0].to_text()}{stop_time[1]}")

    print('tests finished.')
    print('BOT READY')
    # assegna i vari arrivi alle fermate


def build_DB():
    for stop in common.stops:
        inserisci_stop(stop)
    for trip in common.trips:
        inserisci_trip(trip)
    # for stop in common.stops:
    #     for arrival in stop.arrivals:
    #         inserisci_arrival(arrival)


def import_files():
    for dirpath, dirnames, filenames in os.walk('zone'):
        for dirname in dirnames:
            subdirpath = os.path.join('zone', dirname)
            import_stops4(subdirpath)
            import_trips3(subdirpath)
    print('building timetables...')
    for trip in common.trips:
        for stop_time in trip.stopsids_times:
            stop = common.stops_dict[stop_time[0]]
            time = stop_time[1]
            for date in trip.dates:
                stop.add_arrival(datetime.combine(date, time), trip)
    print('timetables built and assigned.')

    # for dirname in dirnames:
    #     subdir_path = os.path.abspath(dirname)
    #     import_stops2(subdir_path)

    # import_stops2(dirpath)

    # for subdir in Utility.iter_subdirectories("zone"):
    #     print(subdir)
    #     subdir_path = os.path.join('zone', subdir)
    #     stop_times_path = os.path.join(subdir, 'stop_times.txt')
    #     routes_path = os.path.join(subdir, 'routes.txt')
    #     stops_path = os.path.join(subdir, 'stops.txt')
    #     trips_path = os.path.join(subdir, 'trips.txt')
    #     import_stops2(subdir_path)
    #     import_trips3(subdir_path)


def import_stops2(folder):
    stop_times_path = folder + '\stop_times.txt'
    stops_path = folder + '\stops.txt'
    print(stops_path)
    if folder == 'zone\linee regionali':
        print('regionali')
        # with open(stops_path, 'r') as file:
        #     content = file.read()
        #     righe_divise = file_to_righe_divise(content)
        #     for stop in fermate:
        #         for riga in righe_divise:
        #             regional_stop = Fermata(riga[4], riga[1], riga[2], riga[3])
        #             # print(f"{stop.id}   {regional_stop.id}")
        #             dist = stop.dist_to(regional_stop)
        #             if not (stop.id == regional_stop.id) and stop.id[-3:] == regional_stop.id[-3:] and dist < 50:
        #                 print(f"{stop.id}   {stop.name}  {regional_stop.id}  {regional_stop.name}")

    # with open(stop_times_path, 'r') as file:
    #     content = file.read()
    #     righe = content.splitlines()
    #     righe.pop(0)
    #     righe_divise: list[list[str]] = []
    #     for row in righe:
    #         row_parts = row.split(',')
    #         for i in range(len(row_parts)):
    #             row_parts[i] = row_parts[i].replace('"', '')
    #         righe_divise.append(row_parts)
    temp_stops = []
    stop_errors = []
    wrong_ids = []
    right_ids = []

    with open('errori codici fermata.txt', 'r') as file2:
        print('mmmm vedimm')
        content2 = file2.read()
        error_tuples = file_to_righe_divise(content2)
        with open(stops_path, 'r') as file:
            content = file.read()
            stops_righe_divise = file_to_righe_divise(content)
            for tuple in error_tuples:
                for riga in stops_righe_divise:
                    if riga[4] == tuple[2]:
                        to_print.append(
                            f"\"{tuple[0]}\",\"{tuple[1]}\",\"{tuple[2]}\",\"{tuple[3]}\",\"{riga[2]}\",\"{riga[3]}\"")

    with open('errori codici fermata.txt', 'r') as file2:
        content2 = file2.read()
        error_tuples = file_to_righe_divise(content2)
        for tuple in error_tuples:
            right_ids.append(tuple[2])
        for tuple in error_tuples:
            wrong_ids.append(tuple[0])
        print(f"wrong ids: {wrong_ids}")
        Utility.remove_duplicates(right_ids)
        Utility.remove_duplicates(wrong_ids)

        for id in right_ids:
            alt_ids = []
            alt_names = []
            lat = ''
            lon = ''
            name = ''
            for tuple in error_tuples:
                if id == tuple[2]:
                    if not (tuple[0] in alt_ids) and not tuple[0] == id:
                        alt_ids.append(tuple[0])
                    if not (tuple[1] in alt_names) and not tuple[1] == tuple[3]:
                        alt_names.append(tuple[1])
                    name = tuple[3]
                    lat = tuple[4]
                    lon = tuple[5]
            stop_errors.append((id, name, alt_ids, alt_names, lat, lon))
        # for stop in stop_errors:
        #     print(stop)

    # aggiunge le fermate che non hanno id sbagliato
    with open(stops_path, 'r') as file:
        content = file.read()
        stops_righe_divise = file_to_righe_divise(content)
        for row in stops_righe_divise:
            id = row[0].replace('_600', '').lower().strip()
            name = row[1]
            lat = row[2]
            lon = row[3]
            if not (id in wrong_ids):
                common.stops.append(Fermata(id, name, lat, lon))

    for stop in common.stops:
        if stop.id in right_ids:
            for error in stop_errors:
                if stop.id == error[0]:
                    stop.name = error[1]
                    stop.alt_ids += error[2]
                    stop.alt_names += error[3]
        stop.alt_ids = Utility.remove_duplicates(stop.alt_ids)
        stop.alt_names = Utility.remove_duplicates(stop.alt_names)

    temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    common.stops_dict.update(temp_stops_dict)

    for error in stop_errors:
        has_duplicates = False
        for stop in common.stops:
            if error[0] == stop.id:
                has_duplicates = True
        if not has_duplicates:
            temp_stop = Fermata(error[0], error[1], error[4], error[5])
            temp_stop.alt_ids += error[2]
            temp_stop.alt_names += error[3]
            temp_stop.alt_ids = Utility.remove_duplicates(temp_stop.alt_ids)
            temp_stop.alt_names = Utility.remove_duplicates(temp_stop.alt_names)
            common.stops.append(temp_stop)

    temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    common.stops_dict.update(temp_stops_dict)

    # with open(stops_path, 'r') as file:
    #     content = file.read()
    #     stops_righe_divise = file_to_righe_divise(content)
    #     for row in stops_righe_divise:
    #         input_stop = Fermata(row[4], row[1], row[2], row[3])
    #         result_stop = input_stop
    #         with open('errori codici fermata.txt', 'r') as file2:
    #             content2 = file2.read()
    #             error_tuples = file_to_righe_divise(content2)
    #             has_error = False
    #             for error_tuple in error_tuples:
    #                 if input_stop.id == error_tuple[0]:
    #                     has_error = True
    #                     result_stop.id = error_tuple[2]
    #                     result_stop.name = error_tuple[3]
    #                     if stop_by_id(result_stop.id) is None:
    #                         common.stops.append(result_stop)
    #                     stop_by_id(result_stop.id).alt_ids.append(input_stop.id)
    #                     stop_by_id(result_stop.id).alt_names.append(input_stop.name)
    #                 elif input_stop.id == error_tuple[2]:
    #                     has_error = True
    #                     if stop_by_id(result_stop.id) is None:
    #                         common.stops.append(result_stop)
    #                     stop_by_id(result_stop.id).alt_ids.append(error_tuple[0])
    #                     stop_by_id(result_stop.id).alt_names.append(error_tuple[1])
    #
    #         if stop_by_id(result_stop.id) is None:
    #             common.stops.append(result_stop)
    #
    #
    #
    #             # if not (result_stop in common.stops):
    #             #     common.stops.append(result_stop)
    #     temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    #     common.stops_dict.update(temp_stops_dict)
    #
    #
    #     for stop in common.stops:
    #         print(f"{stop.id} {stop.alt_ids}")

    #     for row in stops_righe_divise:
    #         fermata = Fermata(row[4], row[1], row[2], row[3])
    #         is_duplicate = False
    #         is_alt = False
    #         if fermata.id in common.stops_dict:
    #             fermata = common.stops_dict[fermata.id]
    #             is_duplicate = True
    #         with open('errori codici fermata.txt', 'r') as file2:
    #             content2 = file2.read()
    #             error_tuples = file_to_righe_divise(content2)
    #             if is_duplicate:
    #                 for error_tuple in error_tuples:
    #                     if fermata.id == error_tuple[2]:
    #                         if not (error_tuple[0] in fermata.alt_ids):
    #                             fermata.alt_ids.append(error_tuple[0])
    #                         if not (error_tuple[1] in fermata.alt_names):
    #                             fermata.alt_names.append(error_tuple[1])
    #             elif not is_duplicate:
    #                 for error_tuple in error_tuples:
    #                     if fermata.id == error_tuple[0]:
    #                         is_duplicate = True
    #                         is_alt = True
    #                         if not (fermata.id in common.stops_dict[error_tuple[2]].alt_ids):
    #                             common.stops_dict[error_tuple[2]].alt_ids.append(fermata.id)
    #                         if not (fermata.name in common.stops_dict[error_tuple[2]].alt_names):
    #                             common.stops_dict[error_tuple[2]].alt_names.append(fermata.name)
    #             #
    #             #
    #             #
    #             # for error_tuple in error_tuples:
    #             #     if fermata.id == error_tuple[0]:
    #             #         fermata.name = error_tuple[1]
    #             #         if not (error_tuple[2] in fermata.alt_ids):
    #             #             fermata.alt_ids.append(error_tuple[2])
    #             #         if not (error_tuple[3] in fermata.alt_names):
    #             #             fermata.alt_names.append(error_tuple[3])
    #
    #         if not is_duplicate:
    #             common.stops.append(fermata)
    #
    # temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    # common.stops_dict.update(temp_stops_dict)


def get_stops_within_radius(lat, lon, dist):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Calcolo delle differenze di latitudine e longitudine per il raggio specificato in metri
    lat_dist = dist / 111000.0
    lon_dist = dist / (111000.0 * cos(radians(lat)))

    # Esecuzione della query per ottenere le fermate entro il raggio specificato
    cursor.execute('''
        SELECT id, name, latitude, longitude
        FROM stops
        WHERE ABS(latitude - ?) < ? AND ABS(longitude - ?) < ?
    ''', (lat, lat_dist, lon, lon_dist))

    stops = cursor.fetchall()
    conn.close()

    # Filtraggio delle fermate basato sulla distanza
    stops_within_radius = [(stop_id, name, latitude, longitude) for stop_id, name, latitude, longitude in stops
                           if Utility.haversine(lat, lon, latitude, longitude) <= dist]

    stop_objs = []
    for stop in stops_within_radius:
        stop_objs.append(Fermata(stop[0], stop[1], stop[2], stop[3]))
    sorted_stop_objs = Utility.sort_stops_by_dist_to(stop_objs, lat, lon)

    return sorted_stop_objs


def import_stops4(folder):
    stop_times_path = folder + '\stop_times.txt'
    stops_path = folder + '\stops.txt'
    print(stops_path)
    temp_stops = []
    stop_errors = []
    wrong_ids = []
    right_ids = []

    with open('errori codici fermata.txt', 'r') as file2:
        print('mmmm vedimm')
        content2 = file2.read()
        error_tuples = file_to_righe_divise(content2)
        with open(stops_path, 'r') as file:
            content = file.read()
            stops_righe_divise = file_to_righe_divise(content)
            for tuple in error_tuples:
                for riga in stops_righe_divise:
                    if riga[4] == tuple[2]:
                        to_print.append(
                            f"\"{tuple[0]}\",\"{tuple[1]}\",\"{tuple[2]}\",\"{tuple[3]}\",\"{riga[2]}\",\"{riga[3]}\"")

    with open('errori codici fermata.txt', 'r') as file2:
        content2 = file2.read()
        error_tuples = file_to_righe_divise(content2)
        for tuple in error_tuples:
            right_ids.append(tuple[2])
        for tuple in error_tuples:
            wrong_ids.append(tuple[0])
        print(f"wrong ids: {wrong_ids}")
        Utility.remove_duplicates(right_ids)
        Utility.remove_duplicates(wrong_ids)

        for id in right_ids:
            alt_ids_names = []
            lat = ''
            lon = ''
            name = ''
            for tuple in error_tuples:
                if id == tuple[2]:
                    alt_ids_names.append((tuple[0], tuple[1]))
                    name = tuple[3]
                    lat = tuple[4]
                    lon = tuple[5]
            stop_errors.append((id, name, alt_ids_names, lat, lon))
        # for stop in stop_errors:
        #     print(stop[2])

    # aggiunge le fermate che non hanno id sbagliato
    with open(stops_path, 'r') as file:
        content = file.read()
        stops_righe_divise = file_to_righe_divise(content)
        for row in stops_righe_divise:
            id = row[0].replace('_600', '').lower().strip()
            name = row[1]
            lat = row[2]
            lon = row[3]
            if (not (id in wrong_ids)) and not (id in common.stops_dict.keys()):
                common.stops.append(Fermata(id, name, lat, lon))

    for stop in common.stops:
        if stop.id in right_ids:
            for error in stop_errors:
                if stop.id == error[0]:
                    stop.name = error[1]
                    stop.alt_ids_names += error[2]
        stop.alt_ids_names = Utility.remove_duplicates(stop.alt_ids_names)
        # print(stop.alt_ids_names)

    temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    common.stops_dict.update(temp_stops_dict)

    for error in stop_errors:
        has_duplicates = False
        for stop in common.stops:
            if error[0] == stop.id:
                has_duplicates = True
        if not has_duplicates:
            temp_stop = Fermata(error[0], error[1], error[3], error[4])
            temp_stop.alt_ids_names += error[2]
            temp_stop.alt_ids_names = Utility.remove_duplicates(temp_stop.alt_ids_names)
            if not (temp_stop.id in common.stops_dict.keys()):
                common.stops.append(temp_stop)

    temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    common.stops_dict.update(temp_stops_dict)

    # with open(stops_path, 'r') as file:
    #     content = file.read()
    #     stops_righe_divise = file_to_righe_divise(content)
    #     for row in stops_righe_divise:
    #         input_stop = Fermata(row[4], row[1], row[2], row[3])
    #         result_stop = input_stop
    #         with open('errori codici fermata.txt', 'r') as file2:
    #             content2 = file2.read()
    #             error_tuples = file_to_righe_divise(content2)
    #             has_error = False
    #             for error_tuple in error_tuples:
    #                 if input_stop.id == error_tuple[0]:
    #                     has_error = True
    #                     result_stop.id = error_tuple[2]
    #                     result_stop.name = error_tuple[3]
    #                     if stop_by_id(result_stop.id) is None:
    #                         common.stops.append(result_stop)
    #                     stop_by_id(result_stop.id).alt_ids.append(input_stop.id)
    #                     stop_by_id(result_stop.id).alt_names.append(input_stop.name)
    #                 elif input_stop.id == error_tuple[2]:
    #                     has_error = True
    #                     if stop_by_id(result_stop.id) is None:
    #                         common.stops.append(result_stop)
    #                     stop_by_id(result_stop.id).alt_ids.append(error_tuple[0])
    #                     stop_by_id(result_stop.id).alt_names.append(error_tuple[1])
    #
    #         if stop_by_id(result_stop.id) is None:
    #             common.stops.append(result_stop)
    #
    #
    #
    #             # if not (result_stop in common.stops):
    #             #     common.stops.append(result_stop)
    #     temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    #     common.stops_dict.update(temp_stops_dict)
    #
    #
    #     for stop in common.stops:
    #         print(f"{stop.id} {stop.alt_ids}")

    #     for row in stops_righe_divise:
    #         fermata = Fermata(row[4], row[1], row[2], row[3])
    #         is_duplicate = False
    #         is_alt = False
    #         if fermata.id in common.stops_dict:
    #             fermata = common.stops_dict[fermata.id]
    #             is_duplicate = True
    #         with open('errori codici fermata.txt', 'r') as file2:
    #             content2 = file2.read()
    #             error_tuples = file_to_righe_divise(content2)
    #             if is_duplicate:
    #                 for error_tuple in error_tuples:
    #                     if fermata.id == error_tuple[2]:
    #                         if not (error_tuple[0] in fermata.alt_ids):
    #                             fermata.alt_ids.append(error_tuple[0])
    #                         if not (error_tuple[1] in fermata.alt_names):
    #                             fermata.alt_names.append(error_tuple[1])
    #             elif not is_duplicate:
    #                 for error_tuple in error_tuples:
    #                     if fermata.id == error_tuple[0]:
    #                         is_duplicate = True
    #                         is_alt = True
    #                         if not (fermata.id in common.stops_dict[error_tuple[2]].alt_ids):
    #                             common.stops_dict[error_tuple[2]].alt_ids.append(fermata.id)
    #                         if not (fermata.name in common.stops_dict[error_tuple[2]].alt_names):
    #                             common.stops_dict[error_tuple[2]].alt_names.append(fermata.name)
    #             #
    #             #
    #             #
    #             # for error_tuple in error_tuples:
    #             #     if fermata.id == error_tuple[0]:
    #             #         fermata.name = error_tuple[1]
    #             #         if not (error_tuple[2] in fermata.alt_ids):
    #             #             fermata.alt_ids.append(error_tuple[2])
    #             #         if not (error_tuple[3] in fermata.alt_names):
    #             #             fermata.alt_names.append(error_tuple[3])
    #
    #         if not is_duplicate:
    #             common.stops.append(fermata)
    #
    # temp_stops_dict = {fermata.id: fermata for fermata in common.stops}
    # common.stops_dict.update(temp_stops_dict)


def import_trips3(folder_path):
    stop_times_path = os.path.join(folder_path, 'stop_times.txt')
    trips_path = os.path.join(folder_path, 'trips.txt')
    routes_path = os.path.join(folder_path, 'routes.txt')
    calendar_dates_path = os.path.join(folder_path, 'calendar_dates.txt')
    print(trips_path)
    with open(trips_path, 'r') as file:
        content = file.read()
        righe_divise_trips = file_to_righe_divise(content)
        for riga in righe_divise_trips:
            common.trips.append(Trip(riga[2]))
        for trip in common.trips:
            for riga in righe_divise_trips:
                if trip.code == riga[2]:
                    trip.route_id = riga[0]
                    trip.headsign = riga[3]
                    trip.service_id = riga[1]
    with open(calendar_dates_path, 'r') as file:
        content = file.read()
        righe_divise_routes = file_to_righe_divise(content)
        for trip in common.trips:
            for riga in righe_divise_routes:
                if trip.service_id == riga[0]:
                    trip.dates.append(Utility.formatted_date(riga[1]))
    with open(stop_times_path, 'r') as file:
        content = file.read()
        righe_divise_stop_times = file_to_righe_divise(content)

        for trip in common.trips:
            stops_times = []
            for riga in righe_divise_stop_times:
                if trip.code == riga[0]:
                    stop = stop_by_id(Utility.fixed_id(riga[3]))
                    raw_time = riga[1]
                    h_m_s = raw_time.split(":")
                    if int(h_m_s[0]) > 23:
                        raw_time = f'{int(h_m_s[0]) - 24}:{h_m_s[1]}:{h_m_s[2]}'

                    time = datetime.strptime(raw_time, "%H:%M:%S").time()
                    # stop_datetime = datetime.datetime.combine(trip.date, time)
                    stops_times.append((stop.id, time))
            trip.stopsids_times += stops_times

    with open(routes_path, 'r') as file:
        content = file.read()
        righe_divise_routes = file_to_righe_divise(content)

        for riga in righe_divise_routes:
            common.lines.append(Line(riga[2], riga[3].split("-")))
            for trip in common.trips:
                if trip.route_id == riga[0]:
                    temp_line = riga[2]
                    if 's' in temp_line:
                        temp_line = temp_line[temp_line.find("s"):]
                    trip.line = temp_line

    temp_trips_dict = {trip.code: trip for trip in common.trips}
    common.trips_dict.update(temp_trips_dict)
    common.lines_dict.update({line.number: line for line in common.lines})

    # for trip in trips_by_line('120'):
    #     print(trip.to_text())
    # print(f"{len(trips_by_line('120'))} trips")


# def import_stops():
#     with open('zone/extra siena/stop_times.txt', 'r') as file:
#         content = file.read()
#         righe = content.splitlines()
#         righe.pop(0)
#         righe_divise: list[list[str]] = []
#         for row in righe:
#             row_parts = row.split(',')
#             for i in range(len(row_parts)):
#                 row_parts[i] = row_parts[i].replace('"', '')
#             righe_divise.append(row_parts)
#     with open('zone/extra siena/stops.txt', 'r') as file:
#         content = file.read()
#         righe = content.splitlines()
#         righe.pop(0)
#         righe_divise: list[list[str]] = []
#         for row in righe:
#             row_parts = row.split(',')
#             for i in range(len(row_parts)):
#                 row_parts[i] = row_parts[i].replace('"', '')
#             temp = row_parts[0].replace('_600', '').split('@')
#             if len(temp) > 1:
#                 id = temp[1]
#             else:
#                 id = temp[0]
#
#             fermata = Fermata(id.lower(), row_parts[1].lower(), row_parts[2], row_parts[3])
#             fermate.append(fermata)
#             righe_divise.append(row_parts)
#     stops_dict = {fermata.id: fermata for fermata in fermate}
# def import_trips2():
#     with open('zone/extra siena/stop_times.txt', 'r') as file:
#         content = file.read()
#         righe = content.splitlines()[1:]
#         righe_divise = [row.replace('"', '').split(',') for row in righe]
#
#         trip_ids = list(set(riga[0] for riga in righe_divise))
#         for code in trip_ids:
#             stops_times = []
#             for riga in righe_divise:
#                 if code == riga[0]:
#                     cleaned_stop_id = clean_raw_stop_id(riga[3])
#                     stop = stop_by_id(cleaned_stop_id)
#                     time = datetime.time.fromisoformat(riga[1])
#                     stops_times.append((stop, time))
#             temp_trip = Trip(code, stops_times, '', '', '')
#             trips.append(temp_trip)
#
#     with open('zone/extra siena/trips.txt', 'r') as file:
#         content = file.read()
#         righe_divise_trips = file_to_righe_divise(content)
#         for trip in trips:
#             for riga in righe_divise_trips:
#                 if trip.code == riga[2]:
#                     trip.route_id, trip.headsign = riga[0], riga[3]
#
#     with open('zone/extra siena/routes.txt', 'r') as file:
#         content = file.read()
#         righe_divise_routes = file_to_righe_divise(content)
#         for trip in trips:
#             for riga in righe_divise_routes:
#                 if trip.route_id == riga[0]:
#                     trip.line = riga[2]
#
#     trips_dict = {trip.code: trip for trip in trips}
# def import_trips():
#     with open('zone/extra siena/stop_times.txt', 'r') as file:
#         content = file.read()
#         righe = content.splitlines()
#         righe.pop(0)
#         righe_divise: list[list[str]] = []
#         for row in righe:
#             row_parts = row.split(',')
#             for i in range(len(row_parts)):
#                 row_parts[i] = row_parts[i].replace('"', '')
#             righe_divise.append(row_parts)
#
#         trip_ids = []
#         for riga in righe_divise:
#             trip_ids.append(riga[0])
#         trip_ids = Utility.remove_duplicates(trip_ids)
#         for code in trip_ids:
#             stops_times = []
#             for riga in righe_divise:
#                 if code == riga[0]:
#                     cleaned_stop_id = clean_raw_stop_id(riga[3])
#                     stop = stop_by_id(cleaned_stop_id)
#                     time = datetime.datetime.strptime(riga[1], "%H:%M:%S").time()
#                     stops_times.append((stop, time))
#             temp_trip = Trip(code, stops_times, '', '', '')
#             trips.append(temp_trip)
#     with open('zone/extra siena/trips.txt', 'r') as file:
#         content = file.read()
#         righe_divise_trips = file_to_righe_divise(content)
#         for trip in trips:
#             for riga in righe_divise_trips:
#                 if trip.code == riga[2]:
#                     trip.route_id = riga[0]
#                     trip.headsign = riga[3]
#     with open('zone/extra siena/routes.txt', 'r') as file:
#         content = file.read()
#         righe_divise_routes = file_to_righe_divise(content)
#         for trip in trips:
#             for riga in righe_divise_routes:
#                 if trip.route_id == riga[0]:
#                     trip.line = riga[2]
#     trips_dict = {trip.code: trip for trip in trips}
#     # for trip in trips_by_line('120'):
#     #     print(trip.to_text())
#     # print(f"{len(trips_by_line('120'))} trips")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Ciao, sono pronto ad aiutarti con i bus. scrivi /help per un aiuto su come usare il bot')


async def button_command(update: Update, context: ContextTypes.context):
    query = update.callback_query
    query_text = query.data
    print(f"query: {query_text}")
    query_descr_array = query_text.split(callback_main_divider)[0].split(callback_command_divider)
    query_arg = query_text.split(callback_main_divider)[1]
    if callback_arg_divider in query_arg:
        query_args = query_arg.split(callback_arg_divider)
        if len(query_descr_array) == 1:
            query_descr = query_descr_array[0]
            if query_descr == 'stopsAtLatLonRadius':
                # await user_location_time_check(update, query.message)
                lat = float(query_args[0])
                lon = float(query_args[1])
                radius = float(query_args[2])
                stops = get_stops_within_radius(lat, lon, radius)
                widen_radius_button = InlineKeyboardButton(f"widen search radius",
                                                           callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}{lon}{callback_arg_divider}{radius + default_search_radius_increment}")
                if len(stops) == 0:
                    await respond_to_stops(update, query.message, stops,
                                           f"Non ho trovato fermate entro {radius} metri dalla posizione data:",
                                           [widen_radius_button], False)
                else:
                    await respond_to_stops(update, query.message, stops,
                                           f"Fermate entro {int(radius)} metri dalla posizione data:",
                                           [widen_radius_button], False)
            elif query_descr == 'widenAtLatLonRadius':
                lat = float(query_args[0])
                lon = float(query_args[1])
                radius = float(query_args[2])
                stops = get_stops_within_radius(lat, lon, radius)
                widen_radius_button = InlineKeyboardButton(f"widen search radius",
                                                           callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}{lon}{callback_arg_divider}{radius + default_search_radius_increment}")

                if len(stops) == 0:
                    await respond_to_stops(update, query.message, stops,
                                           f"Non ho trovato fermate entro {radius} metri dalla posizione data:",
                                           [widen_radius_button], True)
                else:
                    await respond_to_stops(update, query.message, stops,
                                           f"Fermate entro {int(radius)} metri dalla posizione data:",
                                           [widen_radius_button], True)



        elif len(query_descr_array) == 2:
            if query_descr_array[0] == 'stop':
                if query_descr_array[1] == 'arrivals':
                    stop = ricerca_stop_per_id(query_args[0])
                    await show_arrivals(query.message, stop, query_args[1], True)
                elif query_descr_array[1] == 'addFav':
                    user_id = query_args[0]
                    stop_id = query_args[1]
                    remove_from_favorites_button = new_button(f"remove favorite", [f"stop", f"removeFav"],
                                                              [update.effective_user.id, stop_id])
                    await edit_clicked_button(query, remove_from_favorites_button)
                    # button_keyboard = get_buttonKeyboard_from_reply_markup(query.message.reply_markup)
                    # for i, row in enumerate(button_keyboard):
                    #     for j, button in enumerate(row):
                    #         if button.callback_data == query.data:
                    #             remove_from_favorites_button = new_button(f"remove favorite", [f"stop", f"removeFav"],
                    #                                                       [update.effective_user.id, stop_id])
                    #             button_keyboard[i][j] = remove_from_favorites_button
                    # await query.edit_message_reply_markup(InlineKeyboardMarkup(button_keyboard))
                    if not Utility.is_stop_favorite(user_id, stop_id):
                        Utility.add_favorite_stop_to_db(user_id, stop_id)
                        await update.get_bot().sendMessage(update.effective_chat.id, f"Ho AGGIUNTO la fermata {stop_id}, '{ricerca_stop_per_id(stop_id).name}' ai tuoi preferiti.")
                        print(f"stop {stop_id} ADDED to favorites for user {user_id}")
                    else:
                        await update.get_bot().sendMessage(update.effective_chat.id, f"La fermata {stop_id}, '{ricerca_stop_per_id(stop_id).name}' è già tra i tuoi preferiti.")
                        print(f"stop {stop_id} ALREADY a favourite for user {user_id}")
                elif query_descr_array[1] == 'removeFav':
                    user_id = query_args[0]
                    stop_id = query_args[1]
                    add_to_fav_button = new_button(f"add favorite", [f"stop", f"addFav"],
                                                   [update.effective_user.id, stop_id])
                    await edit_clicked_button(query, add_to_fav_button)
                    if Utility.is_stop_favorite(user_id, stop_id):
                        Utility.remove_favorite_stop(user_id, stop_id)
                        await update.get_bot().sendMessage(update.effective_chat.id, f"Ho RIMOSSO la fermata {stop_id}, '{ricerca_stop_per_id(stop_id).name}' dai tuoi preferiti.")
                        print(f"stop {stop_id} REMOVED from favorites for user {user_id}")
                    else:
                        await update.get_bot().sendMessage(update.effective_chat.id,
                                                           f"La fermata {stop_id}, '{ricerca_stop_per_id(stop_id).name}' non è tra i tuoi preferiti.")
                        print(f"stop {stop_id} NOT a favourite for user {user_id}")


                # keyboard = InlineKeyboardMarkup([[widen_radius_button]])
                # await query.message.reply_text('premi qua per allargare la ricerca', reply_markup=keyboard)
    else:
        if len(query_descr_array) == 1:
            query_descr = query_descr_array[0]
            if query_descr == 'stop':
                stop = ricerca_stop_per_id(query_arg.split(' ')[0])
                print(stop)
                await respond_to_stops(update, query.message, [stop], f"Fermata: ", [], False)
                # await show_arrivals(query.message, stop, 0)
            elif query_descr == 'moreStops':
                reply_markup = query.message.reply_markup
                buttons = []
                for row in reply_markup.inline_keyboard:
                    buttons.append(row)
                    # for button in row:
                    #     print(f"button: {button.text}")
                buttons = buttons[:-1]
                stops = common.data[query_arg][1]
                # await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                text = common.data[query_arg][0]
                # stop_ids = common.data[query_arg][1].split(';')

                # for id in stop_ids:
                #     stops.append(ricerca_stop_per_id(id))
                # await show_stops_with_overflow(stops, [], query.message)
                # //////

                stops_to_show = stops[:default_num_of_stops_to_show_on_search]
                print(f"STOPS {len(stops_to_show)}")
                remaining_stops = stops[default_num_of_stops_to_show_on_search:]
                for stop in stops_to_show:
                    buttons.append([InlineKeyboardButton(f"{stop.to_text()}",
                                                         callback_data=f"stop{callback_main_divider}{stop.id}")])
                if len(remaining_stops) > 0:
                    # ids = ''
                    # for stop in remaining_stops:
                    #     ids += f"{stop.id};"
                    # ids = ids.strip()[:-1]
                    # print(f"moreStops_{ids}")
                    dati_id = str(uuid.uuid4())
                    if len(common.data[query_arg]) > 2:
                        buttons_to_add = common.data[query_arg][2]
                        common.data[dati_id] = (text, remaining_stops, buttons_to_add)
                    else:
                        common.data[dati_id] = (text, remaining_stops)
                    more_stops_button = InlineKeyboardButton("...",
                                                             callback_data=f"moreStops{callback_main_divider}{dati_id}")
                    buttons.append([more_stops_button])
                else:
                    if len(common.data[query_arg]) > 2:
                        buttons_to_add = common.data[query_arg][2]
                        buttons.append(buttons_to_add)
                await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                # /////////
            elif query_descr == 'stopsAtUserInRadius':
                if await has_user_shared_location(update, query.message):
                    await user_location_time_check(update, query.message)
                    lat = common.user_locations[update.effective_user.id]['location'][0]
                    lon = common.user_locations[update.effective_user.id]['location'][1]
                    radius = float(query_arg)
                    stops = get_stops_within_radius(lat, lon, radius)
                    widen_radius_button = InlineKeyboardButton(f"widen search radius",
                                                               callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}{lon}{callback_arg_divider}{radius + default_search_radius_increment}")
                    if len(stops) == 0:
                        await respond_to_stops(update, query.message, stops,
                                               f"Non ho trovato fermate entro {radius} metri dalla tua posizione:",
                                               [widen_radius_button], False)
                    else:
                        await respond_to_stops(update, query.message, stops,
                                               f"Fermate entro {int(radius)} metri dalla tua posizione:",
                                               [widen_radius_button], False)
            elif query_descr == 'sortAlpha':
                stops_to_sort = common.data[query_arg]
                sorted_stops = Utility.sort_stops_alpha(stops_to_sort)
                dati_id = str(uuid.uuid4())
                common.data[dati_id] = sorted_stops
                buttons = [[]]

                sort_by_name_button = InlineKeyboardButton(f"sort by name",
                                                           callback_data=f"sortAlpha{callback_main_divider}{dati_id}")
                sort_by_position_button = InlineKeyboardButton(f"sort by position",
                                                               callback_data=f"sortGeo{callback_main_divider}{dati_id}")
                buttons.append([sort_by_name_button, sort_by_position_button])
                if len(sorted_stops) > default_num_of_stops_to_show_on_search:
                    stops_to_show = sorted_stops[:default_num_of_stops_to_show_on_search]
                    remaining_stops = sorted_stops[default_num_of_stops_to_show_on_search:]
                    for stop in stops_to_show:
                        buttons.append(
                            [InlineKeyboardButton(f"{stop.to_text()}",
                                                  callback_data=f"stop{callback_main_divider}{stop.id}")])
                    if len(remaining_stops) > 0:
                        dati_id = str(uuid.uuid4())
                        common.data[dati_id] = (".", remaining_stops)
                        more_stops_button = InlineKeyboardButton("...",
                                                                 callback_data=f"moreStops{callback_main_divider}{dati_id}")
                        buttons.append([more_stops_button])
                    keyboard = InlineKeyboardMarkup(buttons)
                    await query.message.edit_text(f"Fermate preferite:", reply_markup=keyboard)
                else:
                    for stop in sorted_stops:
                        buttons.append(
                            [InlineKeyboardButton(f"{stop.to_text()}",
                                                  callback_data=f"stop{callback_main_divider}{stop.id}")])
                    keyboard = InlineKeyboardMarkup(buttons)
                    await query.message.edit_text(f"Fermate preferite:", reply_markup=keyboard)
            elif query_descr == 'sortGeo':
                if await has_user_shared_location(update, update.message):
                    lat = common.user_locations[update.effective_user.id]['location'][0]
                    lon = common.user_locations[update.effective_user.id]['location'][1]
                    stops_to_sort = common.data[query_arg]
                    sorted_stops = Utility.sort_stops_by_dist_to(stops_to_sort, lat, lon)
                    dati_id = str(uuid.uuid4())
                    common.data[dati_id] = sorted_stops
                    buttons = [[]]
                    sort_by_name_button = InlineKeyboardButton(f"sort by name",
                                                               callback_data=f"sortAlpha{callback_main_divider}{dati_id}")
                    sort_by_position_button = InlineKeyboardButton(f"sort by position",
                                                                   callback_data=f"sortGeo{callback_main_divider}{dati_id}")
                    buttons.append([sort_by_name_button, sort_by_position_button])
                    if len(sorted_stops) > default_num_of_stops_to_show_on_search:
                        stops_to_show = sorted_stops[:default_num_of_stops_to_show_on_search]
                        remaining_stops = sorted_stops[default_num_of_stops_to_show_on_search:]
                        for stop in stops_to_show:
                            buttons.append(
                                [InlineKeyboardButton(f"{stop.to_text()}",
                                                      callback_data=f"stop{callback_main_divider}{stop.id}")])
                        if len(remaining_stops) > 0:
                            dati_id = str(uuid.uuid4())
                            common.data[dati_id] = (".", remaining_stops)
                            more_stops_button = InlineKeyboardButton("...",
                                                                     callback_data=f"moreStops{callback_main_divider}{dati_id}")
                            buttons.append([more_stops_button])
                        keyboard = InlineKeyboardMarkup(buttons)
                        await query.message.edit_text(f"Fermate preferite:", reply_markup=keyboard)
                    else:
                        for stop in sorted_stops:
                            buttons.append(
                                [InlineKeyboardButton(f"{stop.to_text()}",
                                                      callback_data=f"stop{callback_main_divider}{stop.id}")])
                        keyboard = InlineKeyboardMarkup(buttons)
                        await query.message.edit_text(f"Fermate preferite:", reply_markup=keyboard)
                else:
                    await query.message.reply_text(f"Per usare questa funzione ho bisogno che tu mi dia accesso alla posizione. "
                                        f"Se non l'hai già fatto premi l'icona di condivisione, "
                                        f"scegli 'posizione' e poi 'posizione in tempo reale', se invece l'hai "
                                        f"già fatto riprova tra qualche secondo.")







            # elif query_descr == 'widenAtUserInRadius':
            #     user_id = update.effective_user.id
            #     lat = common.user_locations[user_id]['location'][0]
            #     lon = common.user_locations[user_id]['location'][1]
            #     radius = float(query_arg)
            #     stops = get_stops_within_radius(lat, lon, radius)
            #     widen_radius_button = InlineKeyboardButton(f"widen search radius",
            #                                                callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}{lon}{callback_arg_divider}{radius + default_search_radius_increment}")
            #
            #     if len(stops) == 0:
            #         await respond_to_stops(update, query.message, stops,
            #                                f"Non ho trovato fermate entro {radius} metri dalla posizione data:",
            #                                [widen_radius_button], should_edit_latest_message=True)
            #     else:
            #         await respond_to_stops(update, query.message, stops,
            #                                f"Fermate entro {int(radius)} metri dalla posizione data:",
            #                                [widen_radius_button], should_edit_latest_message=True)

            # await respond_to_stops(update, query.message, stops, f"{text}, ti mostro altre {len(stop_ids)} fermate", [])
        # messages_to_send = []
        # if len(arrivals_text) > 0:
        #     messages_to_send.append(f"Fermata: {query_arg}")
        #     info_button = InlineKeyboardButton(f"info", callback_data=f"stop:info_{stop.id}")
        #     keyboard = InlineKeyboardMarkup([[info_button]])
        #
        #     await query.get_bot().sendMessage(chat_id=query.message.chat_id, text=f"Fermata: {query_arg}", reply_markup=keyboard)
        #     await query.get_bot().sendMessage(chat_id=query.message.chat_id, text=arrivals_text)
        # else:
        #     await query.get_bot().sendMessage(chat_id=query.message.chat_id, text=f"Mi spiace, non ho trovato arrivi"
        #                                                                       f" a\n{query_arg}")
        elif len(query_descr_array) == 2:
            if query_descr_array[0] == 'stop':
                stop = ricerca_stop_per_id(query_arg.split(' ')[0])
                if query_descr_array[1] == 'info':
                    # button1 = InlineKeyboardButton(f"{stop.id}   {stop.name}",
                    #                                callback_data=f"stop{callback_main_divider}{stop.id}")
                    # keyboard = InlineKeyboardMarkup([[button1]])
                    # await query.get_bot().sendMessage(chat_id=query.message.chat_id, text='Fermata:',
                    #                                   reply_markup=keyboard)
                    stop_details_text = format_stop_details(get_stop_details(stop.id))
                    coordinates_string = f"{stop.latitude}, {stop.longitude}"
                    await query.get_bot().sendMessage(chat_id=query.message.chat_id, text=stop_details_text)
                    await query.get_bot().sendMessage(chat_id=query.message.chat_id, text=coordinates_string)
                    await query.get_bot().sendLocation(query.message.chat_id, stop.latitude, stop.longitude,
                                                       disable_notification=True)
                elif query_descr_array[1] == 'commands':
                    buttons = [[]]
                    info_button = InlineKeyboardButton(f"info",
                                                       callback_data=f"stop{callback_command_divider}info{callback_main_divider}{stop.id}")
                    to_here_button = InlineKeyboardButton(f"viaggia fino a qui",
                                                          callback_data=f"stop{callback_command_divider}toHere{callback_main_divider}{stop.id}")
                    arrivals_button = InlineKeyboardButton(f"bus in arrivo",
                                                           callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}{callback_arg_divider}0")
                    # near_stops_button = InlineKeyboardButton(f"fermate vicine", callback_data=f"stop:nearStops_{stop.id};0")
                    near_stops_button = InlineKeyboardButton(f"fermate vicine",
                                                             callback_data=f"stopsAtLatLonRadius{callback_main_divider}{stop.latitude}{callback_arg_divider}{stop.longitude}{callback_arg_divider}{default_search_radius}")
                    keyboard = InlineKeyboardMarkup(
                        [[info_button, to_here_button], [arrivals_button, near_stops_button]])
                    await query.get_bot().sendMessage(chat_id=query.message.chat_id,
                                                      text="Cosa vuoi fare con questa fermata?",
                                                      reply_markup=keyboard)
                elif query_descr_array[1] == 'arrivals':
                    await respond_to_stops(update, query.message, [stop], 'Fermata:', [], False)
                elif query_descr_array[1] == 'altro':
                    stop = ricerca_stop_per_id(query_arg)
                    message = query.message
                    old_buttons = get_buttonKeyboard_from_reply_markup(message.reply_markup)
                    for row in old_buttons:
                        for button in row:
                            if button.text == 'altro':
                                (old_buttons[old_buttons.index(row)]).pop(
                                    old_buttons[old_buttons.index(row)].index(button))
                    button1 = InlineKeyboardButton(f"{stop.to_text()}",
                                                   callback_data=f"stop{callback_main_divider}{stop.id}")
                    info_button = InlineKeyboardButton(f"info",
                                                       callback_data=f"stop{callback_command_divider}info{callback_main_divider}{stop.id}")
                    to_here_button = InlineKeyboardButton(f"viaggia fino a qui",
                                                          callback_data=f"stop{callback_command_divider}toHere{callback_main_divider}{stop.id}")
                    near_stops_button = InlineKeyboardButton(f"fermate vicine",
                                                             callback_data=f"stopsAtLatLonRadius"
                                                                           f"{callback_main_divider}{stop.latitude}"
                                                                           f"{callback_arg_divider}{stop.longitude}"
                                                                           f"{callback_arg_divider}{default_search_radius}")

                    remove_from_favorites_button = new_button(f"remove favorite", [f"stop", f"removeFav"], [update.effective_user.id, stop.id])
                    copy_id_button = new_button(f"copy id", [f"stop", f"copyId"], [stop.id])
                    add_to_favorites_button = InlineKeyboardButton(f"add to favorites", callback_data=f"stop{callback_command_divider}"
                                                                                                      f"addFav{callback_main_divider}"
                                                                                                      f"{update.effective_user.id}{callback_arg_divider}"
                                                                                                      f"{stop.id}")
                    stop_user_commands = InlineKeyboardButton(f"stop_commands",
                                                              callback_data=f"stop{callback_command_divider}"
                                                                            f"commands{callback_main_divider}{stop.id}")
                    arrivals_command = InlineKeyboardButton(f"bus in arrivo",
                                                            callback_data=f"stop{callback_command_divider}"
                                                                          f"arrivals{callback_main_divider}{stop.id}{callback_arg_divider}0")

                    buttons = [old_buttons[0], [info_button, copy_id_button]]
                    if Utility.is_stop_favorite(update.effective_user.id, stop.id):
                        buttons.append([near_stops_button, remove_from_favorites_button])
                    else:
                        buttons.append([near_stops_button, add_to_favorites_button])
                    # for button in buttons_to_add:
                    #     buttons.append([button])
                    keyboard = InlineKeyboardMarkup(buttons)
                    await message.edit_text(text=message.text, reply_markup=keyboard)
                    print('ALTROOOOOO')
                elif query_descr_array[1] == 'copyId':
                    stop = ricerca_stop_per_id(query_arg)
                    await query.message.reply_text(f"{stop.id}")
                    await query.message.reply_text(f"Clicca l'id e seleziona 'copia' per copiarlo nella tua clipboard")


# async def user_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                             text="Per favore, condividi la tua posizione per ottenere le coordinate.")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ecco l\'aiuto')


# async def ask_user_position(update, context):
#     # Crea una tastiera personalizzata con il pulsante per condividere la posizione
#     keyboard = [[KeyboardButton("Condividi Posizione", request_location=True)]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
#
#     # Invia un messaggio all'utente con la richiesta di condividere la posizione
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Per abilitare le funzioni ",
#         reply_markup=reply_markup
#     )

async def edit_clicked_button(query, new_button):
    button_keyboard = get_buttonKeyboard_from_reply_markup(query.message.reply_markup)
    for i, row in enumerate(button_keyboard):
        for j, button in enumerate(row):
            if button.callback_data == query.data:
                button_keyboard[i][j] = new_button
    await query.edit_message_reply_markup(InlineKeyboardMarkup(button_keyboard))


async def save_user_location(update, context):
    user_id = update.effective_user.id
    message = None
    if update.edited_message or (update.message.location and update.message.location.live_period):
        if update.edited_message:
            message = update.edited_message
        elif update.message.location and update.message.location.live_period:
            message = update.message
        current_pos = (message.location.latitude, message.location.longitude)
        print(f"current position: {current_pos}")
        common.user_locations[user_id] = {
            'location': current_pos,
            'update_time': Utility.get_now_at_timezone()
        }
    else:
        message = update.message
        stops_at_loc_button = InlineKeyboardButton(f"fermate vicine",
                                                   callback_data=f"stopsAtLatLonRadius{callback_main_divider}{message.location.latitude}{callback_arg_divider}{message.location.longitude}{callback_arg_divider}{default_search_radius}")
        to_loc_button = InlineKeyboardButton(f"viaggia fino a qui",
                                             callback_data=f"toLocation{callback_main_divider}{message.location.latitude}{callback_arg_divider}{message.location.longitude}")
        keyboard = InlineKeyboardMarkup([[stops_at_loc_button, to_loc_button]])
        await message.reply_text('cosa vuoi fare con questa posizione?', reply_markup=keyboard)

        print(message)

    # if context.chat_data.get('action') == 'stopsnearme':
    #     user = update.message.from_user
    #     user_location = update.message.location
    #
    #     # Puoi utilizzare user_location.latitude e user_location.longitude per ottenere le coordinate
    #     latitude = user_location.latitude
    #     longitude = user_location.longitude
    #
    #     print(f"({latitude}, {longitude})")
    #
    # # Puoi fare qualcosa con le coordinate, come salvarle nel database o utilizzarle per altre operazioni
    #
    # # Invia un messaggio di conferma all'utente
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=f"Grazie {user.first_name}! La tua posizione è stata registrata."
    #     )
    #
    #     coordinates = (latitude, longitude)


def get_alt_stops(codice_fermata):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT alt_id, alt_name
        FROM alt_stops
        WHERE stop_id = ?
    ''', (codice_fermata,))
    risultati = cursor.fetchall()

    alt_stops = []
    for risultato in risultati:
        alt_id = risultato[0]
        alt_name = risultato[1]
        alt_stops.append((alt_id, alt_name))

    conn.close()

    return alt_stops


# Funzione per interrogare il database e ottenere tutte le caratteristiche della fermata dato il codice
def get_stop_details(codice_fermata):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT stops.id, stops.name, stops.latitude, stops.longitude
        FROM stops
        WHERE stops.id = ? 
    ''', (codice_fermata,))
    risultati = cursor.fetchall()

    if risultati:
        caratteristiche = {}
        for risultato in risultati:
            stop_id = risultato[0]
            nome = risultato[1]
            latitude = risultato[2]
            longitude = risultato[3]

            alt_stops = get_alt_stops(stop_id)

            caratteristiche = {
                "id": stop_id,
                "name": nome,
                "latitude": latitude,
                "longitude": longitude,
                "alt_stops": alt_stops
            }
            print('caratteristiche fermata:')
            print(caratteristiche)
        conn.close()
        return caratteristiche
    else:
        conn.close()
        return None


def format_stop_details(caratteristiche):
    if not caratteristiche:
        return "Fermata non trovata"
    print(caratteristiche)
    formatted_string = ""
    formatted_string += f"ID: {caratteristiche['id']}\n"
    formatted_string += f"Nome: {caratteristiche['name']}\n"
    # formatted_string += f"Coordinates:\n{caratteristiche['latitude']}, {caratteristiche['longitude']}\n"

    alt_stops = caratteristiche['alt_stops']
    if alt_stops:
        formatted_string += "ID e nomi alternativi:\n"
        for alt_stop in alt_stops:
            formatted_string += f"{alt_stop[0]}   {alt_stop[1]}\n"

    return formatted_string.strip()

def get_stop_lat_lon_string(caratteristiche):
    if not caratteristiche:
        return "Fermata non trovata"
    return f"{caratteristiche['latitude']}, {caratteristiche['longitude']}"

# Funzione per ottenere i pulsanti da un oggetto reply_markup
def get_buttonKeyboard_from_reply_markup(reply_markup):
    if reply_markup is not None and isinstance(reply_markup, InlineKeyboardMarkup):
        inline_keyboard = reply_markup.inline_keyboard
        buttons = [list(row) for row in inline_keyboard]
        return buttons
    else:
        return None


def ricerca_trip_per_fermata_data_tempo(stop_id, date, start_time, end_time):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Controllo se l'intervallo di tempo supera la mezzanotte
    if start_time > end_time:
        # Prima query: intervallo di tempo fino a mezzanotte
        cursor.execute('''
            SELECT trips.code, trips.line, trips.headsign, trip_stops_times.time, stops.name, trip_stops_times.stop_id
            FROM trips
            INNER JOIN trip_dates ON trips.code = trip_dates.trip_id
            INNER JOIN trip_stops_times ON trips.code = trip_stops_times.trip_id
            INNER JOIN stops ON trip_stops_times.stop_id = stops.id
            WHERE trip_dates.date = ? 
            AND trip_stops_times.stop_id = ? 
            AND trip_stops_times.time >= ? 
            AND trip_stops_times.time <= '23:59:59'
            ORDER BY trip_stops_times.time
        ''', (date, stop_id, start_time))

        results = cursor.fetchall()

        # Seconda query: intervallo di tempo dal giorno successivo
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        next_date = next_day.strftime('%Y-%m-%d')

        cursor.execute('''
            SELECT trips.code, trips.line, trips.headsign, trip_stops_times.time, stops.name, trip_stops_times.stop_id
            FROM trips
            INNER JOIN trip_dates ON trips.code = trip_dates.trip_id
            INNER JOIN trip_stops_times ON trips.code = trip_stops_times.trip_id
            INNER JOIN stops ON trip_stops_times.stop_id = stops.id
            WHERE trip_dates.date = ? 
            AND trip_stops_times.stop_id = ? 
            AND trip_stops_times.time >= '00:00:00'
            AND trip_stops_times.time <= ?
            ORDER BY trip_stops_times.time
        ''', (next_date, stop_id, end_time))

        results += cursor.fetchall()
    else:
        # Unica query: intervallo di tempo all'interno dello stesso giorno
        cursor.execute('''
            SELECT trips.code, trips.line, trips.headsign, trip_stops_times.time, stops.name, trip_stops_times.stop_id
            FROM trips
            INNER JOIN trip_dates ON trips.code = trip_dates.trip_id
            INNER JOIN trip_stops_times ON trips.code = trip_stops_times.trip_id
            INNER JOIN stops ON trip_stops_times.stop_id = stops.id
            WHERE trip_dates.date = ? 
            AND trip_stops_times.stop_id = ? 
            AND trip_stops_times.time BETWEEN ? AND ?
            ORDER BY trip_stops_times.time
        ''', (date, stop_id, start_time, end_time))

        results = cursor.fetchall()

    conn.close()

    # Creazione del dizionario dei risultati
    results_dict = {
        'trips': [],
        'stop_name': None,
        'stop_id': None,
        'start_time': None,
        'end_time': None
    }

    for result in results:
        trip_code = result[0]
        line = result[1]
        headsign = result[2]
        time = result[3]

        results_dict['trips'].append({
            'trip_code': trip_code,
            'line': line,
            'headsign': headsign,
            'time': time
        })

    if results_dict['stop_name'] is None:
        results_dict['stop_name'] = ricerca_stop_per_id(stop_id).name
        results_dict['stop_id'] = stop_id
        results_dict['start_time'] = start_time
        results_dict['end_time'] = end_time

    return results_dict

def new_button(text, query_descr, query_args):
    callback = ''
    if len(query_descr) == 0:
        print("ERROR in button, no query descr")
        return
    if len(query_args) == 0:
        print("ERROR in button, no query args")
        return
    if len(query_descr) >= 1:
        for i, descr in enumerate(query_descr):
            if i == 0:
                callback += f"{descr}"
            else:
                callback += f"{callback_command_divider}{descr}"
    callback += f"{callback_main_divider}"
    if len(query_args) >= 1:
        for i, arg in enumerate(query_args):
            if i == 0:
                callback += f"{arg}"
            else:
                callback += f"{callback_arg_divider}{arg}"

    return InlineKeyboardButton(text, callback_data=callback)

def new_stop_button(stop_id):
    stop = ricerca_stop_per_id(stop_id)
    return new_button(f"{stop.id}  {stop.name}", [f"stop"], [stop_id])


def format_trip_results(results_dict):
    arrow_up = "\u2B06"
    arrow_down = "\u2B07"
    if not results_dict['trips']:
        formatted_string = f"Fermata {results_dict['stop_id']}, {results_dict['stop_name']}\n" \
                           f"Nessun bus in transito dalle {results_dict['start_time']} alle {results_dict['end_time']}\n\n"
        return formatted_string

    formatted_string = f"Fermata {results_dict['stop_id']}, {results_dict['stop_name']}\n" \
                       f"Bus in transito dalle {results_dict['start_time']} alle {results_dict['end_time']}\n\n"
    now = Utility.get_now_at_timezone_str()
    stamped_now_line = False

    for i, trip in enumerate(results_dict['trips']):
        trip_code = trip['trip_code']
        line = trip['line']
        headsign = trip['headsign']
        time = trip['time']

        if time > now and not stamped_now_line:
            if i > 0:
                formatted_string += f"{arrow_up}{arrow_up}  PASSATI\n"
                formatted_string += f"{now}\n"
                formatted_string += f"{arrow_down}{arrow_down}  IN ARRIVO\n"

            stamped_now_line = True

        formatted_string += f"{time[:-3]}  {line}  {headsign}\n"

    return formatted_string.strip()


def ricerca_linee_per_fermata(stop_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT trips.line, trips.headsign
        FROM trips
        INNER JOIN trip_stops_times ON trips.code = trip_stops_times.trip_id
        WHERE trip_stops_times.stop_id = ?
    ''', (stop_id,))

    results = cursor.fetchall()

    conn.close()

    return results


def ricerca_stop_per_id(id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Cerca nella tabella "stops"
    cursor.execute('SELECT * FROM stops WHERE id = ?', (id,))
    result = cursor.fetchone()

    if result:
        conn.close()
        return Fermata(result[0], result[1], result[2], result[3])

    # Cerca nella tabella "alt_stops"
    cursor.execute('''
        SELECT stops.*
        FROM stops
        INNER JOIN alt_stops ON stops.id = alt_stops.stop_id
        WHERE alt_stops.alt_id = ?
    ''', (id,))
    result = cursor.fetchone()

    conn.close()
    if len(result) > 0:
        return Fermata(result[0], result[1], result[2], result[3])
    else:
        print(f"no stops found for {id}")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('test')

    print(Utility.strings_similarity_ratio('montkuc', 'biagio di montluc'))

    print('running tests...')

    print('finished tests')

    # print('arrivi a 9@s0067')
    # for element in ricerca_trip_per_fermata_data_tempo('9@s0067', '2023-05-22', '21:53:40', '23:43:40'):
    #     print(element)
    # print(ricerca_trip_per_fermata_data_tempo('9@s0067', '2023-05-22', '21:53:40', '14:43:40'))
    #
    # print('linee in 9@s0067')
    # for element in ricerca_linee_per_fermata('9@s0067'):
    #     print(element)
    #
    # print(f"fermata corrispondente a 8@0067: {ricerca_stop_per_id('8@0067')}")
    #
    # print('hai cercato: montluc')
    # for element in search_db_for('montluc'):
    #     print(element.to_text())
    #
    # print('hai cercato: 0067')
    # for element in search_db_for('0067'):
    #     print(element.to_text())

    # with open('zone/linee regionali/stops.txt', 'r') as file:
    #     for stop1 in fermate:
    #         for stop2 in fermate:
    #             # print(f"{stop.id}   {regional_stop.id}")
    #             dist = stop1.dist_to(stop2)
    #             if not (stop1.id == stop2.id) and stop1.id[-3:] == stop2.id[-3:] and dist < 50:
    #                 print(f"{stop1.id}, {stop1.name}, {stop2.id}, {stop2.name}")
    #             # else:
    #             #     if not (stop1.id == stop2.id) and difflib.SequenceMatcher(None, stop1.name,
    #             #                                                               stop2.name).ratio() > 0.8 and dist < 50:
    #             #         print(f"{stop1.id}, {stop1.name}, {stop2.id}, {stop2.name}, name")

    # for id1 in regional_stops_dict:
    #     for id2 in stops_dict.items():
    #         stop1 = regional_stops_dict[id1]
    #         stop2 = stops_dict[id2]
    #         dist = stop1.dist_to(stop2)
    #         if not (stop1.id == stop2.id) and stop1.id[-3:] == stop2.id[-3:] and dist < 50:
    #             print(f"{stop1.id}, {stop1.name}, {stop2.id}, {stop2.name}")
    # print('tests finished.')

    # temp_stop = stop_by_id('s0067')
    # print('making request..')
    # print(temp_stop.to_text())
    # # print(trips_dict)
    # temp = Utility.sort_arrivals(temp_stop.arrivals_in_datetime_range(datetime.datetime(2023, 5, 8, 18, 0), 500))
    # print(Utility.arrivals_to_text(temp))

    # print(Utility.arrivals_to_text(temp_stop.arrivals))

    # print(temp_stop.passing_lines())

    # for stop in fermate:
    #     print(stop.id)

    # for trip in trips:
    #     if trip.line == 's10':
    #         print(trip.to_text())


def search_stops_by_similarity(input_string):
    processed = input_string.lower().strip()
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    stop_results = []

    # Ricerca di tutte le fermate nel database
    cursor.execute('SELECT * FROM stops')
    all_stops = cursor.fetchall()

    # Filtraggio delle fermate in base alla similarità dei nomi e dei nomi alternativi
    for stop in all_stops:
        name_similarity = Utility.strings_similarity_ratio(processed, stop[1].lower())
        alt_name_similarity = 0
        cursor.execute('SELECT alt_name FROM alt_stops WHERE stop_id = ?', (stop[0],))
        alt_names = [alt_name[0] for alt_name in cursor.fetchall()]
        for alt_name in alt_names:
            alt_name_similarity = max(alt_name_similarity,
                                      Utility.strings_similarity_ratio(processed, alt_name.lower()))
        if name_similarity > SIMILARITY_THRESHOLD or alt_name_similarity > SIMILARITY_THRESHOLD or \
                Utility.do_strings_contain_similar_word(processed, stop[1].lower(), SIMILARITY_THRESHOLD):
            stop_instance = Fermata(stop[0], stop[1], stop[2], stop[3])
            stop_results.append(stop_instance)

    # Eliminazione dei duplicati in base all'id della fermata
    unique_stops = {stop.id: stop for stop in stop_results}.values()

    conn.close()

    return list(unique_stops)


def search_db_for(text: str) -> []:
    processed = text.lower().strip()

    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    stop_results = []

    # Ricerca nelle stops per corrispondenze nel nome o negli alt_names
    cursor.execute('SELECT * FROM stops WHERE lower(name) LIKE ? '
                   'OR EXISTS (SELECT 1 FROM alt_stops WHERE stops.id = alt_stops.stop_id AND lower(alt_name) LIKE ?) '
                   'OR EXISTS (SELECT 1 FROM alt_stops WHERE stops.id = alt_stops.stop_id AND lower(alt_id) LIKE ?) '
                   'OR lower(id) LIKE ?',
                   ('%' + processed + '%', '%' + processed + '%', '%' + processed + '%', '%' + processed + '%'))
    stop_rows = cursor.fetchall()

    for row in stop_rows:
        stop = Fermata(row[0], row[1], row[2], row[3])
        stop_results.append(stop)

    if len(stop_results) == 0:
        # # Esegui un'altra query basata sulla similarità
        # cursor.execute('SELECT name FROM stops')
        # all_stops = [row[0] for row in cursor.fetchall()]
        # similar_stops = Utility.get_sorted_similar_strings(all_stops, processed, 0.7)
        # for similar_stop in similar_stops:
        #     cursor.execute('SELECT * FROM stops WHERE lower(name) = ?', (similar_stop.lower(),))
        #     row = cursor.fetchone()
        #     stop = Fermata(row[0], row[1], row[2], row[3])
        #     stop_results.append(stop)
        for stop in search_stops_by_similarity(processed):
            stop_results.append(stop)

    if len(stop_results) == 0:
        print('No stops found\n')

    conn.close()

    combined_search_results = stop_results
    return combined_search_results


def search_for(text: str) -> []:
    processed: str = text.lower().strip()
    responses = []
    found_valid_response = False
    matches = 0
    lastMatchIndex = 0
    stop_results = []
    line_results = []
    print(f"searching for {processed}")
    if processed.replace('@', '').isalnum() and len(processed.split(' ')) == 1 and not processed.isalpha():
        for id in common.stops_dict.keys():
            stop = common.stops_dict[id]
            if processed in id and not (stop in stop_results):
                # responses.append(f"{stop.to_text()}")
                stop_results.append(stop)
            elif len(stop.alt_ids()) > 0:
                if any(processed in s for s in stop.alt_ids()) and not (stop in stop_results):
                    stop_results.append(stop)
        for line_num in common.lines_dict.keys():
            if len(processed) >= 2 and processed in line_num:
                line = common.lines_dict[line_num]
                # responses.append(f"{line.to_text()}")
                line_results.append(line)
    else:
        for id in common.stops_dict.keys():
            stop = common.stops_dict[id]
            if processed in stop.name:
                stop_results.append(stop)
            elif len(stop.alt_names) > 0:
                if any(processed in s for s in stop.alt_names) and not (stop in stop_results):
                    stop_results.append(stop)
            elif Utility.strings_similarity_ratio(stop.name, processed) > 0.7 and not (stop in stop_results):
                stop_results.append(stop)

    print(f"found {len(stop_results)} stops and {len(line_results)} lines")
    combined_search_results = stop_results + line_results
    if len(combined_search_results) == 0:
        print('La ricerca non ha prodotto risultati')
    return combined_search_results

    #
    #
    #
    #
    #
    #
    #
    #
    # if 'ciao' in processed:
    #     response = 'ciao a te'
    #     found_valid_response = True
    # else:
    #     for i in range(len(fermate)):
    #         id_fermata = fermate[i].id
    #         if id_fermata == processed:
    #             found_valid_response = True
    #             responses.append(f"{fermate[i].id}   {fermate[i].name}")
    #             matches += 1
    #             lastMatchIndex = i
    #             print('BOT: found id')
    #     if not found_valid_response:
    #         for i in range(len(fermate)):
    #             id_fermata = fermate[i].id
    #             if id_fermata in processed or processed in id_fermata:
    #                 found_valid_response = True
    #                 responses.append(f"{fermate[i].id}   {fermate[i].name}")
    #                 matches += 1
    #                 lastMatchIndex = i
    #                 print('BOT: found id')
    #     print(len(responses))
    #     if not found_valid_response:
    #         for i in range(len(fermate)):
    #             nome_fermata = fermate[i].name
    #             if processed == nome_fermata:
    #                 found_valid_response = True
    #                 responses.append(f'{fermate[i].id}   {fermate[i].name}')
    #                 matches += 1
    #                 lastMatchIndex = i
    #                 print('BOT: found name')
    #     if not found_valid_response:
    #         for i in range(len(fermate)):
    #             nome_fermata = fermate[i].name
    #             if processed in nome_fermata:
    #                 found_valid_response = True
    #                 responses.append(f'{fermate[i].id}   {fermate[i].name}')
    #                 matches += 1
    #                 lastMatchIndex = i
    #                 print('BOT: found name')
    #
    #     # if matches == 0:
    #     #     print('BOT: try id')
    #     #     ids = Fermata.lista_nomi_fermate(fermate)
    #     #     strMatches = difflib.get_close_matches(processed, ids, 20, 0.9)
    #     #     if len(strMatches) > 0:
    #     #         found_valid_response = True
    #     #         for match in strMatches:
    #     #             response += match
    #     #     matches = len(strMatches)
    #     print(len(responses))
    #     if matches != 1:
    #         print('BOT: try name')
    #         names = []
    #         for stop in fermate:
    #             names.append(stop.name)
    #         matched_names = list(set(difflib.get_close_matches(processed, names, 15, 0.8)))
    #         sorted_matched_names = sorted(matched_names,
    #                                       key=lambda x: difflib.SequenceMatcher(None, processed, x).ratio(),
    #                                       reverse=True)
    #         print(len(f"matched names {sorted_matched_names}"))
    #         result_stops = []
    #         for name in sorted_matched_names:
    #             matched_stops = stops_by_name(name)
    #             if len(matched_stops) > 1:
    #                 for stop in matched_stops:
    #                     result_stops.append(stop)
    #         if len(result_stops) > 0:
    #             found_valid_response = True
    #             result_stops = list(set(result_stops))
    #             responses.append(result_stops)
    #             matches += len(result_stops)
    #
    #         # if len(strMatches) > 0:
    #         #     found_valid_response = True
    #         #     for match in strMatches:
    #         #         response += f"{match} \n"
    #         # matches = len(strMatches)
    #     print(matches)
    # print(len(responses))
    # if matches == 1:  # se c'è un solo match fai robe
    #     print("babbala")
    #     id_fermata = fermate[lastMatchIndex].id
    #     fermata = stops_dict[id_fermata]
    #     # responses.append(Utility.arrivals_to_brief_text(Utility.sort_arrivals(fermata.arrivals_in_minutes_range(60))))
    #
    # if found_valid_response:
    #     return responses
    # else:
    #     return 'non ho capito'


# def arrivals_near_pos(lat, lon, radius, time, delta_time):

# async def arrivals_near_user_command(update, context):
#     user_id = update.effective_user.id
#     if not (user_id in common.user_locations.keys()):
#         await update.message.reply_text(f"Per usare questa funzione ho bisogno che tu mi dia accesso alla posizione. "
#                                         f"Se non l'hai già fatto premi l'icona di condivisione, "
#                                         f"scegli 'posizione' e poi 'posizione in tempo reale', se invece l'hai "
#                                         f"già fatto riprova tra qualche secondo.")
#     else:
#         await user_location_time_check(update, update.message)
#         coordinates = common.user_locations[user_id]['location']
#         lat = coordinates[0]
#         lon = coordinates[1]
#         radius = default_search_radius
#         stops = get_stops_within_radius(lat, lon, radius)
#         widen_radius_button = InlineKeyboardButton(f"widen search radius",
#                                                    callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}"
#                                                                  f"{lon}{callback_arg_divider}{radius + default_search_radius_increment}")
#

async def stops_near_user_command(update, context):
    user_id = update.effective_user.id
    if not (user_id in common.user_locations.keys()):
        await update.message.reply_text(f"Per usare questa funzione ho bisogno che tu mi dia accesso alla posizione. "
                                        f"Se non l'hai già fatto premi l'icona di condivisione, "
                                        f"scegli 'posizione' e poi 'posizione in tempo reale', se invece l'hai "
                                        f"già fatto riprova tra qualche secondo.")
    else:
        await user_location_time_check(update, update.message)
        # time_since_update = datetime.now() - common.user_locations[user_id]['update_time']
        # print(f"time since update {time_since_update}")
        # if time_since_update > timedelta(minutes=2):
        #     await update.message.reply_text(f"La tua posizione non viene aggiornata da almeno {int(time_since_update.total_seconds() // 60)} minuti, condividi nuovamente la tua posizione per risultati più accurati")
        coordinates = common.user_locations[user_id]['location']
        lat = coordinates[0]
        lon = coordinates[1]
        radius = default_search_radius
        stops = get_stops_within_radius(lat, lon, radius)
        widen_radius_button = InlineKeyboardButton(f"widen search radius",
                                                   callback_data=f"widenAtLatLonRadius{callback_main_divider}{lat}{callback_arg_divider}{lon}{callback_arg_divider}{radius + default_search_radius_increment}")
        if len(stops) == 0:
            await respond_to_stops(update, update.message, stops,
                                   f"Non ho trovato fermate entro {radius} metri dalla tua posizione:",
                                   [widen_radius_button], False)
        else:
            await respond_to_stops(update, update.message, stops, f"Fermate entro {radius} metri dalla tua posizione:",
                                   [widen_radius_button], False)
        # await update.message.reply_text(f"//cerca le fermate vicino a {location}")

async def show_favorites_command(update, context):
    user_id = update.effective_user.id
    fav_ids = Utility.get_fav_stop_ids(user_id)
    fav_stops = []
    for fav_id in fav_ids:
        fav_stops.append(ricerca_stop_per_id(fav_id))

    dati_id = str(uuid.uuid4())
    common.data[dati_id] = fav_stops

    if await has_user_shared_location(update, update.message):
        lat = common.user_locations[update.effective_user.id]['location'][0]
        lon = common.user_locations[update.effective_user.id]['location'][1]
        fav_stops = Utility.sort_stops_by_dist_to(fav_stops, lat, lon)

    buttons = [[]]

    # sort_by_name_button = InlineKeyboardButton(f"sort by name", callback_data=f"sortAlpha{callback_main_divider}{dati_id}")
    sort_by_name_button = new_button(f"sortByName", [f"sortAlpha"], [dati_id])
    sort_by_position_button = new_button(f"sortByPos", [f"sortGeo"], [dati_id])
    buttons.append([sort_by_name_button, sort_by_position_button])

    await show_fav_stops(fav_stops, buttons, update.message, user_id)
        # await respond_to_found_stops(update, message, stops_to_show, text, search_str)


    # for stop in fav_stops:
    #     buttons.append([InlineKeyboardButton(f"{stop.to_text()}", callback_data=f"stop{callback_main_divider}{stop.id}")])
    # await update.message.reply_text(f"Fermate preferite:", reply_markup=InlineKeyboardMarkup(buttons))



    # await respond_to_stops(update, update.message, fav_stops, f"Fermate preferite:", [], False)

async def show_fav_stops(stops, buttons, message, user_id):
    if len(stops) > default_num_of_stops_to_show_on_search:
        stops_to_show = stops[:default_num_of_stops_to_show_on_search]
        remaining_stops = stops[default_num_of_stops_to_show_on_search:]
        for stop in stops_to_show:
            # remove_from_fav_button = new_button(f"X", [f"stop", f"removeFav"], [user_id, stop.id])
            buttons.append(
                [new_stop_button(stop.id)])
        if len(remaining_stops) > 0:
            dati_id = str(uuid.uuid4())
            common.data[dati_id] = (".", remaining_stops)
            more_stops_button = new_button("...", [f"moreStops"], [dati_id])
            buttons.append([more_stops_button])
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(f"Fermate preferite:", reply_markup=keyboard)
    else:
        for stop in stops:
            buttons.append(
                [new_stop_button(stop.id)])
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(f"Fermate preferite:", reply_markup=keyboard)

async def user_location_time_check(update, message):
    user_id = update.effective_user.id
    if user_id in common.user_locations.keys():
        time_since_update = Utility.get_now_at_timezone() - common.user_locations[user_id]['update_time']
    else:
        print('no updates for this user id')
        return
    print(f"time since update {time_since_update}")
    if time_since_update > timedelta(minutes=2):
        await update.get_bot().sendMessage(chat_id=message.chat_id, text=f"La tua posizione non viene aggiornata da "
                                                                         f"almeno {int(time_since_update.total_seconds() // 60)} "
                                                                         f"minuti, condividi nuovamente la tua posizione per risultati più accurati")


async def has_user_shared_location(update, message):
    user_id = update.effective_user.id
    if user_id in common.user_locations.keys():
        return True
    else:
        return False


async def display_search_results(update, search_str, search_res):
    if len(search_res) > 100:
        await update.message.reply_text(f"Hai cercato '{search_str}', ma non ho capito. Prova ad essere più specifico.")
    elif len(search_res) == 0:
        await update.message.reply_text(
            f"Hai cercato '{search_str}', ma non ho capito.")
    else:
        found_stops = []
        found_lines = []
        for object in search_res:
            if isinstance(object, Fermata):
                found_stops.append(object)
            if isinstance(object, Line):
                found_lines.append(object)
        for stop in found_stops:
            print(stop.to_text())
        if update.effective_user.id in common.user_locations.keys():
            lat = common.user_locations[update.effective_user.id]['location'][0]
            lon = common.user_locations[update.effective_user.id]['location'][1]
            found_stops = Utility.sort_stops_by_dist_to(found_stops, lat, lon)
        else:
            found_stops = Utility.sort_stops_by_name_similarity(found_stops, search_str)
        await respond_to_found_stops(update, update.message, found_stops, f"Hai cercato '{search_str}'", search_str)


async def respond_to_found_stops(update, message, stops, text, search_str):
    # stops = input_stops[::-1]
    if len(stops) > default_num_of_stops_to_show_on_search:
        ids = ''
        stops_to_show = stops[:default_num_of_stops_to_show_on_search]
        remaining_stops = stops[default_num_of_stops_to_show_on_search:]
        buttons = []
        for stop in stops_to_show:
            buttons.append(
                [InlineKeyboardButton(f"{stop.to_text()}", callback_data=f"stop{callback_main_divider}{stop.id}")])
        if len(remaining_stops) > 0:
            # for stop in remaining_stops:
            #     ids += f"{stop.id};"
            # ids = ids.strip()[:-1]
            # print(f"moreStops_{ids}")
            dati_id = str(uuid.uuid4())
            common.data[dati_id] = (text, remaining_stops)
            more_stops_button = InlineKeyboardButton("...", callback_data=f"moreStops{callback_main_divider}{dati_id}")
            buttons.append([more_stops_button])
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(text, reply_markup=keyboard)
    else:
        buttons = []
        for stop in stops:
            buttons.append(
                [InlineKeyboardButton(f"{stop.to_text()}", callback_data=f"stop{callback_main_divider}{stop.id}")])
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(text, reply_markup=keyboard)
        # await respond_to_found_stops(update, message, stops_to_show, text, search_str)


async def respond_to_stops(update, message, stops, text, buttons_to_add, should_edit_latest_message):

    #///////////////////////////////////////////////////////////////
    num_of_stops_to_show = 0
    if should_edit_latest_message:
        num_of_stops_shown = len(message.reply_markup.inline_keyboard)
        num_of_stops_to_show = num_of_stops_shown + default_num_of_stops_to_show_on_search
    else:
        num_of_stops_to_show = default_num_of_stops_to_show_on_search
    if len(stops) > num_of_stops_to_show:
        remaining_stops_ids = ''
        stops_to_show = []
        stops_to_show = stops[:num_of_stops_to_show]
        remaining_stops = stops[num_of_stops_to_show:]
        if len(remaining_stops) > 0:
            # print(f"moreStops_{remaining_stops_ids}")
            dati_id = str(uuid.uuid4())
            common.data[dati_id] = (text, remaining_stops, buttons_to_add)
            more_stops_button = InlineKeyboardButton("...", callback_data=f"moreStops{callback_main_divider}{dati_id}")
            await respond_to_stops(update, message, stops_to_show, text, [more_stops_button], True)
        else:
            await respond_to_stops(update, message, stops_to_show, text, [], True)

        # OLD
        # await message.reply_text(text=f"{stops_to_text(stops)}")
        # OLD
    # if should_edit_latest_message:
    #     stops_shown = len(message.reply_markup.inline_keyboard)
    #     stops_to_show = stops_shown
    elif len(stops) > 1:
        buttons = [[]]
        for stop in stops:
            buttons.append(
                [InlineKeyboardButton(f"{stop.to_text()}", callback_data=f"stop{callback_main_divider}{stop.id}")])

        # print(buttons)
        for button in buttons_to_add:
            buttons.append([button])
        keyboard = InlineKeyboardMarkup(buttons)
        print(f"edit {should_edit_latest_message}")
        if should_edit_latest_message:
            await message.edit_text(text=text, reply_markup=keyboard)
        else:
            await message.reply_text(text, reply_markup=keyboard)
    elif len(stops) == 1:
        # buttons = []
        # button1 = InlineKeyboardButton(f"{stops[0].to_text()}", callback_data=f"stop{callback_main_divider}{stops[0].id}")
        # # info_button = InlineKeyboardButton(f"info", callback_data=f"stop:info_{stops[0].id}")
        # stop_user_commands = InlineKeyboardButton(f"stop_commands", callback_data=f"stop{callback_command_divider}commands{callback_main_divider}{stops[0].id}")
        # arrivals_command = InlineKeyboardButton(f"arrivi", callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stops[0].id}{callback_arg_divider}0")
        # buttons.append([button1, stop_user_commands])
        # buttons.append([arrivals_command])
        # for button in buttons_to_add:
        #     buttons.append([button])
        # keyboard = InlineKeyboardMarkup(buttons)
        # if should_edit_latest_message:
        #     await message.edit_text(text=text, reply_markup=keyboard)
        # else:
        #     await message.reply_text(text=f"{text}",
        #                             reply_markup=keyboard)
        await show_arrivals(message, stops[0], 0, False)

        # await respond_to_stops(update, message, stops,f"{stops[0].to_text()}", [])
        # arrivi_text = format_trip_results(ricerca_trip_per_fermata_data_tempo(stops[0].id, Utility.get_current_date_str(), Utility.get_now_plus_deltamins(-10), Utility.get_now_plus_deltamins(default_time_range)))
        # print(arrivi_text)
        # # arrivals = Utility.sort_arrivals(stops[0].arrivals_in_minutes_range(10, default_time_range))
        # # arrivals_text = Utility.arrivals_to_brief_text(arrivals)
        # if len(arrivi_text) > 0:
        #     await message.reply_text(text=arrivi_text)
        # else:
        #     await message.reply_text(text=f"Mi spiace, non ho trovato arrivi a\n{stops[0].to_text()}")
    elif len(stops) == 0:
        buttons = [[]]
        for button in buttons_to_add:
            buttons.append([button])
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(text=f"{text}",
                                 reply_markup=keyboard)
    else:
        pass
    #//////////////////////////////////////////////////


async def show_arrivals(message, stop, delta_minutes, should_edit_latest_message):
    if should_edit_latest_message:
        arrivi_text = format_trip_results(ricerca_trip_per_fermata_data_tempo(stop.id, Utility.get_current_date_str(),
                                                                              Utility.get_now_plus_deltamins(
                                                                                  -15 + int(delta_minutes)),
                                                                              Utility.get_now_plus_deltamins(
                                                                                  default_time_range + int(
                                                                                      delta_minutes))))
        print(arrivi_text)
        if len(arrivi_text) > 0:
            buttons = [[]]
            old_buttons = get_buttonKeyboard_from_reply_markup(message.reply_markup)
            print(old_buttons)
            for old_row in old_buttons:
                row = []
                for button in old_row:
                    if button.text == '-30 min':
                        prima_button = InlineKeyboardButton('-30 min',
                                                            callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}"
                                                                          f"{callback_arg_divider}{int(delta_minutes) - 30}")
                        row.append(prima_button)
                    elif button.text == '+30 min':
                        dopo_button = InlineKeyboardButton('+30 min',
                                                           callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}"
                                                                         f"{stop.id}{callback_arg_divider}{int(delta_minutes) + 30}")
                        row.append(dopo_button)
                    else:
                        row.append(button)
                buttons.append(row)

            # prima_button = InlineKeyboardButton('-30 min',
            #                                     callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}{callback_arg_divider}{int(delta_minutes) - 30}")
            # # altro_button = InlineKeyboardButton('altro',
            # #                                     callback_data=f"stop{callback_command_divider}altro{callback_main_divider}{stop.id}")
            # dopo_button = InlineKeyboardButton('+30 min',
            #                                    callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}{callback_arg_divider}{int(delta_minutes) + 30}")
            # buttons.insert(0, [prima_button, dopo_button])
            await message.edit_text(text=arrivi_text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        arrivi_text = format_trip_results(ricerca_trip_per_fermata_data_tempo(stop.id, Utility.get_current_date_str(),
                                                                              Utility.get_now_plus_deltamins(
                                                                                  -15 + int(delta_minutes)),
                                                                              Utility.get_now_plus_deltamins(
                                                                                  default_time_range + int(
                                                                                      delta_minutes))))
        print(arrivi_text)
        # arrivals = Utility.sort_arrivals(stops[0].arrivals_in_minutes_range(10, default_time_range))
        # arrivals_text = Utility.arrivals_to_brief_text(arrivals)
        if len(arrivi_text) > 0:
            buttons = [[]]
            prima_button = InlineKeyboardButton('-30 min',
                                                callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}{callback_arg_divider}{int(delta_minutes) - 30}")
            altro_button = InlineKeyboardButton('altro',
                                                callback_data=f"stop{callback_command_divider}altro{callback_main_divider}{stop.id}")
            dopo_button = InlineKeyboardButton('+30 min',
                                               callback_data=f"stop{callback_command_divider}arrivals{callback_main_divider}{stop.id}{callback_arg_divider}{int(delta_minutes) + 30}")
            buttons.append([prima_button, altro_button, dopo_button])
            keyboard = InlineKeyboardMarkup(buttons)
            await message.reply_text(text=arrivi_text, reply_markup=keyboard)
        else:
            await message.reply_text(text=f"Mi spiace, non ho trovato arrivi a\n{stop.to_text()}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not Utility.check_user_id_exists(user_id):
        Utility.insert_user_id(user_id)
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(update.message.location)

    print(f'User id: "{user_id}", chat id: "{update.message.chat.id}" in {message_type}: "{text}"')

    if message_type == 'group':
        return
    else:
        search_res = search_db_for(text)
    print(len(search_res))

    await display_search_results(update, text, search_res)

    # print('Bot:', response)
    # if len(responses) == 1:
    #     button1 = InlineKeyboardButton(f"{responses[0]}", callback_data=f"stop_{responses[0]}")
    #     keyboard = InlineKeyboardMarkup([[button1]])
    #     await update.message.reply_text(text, reply_markup=keyboard)
    # else:
    #     if 10 > len(responses) > 1:
    #         buttons = [[]]
    #         print(responses)
    #         for response in responses:
    #             buttons.append([InlineKeyboardButton(f"{response}", callback_data=f"stop_{response}")])
    #         keyboard = InlineKeyboardMarkup(buttons)
    #
    #         # print(buttons)
    #         await update.message.reply_text(text, reply_markup=keyboard)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update}\n caused error {context.error}\n')
    traceback.print_exc()


def stop_by_id(id):
    for stop in common.stops:
        if id == stop.id:
            return stop
        for alt_id_name in stop.alt_ids_names:
            # print(alt_id_name)
            if id == alt_id_name[0]:
                return stop
    if id in common.stops_dict.keys():
        return common.stops_dict[id]
    print(f'error in stop_by_id, no stop found. stop: {id}')
    return None


def trips_by_line(line):
    result = []
    for trip in common.trips:
        if line == trip.line:
            result.append(trip)
    return result


def stops_by_name(name):
    stops = []
    for stop in common.stops:
        if name == stop.name:
            stops.append(stop)
    return stops


def stops_to_text(stops):
    result = ''
    for stop in stops:
        result += f"{stop.id}   {stop.name}\n"
    return result


def clean_raw_stop_id(id):
    temp = id.replace('_600', '').split('@')
    result = ''
    if len(temp) > 1:
        result = temp[1]
    else:
        result = temp[0]
    return result.lower()


def file_to_righe_divise(s):
    righe = s.splitlines()
    righe.pop(0)
    righe_divise: list[list[str]] = []
    for row in righe:
        row_parts = row.split('","')
        for i in range(len(row_parts)):
            row_parts[i] = row_parts[i].replace('"', '')
            row_parts[i] = row_parts[i].lower().strip()
        righe_divise.append(row_parts)
    return righe_divise


def save_data_thread(file_path, data):
    save_thread = threading.Thread(target=Utility.save_data, args=(file_path, data))
    tempo_inizio = time.time()
    save_thread.start()
    while save_thread.is_alive():
        tempo_passato = int(time.time() - tempo_inizio)
        print(f'Saving... Tempo trascorso: {tempo_passato} secondi')
        time.sleep(2)  # Pausa di 1 secondo prima di effettuare il controllo successivo


# def handle_callback(update, context: CallbackContext):
#     query = update.callback_query
#     action = query.data
#     print(f'action {action}')
#     # if action == 'get_arrivals_action':
#     #     print(query.data)
def update_dicts():
    common.stops_dict.update({stop.id: stop for stop in common.stops})
    common.trips_dict.update({trip.code: trip for trip in common.trips})
    common.lines_dict.update({line.number: line for line in common.lines})


def crea_tabelle():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stops (
            id TEXT PRIMARY KEY,
            name TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alt_stops (
            stop_id TEXT,
            alt_id TEXT,
            alt_name TEXT,
            FOREIGN KEY (stop_id) REFERENCES stops (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            code TEXT PRIMARY KEY,
            route_id TEXT,
            line TEXT,
            headsign TEXT,
            service_id TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arrivals (
            id INTEGER PRIMARY KEY,
            stop_id TEXT,
            datetime TEXT,
            trip_id TEXT,
            FOREIGN KEY (stop_id) REFERENCES stops (id),
            FOREIGN KEY (trip_id) REFERENCES trips (code)
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_dates (
                id INTEGER PRIMARY KEY,
                trip_id TEXT,
                date TEXT,
                FOREIGN KEY (trip_id) REFERENCES trips (code)
            )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_stops_times (
                id INTEGER PRIMARY KEY,
                trip_id TEXT,
                stop_id TEXT,
                time TEXT,
                FOREIGN KEY (trip_id) REFERENCES trips (code),
                FOREIGN KEY (stop_id) REFERENCES stops (id)
            )
        ''')
    conn.commit()
    conn.close()


# Funzione per inserire uno stop nel database
def inserisci_stop(stop):
    print(f"inserting stop: {stop.to_text()}")
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stops (id, name, latitude, longitude) VALUES (?, ?, ?, ?)',
                   (stop.id, stop.name, float(stop.latitude), float(stop.longitude)))

    # Inserisci gli alt_ids e gli alt_names nella tabella alt_stops
    if len(stop.alt_ids_names) > 0:
        for alt_id_name in stop.alt_ids_names:
            print(alt_id_name)
            cursor.execute('INSERT INTO alt_stops (stop_id, alt_id, alt_name) VALUES (?, ?, ?)',
                           (stop.id, alt_id_name[0], alt_id_name[1]))

    conn.commit()
    conn.close()


def inserisci_trip(trip):
    print(f"inserting trip: {trip.code}  {trip.line}  {trip.headsign}")
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO trips (code, route_id, line, headsign, service_id) VALUES (?, ?, ?, ?, ?)',
                   (trip.code, trip.route_id, trip.line, trip.headsign, trip.service_id))
    for date in trip.dates:
        print(f"inserting trip date: {trip.code}  {date}")
        cursor.execute('INSERT INTO trip_dates (trip_id, date) VALUES (?, ?)',
                       (trip.code, date.strftime('%Y-%m-%d')))
    for stopid_time in trip.stopsids_times:
        print(f"inserting trip time: {trip.code}  {stopid_time[1]}")
        cursor.execute('INSERT INTO trip_stops_times (trip_id, stop_id, time) VALUES (?, ?, ?)',
                       (trip.code, stopid_time[0], stopid_time[1].strftime('%H:%M:%S')))
    conn.commit()
    conn.close()


def inserisci_arrival(arrival):
    print(f"inserting arrival: {arrival.to_text()}")
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO arrivals (stop_id, datetime, trip_id) VALUES (?, ?, ?)',
                   (arrival.stop_id, arrival.time.strftime('%Y-%m-%d %H:%M:%S'), arrival.trip_id))

    conn.commit()
    conn.close()


def ottieni_nome_fermata(codice_fermata):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM stops WHERE id = ?', (codice_fermata,))
    risultato = cursor.fetchone()

    if risultato:
        nome_fermata = risultato[0]
        print("Il nome della fermata con codice", codice_fermata, "è:", nome_fermata)
    else:
        print("Fermata non trovata")

    conn.close()


def load_data_thread():
    data = Utility.load_data('data.pickle')
    if data:
        common.stops, common.trips, common.lines = data["liste"]
        common.regional_stops_dict = data["dizionari"]
        update_dicts()
        print('Operazione completata!')
    else:
        print('Data not available yet.')

def build_user_data_db():
    conn = sqlite3.connect('userData.db')  # Crea o connettiti a un database esistente
    cursor = conn.cursor()

    # Crea la tabella per memorizzare i codici utente
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_ids (
                user_id TEXT PRIMARY KEY
            )
        ''')

    # Crea la tabella per memorizzare le fermate preferite degli utenti
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_stops (
                user_id TEXT,
                favorite_stop_id TEXT,
                FOREIGN KEY (user_id) REFERENCES user_ids (user_id)
            )
        ''')

    # Esegui il commit delle modifiche e chiudi la connessione
    conn.commit()
    conn.close()


flask_app = Flask(__name__)
@flask_app.route("/")
def flask_main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main2())
    return "ma come cazzo si usa sto flask"
async def main2():

    app = Application.builder().token(TOKEN).build()
    # bot = app.bot
    webhook_url = "https://aPlanetaryCitizen.pythonanywhere.com/" + TOKEN
    # bot.setWebhook(webhook_url)

    if not os.path.isfile('bot.db'):
        start()
    if not os.path.isfile('userData.db'):
        build_user_data_db()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('test', test_command))
    app.add_handler(CommandHandler('stopsnearme', stops_near_user_command))
    app.add_handler(CommandHandler('showfavorites', show_favorites_command))
    # app.add_handler(CommandHandler('arrivalsHere', arrivals_near_user_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CallbackQueryHandler(button_command))
    app.add_handler(MessageHandler(filters.LOCATION, save_user_location))

    app.add_error_handler(error)

    # VA CREATA UNA "ENVIRONMENT VARIABLE" PER IL SECRET TOKEN PERCHE' NON E' IL CASO DI SCRIVERLA QUI,
    # PAROLE DELLA GUIDA DI PYTHON-TELEGRAM-BOT
    app.run_webhook(
        listen='0.0.0.0',
        port=8443,
        secret_token='DA_CAMBIARE_SECRET_TOKEN',
        key='private.key',
        cert='cert.pem',
        webhook_url=webhook_url
    )
    await asyncio.sleep(1)


def main():
    PORT = int(os.environ.get('PORT', '5000'))
    app = Application.builder().token(TOKEN).build()
    bot = app.bot
    bot.setWebhook("https://aPlanetaryCitizen.pythonanywhere.com/" + TOKEN)

    if not os.path.isfile('bot.db'):
        start()
    if not os.path.isfile('userData.db'):
        build_user_data_db()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('test', test_command))
    app.add_handler(CommandHandler('stopsnearme', stops_near_user_command))
    app.add_handler(CommandHandler('showfavorites', show_favorites_command))
    # app.add_handler(CommandHandler('arrivalsHere', arrivals_near_user_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CallbackQueryHandler(button_command))
    app.add_handler(MessageHandler(filters.LOCATION, save_user_location))

    app.add_error_handler(error)

    print('polling...')
    app.run_polling(poll_interval=1)

    # bot = Bot(app)
    # bot.deleteWebhook
    #
    # @flask_app.route('/')
    # def webhook



    # bot = Bot(app)
    # bot.deleteWebhook
    #
    # @flask_app.route('/')
    # def webhook




# if __name__ == '__main__':
#
#     main2()

    # app = Application.builder().token(TOKEN).build()
    #
    # # # BUONO
    # # if os.path.isfile('data.pickle'):
    # #     print('Data found.\nLoading data...')
    # #
    # #
    # #     tempo_inizio = time.time()  # Memorizza il tempo di inizio dell'operazione
    # #
    # #     load_thread = threading.Thread(target=load_data_thread)
    # #     load_thread.start()
    # #
    # #     while load_thread.is_alive():
    # #         tempo_passato = int(time.time() - tempo_inizio)
    # #         print(f'Waiting... Tempo trascorso: {tempo_passato} secondi')
    # #         time.sleep(2)  # Pausa di 1 secondo prima di effettuare il controllo successivo
    # #
    # #     load_thread.join()  # Attendere il completamento del thread di caricamento
    # # # ^^^^^^^^^^
    # # # BUONO
    #
    # # if os.path.isfile('data.pickle'):
    # #     print('Data found.\nLoading data...')
    # #     tempo_inizio = time.time()  # Memorizza il tempo di inizio dell'operazione
    # #
    # #     while True:
    # #         # if time.time() - tempo_inizio >= 10:  # Imposta il tempo massimo di attesa a 10 secondi
    # #         #     print('Tempo massimo di attesa raggiunto senza completare l\'operazione.')
    # #         #     break
    # #
    # #         data = Utility.load_data('data.pickle')
    # #         if data:
    # #             common.stops, common.trips, common.lines = data["liste"]
    # #             common.regional_stops_dict = data["dizionari"]
    # #             update_dicts()
    # #             print('Operazione completata!')
    # #             break
    # #         else:
    # #             print('Data not available yet. Waiting...')
    # #             sys.stdout.flush()
    # #             time.sleep(1)  # Pausa di 1 secondo prima di effettuare il controllo successivo
    # if not os.path.isfile('bot.db'):
    #     start()
    #
    # app.add_handler(CommandHandler('start', start_command))
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('test', test_command))
    # app.add_handler(CommandHandler('stopsnearme', stops_near_user_command))
    # # app.add_handler(CommandHandler('arrivalsHere', arrivals_near_user_command))
    #
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # app.add_handler(CallbackQueryHandler(button_command))
    # app.add_handler(MessageHandler(filters.LOCATION, save_user_location))
    #
    # app.add_error_handler(error)
    #
    # print('polling...')
    # app.run_polling(poll_interval=1)



import os
import json
import csv
import sys
import io
from shutil import copy2
import pandas as pd


def filter_json_food_files():
    foody = 'FOOD-SYSTEM'
    foodPath = 'FOOD'
    unfoodPath = 'UNFOOD'

    for filename in os.listdir(foody):
        copyFile = foody + '/' + filename
        with io.open(copyFile,'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            if len(data['foods']) > 0:
                copy2(copyFile, foodPath)
            elif len(data['foods']) == 0:
                copy2(copyFile, unfoodPath)

def convert_json_to_csv(index, fileName, csvFile):
    data = None
    with io.open(fileName,'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        if data is not None:
            with io.open(csvFile, 'a', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                id = index
                name = data['name']
                link = data['link']
                address = data['address']
                open_time = data['open_time']
                price_range = data['price_range']
                average_score = data['summary']['average_score']
                total_review = data['summary']['total_review']
                row = [str(id), name, link, address, open_time, price_range, average_score, total_review]
                writer.writerow(row)

def convert_values_json_to_csv(index, fileName, csvFile):
    data = None
    with io.open(fileName,'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        if data is not None:
            with io.open(csvFile, 'a', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                placeID = index
                values = data['values']
                quality = 0
                price = 0
                service = 0
                position = 0
                space = 0
                for value in values:
                    if str(value['label']) == 'Chất lượng':
                        quality = value['score']
                    if str(value['label']) == 'Giá cả':
                        price = value['score']
                    if str(value['label']) == 'Phục vụ':
                        service = value['score']
                    if str(value['label']) == 'Vị trí':
                        position = value['score']
                    if str(value['label']) == 'Không gian':
                        space = value['score']

                row = [str(placeID), quality, price, service, position, space]
                writer.writerow(row)

def convert_food_json_to_csv(index, fileName, csvFile):
    data = None
    with io.open(fileName,'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        if data is not None:
            with io.open(csvFile, 'a', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                placeID = index
                foods = data['foods']
                name = ''
                price = 0
                total_orders = 0
                for food in foods:
                    name = food['name']
                    price = food['price']
                    total_orders = food['total_orders']
                    row = [str(placeID), name, price, total_orders]
                    writer.writerow(row)
USERID = 0
def convert_user_json_to_csv(index, fileName, csvFile):
    data = None
    with io.open(fileName,'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        if data is not None:
            with io.open(csvFile, 'a', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                placeID = index
                userComments = data['user_comments']
                userID = 0
                name = ''
                rating = 0
                link = ''
                comment = ''
                uniqueUsers = []
                for user in userComments:
                    global USERID
                    USERID += 1
                    name = user['user']
                    link = user['link']
                    existedUser = find_user_in_list(uniqueUsers, link)
                    if existedUser is not None:
                        userID = existedUser['id']
                        print('....existed user....' + str(userID))
                    else:
                        uniqueUsers.append({'id':USERID, 'link':link})
                        userID = USERID

                    rating = user['score']
                    comment = user['comment']

                    row = [str(userID), str(placeID), name, link, str(rating), comment]
                    writer.writerow(row)

def find_user_in_list(userList, link):
    for user in userList:
        if user['link'] == link:
            return user
    return None

def combine_data_to_csv():
    placeCsvFile = 'DATA/places-raw.csv'
    ratingCsvFile = 'DATA/ratings-raw.csv'
    foodCsvFile = 'DATA/foods-raw.csv'
    userCsvFile = 'DATA/users-raw.csv'
    write_title_of_columns_to_place_csv_file(placeCsvFile)
    write_title_of_columns_to_rating_csv_file(ratingCsvFile)
    write_title_of_columns_to_foods_csv_file(foodCsvFile)
    write_title_of_columns_to_users_csv_file(userCsvFile)

    foody = 'FOODY'
    index = 0

    for filename in os.listdir(foody):
        index = index + 1
        jsonFile = foody + '/' + filename
        try:
            convert_json_to_csv(index, jsonFile, placeCsvFile)
            convert_values_json_to_csv(index, jsonFile, ratingCsvFile)
            convert_food_json_to_csv(index, jsonFile, foodCsvFile)
            convert_user_json_to_csv(index, jsonFile, userCsvFile)
        except:
            e = sys.exc_info()[0]
            print('error' + jsonFile)
            print(e)
            continue


def write_title_of_columns_to_place_csv_file(csvFile):
    with io.open(csvFile, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        columnTitleRow = ['placeID', 'name', 'link', 'address', 'open_time', 'price_range', 'average_score',
                          'total_review']
        writer.writerow(columnTitleRow)

def write_title_of_columns_to_rating_csv_file(csvFile):
    with io.open(csvFile, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        columnTitleRow = ['placeID', 'quality', 'price', 'service', 'position', 'space']
        writer.writerow(columnTitleRow)

def write_title_of_columns_to_foods_csv_file(csvFile):
    with io.open(csvFile, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        columnTitleRow = ['placeID', 'name', 'price', 'total_orders']
        writer.writerow(columnTitleRow)

def write_title_of_columns_to_users_csv_file(csvFile):
    with io.open(csvFile, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        columnTitleRow = ['userID', 'placeID', 'name', 'link', 'rating', 'comment']
        writer.writerow(columnTitleRow)

def test_write_unicode_file():
    fileName = 'test-unicode.txt'
    string = 'Ăn Vặt Quán Ngon'
    with io.open(fileName, 'w', encoding='utf-8') as outfile:
        outfile.write(string)

N_USERID = 2103
def convert_user_json_new_to_csv(csvFile):
    userCsvFile = 'DATA/users.csv'
    placeCsvFile = 'DATA/places.csv'

    places = pd.read_csv(placeCsvFile)
    users = pd.read_csv(userCsvFile)

    userDir = 'USER'
    for filename in os.listdir(userDir):
        userFile = userDir + '/' + filename
        with io.open(userFile, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            if data is not None:
                with io.open(csvFile, 'a', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    placeLink = data['link']
                    placeID = places[places['link'] == placeLink].placeID.values[0]
                    user_comments = data['user_comments']
                    for comment in user_comments:
                        name = comment['user']
                        userLink = comment['link']
                        if name == '' or userLink == '':
                            continue

                        rating = comment['score']
                        cm = comment['comment']
                        userID = users[users['link'] == userLink].userID
                        u_placeID = users[users['link'] == userLink].placeID

                        if u_placeID is not None and not u_placeID.empty:
                            pID = u_placeID.values[0]
                            if placeID == pID:
                                continue

                        if userID is not None and not userID.empty:
                            uID = userID.values[0]
                        else:
                            global N_USERID
                            N_USERID += 1
                            uID = N_USERID

                        row = [str(uID), str(placeID), name, userLink, str(rating), cm]
                        writer.writerow(row)

def append_users_data():
    userCsvFile = 'DATA/users-new-raw.csv'
    write_title_of_columns_to_users_csv_file(userCsvFile)
    convert_user_json_new_to_csv(userCsvFile)

# file = 'FOOD/Ăn Vặt Quán Ngon.json'
# convert_json_to_csv(1,file, 'anvat.csv')
# test_write_unicode_file()
# filter_json_food_files()
append_users_data()
# combine_data_to_csv()
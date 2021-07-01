#!/usr/bin/env python3
# coding: utf-8

import locale
import datetime as dt
import json

def get_weekday(year, month, day):
    locale.setlocale(locale.LC_ALL, '')
    s = f"{year}-{month}-{day}"
    date = dt.datetime.strptime(s, '%Y-%m-%d')
    youbi = date.strftime('%A')
    return youbi

def get_student_id_list(json_path):
    student_id_list = []
    with open(json_path, "r", encoding = "utf-8") as f:
        data_dic = json.load(f)
        dic_keys = data_dic.keys()
        student_id_list = list(dic_keys)
    return student_id_list

def get_student_data(json_path, student_id):
    with open(json_path, "r", encoding = "utf-8") as f:
        data_dic = json.load(f)
        if student_id in data_dic :
            student_data_dic = data_dic[student_id]
            sdd = student_data_dic
            your_name = sdd["name"]
            your_id = sdd["s_id"]
            your_status = sdd["In_room"]
            return your_name, your_id, your_status
        else :
            return None

def write_new_student_data(json_path, student_id, student_name):
    new_value = {"name": student_name, "s_id": student_id, "In_room": "false"}
    with open(json_path, "r", encoding = "utf-8") as f :
        update_dic = json.load(f)
        update_dic[student_id] = new_value

    with open(json_path, "wt", encoding = "utf-8") as f:
        json.dump(update_dic, f, ensure_ascii=False)


def write_student_data(json_path, student_id, key, new_value):
    with open(json_path, "r", encoding = "utf-8") as f :
        update_dic = json.load(f)
        update_dic[student_id][key] = new_value

    with open(json_path, "wt", encoding = "utf-8") as f:
        json.dump(update_dic, f, ensure_ascii=False)

def get_in_room_data(json_path):
    with open(json_path, "r", encoding = 'utf-8') as f :
        data_dic = json.load(f)
        dic_len = len(data_dic)
        return data_dic

def write_in_room_data(json_path, new_dic) :
    with open(json_path, "wt", encoding = "utf-8") as f :
        json.dump(new_dic, f, ensure_ascii = False)

def get_prefix(key) :
    split_list = key.split("/")
    prefix = split_list[0]
    key = split_list[1]

    return prefix, key
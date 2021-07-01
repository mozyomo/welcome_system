# !/usr/bin/env python3
# coding: utf-8

import PySimpleGUI as sg
import json
import datetime
from tools import get_weekday, get_student_data, get_prefix, write_student_data, get_in_room_data, write_in_room_data
import time

date = datetime.datetime.now()
year = date.year
month = date.month
today = date.day
hour = date.hour
minute = date.minute
day_of_the_week = get_weekday(year, month, today)
date_for_data = date.strftime("%Y/%m/%d %H:%M:%S")
ROOM_BOOL_LIST = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
CHECK_LIST = [1] * 12
ROOM_NAME_LIST = ["B326", "B328","B320(教授室)","B325(共同)", "B324", "遺203(植物室)",\
 "遺311(シーケンス室)", "B126(共焦点)", "島津分析室", "その他"] #名前表示用
PEOPLE_IN_ROOM_JSON = "./args/people_in_room.json"
STUDENT_DATA_JSON = "./args/test.json"

space = " " * 150



def appgui_for_await():
    sg.theme("Green")
    layout = [
        [sg.Text("学生証のバーコードをカードリーダーにかざしてください", font = ("游ゴシック, 15"))],
        [sg.Text("カードは、カードリーダーから15cm以上離してかざしてください", font = ("游ゴシック, 15"))],
        [sg.Text("学籍(職員)番号", font = ("游ゴシック", 20)), sg.InputText(font = ("游ゴシック", 20), size = (8,1))]
    ]

    window = sg.Window("入退室管理ツール", layout, no_titlebar = True, resizable = True,  grab_anywhere=True, return_keyboard_events=True)
    while True:
        event, values = window.read()
        your_id = values[0]
        if event == '\r' :
            return your_id


def appgui_for_new_commer(id):
    sg.theme("Green")
    layout = [
        [sg.Text("データを作成します！以下のフォームに入力してください", font = ("游ゴシック, 20"))],
        [sg.Text("お名前", font = ("游ゴシック, 20")), sg.InputText(font = ("游ゴシック", 20), size = (10,1), key = "name")],
        [sg.Text("学籍(職員番号): ", font = ("游ゴシック, 20")), sg.Text(id, font = ("游ゴシック, 20"))]
        [sg.Button("Push", key = "push")]
        ]

    window = sg.Window("入退室管理ツール", layout, no_titlebar = True, resizable = True)
    while True:
        event, values = window.read()
        if '\u3000' in values["name"]:
            values = values["name"].replace('\u3000', ' ')
            name = values
            verification = f"お名前は{name}でよろしいですか？"
            if event == "push":
                value = sg.popup_ok_cancel(verification)
                print(value)
                if value == "Cancel" or None:
                    value = sg.popup("もう一度やり直してください")
                    print(value)
                    continue
                else :
                    return id, name
        else :
            window.close()
            break


def appgui_for_enter(your_name, your_id, your_status) :
    hello_default = "おはようございます!!内容を確認して、Pushボタンを押してください."
    close_flag_1 = False
    enter_list = [your_name, your_id, date_for_data]
    room_people_dict = get_in_room_data(PEOPLE_IN_ROOM_JSON)
    room_people_dict[your_id] = your_name
    write_in_room_data(PEOPLE_IN_ROOM_JSON, room_people_dict)

    sg.theme("Green")
    layout = [
        [sg.Text("入室時間", font = ("游ゴシック", 20)), sg.InputText(default_text = year, font = ("游ゴシック", 20), size = (4,1)), sg.Text("年", font = ("游ゴシック", 20)),\
        sg.InputText(default_text = month, font = ("游ゴシック", 20), size = (2,1)), sg.Text("月", font = ("游ゴシック", 20)), sg.InputText(default_text = today, font = ("游ゴシック", 20), size = (2,1)), sg.Text("日", font = ("游ゴシック", 20), size = (2,1)),  sg.InputText(default_text = day_of_the_week, font = ("游ゴシック", 20), size = (6,1))],
        [sg.Text("現在時刻", font = ("游ゴシック", 20)),\
        sg.InputText(default_text = hour, font = ("游ゴシック", 20), size = (2,1)), sg.Text("時", font = ("游ゴシック", 20)),sg.InputText(default_text = minute, font = ("游ゴシック", 20), size = (2,1)), sg.Text("分", font = ("游ゴシック", 20))],
        [sg.Text("氏名", font = ("游ゴシック", 20)), sg.InputText(default_text = your_name, font = ("游ゴシック", 20), size = (8,1))],
        [sg.Text("学籍(職員)番号", font = ("游ゴシック", 20)), sg.InputText(default_text = your_id, font = ("游ゴシック", 20), size = (10,1))],
        [sg.Text("体温は37.5℃以下ですか？", font = ("游ゴシック", 20))],
        [sg.Button("はい", key = "temp/yes"), sg.Button("いいえ", key = "temp/no")],
        [sg.Button("Push", key = "push/push")],
        [sg.Text()],
        [sg.Text(hello_default, font = ("遊ゴシック", 10), key = "hello_default")]
    ]

    window = sg.Window("入退室管理ツール", layout, no_titlebar = True, resizable = True)
    while True:
        event, values = window.read()
        if event != None:
            prefix, event = get_prefix(event)
            if prefix == "temp" :
                temp_status = event
                enter_list.append(temp_status)
            elif prefix == "push" :
                write_student_data(STUDENT_DATA_JSON, your_id, "In_room", "true")
                hello = "ご協力ありがとうございます。今日も一日頑張りましょー!!"
                window['hello_default'].update(hello)
                close_flag_1 = True

            if close_flag_1 == True :
                time.sleep(1)
                window.close()
        else :
            window.close()
            break
    enter_tuple = tuple(enter_list)
    return enter_tuple


def appgui_for_exit(your_name, your_id, your_status):
    room_list_for_show = []
    room_bool_list =  ROOM_BOOL_LIST
    close_flag_2 = False
    exit_list = [your_name, your_id, date_for_data]
    last_one_flag = False
    global room_people_dict
    room_people_dict = get_in_room_data(PEOPLE_IN_ROOM_JSON)
    if your_id in room_people_dict :
        del room_people_dict[your_id]
        write_in_room_data(PEOPLE_IN_ROOM_JSON, room_people_dict)

    goodbye_default = "今日も一日お疲れさまでした!!内容を確認して、Pushボタンを押してください."
    sg.theme("Green")
    layout = [
        [sg.Text("退室時間", font = ("游ゴシック", 20)), sg.InputText(default_text = year, font = ("游ゴシック", 20), size = (4,1)), sg.Text("年", font = ("游ゴシック", 20)),\
        sg.InputText(default_text = month, font = ("游ゴシック", 20), size = (2,1)), sg.Text("月", font = ("游ゴシック", 20)), sg.InputText(default_text = today, font = ("游ゴシック", 20), size = (2,1)), sg.Text("日", font = ("游ゴシック", 20), size = (2,1)),  sg.InputText(default_text = day_of_the_week, font = ("游ゴシック", 20), size = (6,1))],
        [sg.Text("現在時刻", font = ("游ゴシック", 20)),\
        sg.InputText(default_text = hour, font = ("游ゴシック", 20), size = (2,1)), sg.Text("時", font = ("游ゴシック", 20)),sg.InputText(default_text = minute, font = ("游ゴシック", 20), size = (2,1)), sg.Text("分", font = ("游ゴシック", 20))],
        [sg.Text("氏名", font = ("游ゴシック", 20)), sg.InputText(default_text = your_name, font = ("游ゴシック", 20), size = (8,1))],
        [sg.Text("学籍(職員)番号", font = ("游ゴシック", 20)), sg.InputText(default_text = your_id, font = ("游ゴシック", 20), size = (10,1))],
        [sg.Text("滞在した部屋",font = ("游ゴシック", 20))],
        [sg.Button("B326", key = "room/0"),sg.Button("B328", key = "room/1"),sg.Button("B320(教授室)", key = "room/2"),sg.Button("B325(共同)", key = "room/3")],
        [sg.Button("B324", key = "room/4"),sg.Button("遺203(植物室)", key = "room/5"),sg.Button("遺311(シーケンス室)", key = "room/6"),sg.Button("B126(共焦点)", key = "room/7")],
        [sg.Button("島津分析室", key = "room/8"),sg.Button("その他", key = "room/9")],
        [sg.Button("Push", key = "push/push"), sg.Button("Clear", key = "clear/clear")],
        [sg.Image(filename = './documents/door.png')],[sg.Text(space, font = ("遊ゴシック", 10), key = "room_check")],
        [sg.Text(goodbye_default, font = ("遊ゴシック", 15), key = ("goodbye_default"))],
        [sg.Text("ラストの人は下のボタンをクリック！！", font = ("游ゴシック", 15))],
        [sg.Button("施錠等確認", key = "check/check")]
    ]

    window = sg.Window("入退室管理ツール", layout, no_titlebar = True, resizable = True)
    while True:
        event, values = window.read()
        if event != None:
            prefix, event = get_prefix(event)
            if prefix == "room" :
                room_index = int(event)
                room_bool_list[room_index] = 0 # 0:True, 1:False
                room_list_for_show.append(ROOM_NAME_LIST[room_index])
                window['room_check'].update(room_list_for_show)
            elif prefix == "push" :
                exit_list.extend(room_bool_list)
                write_student_data(STUDENT_DATA_JSON, your_id, "In_room", "false")
                goodbye = "ご協力ありがとうございます。お気をつけて～。"
                window["goodbye_default"].update(goodbye)
                close_flag_2 = True

            if close_flag_2 == True :
                time.sleep(1)
                window.close()

            elif prefix == "clear" :
                room_bool_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                print(room_bool_list)
                room_list_for_show = []
                window['room_check'].update(room_list_for_show)
            elif prefix == "check" :
                last_one_flag = True
                exit_list.extend(room_bool_list)
                write_student_data(STUDENT_DATA_JSON, your_id, "In_room", "false")
                goodbye = "ご協力ありがとうございます。お気をつけて～。"
                window["goodbye_default"].update(goodbye)
                close_flag_2 = True

            if close_flag_2 == True :
                time.sleep(1)
                window.close()
        else :
            window.close()
            break
    exit_tuple = tuple(exit_list)
    return exit_tuple, room_people_dict, last_one_flag


def appgui_for_last_one(your_name) :
    check_list = CHECK_LIST
    your_name = your_name.split(" ")[0]
    check_message_default = f"{your_name}さん、遅くまでお疲れ様です！！最後の確認をお願いします！！"
    sg.theme("Green")
    layout = [
        [sg.Text("ガスの元栓は閉じていますか？", font = ("游ゴシック", 15))],
        [sg.Button("クレブ卓", font = ("游ゴシック", 15), key = "0/0"), sg.Button("大部屋", font = ("游ゴシック", 15), key = "1/0"),\
         sg.Button("藻類部屋", font = ("游ゴシック", 15), key = "2/0")],
        [sg.Text("UVランプは消えていますか？", font = ("游ゴシック", 15))],
        [sg.Button("クレブ卓", font = ("游ゴシック", 15), key = "3/0"), sg.Button("大部屋", font = ("游ゴシック", 15), key = "4/0"),\
         sg.Button("藻類部屋", font = ("游ゴシック", 15), key = "5/0")],
        [sg.Text("-20℃の冷凍庫の温度は-20℃以下ですか？")],
        [sg.Button("Yes", key = "6/0"), sg.Button("No", key = "6/1")],
        [sg.Text("-80℃の冷凍庫の温度は-75℃以下ですか？")],
        [sg.Button("Yes", key = "7/0"), sg.Button("No", key = "7/1")],
        [sg.Text("給湯器の電源は切れていますか？", font = ("游ゴシック", 15))],
        [sg.Button("Yes", key = "8/0"), sg.Button("No", key = "8/1")],
        [sg.Text("電気泳動槽の電源は切りましたか？", font = ("游ゴシック", 15))],
        [sg.Button("Yes", key = "9/0"), sg.Button("No", key = "9/1")],
        [sg.Text("空調の電源は切りましたか？", font = ("游ゴシック", 15))],
        [sg.Button("Yes", key = "10/0"), sg.Button("No", key = "10/1")],
        [sg.Text("水銀灯のスイッチは消しましたか？", font = ("游ゴシック", 15))],
        [sg.Button("Yes", key = "11/0"), sg.Button("No", key = "11/1")],
        [sg.Button("Push", key = "push/push")],
        [sg.Text(check_message_default, font = ("游ゴシック", 15), key = "check_message_default")]
    ]
    window = sg.Window("危険要因確認ツール", layout, no_titlebar = True, resizable = True)
    while True :
        event, values = window.read()

        if event != None :
            prefix, event = get_prefix(event)
            if prefix != "push":
                prefix = int(prefix)
                event = int(event)
                check_list[prefix] = event
            else :
                check_massege = "ご協力ありがとうございます！問題があった場合は、メーリスなどで共有してください。"
                window["check_message_default"].update(check_massege)
                time.sleep(1)
                window.close()
        elif event == None :
            break
    check_tuple = tuple(check_list)
    return check_tuple
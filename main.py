#!/usr/bin/env python3
# coding: utf-8

from tools import get_student_data, get_student_id_list, write_new_student_data
from gui import appgui_for_enter, appgui_for_exit, appgui_for_last_one, appgui_for_await, appgui_for_new_commer
from my_sql import MySQL

JSON_PATH = "./args/test.json"

def main():
    while True:
        barcode_data = appgui_for_await()
        student_id_list = get_student_id_list(JSON_PATH)
        if not barcode_data in student_id_list :
            id = barcode_data
            new_id, new_name = appgui_for_new_commer(id)
            write_new_student_data(JSON_PATH, new_id, new_name)

        your_name, your_id, your_status = get_student_data(JSON_PATH, barcode_data)
        if your_status == "false":
            enter_tuple = appgui_for_enter(your_name, your_id, your_status)
            print(enter_tuple)

            insertion = f"INSERT INTO enter_table VALUES {enter_tuple}"
            with MySQL("localhost") as action :
                res = action.call("USE mysql")
                action.commit()
                res = action.call(insertion)
                action.commit()

        elif your_status == "true" :
            exit_tuple, room_people_dict, last_one_flag = appgui_for_exit(your_name, your_id, your_status)
            print(exit_tuple)

            insertion = f"INSERT INTO exit_table VALUES {exit_tuple}"
            with MySQL("localhost") as action :
                res = action.call("USE mysql")
                action.commit()
                res = action.call(insertion)
                action.commit()

            if room_people_dict == {} or last_one_flag == True:
                check_tuple = appgui_for_last_one(your_name)
                print(check_tuple)

                insertion = f"INSERT INTO check_list_table VALUES {check_tuple}"
                with MySQL("localhost") as action :
                    res = action.call("USE mysql")
                    action.commit()
                    res = action.call(insertion)
                    action.commit()

if __name__ == "__main__" :
    main()
import json
import tkinter as tk
from tkinter import ttk
from config import *

# 加密函数
def encrypt_value(value, yq, data_key):
    if isinstance(value, str):
        value = int(value)
    if data_key in ['尸首数', '花费尸首数']:
        return value * -17 + 2413
    else:
        return value * -17 + 2413 + yq

# 解密函数
def decrypt_value(value, yq, data_key):
    if data_key in ['尸首数', '花费尸首数']:
        return (value - 2413) // -17
    else:
        return (value - 2413 - yq) // -17

def convert_to_int_if_numeric(s):
    if isinstance(s, str) and s.isdigit():
        return int(s)
    else:
        return s
def pvz_json_key_get_data(json_data, json_key, encrypt = False):
    if '继续' not in json_data:
        raise KeyError('没有存档，请开启一个新存档')
    if json_key in json_data:
        data_key = json_key
        data_value = json_data.get(json_key, [])
    else:
        data_key = next(iter(json_data['继续']))
        data_value = json_data['继续'][data_key][json_key]
    if encrypt:
        yq = next(iter(json_data['继续'].values()))[16]
        insert_value = decrypt_value(data_value, yq, data_key)
    else:
        insert_value = data_value

    return insert_value


def create_textarea_widget(window, title, json_data, json_key, row, column, encrypt = False):
    tk.Label(window, text = title).grid(row = row, column = column)
    entry_width = 6  # 统一的宽度设置
    entry = tk.Entry(window, width=entry_width)

    insert_value = pvz_json_key_get_data(json_data, json_key, encrypt)
    entry.insert(0, insert_value)
    entry.grid(row = row, column = column + 1)
    current_row = row + 1
    return (entry, encrypt), current_row


def create_combobox_widget(window, title, json_data, json_key, row, column, choices_list, encrypt = False):
    tk.Label(window, text=title).grid(row=row, column=column)

    insert_value = pvz_json_key_get_data(json_data, json_key, encrypt)

    var = tk.StringVar(value=insert_value)
    var_width = 7
    combobox = ttk.Combobox(window, textvariable=var, values=choices_list, width=var_width)
    combobox.grid(row=row, column=column + 1, sticky="w")
    if insert_value in choices_list:
        combobox.current(choices_list.index(insert_value))  # Set the current value if it's in choices
    current_row = row + 1
    return (var, encrypt), current_row

def select_all(checkbox_vars, value=True):
    """更新所有复选框的选中状态."""
    for var in checkbox_vars.values():
        var.set(value)
def create_checkboxes_widget(window, title, json_data, json_key, row, column, options_list, encrypt = False):
    tk.Label(window, text=title).grid(row=row, column=column, sticky="w")
    checkboxes = {}
    checkbox_vars = {}
    for i, option in enumerate(options_list):
        checkbox_vars[option] = tk.BooleanVar(value=option in pvz_json_key_get_data(json_data, json_key))
        row_offset = (i // 8) + 1  # Calculate row offset, start on the next row after the title
        column_offset = (i % 8)  # Calculate column offset, 8 checkboxes per row
        checkboxes[option] = tk.Checkbutton(window, text=option, variable=checkbox_vars[option])
        checkboxes[option].grid(row=row + row_offset, column=column + column_offset, sticky="w")
    # 添加全选按钮
    select_all_button = tk.Button(window, text="全选", command=lambda: select_all(checkbox_vars))
    select_all_button.grid(row=row, column=column + 1, sticky="w")
    current_row = row + row_offset + 1
    return (checkbox_vars, encrypt), current_row

def create_ratio_widget(window, title, json_data, json_key, row, column, choices_list, encrypt = False):
    tk.Label(window, text=title).grid(row = row, column = column)

    insert_value = pvz_json_key_get_data(json_data, json_key, encrypt)
    var_width = 7
    var = tk.StringVar(value=insert_value)
    for i, choice in enumerate(choices_list):
        tk.Radiobutton(window, text=choice, variable=var, value=choice, width=var_width).grid(row=row, column=column+1+i, sticky="w")
    current_row = row + 1
    return (var, encrypt), current_row


def pvz_json_key_value_update_data(json_data, json_key, json_value, encrypt = False):
    if '继续' not in json_data:
        raise KeyError('没有存档，请开启一个新存档')
    if encrypt:
        yq = next(iter(json_data['继续'].values()))[16]
        update_value = encrypt_value(json_value, yq, json_key)
    else:
        update_value = convert_to_int_if_numeric(json_value)

    if json_key in json_data:
        data_key = json_key
        if json_key == '打败boss':
            update_value = {mode: achievements[mode] for mode in json_value}
        json_data[json_key] = update_value
    else:
        data_key = next(iter(json_data['继续']))
        json_data['继续'][data_key][json_key] = update_value

    #updated json data (single value update)
    return json_data


def print_layout(widget, level=0):
    # 打印当前控件的信息
    print(' ' * level * 2, widget.winfo_class(), 'Manager:', widget.winfo_manager(), 'Geometry:', widget.winfo_geometry())
    # 如果当前控件是容器，递归打印其子控件的信息
    if widget.winfo_children():
        for child in widget.winfo_children():
            print_layout(child, level + 1)

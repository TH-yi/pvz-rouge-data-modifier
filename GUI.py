# GUI.py
import tkinter as tk
from tkinter import ttk, Toplevel
import os
import sys
import json
import shutil
import subprocess
import psutil
from datetime import datetime
from config import *
from GUIWidgets import *

def list_json_files(directory):
    """列出指定目录下的所有JSON文件"""
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def encode_strings_to_unicode(input_file, output_file):
    """
    Reads a JSON file, encodes all string values to Unicode escape sequences,
    and writes the modified JSON to another file.

    Args:
    - input_file: The path to the input JSON file.
    - output_file: The path to the output JSON file where the modified JSON will be saved.
    """
    # Load the JSON data from the input file
    if isinstance(input_file, dict):
        json_data = input_file
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

    # Encode the JSON data to Unicode
    encoded_data = json.dumps(json_data, ensure_ascii=True)

    # Write the encoded data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encoded_data)

class AppGUI:
    def __init__(self, root = None):
        if not root:
            root = tk.Tk()
        root.title('PVZ-Rouge 存档修改器 By: 冰竹青 (Bilibili: IcyWindy)')
        self.root = root


        self.root.iconbitmap(default=icon_path)
        self.json_data = None
        self.input_directory = tk.StringVar(value=default_input_dir)
        self.decodeoutput_directory = tk.StringVar(value=default_output_dir)
        self.reencodeoutput_directory = tk.StringVar(value=default_output_dir)

        self.create_widgets()
        self.decode_json()

    def create_widgets(self):
        # Log Text widget setup
        self.log_text = tk.Text(self.root, state=tk.DISABLED, height=10)
        tk.Label(self.root, text='操作日志:').grid(row=4, column=0, sticky=tk.W)
        self.log_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # 输入文件夹和文件选择
        #tk.Label(self.root, text='Input File:').grid(row=0, column=0, sticky=tk.W)
        self.input_file_combobox = ttk.Combobox(self.root)
        #self.input_file_combobox.grid(row=0, columnspan=2, column=1)
        self.input_file_combobox.set('pvzrouge.json')

        # 输出文件夹和文件选择
        #tk.Label(self.root, text='Decode Output File:').grid(row=1, column=0, sticky=tk.W)
        self.decodeoutput_file_combobox = ttk.Combobox(self.root)
        #self.decodeoutput_file_combobox.grid(row=1, columnspan=2, column=1)
        self.decodeoutput_file_combobox.set('decodeoutput.json')

        #tk.Label(self.root, text='Reencode Output File:').grid(row=2, column=0, sticky=tk.W)
        self.reencodeoutput_file_combobox = ttk.Combobox(self.root)
        #self.reencodeoutput_file_combobox.grid(row=2, columnspan=2, column=1)
        self.reencodeoutput_file_combobox.set('pvzrouge.json')

        # 编码和解码按钮
        decode_button = tk.Button(self.root, text="备份存档", command=self.decode_and_backup)
        decode_button.grid(row=0, column=0, sticky=tk.W+tk.E)

        combined_button = tk.Button(self.root, text="重启游戏", command=self.replace_data_restart)
        combined_button.grid(row=1, column=1, sticky=tk.W+tk.E)

        clear_and_refresh_button = tk.Button(self.root, text="刷新修改器", command=self.clear_log_and_refresh_lists)
        clear_and_refresh_button.grid(row=0, column=1, sticky=tk.W+tk.E)

        edit_button = tk.Button(self.root, text="编辑存档", command=self.create_secondary_window_modify_json)
        edit_button.grid(row=1, column=0, sticky=tk.W+tk.E)

    def on_frame_configure(self, canvas):
        '''重置画布的滚动区域以包含当前所有子组件'''
        canvas.configure(scrollregion=canvas.bbox("all"))


    def create_secondary_window_modify_json(self):
        self.secondary_window_modify_json = Toplevel(self.root)
        self.secondary_window_modify_json.title("修改存档数据")
        self.secondary_window_modify_json.geometry("650x750")
        self.secondary_window_modify_json.iconbitmap(default=icon_path)
        # 初始化存储控件变量的字典
        entries = {}  # 对于Entry控件
        radiobutton_vars = {}  # 对于Radiobutton控件
        checkbox_vars = {}  # 对于Checkbutton控件
        combobox_vars = {}  # 对于Combobox控件
        current_row = 0
        column_span = 2 # 定义功能按钮span

        onekey_cheat_button = tk.Button(self.secondary_window_modify_json, text="一键修改",
                                        command=lambda: self.onekey_cheat(entries, radiobutton_vars, checkbox_vars,
                                                                          combobox_vars))
        onekey_cheat_button.grid(row=current_row, column=0, columnspan=column_span, sticky=tk.W + tk.E)

        apply_button = tk.Button(self.secondary_window_modify_json, text="应用修改",
                                 command=lambda: self.apply_changes_to_json(entries, radiobutton_vars, checkbox_vars,
                                                                            combobox_vars))
        apply_button.grid(row=current_row, column=2, columnspan=column_span, sticky=tk.W + tk.E)

        combined_button = tk.Button(self.secondary_window_modify_json, text="保存并重启游戏",
                                    command=lambda: self.save_and_restart(entries, radiobutton_vars, checkbox_vars,
                                                                          combobox_vars))
        combined_button.grid(row=current_row, column=4, columnspan=column_span, sticky=tk.W + tk.E)

        cancel_button = tk.Button(self.secondary_window_modify_json, text="取消",
                                  command=self.secondary_window_modify_json.destroy)
        cancel_button.grid(row=current_row, column=6, columnspan=column_span, sticky=tk.W + tk.E)

        current_row = current_row + 1

        entries['尸首数'] , current_row = create_textarea_widget(self.secondary_window_modify_json, '尸首数', self.json_data,
                               '尸首数', current_row, 0, True)
        entries['花费尸首数'] , current_row = create_textarea_widget(self.secondary_window_modify_json, '下次抽奖花费', self.json_data,
                               '花费尸首数', current_row, 0, True)
        entries[3], current_row = create_textarea_widget(self.secondary_window_modify_json, '初始阳光', self.json_data,
                               3, current_row, 0, True)
        entries[4], current_row  = create_textarea_widget(self.secondary_window_modify_json, '卡槽数', self.json_data,
                               4, current_row, 0, True)
        entries[5], current_row  = create_textarea_widget(self.secondary_window_modify_json, '钱', self.json_data,
                               5, current_row, 0, True)
        '''entries[8], current_row  = create_textarea_widget(self.secondary_window_modify_json, '防守', self.json_data,
                               8, current_row, 0, True)
        entries[9], current_row  = create_textarea_widget(self.secondary_window_modify_json, '作战数', self.json_data,
                               9, current_row, 0, True)'''
        entries[1], current_row = create_textarea_widget(self.secondary_window_modify_json, '天数（第x天）', self.json_data,
                                                         1, current_row, 0, True)
        combobox_vars[11], current_row = create_combobox_widget(self.secondary_window_modify_json, '地图',
                                                                self.json_data,
                                                                11, current_row, 0, maps)
        radiobutton_vars[2], current_row  = create_ratio_widget(self.secondary_window_modify_json, '昼/夜', self.json_data,
                               2, current_row, 0, ['白天', '黑天'])

        combobox_vars[14], current_row = create_combobox_widget(self.secondary_window_modify_json, '模式',
                                                                self.json_data,
                                                                14, current_row, 0, modes)
        checkbox_vars[0], current_row  = create_checkboxes_widget(self.secondary_window_modify_json, '拥有植物', self.json_data,
                               0, current_row, 0, plants)

        checkbox_vars[15], current_row = create_checkboxes_widget(self.secondary_window_modify_json, '拥有秘籍',
                                                                 self.json_data,
                                                                 15, current_row, 0, skills)
        checkbox_vars['拟人'], current_row = create_checkboxes_widget(self.secondary_window_modify_json, '花园（拟人）',
                                                                 self.json_data,
                                                                 '拟人', current_row, 0, plants)

        checkbox_vars['打败boss'], current_row = create_checkboxes_widget(self.secondary_window_modify_json, '通关模式',
                                                                      self.json_data,
                                                                      '打败boss', current_row, 0, achievements)

        #print_layout(self.secondary_window_modify_json)
    def onekey_cheat(self, entries, radiobutton_vars, checkbox_vars,combobox_vars):
        entries['尸首数'][0].delete(0, tk.END)
        entries['尸首数'][0].insert(0, '99999')
        entries['花费尸首数'][0].delete(0, tk.END)
        entries['花费尸首数'][0].insert(0, '1')
        entries[3][0].delete(0, tk.END)
        entries[3][0].insert(0, '99999')
        entries[4][0].delete(0, tk.END)
        entries[4][0].insert(0, '17')
        entries[5][0].delete(0, tk.END)
        entries[5][0].insert(0, '99999')
        for checkbox_var_key, checkbox_var_value in checkbox_vars.items():
            select_all(checkbox_var_value[0])
    def apply_changes_to_json(self, entries, radiobutton_vars, checkbox_vars, combobox_vars):
        json_data = self.json_data
        for key, entry_encrypt in entries.items():
            json_value = entry_encrypt[0].get()
            encrypt = entry_encrypt[1]
            json_data = pvz_json_key_value_update_data(json_data, key, json_value, encrypt)

        for key, var_encrypt in radiobutton_vars.items():
            json_value = var_encrypt[0].get()
            encrypt = var_encrypt[1]
            json_data = pvz_json_key_value_update_data(json_data, key, json_value, encrypt)

            # 更新复选框的值
        for key, var_encrypt in checkbox_vars.items():
            json_values = var_encrypt[0]
            encrypt = var_encrypt[1]
            plant_lst = []
            for plant, plant_var in json_values.items():
                is_selected = plant_var.get()
                if is_selected:
                    plant_lst.append(plant)

            json_value = plant_lst
            json_data = pvz_json_key_value_update_data(json_data, key, json_value, encrypt)
            # 当key=0时，需要更新商店存货
            if key == 0:
                plants_set = set(plants)
                special_plants_set = set(special_plants)
                plants_existing_set = set(plant_lst)
                special_plants_existing_set = plants_existing_set.intersection(special_plants_set)
                special_plants_nonexisting_set = special_plants_set.difference(special_plants_existing_set)
                special_plants_nonexisting_list = list(special_plants_nonexisting_set)
                # 清空存货植物，补全商店植物
                json_data = pvz_json_key_value_update_data(json_data, 7, [], encrypt)
                json_data = pvz_json_key_value_update_data(json_data, 6, special_plants_nonexisting_list, encrypt)
        # 更新下拉列表的值
        for key, var_encrypt in combobox_vars.items():
            json_value = var_encrypt[0].get()
            encrypt = var_encrypt[1]
            json_data = pvz_json_key_value_update_data(json_data, key, json_value, encrypt)
            # key = 14更新继续key值
            if key == 14:
                if json_value != list(json_data['继续'].keys())[0]:
                    # 保存旧键的值
                    old_key = list(json_data['继续'].keys())[0]
                    value_to_transfer = json_data['继续'][old_key]

                    # 删除旧键
                    del json_data['继续'][old_key]

                    # 添加新键，保留原来的值
                    json_data['继续'][json_value] = value_to_transfer

        # updated json_data
        self.json_data = json_data
        self.log_action('应用修改成功', '')

    def save_and_restart(self, entries, radiobutton_vars, checkbox_vars, combobox_vars):
        self.apply_changes_to_json(entries, radiobutton_vars, checkbox_vars, combobox_vars)
        self.replace_data_restart()
    def decode_json(self):
        try:
            for warning in conf_warnings:
                if warning:
                    self.log_action(warning, "")
            input_file = os.path.join(self.input_directory.get(), self.input_file_combobox.get())

            with open(input_file, 'r', encoding='utf-8') as f:
                encoded_data = f.read()
            decoded_data = json.loads(encoded_data)
            self.json_data = decoded_data
            self.log_action('解析存档成功:', input_file)

        except Exception as e:
            self.log_action('解析存档错误，请检查是否开启了新存档（不包括我是僵尸/测试模式）\n', str(e))

    def save_decoded_json(self):
        if not self.json_data:
            try:
                self.decode_json()
            except Exception as e:
                self.log_action('保存存档失败：未解析存档文件', str(e))
        else:
            try:
                decode_output_file = os.path.join(self.decodeoutput_directory.get(), self.decodeoutput_file_combobox.get())
                with open(decode_output_file, 'w', encoding='utf-8') as f:
                    json.dump(self.json_data, f, ensure_ascii=False, indent=4)
                self.log_action('保存存档成功', decode_output_file)
                # 使用默认程序打开JSON文件
                os.startfile(decode_output_file)
            except Exception as e:
                self.log_action('保存存档失败', str(e))

    def backup_input_json(self):
        try:
            # 获取输入文件的完整路径
            input_file_path = os.path.join(self.input_directory.get(), self.input_file_combobox.get())
            # 设置备份文件的目标路径和名称
            backup_file_path = os.path.join(self.decodeoutput_directory.get(), "backup.json")

            # 使用shutil.copyfile复制文件
            shutil.copyfile(input_file_path, backup_file_path)

            # 记录操作日志
            self.log_action('Backup Success', backup_file_path)
            # 可选：使用默认程序打开备份的JSON文件
            #os.startfile(backup_file_path)

        except Exception as e:
            self.log_action('Backup Error', str(e))


    def decode_and_backup(self):
        self.decode_json()
        self.backup_input_json()

    def replace_data_restart(self):
        def restart_executable(path_to_executable):
            try:
                # Check if the executable is already running
                for process in psutil.process_iter(attrs=['pid', 'name']):
                    if process.info['name'] == 'PVZ-Rouge.exe':  # Adjust as needed
                        process.terminate()
                        process.wait()
                        self.log_action('Terminate Success', path_to_executable)

                # Start the executable in its directory
                executable_dir = os.path.dirname(path_to_executable)
                subprocess.Popen(path_to_executable, cwd=executable_dir)
                self.log_action('Start Success', path_to_executable)
            except Exception as e:
                self.log_action('Restart Error', str(e))

        def copy_and_overwrite_file(source_file, destination_dir, delete_original=True):
            try:
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                destination_file = os.path.join(destination_dir, os.path.basename(source_file))
                shutil.copyfile(source_file, destination_file)
                #self.log_action('Copy Success', destination_file)  # Log success

                if delete_original:
                    original_file = os.path.join(self.input_directory.get(), 'pvzrougeb.json')
                    if os.path.exists(original_file):
                        os.remove(original_file)
                        self.log_action('Delete Original', original_file)  # Log deletion

                return destination_file
            except Exception as e:
                self.log_action('Copy/Error', str(e))  # Log failure or error
                return None
        # Reencode
        try:
            #input_file = os.path.join(self.input_directory.get(), self.input_file_combobox.get())
            #decode_output_file = os.path.join(self.decodeoutput_directory.get(), self.decodeoutput_file_combobox.get())
            reencode_output_file = os.path.join(self.reencodeoutput_directory.get(), self.reencodeoutput_file_combobox.get())
            encode_strings_to_unicode(self.json_data, reencode_output_file)
            self.log_action('Reencode Success', reencode_output_file)
        except Exception as e:
            self.log_action('Reencode Error', str(e))

        # Copy file to input
        try:
            copied_file_path = copy_and_overwrite_file(reencode_output_file, self.input_directory.get())
            self.log_action('Copy Success', copied_file_path)
        except Exception as e:
            self.log_action('Copy Error', str(e))

        # Restart executable
        try:
            restart_executable(pvz_rouge_path)
        except Exception as e:
            self.log_action('自动重启游戏失败，请检查路径是否正确（不影响存档修改）', str(e))

    def log_action(self, action, file_path):
        current_time = datetime.now().strftime("%m-%d %H:%M:%S")
        log_entry = f"{current_time} {action} {file_path}\n"
        # Insert log entry at the end
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        # Keep only the 7 most recent log entries
        log_lines = self.log_text.get('1.0', tk.END).split('\n')
        if len(log_lines) > 10:
            self.log_text.delete('1.0', '2.0')  # Adjust to remove the oldest entry from the top
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)  # Auto-scroll to the bottom

    def refresh_input_files_list(self):
        # 假设您的输入文件夹和输出文件夹相同
        new_input_files = list_json_files(self.input_directory.get())
        self.input_file_combobox['values'] = new_input_files
        if new_input_files:
            self.input_file_combobox.set(new_input_files[0])
        else:
            self.input_file_combobox.set('')

    def refresh_output_files_list(self):
        # 假设解码和重新编码输出到同一个目录
        new_output_files = list_json_files(self.decodeoutput_directory.get())
        self.decodeoutput_file_combobox['values'] = new_output_files
        self.reencodeoutput_file_combobox['values'] = new_output_files
        if new_output_files:
            self.decodeoutput_file_combobox.set('decodeoutput.json')
            self.reencodeoutput_file_combobox.set('pvzrouge.json')
        else:
            self.decodeoutput_file_combobox.set('')
            self.reencodeoutput_file_combobox.set('')
    def clear_log_and_refresh_lists(self):
        # 清理日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        # log_action('Log Cleared', 'All lists refreshed')  # 可选：记录这个操作

        # 重新获取并刷新输入框列表
        self.decode_json()
        self.refresh_input_files_list()
        self.refresh_output_files_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
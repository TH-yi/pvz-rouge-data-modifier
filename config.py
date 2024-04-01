import os
import sys
import shutil
import ctypes
from ctypes import wintypes
from configparser import ConfigParser

# 初始化ConfigParser
config = ConfigParser()
config_warning = common_warning = private_warning = None

config_path = os.path
config_file = 'config.ini'

ctypes.windll.shell32.SHGetFolderPathW.argtypes = [
    wintypes.HWND, wintypes.INT, wintypes.HANDLE, wintypes.DWORD, wintypes.LPCWSTR]

def get_common_documents_path():
    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, 0x002e, None, 0, path_buf)
    return path_buf.value

def copy_file_if_not_exists(src, dest):
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(src, dest)
        return True
    return False

if getattr(sys, 'frozen', False):
    # 如果程序是被冻结打包的，则使用这个路径
    bundle_dir = sys._MEIPASS
else:
    # 程序不是打包的，使用这个路径
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


if not os.path.exists(config_file):
    pvzrouge_filename = "pvzrouge.json"
    current_directory_pvzrouge = os.path.join(bundle_dir, pvzrouge_filename)

    private_documents_path = os.path.expandvars(f"${'USERPROFILE'}")
    private_documents_pvzrouge_path = os.path.join(private_documents_path, pvzrouge_filename)

    # 检查公共文档文件夹
    common_documents_path = get_common_documents_path()
    common_documents_pvzrouge_path = os.path.join(common_documents_path, pvzrouge_filename)

    if os.path.exists(private_documents_pvzrouge_path):
        input_dir = private_documents_path
    elif os.path.exists(common_documents_pvzrouge_path):
        input_dir = common_documents_path
    else:
        # 尝试复制到当前目录
        try:
            shutil.copy(current_directory_pvzrouge, private_documents_path)
            private_warning = f'在{private_documents_path}创建了一个示例存档！'
            input_dir = private_documents_path
        except Exception as e:
            private_warning = f"创建存档失败:{private_documents_path} {e}"
            try:
                shutil.copy(current_directory_pvzrouge, common_documents_path)
                common_warning = f'在{common_documents_path}创建了一个示例存档！'
                input_dir = common_documents_path
            except Exception as err:
                common_warning = f"创建存档失败:{common_documents_path}, {err}"
                input_dir = private_documents_path
    # 设置默认配置
    config['DEFAULT'] = {'InputDir': input_dir,
                         'OutputDir': './output'}



    config['PATHS'] = {'PVZ_Rouge_Path': 'D:/PVZ-Rouge-v1.4.8/PVZ-Rouge.exe'}
    config_warning = '未找到配置文件，已自动创建config.ini'
    # 写入到配置文件
    with open(config_file, 'w') as configfile:
        config.write(configfile)
else:
    # 读取配置文件
    config.read(config_file)



# 获取默认输入目录，并替换环境变量
default_input_dir_name = config['DEFAULT']['InputDir']
if default_input_dir_name == 'USERPROFILE':
    default_input_dir = os.path.expandvars(f"${default_input_dir_name}")
else:
    default_input_dir = os.path.abspath(config['DEFAULT']['InputDir'])
# 获取默认输出目录，这里使用os.path.abspath确保路径是绝对路径
default_output_dir = os.path.abspath(config['DEFAULT']['OutputDir'])
# 检查目录是否存在，如果不存在则创建
if not os.path.exists(default_output_dir):
    os.makedirs(default_output_dir)
    print(f"Directory '{default_output_dir}' was created.")
else:
    print(f"Directory '{default_output_dir}' already exists.")

conf_warnings = [config_warning, common_warning, private_warning]
# 构建PVZ-Rouge路径，确保使用正确的目录分隔符
pvz_rouge_path = os.path.abspath(config['PATHS']['PVZ_Rouge_Path'])

plants = ['阳光菇', '冰瓜投手', '咖啡豆', '忧郁蘑菇', '寒冰菇', '裂荚射手', '胆小菇', '路灯花', '西瓜投手', '大喷菇', '小喷菇', '花盆',
          '向日葵', '金盏花', '豌豆射手', '香蒲', '玉米加农炮', '玉米投手', '模仿者', '地刺王', '缠绕海草', '睡莲', '机枪射手', '毁灭菇',
          '火炬树桩', '地刺', '仙人掌', '吸金磁', '寒冰射手', '卷心菜投手', '萝卜伞', '魅惑菇', '坚果', '高坚果', '火爆辣椒', '杨桃',
          '三叶草', '大嘴花', '南瓜头', '大蒜', '墓碑吞噬者', '樱桃炸弹', '窝瓜', '海蘑菇', '磁力菇', '双发射手', '土豆地雷', '双子向日葵']

special_plants = ['机枪射手', '双子向日葵', '忧郁蘑菇', '香蒲', '冰瓜投手', '吸金磁', '地刺王', '玉米加农炮', '模仿者']
skills = ['光疗', '硬化', '大帝', '猫尾', '补光', '无土栽培', '石果', '地雷', '防守', '气球', '魅惑', '咖啡', '速植', '体香','胆大',
          '尖刺', '压顶', '蓝火', '疾行', '核平', '雷霆', '磁力', '黄油', '卷心菜', '地刺', '水兵', '龙蒺藜', '小喷']
maps = ['家院', '小镇', '山地', '绿洲', '遗迹', '大桥', '木船', '沙城', '要塞', '铁道', '古堡', '大楼']
modes = ['正常模式', '抽奖模式', '极难模式', '末日模式']
achievements = {'正常模式': ['红眼巨人僵尸'], '抽奖模式': ['红眼巨人僵尸'], '极难模式': ['红眼巨人僵尸'], '末日模式': ['红眼巨人僵尸']}


# 资源文件的完整路径
icon_path = os.path.join(bundle_dir, 'icon.ico')
if __name__ == "__main__":
    print('Input dir:', default_input_dir)
    print('Output dir:', default_output_dir)
    print('PVZ rouge path:', pvz_rouge_path)
    print('Plants:', plants)
    print('Special plants:', special_plants)
    print('Skills:', skills)
    print('Maps:', maps)
    print('Modes:', modes)
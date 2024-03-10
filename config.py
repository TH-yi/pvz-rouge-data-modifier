import os
import sys
from configparser import ConfigParser

# 初始化ConfigParser
config = ConfigParser()

# 读取配置文件
config.read('config.ini')

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

# 构建PVZ-Rouge路径，确保使用正确的目录分隔符
pvz_rouge_path = os.path.abspath(config['PATHS']['PVZ_Rouge_Path'])

plants = ['阳光菇', '冰瓜投手', '咖啡豆', '忧郁蘑菇', '寒冰菇', '裂荚射手', '胆小菇', '路灯花', '西瓜投手', '大喷菇', '小喷菇', '花盆',
          '向日葵', '金盏花', '豌豆射手', '香蒲', '玉米加农炮', '玉米投手', '模仿者', '地刺王', '缠绕海草', '睡莲', '机枪射手', '毁灭菇',
          '火炬树桩', '地刺', '仙人掌', '吸金磁', '寒冰射手', '卷心菜投手', '萝卜伞', '魅惑菇', '坚果', '高坚果', '火爆辣椒', '杨桃',
          '三叶草', '大嘴花', '南瓜头', '大蒜', '墓碑吞噬者', '樱桃炸弹', '窝瓜', '海蘑菇', '磁力菇', '双发射手', '土豆地雷', '双子向日葵']

special_plants = ['机枪射手', '双子向日葵', '忧郁蘑菇', '香蒲', '冰瓜投手', '吸金磁', '地刺王', '玉米加农炮', '模仿者']
skills = ['光疗', '硬化', '大帝', '猫尾', '补光', '无土栽培', '石果', '地雷', '防守', '气球', '魅惑', '咖啡']
maps = ['家院', '小镇', '山地', '绿洲', '遗迹', '大桥', '木船', '沙城', '要塞', '铁道']
modes = ['正常模式', '抽奖模式', '极难模式', '末日模式']
achievements = {'抽奖模式': ['红眼巨人僵尸'], '末日模式': ['红眼巨人僵尸'], '极难模式': ['红眼巨人僵尸'], '正常模式': ['红眼巨人僵尸']}

if getattr(sys, 'frozen', False):
    # 如果程序是被冻结打包的，则使用这个路径
    bundle_dir = sys._MEIPASS
else:
    # 程序不是打包的，使用这个路径
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

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
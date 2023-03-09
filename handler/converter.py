#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    将Excel中的数据转化为rpy中的对象
"""
from collections import namedtuple

from const.converter_setting import ElementColNumMapping, PositionMapping, ImageCmdMapping, TransitionMapping, \
    ReplaceCharacterMapping
from model.element import Text, Image, Transition, Audio, Role, complexRole, Command, Voice, Menu
# - 取自编待调用

SheetConvertResult = namedtuple('SheetConvertResult', ['label', 'data'])

RowConvertResult = namedtuple('RowConvertResult',
                              ['role',  # 角色
                               'mode',  # 模式
                               'text',  # 文本
                               'music',  # 音乐
                               'character',  # 立绘
                               'change_page',  # 换页
                               'background',  # 背景
                               'remark',  # 备注
                               'sound',  # 音效
                               'transition',  # 转场
                               'voice',  # 语音
                               'menu',  # 条件跳转
                               'side_character'  # 头像
                               ])


class Converter(object):

    def __init__(self, parser):
        self.parser = parser        # 调用parser.py
        self.roles = list()         # 这个应该是个无用的列表变量
        self.role_name_mapping = dict() # 真名（键）- 混合定义字符变量（值）字典
        self.current_mode = 'nvl'   # 当前故事模式标志

#        self.current_role = Role("narrator_nvl", "None")    # 当前说话角色标志
        self.current_role = complexRole("narrator_nvl", "None")    # 当前说话角色标志
        self.characters = list()    # 屏上立绘显隐列表
        self.side_characters = dict()   # 真名（键）- 混合定义字符变量（值）字典

    def add_role(self, name):
        role = self.role_name_mapping.get(name)
        # - 检测是否已加入真名（键）-代称模板混合字符串（值），没有的增加为role{1,2,3,4,5……}
        if not role:
            role = Role("role{}".format(len(self.role_name_mapping.keys()) + 1), name)
            self.role_name_mapping[name] = role

        return role

    #SFR
    def add_fixrole(self, name, fixpronoun=None,
            char_color=None, char_whocolor=None, char_whatcolor=None,
            char_voicetag=None,
            char_whatprefix=None, char_whatsuffix=None):
        role = self.role_name_mapping.get(name)
        # - 检测是否已加入真名（键）-代称模板混合字符串（值），没有的增加为role{1,2,3,4,5……}
        if not role:
            if fixpronoun:  #如果有预设代称，我就认为你想要自定义，于是把传入的参数尽数给complexRole()函数
                # - 但是至于你到底有没有给有效参数我是不知道的
                # - complexRole()会判断
                role = complexRole(fixpronoun, name, char_color,
                 char_whocolor, char_whatcolor,
                 char_voicetag,
                 char_whatprefix, char_whatsuffix)
                self.role_name_mapping[name] = role
            else:
                role = complexRole("role{}".format(len(self.role_name_mapping.keys()) + 1), name)
                self.role_name_mapping[name] = role

        return role


    def generate_rpy_elements(self):
        # - 这个会被app.py调用，整合好的大类
        result = []
        parsed_sheets = self.parser.get_parsed_sheets()

        #parsed_sheets[1]

        for idx, parsed_sheet in enumerate(parsed_sheets):
            if idx == 0:
                # - 第一个表格会被用作start
                label = 'start'
            else:
                label = parsed_sheet.name
                # - 就是拿子表格名了
            result.append(SheetConvertResult(label=label, data=self.parse_by_sheet(parsed_sheet.row_values)))
            # - 按照子表格，把所有内容塞进一个tuple中
            # - 通过调用parse_by_sheet分了表、同时表也和label同名，并且是把
            #    - 通过调用parse_by_row_value、进而调用RowConverter，把RowConvertResult这个通过nametuple建立的元组中的属性
            #    - 赋给了parse_by_sheet中的result，并且按行堆叠列表
        return result



    @classmethod
    def generate_character(cls, img_str, atxform=""):   # 说是generate，其实是显示图像
        atxformaflg = True if (img_str.split(" ")[-1])[-1] == ":" else False

        last_word = img_str.split(" ")[-1]  # - 取;分隔下，每个立绘的最后一个字
        position = PositionMapping.get(last_word)   #看看是不是位置参数
        #isname = self.role_name_mapping.get(last_word)

        print(last_word)
        print(atxformaflg)
        if bool(position) & (last_word!="hide"):    #如果是普通位置参数
            return Image(img_str.replace(last_word, "").strip(), "show", position, atxform, atxformaflg)
            # - 非常典型的写法，删去最后一个字，并去掉剩下部分内容的两边空格，如果不止想去空格也可以这样写，Eg. .rstrip(':')：非侵入去掉右边的英文冒号
        elif bool(not position) & bool(not atxformaflg) & (last_word!="hide"):    #如果不是从位置参数又不是冒号结尾
            atxform = img_str.split(" ")[-1]
            print("ie:")
            print(atxform)
            return Image(img_str.replace(last_word, "").strip(), "show", position, atxform, atxformaflg)
        elif bool(atxformaflg) & (last_word!="hide"):
            return Image(img_str.replace(last_word, "").strip(), "show", position, atxform, atxformaflg)
        else:
            return Image(img_str.replace(last_word, "").strip(), ImageCmdMapping.get(last_word, "hide"))
            # - 就是说如果手动hide了，也可以hide

    def parse_by_sheet(self, values):   #【√】
        result = []
        for row_value in values:
            result.append(self.parse_by_row_value(row_value))
        return result

    def parse_by_row_value(self, row):  #【√】
        row_converter = RowConverter(row, self)
        return row_converter.convert()


class RowConverter(object):

    def __init__(self, row, converter):
        self.row = row
        self.converter = converter

    def convert(self):
        return RowConvertResult(
            mode=self._converter_mode(),
            role=self._converter_role(),
            text=self._converter_text(),
            music=self._converter_music(),
            character=self._converter_character(),
            change_page=self._converter_change_page(),
            background=self._converter_background(),
            remark=self._converter_remark(),
            sound=self._converter_sound(),
            transition=self._converter_transition(),
            voice=self._converter_voice(),
            menu=self._converter_menu(),
            side_character=self._converter_side_character(),
        )

    def _converter_mode(self):  #【√】
        # 模式
        mode = self.row[ElementColNumMapping.get('mode')]
        if mode:
            self.converter.current_mode = mode
        return mode

    def _converter_role(self):  #【√】用于管理和创建有名角色和旁白、并捕捉当前行的current_role作为标志
        # 角色
        #preSFR
        fixpronoun = self.row[ElementColNumMapping.get('fixpronoun')]
        char_color = self.row[ElementColNumMapping.get('char_color')]
        char_whocolor = self.row[ElementColNumMapping.get('char_whocolor')]
        char_whatcolor = self.row[ElementColNumMapping.get('char_whatcolor')]
        char_voicetag = self.row[ElementColNumMapping.get('char_voicetag')]
        char_whatprefix = self.row[ElementColNumMapping.get('char_whatprefix')]
        char_whatsuffix = self.row[ElementColNumMapping.get('char_whatsuffix')]

        role_name = self.row[ElementColNumMapping.get('role_name')]
        if role_name not in ["", "旁白"]:
            # 当其他角色出现时，重置模式为nvl
            #self.converter.current_role = self.converter.add_role(role_name)
            #preSFR
            self.converter.current_role = self.converter.add_fixrole(role_name, fixpronoun,
                        char_color, char_whocolor, char_whatcolor,
                char_voicetag,
                char_whatprefix, char_whatsuffix)
            # -
        elif role_name == "" and self.converter.current_mode == "": # 顺继承姓名并 不改变模式
            return self.converter.current_role
        else:
            #self.converter.current_role = Role("narrator_{}".format(self.converter.current_mode), "None")
            self.converter.current_role = complexRole("narrator_{}".format(self.converter.current_mode), "None")
        # elif role_name != "":
        #     # 当其他角色出现时，重置模式为nvl
        #     self.converter.current_role = self.converter.add_role(role_name)
        #     self.converter.current_mode = "nvl"
        return self.converter.current_role

    def _converter_text(self):  #【√】，返回当前行转换完毕文本
        # 文本
        text = str(self.row[ElementColNumMapping.get('text')]).replace("\n", "\\n")
        if not text:
            return None
        replace_index_char = []
        for idx, t in enumerate(text):
            if ReplaceCharacterMapping.get(t):
                replace_index_char.append((idx, t))

        if replace_index_char:
            new_text_list = list(text)
            for idx, char in replace_index_char:
                new_text_list[idx] = ReplaceCharacterMapping.get(char)
            text = ''.join(new_text_list)
        return Text(text, self.converter.current_role)
        # - 有外调用，返回属性text, role, triggers=None

    def _converter_music(self):
        # 音乐
        music = self.row[ElementColNumMapping.get('music')]
        fromto = self.row[ElementColNumMapping.get('fromto')]
        fadeinout = self.row[ElementColNumMapping.get('fadeinout')]
        if not music:
            return None

        cmd = "stop" if music == "none" else "play"
        # 想
        return Audio(music, cmd, fromto, fadeinout)
        # - 有外调用，返回属性

    def _converter_background(self):
        # 背景
        background = self.row[ElementColNumMapping.get('background')]
        if not background:
            return None
        return Image(background, "scene")
        # - 立绘和background共用一个Image函数

    def _converter_character(self):
        # 立绘
        character_str = str(self.row[ElementColNumMapping.get('character')]).strip()
        xforma_str = str(self.row[ElementColNumMapping.get('xforma')]).strip()

        # 你还记得我们表格里的输入的显示图片的参数是无后缀图片名称+位置参数+;分隔吗？
        # - 这就是new_characters列表（没有定义，只是个中间列表）中，通过generate_characters -> Image 进一步调用的语句
        if not character_str:
            return []

        characters = [] # 一个当前显示在屏幕上的立绘的暂存列表
        # 新立绘出现时回收旧立绘
        for character in self.converter.characters:
            characters.append(Image(character.name, 'hide'))
            # - 传参hide调用Image使其隐藏

        new_characters = [Converter.generate_character(ch,xtf) for ch,xtf in zip(character_str.split(";"),xforma_str.split(";"))]

        self.converter.characters = new_characters
        characters.extend(new_characters)   # 这是由于new_characters本身早了一个列表，如果是纯元素，就是append了，总之是在同级
        # - 看样子这个character的列表长度会不断增长
        return characters

    def _converter_remark(self):
        pass

    def _converter_sound(self):
        # 音效
        sound = self.row[ElementColNumMapping.get('sound')]
        if not sound:
            return None

        if sound.startswith('循环'):
            return Audio(sound.replace('循环', ''), 'loop')
        else:
            cmd = "stop" if sound == "stop" else "sound"
            return Audio(sound, cmd)

    def _converter_transition(self):
        # 转场
        transition = self.row[ElementColNumMapping.get('transition')]
        if not transition:
            return None
        t_style = TransitionMapping.get(transition, "")
        return Transition(t_style)

    def _converter_change_page(self):   #【√】
        # 换页
        change_page = self.row[ElementColNumMapping.get('change_page')]
        if not change_page:
            return None
        return Command("nvl clear") # 并不是有写东西就是nvl换页，gn真是（流汗黄豆））
        # - 取决于我是从哪里给cmd赋了值
        # - 可以是每个_converter_...里直接给出cmd指令（比如说Music和sound）
        # - 也可以像这样间接调用Command，让element.py处的函数给cmd赋值

    def _converter_voice(self):
        voice_str = str(self.row[ElementColNumMapping.get('voice')]).strip()

        if not voice_str:
            return None

        if voice_str.split(" ")[-1] == "sustain":
            voice_name = voice_str.split(" ")[0]
            return Voice(voice_name, sustain=True)
        # - 这部分决定当句文本对应的角色语音是否随鼠标点击、切换至下一句文本时停止
        else:
            return Voice(voice_str)
        # -  用的是一个独立于Audio（掌管music和sound）的element.py中的函数来播放

    def _converter_menu(self):
        # 分支条件的label写在对话文本列
        menu = self.row[ElementColNumMapping.get('menu')]
        # - 取一下目标跳转的lebel名

        if not menu:
            return None

        text = str(self.row[ElementColNumMapping.get('text')]).replace("\n", "\\n")

        if not text:
            return None
        # - 如果选项上没有写文本，就不对文本进行映射替换处理
        # 如果选项上需要写文本，就跟一般文本一样进行映射替换处理
        replace_index_char = []
        for idx, t in enumerate(text):
            if ReplaceCharacterMapping.get(t):
                replace_index_char.append((idx, t))
        if replace_index_char:
            new_text_list = list(text)
            for idx, char in replace_index_char:
                new_text_list[idx] = ReplaceCharacterMapping.get(char)
            text = ''.join(new_text_list)
        return Menu(label=text, target=menu)
        # - 与普通文本显示的区别是调用的element.py函数不同
        # - 返回值时继承调用函数的属性，也是python的一大特色

    def _converter_side_character(self):
        # 对话框头像
        character_str = str(self.row[ElementColNumMapping.get('side_character')]).strip()

        if not character_str:
            return None

        self.converter.side_characters[self.converter.current_role.fixpronoun] = character_str
        return None

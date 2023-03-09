# encoding: utf-8
"""
    Rpy游戏的基本元素
"""
from corelib.exception import RenderException
from model import RpyElement

ROLE_TEMPLATE = "define {name} = Character('{role}', color=\"{color}\", image=\"{side_character}\")"  # 角色模板

NAMEROLECLR_TEMPLATE = "define {name} = Character(\'{role}\', color=\"{color}\""
WHOCOLOR_TEMPLATE = ", who_color=\"{char_whocolor}\""
WHATCOLOR_TEMPLATE = ", what_color=\"{char_whatcolor}\""
IMAGETAG_TEMPLATE = ", image=\"{side_character}\""
VOICETAG_TEMPLATE = ", voice_tag=\"{char_voicetag}\""
PREFIX_TEMPLATE = ", what_prefix=\"{char_whatprefix}\""
SUFFIX_TEMPLATE = ", what_suffix=\"{char_whatsuffix}\""
SUFBRACKET_TEMPLATE = ")"




# 对话
class Text(RpyElement):

    def __init__(self, text, role, triggers=None):
        """
        :param text: 文本
        :param role: 角色
        @:param triggers: 触发器：背景、音乐等等改变
        """
        self.text = text
        self.role = role
        self.triggers = triggers or list()

    def render(self, mode='nvl'):
        # result = [t.render() for t in self.triggers]
        result = []
        if self.role:
            #result.append("{character} {text}".format(character=self.role.pronoun, text="\"{}\"".format(self.text)))
            result.append("{character} {text}".format(character=self.role.fixpronoun, text="\"{}\"".format(self.text)))
        elif mode == 'nvl':
            result.append("{character} {text}".format(character="narrator_nvl", text="\"{}\"".format(self.text)))
        elif mode == 'adv':
            result.append("{character} {text}".format(character="narrator_adv", text="\"{}\"".format(self.text)))
        return "\n".join(result)

    def add_triggers(self, *triggers):
        if not self.triggers:
            self.triggers = triggers
        else:
            self.triggers += triggers


# 角色
class Role(RpyElement):

    def __init__(self, pronoun, name, color=None):
        """
        :param pronoun: 代称
        :param name: 角色名
        :param color: 颜色
        """
        self.pronoun = pronoun
        self.name = name
        self.color = color or "#c8c8ff"

    def render(self):
        if not self.name:
            return ""
        return ROLE_TEMPLATE.format(name=self.pronoun, role=self.name, color=self.color, side_character=self.pronoun)

class complexRole(RpyElement):
    def __init__(self, fixpronoun, name, char_color=None,
                 char_whocolor=None, char_whatcolor=None,
                 char_voicetag=None,
                 char_whatprefix=None, char_whatsuffix=None):
        self.fixpronoun = fixpronoun
        self.name = name
        self.char_color = char_color or "#c8c8ff"
        self.char_whocolor = char_whocolor
        self.char_whatcolor = char_whatcolor
        self.char_voicetag = char_voicetag
        self.char_whatprefix = char_whatprefix
        self.char_whatsuffix = char_whatsuffix

    def shielded(self):
        catstr = []
        #name:
        #    return ""

        if self.name:
            catstr.append(NAMEROLECLR_TEMPLATE.format(name=self.fixpronoun, role=self.name, color=self.char_color))
        if self.char_whocolor:
            catstr.append(WHOCOLOR_TEMPLATE.format(char_whocolor = self.char_whocolor))
        if self.char_whatcolor:
            catstr.append(WHATCOLOR_TEMPLATE.format(char_whatcolor = self.char_whatcolor))
        if self.char_voicetag:
            catstr.append(VOICETAG_TEMPLATE.format(char_voicetag = self.char_voicetag))
        if self.char_whatprefix:
            catstr.append(PREFIX_TEMPLATE.format(char_whatprefix = self.char_whatprefix))
        if self.char_whatsuffix:
            catstr.append(SUFFIX_TEMPLATE.format(char_whatsuffix = self.char_whatsuffix))
        catstr.append(IMAGETAG_TEMPLATE.format(side_character = self.fixpronoun))
        catstr.append(SUFBRACKET_TEMPLATE)
        catstrout0 = "".join(catstr)
        #print(catstrout0)
        #return catstrout0   # 总之跟之前一样，返回一个拼接好的模板
        # - 不能返回真的全字符模板，而是应该带有实际变量的
        return catstrout0

    def render(self):
        if not self.name:
            return ""
        if self.name:
            return self.shielded()


# 图像
class Image(RpyElement):

    def __init__(self, name, cmd, position="", atxform="",atxformaflg=False):
        """
        :param name: 图像名
        :param cmd: 指令: hide、scene、show
        :param position: 位置：left 表示界面左端， right 表示屏幕右端， center 表示水平居中(默认位置)， truecenter 表示水平和垂直同时居中。
        """
        self.name = name
        self.cmd = cmd
        self.position = position
        #SFRmodi
        self.atxform = atxform
        self.atxformaflg = atxformaflg

    # 当某个角色离开但场景不变化时，才需要使用hide
    def hide(self):
        if not self.name:
            return ""
        else:
            return "hide {name}".format(name=self.name)

    # 清除所有图像并显示了一个背景图像
    def scene(self):
        return "scene {name}".format(name=self.name)

    def show(self):
        catstr = []
        if bool(self.position) & (not self.atxform) & (not self.atxformaflg):
            return "show {name} at {position}".format(name=self.name, position=self.position)
        elif bool(not self.position) & bool(self.atxform) & (not self.atxformaflg):
            return "show {name} at {atxform}".format(name=self.name, atxform=self.atxform)
        elif self.atxformaflg:
            catstr1 = []
            atxformsplit = self.atxform.split("\n")
            for rowatxform in atxformsplit:
                catstr1.append("{content}".format(content=rowatxform))
            catstr1.insert(0, "show {name}:".format(name=self.name))
            catstrout = "\n    ".join(catstr1)
            return catstrout
        else:
            return "show {name}".format(name=self.name)

    def render(self):
        if self.cmd == 'show':
            return self.show()
        elif self.cmd == 'scene':
            return self.scene()
        elif self.cmd == 'hide':
            return self.hide()
        else:
            raise RenderException("不存在的Image指令:{}".format(self.cmd))


# 转场
class Transition(RpyElement):

    def __init__(self, style):
        """
        :param style: 转场效果：dissolve (溶解)、fade (褪色)、None (标识一个特殊转场效果,不产生任何特使效果)
        """
        self.style = style

    def render(self):
        return "with {}".format(self.style) if self.style else ""


# 音效
class Audio(RpyElement):

    def __init__(self, name, cmd, fromto="", fadeinout=";", **args):
        """
        :param name: 音效名
        :param cmd: 指令
        :param args: 参数 fadeout/fadein: 音乐的淡入淡出  next_audio:下一个音效
        """
        if isinstance(name, float):
            self.name = str(int(name))
        elif isinstance(name, int):
            self.name = str(name)
        else:
            self.name = name
        # - 首先先确保转换名字为字符型

        # 针对大写
        if self.name.split(".")[-1].lower() != 'mp3':
            self.name += ".mp3"


        self.name = "audio/" + self.name    # 路径名称
        self.cmd = cmd
        self.fromto = fromto
        self.fadeinout = fadeinout

        self.next_audio = args.get("next_audio")

    # 循环播放音乐
    def play(self):
        musiccatstr = []
        if self.fromto:
            #musiccatstr = []
            musiccatstr.append("play music \"<from {tstart} to {tend}>{musicname}\" ".format(tstart=self.fromto.split(";")[0], tend=self.fromto.split(";")[1], musicname=self.name))
            if self.fadeinout:
                if self.fadeinout.split(";")[0]:
                    musiccatstr.append("fadein {fadein} ".format(fadein=self.fadeinout.split(";")[0]))
                if self.fadeinout.split(";")[1]:
                    musiccatstr.append("fadeout {fadeout} ".format(fadeout=self.fadeinout.split(";")[1]))
            musiccatstrout = "".join(musiccatstr)
            #return musiccatstrout
        else:
            #musiccatstr = []
            musiccatstr.append(
                "play music \"{musicname}\" ".format(musicname=self.name))
            if self.fadeinout:
                if self.fadeinout.split(";")[0]:
                    musiccatstr.append("fadein {fadein} ".format(fadein=self.fadeinout.split(";")[0]))
                if self.fadeinout.split(";")[1]:
                    musiccatstr.append("fadeout {fadeout} ".format(fadeout=self.fadeinout.split(";")[1]))
            musiccatstrout = "".join(musiccatstr)
            #return musiccatstrout
        return musiccatstrout

    # 用于旧音乐的淡出和新音乐的淡入
    def fade(self):
        return self.play() + "fadeout {fadeout} fadein {fadein}".format(fadeout=self.fadeout, fadein=self.fadein)

    # 当前音乐播放完毕后播放的音频文件
    def queue(self):
        if self.next_audio:
            return "queue \"{audio_name}\"".format(audio_name=self.next_audio.name)
        else:
            return self.play()

    # 不会循环播放
    def sound(self):
        return "play sound \"{}\"".format(self.name)

    # 不会循环播放
    def loop(self):
        return self.sound() + " loop"

    # 停止播放音乐
    def stop(self):
        return "stop music"

    # 下面这些也就是写法
    def render(self):
        if self.cmd == 'play':
            return self.play()
        elif self.cmd == 'fade':
            return self.fade()
        elif self.cmd == 'queue':
            return self.queue()
        elif self.cmd == 'sound':
            return self.sound()
        elif self.cmd == 'stop':
            return self.stop()
        elif self.cmd == 'loop':
            return self.loop()
        else:
            raise RenderException("不存在的Audio指令:{}".format(self.cmd))


class Mode(RpyElement):

    def __init__(self, mode):
        self.mode = mode

    def render(self):
        if self.mode in ['nvl', 'adv']:
            return ''
        else:
            return 'nvl clear'


class Voice(RpyElement):
    def __init__(self, name, sustain=False):
        self.name = name
        self.sustain = sustain
        # - sustain属性取决于调用是否有给

    def render(self):
        return 'voice "{}"'.format(self.name)
        # - 简单地写上罢了

class Menu(RpyElement):
    def __init__(self, label, target):
        self.label = label
        self.target = target
    # - 就是个简单转换罢了

# 自定义指令
class Command(RpyElement):
    def __init__(self, cmd):
        self.cmd = cmd

    def render(self):
        return self.cmd
    # - 就是个简单转换罢了
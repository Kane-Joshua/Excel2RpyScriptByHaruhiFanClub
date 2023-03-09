# RPY元素与sheet中每列的对应关系
from model.element import Text, Image, Transition, Audio

ElementColNumMapping = {
    'role_name': 0,
    'text': 1,
    'music': 2,

    'fromto': 3,
    'fadeinout': 4,

    'character': 5,

    'xforma':6,

    'change_page': 7,
    'background': 8,
    'remark': 9,
    'mode': 10,
    'sound': 11,
    'transition': 12,
    'special': 13,
    'voice': 14,
    'menu': 15,
    'side_character': 16,

    'fixpronoun': 17,
    'char_color': 18,
    'char_whocolor': 19,
    'char_whatcolor': 20,
    'char_voicetag': 21,
    'char_whatprefix': 22,
    'char_whatsuffix': 23,
}


# 元素映射
ElementMapping = {
    "文本": Text,
    "立绘": Image,
    "背景": Image,
    "转场": Transition,
    "音效": Audio,
}

# 位置映射
PositionMapping = {
    "left": "left",
    "right": "right",
    "mid": "center",
    "truecenter": "truecenter",
}

# 图片指令
ImageCmdMapping = {
    "hide": "hide",
}

# 转场指令
TransitionMapping = {
    "溶解": "dissolve",
    "褪色": "fade",
    "闪白": "Fade(0.1,0.0,0.5,color=\"#FFFFFF\")",
    "像素化": "pixellate",
    "横向振动": "hpunch",
    "纵向振动": "vpunch",
    "百叶窗": "blinds",
    "网格覆盖": "squares",
    "擦除": "wipeleft",
    "滑入": "slideleft",
    "滑出": "slideawayleft",
    "推出": "pushright",
}

# 音效指令
SoundCmdMapping = {
    "循环": "loop"
}

ReplaceCharacterMapping = {
    "%": "\\%",  # % --> \%
    "\"": "\\\"",  # " -> \"
    "\'": "\\\'",  # ' -> \'
    #"{": "{{",  # { -> {{
    #"[": "[[",  # [ -> [[
}

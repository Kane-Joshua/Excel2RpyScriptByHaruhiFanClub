#!/usr/bin/env python
# -*- coding:utf-8 -*-
MENU_TEMPLATE = "    \"{label}\":\n        jump {target}\n" #选择肢菜单模板
SIDE_CHARACTER_TEMPLATE = "image side {role_name} = \"{path}\"\n"   #头像模板


class RpyFileWriter(object):

    @classmethod
    def write_file(cls, output_dir, res, role_name_mapping, role_side_character_mapping):
        output_path = output_dir + "/" + res.label + '.rpy' #输出的表名
        with open(output_path, 'w', encoding='utf-8') as f:
            # - 各自开一个.rpy文件
            for k, v in role_name_mapping.items():
                f.write(v.render() + "\n")
            # - 上面这个是写自定义的角色的
            # - 把内容用render方法写下
            # 下面这三个是固定写入的
            f.write("define narrator_nvl = Character(None, kind=nvl)\n")
            f.write("define narrator_adv = Character(None, kind=adv)\n")
            f.write("define config.voice_filename_format = \"audio/{filename}\"\n")

            for k, v in role_side_character_mapping.items():
                f.write(SIDE_CHARACTER_TEMPLATE.format(role_name=k, path=v))
            # - 这个是写角色头像模板的

            f.write("\nlabel {}:\n".format(res.label))
            last_voice = None
            current_menus = []  #选择肢菜单

            # 下面就开始对所有内容逐行写入
            # - 有些是依据情况、手动调整，有些是借助各元素类属性中的render（不尽相同）来实现
            for rpy_element in res.data:
                # - data是res的属性
                # - res还有很多属性，比如下面的menu、music，etc
                # - 这些属性是由对应类产生的，有各自的类内render函数
                if rpy_element.menu:
                    current_menus.append(rpy_element.menu)
                    continue

                # - 如果这个标签名属于renpy保留标签名（？）
                if current_menus:
                    # 但是menu是没有render函数的，所以要手动写，等于把上面那个模板打上去
                    f.write("menu:\n" + "\n".join(
                        [MENU_TEMPLATE.format(label=m.label, target=m.target) for m in current_menus]))
                        # - 可以看到是选择肢模板，对应模板中元素，一个选项对应一个label一个target
                        # - 两行跳转，可能是空一行出来给写文字？
                    current_menus.clear()
                    continue

                if rpy_element.music:
                    f.write(rpy_element.music.render() + '\n')
                    # - music属性用自带render写入

                if rpy_element.character:
                    for ch in rpy_element.character:
                        f.write(ch.render() + '\n')
                    # - character属性，每个角色ch用自带的render写
                if rpy_element.background:
                    f.write(rpy_element.background.render() + '\n')
                    # - background用render写入
                if rpy_element.sound:
                    f.write(rpy_element.sound.render() + '\n')
                    # - sound用render写入
                if rpy_element.transition:
                    f.write(rpy_element.transition.render() + '\n')
                    # - 转场用render写入
                if rpy_element.voice:
                    f.write(rpy_element.voice.render() + '\n')
                    # - voice用render写入
                if rpy_element.text:
                    if last_voice and last_voice.sustain:
                        # - last_voice <- rpy_element.voice应该是有一个sustain的标志
                        f.write("voice sustain\n")
                    f.write(rpy_element.text.render() + '\n')

                if rpy_element.change_page:
                    f.write(rpy_element.change_page.render() + '\n')

                last_voice = rpy_element.voice
                # - 永远记录当前（上一句话）

            if current_menus:
                # fix menu在最后一行
                # - 可能就是说最后一个跳转没能读到？
                f.write("menu:\n" + "\n".join(
                    [MENU_TEMPLATE.format(label=m.label, target=m.target) for m in current_menus]))
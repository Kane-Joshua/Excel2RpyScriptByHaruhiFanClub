define XTag1 = Character('测试名称1', color="#aabb00", who_color="#aabb00", what_color="#aabb00", voice_tag="XTag1vo", what_prefix="【", what_suffix="】", image="XTag1")
define XTag2 = Character('测试名称2', color="#00bbcc", who_color="#00bbcc", voice_tag="XTag2vo", what_prefix="Echo", what_suffix="desu", image="XTag2")
define role3 = Character('aaa', color="#c8c8ff", image="role3")
define role4 = Character('aaabv', color="#c8c8ff", image="role4")
define role5 = Character('阿虚', color="#c8c8ff", image="role5")
define role6 = Character('春日', color="#c8c8ff", image="role6")
define role7 = Character('春日bbbb', color="#c8c8ff", image="role7")
define narrator_nvl = Character(None, kind=nvl)
define narrator_adv = Character(None, kind=adv)
define config.voice_filename_format = "audio/{filename}"
image side role3 = "images/haruhi 1.png"

label start:
play music "<from 114 to 514>audio/19.mp3" fadein 1.0 fadeout 5.0 
show haruhi 1 at left
scene bg34
with dissolve
narrator_nvl "\"喂，你们知道肾上腺素这种东西吗？\""
narrator_nvl "\"没错，就是那种当人遭遇某种突如其来的刺激时才会分泌，可以使人呼吸加快、心跳加速、瞳孔放大，激发身体潜能好应对可能发生的事情的那种激素。\""
XTag1 "\"如果现在我的身上有那么一个用来测量这种激素浓度的仪器，那么上面的数字恐怕一定是在不断地飙升的吧——\""
nvl clear
narrator_nvl "\"什么？你问我怎么知道？\""
XTag2 "\"因为现在的我正带着着自己越来越沉重的呼吸，在心脏以超常速度泵出来的血液和随着时间的推进而不断绷紧的神经的伴随下，\n和那个名叫凉宫春日的女人缓慢地穿行在空旷且黑暗的隧道里。 \""
stop music
play sound "audio/zou_lu_1.mp3" loop
narrator_adv "\"不错，到目前为止我和春日已经沿着隧道壁走了半个小时， 但仍没有一点要找到出口的迹象。\""
play music "audio/19.mp3" fadein 1.0 
hide haruhi 1
show haruhi 1 at predefxform
show kyon:
    xpos 0.5
    yalign 0.7
hide minamisawa
show mononobe:
    punch with 
    whatever word you say
with dissolve
narrator_adv "\"包裹在右手上的外套一直摩擦着粗糙的岩壁，回音在隧道里相互叠加不断传递 ，最终汇聚成了一股丝毫都不悦耳、反而让人愈加烦躁的声音。 \""
narrator_adv "\"如果这是一个恐怖游戏的关卡，那么我一定要提名它拿今年科隆游戏展的最佳恐怖游戏配音奖——如果有这个奖项的话。\""
play music "audio/20.mp3" 
XTag1 "\"就在我试图用一些轻松一点的想法冲淡自己的紧张，尽量不让自己在逃出去之前就被自己的肾上腺素毒死之时，我那紧紧握着春日右手的左手，又一次感受到了来自春日那微微地握力。 \""
XTag2 "\"不仅是我，就连平日里元气十足、坐镇北高文学部部室四处征伐的团长大人，此刻也通过手心里微微渗出的汗滴来委婉地告诉我她的不安。\""
narrator_adv "\"而这时不时传来的、看似微弱但却异常敏感的身体信号，则更是从频率上在暗示着她和我一样不断加重的负面情绪。\""
role3 "\"从刚刚开始，我们就一直拉着手——像是在孤岛那会儿一样，只不过这次面对的，似乎是更加未知的前景。\""
narrator_adv "\"我对春日报以相同的回应，也握了握她的手。\""
XTag1 "\"老实说，我并不怀疑春日这难得的、稳扎稳打的脱险方法，更坚信走出去只是迟早的事情——但不知为什么，不安和焦虑，却顽固地笼罩在我心里这个看似光明的信念上，挥之不去。\""
menu:
    "跳转到Sheet2":
        jump Sheet2

    "跳转到Sheet3":
        jump Sheet3

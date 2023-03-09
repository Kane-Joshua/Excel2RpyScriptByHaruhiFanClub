# Excel文件转Rpy脚本(0.2.4(-mk4))

## 开发环境
- Python 3.8
-> Python 3.10.9(-mk4)

## 模块划分
```
|
|-corelib 基础依赖
     |-- exception  自定义的异常
|-dist 打包的exe文件
|-handler
     |-- converter  将Excel中的数据转化为rpy中的对象
     |-- render     将model中的元素与进程控制渲染成Rpy脚本文件
|-model
     |-- element Rpy游戏的基本元素
     |-- process Rpy游戏的进程控制
|--tools  工具类
|--app.py 程序入口
```


## 打包程序
- 工具: pyinstaller  
- CMD: `pyinstaller -F -w -i .\asset\sos.ico .\app.py -n Excel2RpyScript`

## relase notes
- 0.1.1
    - fix [立绘回收 #20](https://github.com/HaruhiFanClub/Excel2RpyScript/issues/20)
    - fix [Nvl模式与adv模式的切换 #19](https://github.com/HaruhiFanClub/Excel2RpyScript/issues/19)
    - 去掉Exe文件的外部依赖

- 0.2.4
    - fix 条件选择在最后一行时无法读取
    - 支持对话框头像
  
- 0.2.4(mk1-mk4)
    - mk1-mk4均未测试且屎山，欢迎反馈。
    - mk4对mk1为包含关系，想要测试请直接测试mk4
    - mk1
        - 重新编排了行列和表格
        - 删除了文字对话中{->{{、[->[[的替换映射
    - mk2
        - 支持了在表格中，角色首次登场时，可以在当行设置该角色的更多信息
          - 角色的固定tag
          - 角色颜色（可能与后面的文字颜色冲突），角色姓名框文字颜色，角色对话文字颜色
          - 角色语音通道标志
          - 角色对话前缀、角色对话后缀
    - mk3
        - 支持了在表格中，通过transform名称，对登场的人物立绘应用预先定义好的transform。（支持同一屏幕多个立绘单独应用）
        - 支持了在表格中，即时为人物立绘编写transform。（支持同一屏幕多个立绘单独应用）
    - mk4
        - 支持了在表格中，对音乐（仅音乐，不包括音效和语音）的循环内容的段选
        - 支持了在表格中，对音乐的渐入渐出的具体时间设置。（可单独设置渐入或渐出）
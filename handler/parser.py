#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import namedtuple

from const.parser_setting import EXCEL_PARSE_START_ROW, EXCEL_PARSE_START_COL
from corelib.exception import ParseFileException
from tools.excel import read_excel

# 解析结果(sheet粒度)，包含sheet和数据
SheetParseResult = namedtuple('ParseResult', ['name', 'row_values'])


class Parser(object):
    """
    Excel解析器
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_excel_wb(self):
        """
        解析文件
        :return RpyElement列表
        """
        try:
            wb = read_excel(self.file_path)
            # - 总之就是读入工作表打开
        except ParseFileException as err:
            raise err
        return wb

    def get_parsed_sheets(self):
        """
        解析文件
        :return RpyElement列表
        """
        wb = self.get_excel_wb()
        # - wb会有sheets属性
        result = []
        for sheet in wb.sheets():
            result.append(SheetParseResult(name=sheet.name, row_values=self.parse_sheet(sheet)))
            # - 堆叠对应子表名下的所有行
        return result

    def parse_sheet(self, sheet):
        result = [] # 函数方法服用变量*就是说在其他地方会有多个同名不同类不通用途的变量
        for i in range(EXCEL_PARSE_START_ROW, sheet.nrows):
            # - nrows 是sheet可被读出的属性
            data = [r.value for r in sheet.row(i)]
            # - 读取每行的所有数据
            # - row 是sheet可被读出的属性/操作句柄
            if not any(data):
                continue
            # - 如果当前工作表所有行为空，则跳过当轮（行）（指for循环中的某轮）
            if len(data) < EXCEL_PARSE_START_COL:
                # - 对于在要读取列内的左右列
                # 补全数据【？】这是要补全什么？
                data.extend(["" for i in range(EXCEL_PARSE_START_COL - len(data))])
                # - 列表内数据补全，补一个""不存在
            assert len(data) == EXCEL_PARSE_START_COL
            # - 一个预判断异常的状况，不满足条件的时候直接触发一场终止程序，而不必要等执行到相关错误再停止
            result.append(data)
            # - 在result列表中堆叠data的列表
        return result

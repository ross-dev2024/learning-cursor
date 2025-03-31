#!/usr/bin/env python3
import csv
import re
from datetime import datetime

def convert_date(date_string):
    """
    日付文字列を YYYY-MM-DD 形式に変換する関数
    対応フォーマット：
    - YYYY/MM/DD
    - YYYY-MM-DD
    - MM/DD/YYYY
    - MM-DD-YYYY
    - MM.DD.YYYY
    - 英語の月名 DD, YYYY
    - YYYY年MM月DD日
    """
    if re.match(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', date_string):
        return datetime.strftime(datetime.strptime(date_string, '%Y/%m/%d'), '%Y-%m-%d')
    elif re.match(r'\d{1,2}[-/.]\d{1,2}[-/.]\d{4}', date_string):
        try:
            return datetime.strftime(datetime.strptime(date_string, '%m-%d-%Y'), '%Y-%m-%d')
        except ValueError:
            return datetime.strftime(datetime.strptime(date_string, '%m.%d.%Y'), '%Y-%m-%d')
    elif re.match(r'[A-Za-z]+ \d{1,2}, \d{4}', date_string):
        return datetime.strftime(datetime.strptime(date_string, '%B %d, %Y'), '%Y-%m-%d')
    elif re.match(r'\d{4}年\d{1,2}月\d{1,2}日', date_string):
        return datetime.strftime(datetime.strptime(date_string, '%Y年%m月%d日'), '%Y-%m-%d')
    else:
        return date_string

def process_csv(input_file, output_file):
    """
    CSVファイルの日付列を YYYY-MM-DD 形式に変換する関数
    """
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    for i in range(len(data)):
        data[i][0] = convert_date(data[i][0])

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == '__main__':
    input_file = 'data.csv'
    output_file = 'data_out.csv'
    process_csv(input_file, output_file) 
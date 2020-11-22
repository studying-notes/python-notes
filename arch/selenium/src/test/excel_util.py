from itertools import islice
from openpyxl import load_workbook



def get_data_from_sheet(excel_path, sheet_name):
    wb = load_workbook(excel_path, read_only=True)
    sheet = wb[sheet_name]
    data_list = [ ]
    for line in islice(sheet.rows, 1, None):
        tmp_list = [ ]
        tmp_list.append(line[1].value)
        tmp_list.append(line[2].value)
        data_list.append(tmp_list)
    return data_list


if __name__ == '__main__':
    excel_path = 'data.xlsx'
    sheet_name = '搜索数据表'
    for i in get_data_from_sheet(excel_path, sheet_name):
        print(i[0], i[1])

import xlsxwriter
from scraping import array


def writer(p):
    book = xlsxwriter.Workbook(
        r"C:\Users\Админ\Desktop\projects_from_github\trial_parsingauthoriz\data.xlsx")
    page = book.add_worksheet('product')

    row = 0
    column = 0

    page.set_column('A:A', 20)
    page.set_column('B:B', 50)
    page.set_column('C:C', 56)
    page.set_column('D:D', 18)
    page.set_column('E:E', 67)

    for i in p():
        page.write(row, column, i[0])
        page.write(row, column+1, i[1])
        page.write(row, column+2, i[2])
        page.write(row, column+3, i[3])
        page.write(row, column+4, i[4])
        row += 1
    book.close()


if __name__ == '__main__':
    writer(array)

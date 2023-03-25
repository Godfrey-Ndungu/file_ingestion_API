import csv
import xlrd


class FileReader:
    @staticmethod
    def read_file(file_path):
        extension = file_path.split(".")[-1]
        if extension == "csv":
            return FileReader.read_csv_file(file_path)
        elif extension in ["xls", "xlsx"]:
            return FileReader.read_excel_file(file_path)
        else:
            raise ValueError(f"Invalid file extension: {extension}")

    @staticmethod
    def read_csv_file(file_path):
        with open(file_path, mode="r") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
            return rows

    @staticmethod
    def read_excel_file(file_path):
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)
        rows = []
        for row_idx in range(1, sheet.nrows):
            row = {}
            for col_idx in range(sheet.ncols):
                key = sheet.cell_value(0, col_idx)
                val = sheet.cell_value(row_idx, col_idx)
                row[key] = val
            rows.append(row)
        return rows

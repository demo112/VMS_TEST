import os

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# print(PROJECT_PATH)


CSV_FILE_PATH = PROJECT_PATH + "\csv_file\\"
CSV_OUTPUT_PATH = PROJECT_PATH + "\csv_output\\"

if __name__ == '__main__':
    print(CSV_FILE_PATH)
    print(CSV_OUTPUT_PATH)

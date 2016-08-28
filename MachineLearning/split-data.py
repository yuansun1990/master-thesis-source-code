import pandas
import re
import string
import sys

"""split-data.py: split data into different classes according to labels"""
__author__ = "YuanSun"

def main(input_file, output_path):
    df = pandas.read_csv(input_file)
    n = max(df['label'].values)

    # split file according to labels
    for i in range(1, n+1):
        output_file = output_path + str(i) + '.txt'
        with open(output_file, "w") as f:
            for item in df['message'][df['label'] == i]:
                text = re.sub("http\S+", 'URLS', item)
                text = re.sub('[%s]' % string.digits, ' NUMBERS', text)
                f.write(text + '\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

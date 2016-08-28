import sys
import nltk
import string, re
import csv, pandas
import numpy

"""feature-extract.py: extract data with a features list"""
__author__ = "YuanSun"

# main
def main(feature_list_file, input_file, output_file):
    df_feature = pandas.read_csv(feature_list_file)
    feature_list = df_feature.values[:,0]
    feature_list = numpy.unique(feature_list).astype(numpy.str)
    print len(feature_list)

    colnames = ['label', 'id','message','source']
    data = pandas.read_csv(input_file, names=colnames)
    message = data.message.tolist()
    label = data.label.tolist()
    ids = data.id.tolist()

    # clean data, change urls to the string "URLS" and numbers to the string "NUMBERS"
    text = [re.sub("http\S+", 'URLS', t) for t in message]
    me_list = [re.sub('[%s]' % string.digits, ' NUMBERS', s) for s in text ] 

    fex_ma = []
    for me in me_list:
        fextract_list = []
        for fe in feature_list:
            if fe in me:
                fextract_list.extend("1")
            else:
                fextract_list.extend("0")
        fex_ma.append(fextract_list)

    print len(label)
    print len(ids)
    print len(fex_ma)

    all_list = numpy.column_stack((label, ids, fex_ma))
    print all_list
    with open(output_file, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(all_list)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

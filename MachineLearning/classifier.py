"""classifier.py: do text classification by SVM on unbalanced data, using sklearn, evaluate the classifier with 5/10 cross validation"""
__author__ = "YuanSun"

from __future__ import division

import sys
import random
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from sklearn import metrics, svm
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.cross_validation import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_decomposition import CCA

def evaluate(model, X, y, n_folds):
    sum_prec = 0
    sum_recall = 0
    sum_F1 = 0
    sum_accu = 0

    kf = KFold(len(y), n_folds=n_folds)
    for train, test in kf:
        # split data
        X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)

        sum_prec += metrics.precision_score(y_test, y_predict, pos_label=None, average='weighted')
        sum_recall += metrics.recall_score(y_test, y_predict, pos_label=None, average='weighted')
        sum_F1 += metrics.f1_score(y_test, y_predict, pos_label=None, average='weighted')
        sum_accu += metrics.accuracy_score(y_test, y_predict)

    print 'avg_precision =', sum_prec / n_folds
    print 'avg_recall =', sum_recall / n_folds
    print 'avg_F1 =', sum_F1 / n_folds
    print 'avg_accuracy =', sum_accu / n_folds

def plot_confusion_matrix(model, X, y, labels, file_name, category_name, n_folds):
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    n_labels = len(labels)
    cm = np.zeros([n_labels, n_labels])
    kf = KFold(len(y), n_folds=n_folds)
    for train, test in kf:
        # split data
        X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)

        # Compute confusion matrix
        cm += confusion_matrix(y_test, y_predict, labels=range(1, n_labels+1))
    	#cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.figure()
    if category_name == 'agent':
    	tit = 'Tweets for Agent'
    if category_name == 'agent_f':
    	tit = 'Forum Messages for Agent'
    if category_name == 'step':
    	tit = 'Tweets for Step'
    if category_name == 'step_f':
    	tit = 'Forum Messages for Step'
    if category_name == 'purpose':
    	tit = 'Tweets for Purpose'
    if category_name == 'purpose_f':
    	tit = 'Forum Messages for Purpose'
    if category_name == 'sentiment':
    	tit = 'Tweets for Sentiment'
    if category_name == 'sentiment_f':
    	tit = 'Forum Messages for Sentiment'

    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    # add numbers in the plot
    for i, cas in enumerate(cm):
    	for j, c in enumerate(cas):
       		if c>0:
            		plt.text(j-.2, i, c.astype(int), fontsize=14)

    plt.title('Confusion matrix of classifier on ' + tit)
    plt.colorbar()
    tick_marks = range(n_labels)
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    plt.savefig(file_name, format='png')


def plot_svm(model, X, y, title, file_name):
    C = 1.0  # SVM regularization parameter
    X = X[:, :2]
    model.fit(X, y)
    x_min, x_max = X[:, 0].min() - .1, X[:, 0].max() + .1
    y_min, y_max = X[:, 1].min() - .1, X[:, 1].max() + .1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure()

    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

    plt.title(title)
    plt.savefig(file_name, format='pdf')

def main(input_file, input_file_labels, category_name, output_path):
    # read labels
    df_labels = pd.read_csv(input_file_labels, sep='\s', header=None)
    labels = df_labels.values[0]

    data = pd.read_csv(input_file).values

    X = data[:,2:].astype(np.int)
    y = data[:,0].astype(np.int)

    # SVM model
    modelSVM = svm.SVC(kernel = 'linear', class_weight='balanced')

    print "Evaluating SVM, n_fold=5"
    evaluate(modelSVM, X, y, 5)
    print "Evaluating SVM, n_fold=10"
    evaluate(modelSVM, X, y, 10)
    print "Plotting confusion matrix for SVM ..."
    file_name = output_path + category_name + '-SVM.png'
    plot_confusion_matrix(modelSVM, X, y, labels, file_name, category_name, 5)

    print "Plotting SVM ..."
    file_name = output_path + category_name + '-plot_SVM.pdf'
    plot_svm(modelSVM, X, y, "svm", file_name)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

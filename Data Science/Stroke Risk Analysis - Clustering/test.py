from tokenize import Name
from myfunctions import execute_this
from scipy.spatial.distance import squareform
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from typing import NamedTuple
from statistics import mean, median, stdev
import time

Row = NamedTuple('Row', [("id", int), ("gender", str), ("hypertension", bool), ("heart_disease", bool), ("married", bool), ("work", str), ("smoking", str), ("stroke", bool), ("bmi", float), ("age", str), ("glucose", str), ("home", str)])


rows:list[Row]=[]
filtered_rows = []

diff= []


def read_jaccard():
    f = open('nonull.csv','r', encoding='utf-8')
    f.readline()
    t = 0
    for x in f:
        d = x.replace('\n','')
        row_data = d.split(',')[1:]
        marry = True if row_data[5][0] == 'Y' else False
        rows.append(Row(id=row_data[0], gender=row_data[1], age=row_data[13], hypertension=bool(int(row_data[3])), heart_disease=bool(int(row_data[4])), married=marry, work=row_data[6], home=row_data[7], glucose=row_data[14], bmi=row_data[12], smoking=row_data[10], stroke=bool(int(row_data[11]))))
    print(len(rows))

def calc_jaccard(row1:set, row2:set):
    return (len(row1.intersection(row2)) / len(row1.union(row2)))

def has_stroke_rows():
    for row in rows:
        if row.stroke is True:
            yield row

def no_stroke_rows():
    for row in rows:
        if row.stroke is False:
            yield row

def married_people_rows():
    for row in rows:
        if row.married is True:
            yield row

def unmarried_people_rows():
    for row in rows:
        if row.married is False:
            yield row

def elderly_people_rows(rows_to_search:list[Row] = None):
    if rows_to_search is None:
        for row in rows:
            if row.age[0] == "E":
                yield row
    else:
        for row in rows_to_search:
            if row.age[0] == "E":
                yield row


def heart_disease_people():
    for row in rows:
        if row.heart_disease is True:
            yield row

def overweight_and_obese_people():
    for row in rows:
        if row.bmi[0] == 'O':
            yield row

def younger_people():
    for row in rows:
        if row.age[0] != 'E':
            yield row

def formerly_smoked_people():
    for row in rows:
        if row.smoking[0] == 'f':
            yield row

def self_emp_people():
    for row in rows:
        if row.work[0] == 'S':
            yield row


def hypertension_people():
    for row in rows:
        if row.hypertension is True:
            yield row


def males():
    for row in rows:
        if row.gender[0] == 'M':
            yield row


def urban():
    for row in rows:
        if row.home[0] == 'U':
            yield row


def high_glucose():
    for row in rows:
        if row.glucose[0] == 'H' or row.glucose[0] == 'V':
            yield row

def very_high_glucose():
    for row in rows:
        if row.glucose[0] == 'V':
            yield row

def calc_diff_jaccard():
    similarites: list[list[float]] = []
    stroked_people = tuple(has_stroke_rows())
    for idx, married_person in enumerate(stroked_people):
        simis = []
        married_set = {married_person[x] for x in range(1, 12)}
        for i in range(idx + 1, len(stroked_people)):
            # print(calc_jaccard(married_set, {stroked_person[x] for x in range(1, 12)}))
            similarites.append(calc_jaccard(married_set, {stroked_people[i][x] for x in range(1, 12)}))
        
        # similarites.append(simis)

    print(mean(similarites))
    print(median(similarites))
    print(max(similarites))
    print(min(similarites))
    print(stdev(similarites))
    

        
    # for married_person in married_people:

    #     for stroked_peroson in have_stroke_rows:

    # for x, row in enumerate(rows):
    #     for c in range(x):
    #         temp.append(diff[c][x])
    #     for y in range(x, len(rows)):
    #         temp.append(calc_jaccard(row, rows[y]))
    #     diff.append(temp)
    #     temp=[]






@execute_this
def main():
    read_jaccard()
    calc_diff_jaccard()
    # ff = open('euclid_small.txt','w', encoding='utf-8')
    # for x in diff:
    #     string = ''
    #     for c in x: 
    #         if(c!=0): 
    #             string+=str(c)+'\t'
    #     ff.write(string+'\n')

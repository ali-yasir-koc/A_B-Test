import pandas as pd
import numpy as np
import os
import functions as f
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro
import scipy.stats as stats

path = "C:\\Users\\hseym\\OneDrive\\Masaüstü\\Yeni klasör\\sample data and codes\\bidding_AB_test"
os.chdir(path)
f.display()
""" Data Import and Explore """
data = pd.read_csv("control_group.csv", sep=";",parse_dates = ["Date"])
data.head()
test =  pd.read_csv("test_group.csv", sep=";",parse_dates = ["Date"])
test.head()
data.info()
test.info()
columns = ['Campaign Name', 'Date', 'Amount_Spent', 'Impressions', 'Reach', 'Website_Clicks',
            'Searches_Received', 'Content_Viewed', 'Added_Cart', 'Purchases']
data.columns = columns
test.columns = columns
data.dropna(inplace = True)
data.describe()
test.describe()

metric_columns=['Amount_Spent', 'Impressions', 'Reach', 'Website_Clicks',
            'Searches_Received', 'Content_Viewed', 'Added_Cart', 'Purchases']
test[metric_columns]=test[metric_columns].astype(float)

""" Calculate """
data["metric"] =(data["Impressions"]
                 *data["Reach"]
                 *data["Website_Clicks"]
                 *data["Searches_Received"]
                 *data["Content_Viewed"]
                 *data["Added_Cart"]
                 *data["Purchases"]
                 )/data["Amount_Spent"]

test["metric"] =(test["Impressions"]
                 *test["Reach"]
                 *test["Website_Clicks"]
                 *test["Searches_Received"]
                 *test["Content_Viewed"]
                 *test["Added_Cart"]
                 *test["Purchases"]
                 )/test["Amount_Spent"]

""" Assignment of Groups """
group_a = data["metric"]
group_b = test["metric"]

""" Assumption 1 : Normal Distribution """
group_a.plot.hist()
group_b.plot.hist()

test_ist_a, p_value_a  = shapiro(group_a)
test_ist_b, p_value_b  = shapiro(group_b)
print("p value of a group = %.4f" % (p_value_a))
print("p value of b group = %.4f" % (p_value_b))                                                                        ### yani bunlar normal dağılmıyor.

""" Assumption 2 :Homogeneity"""
stats.levene(group_a,group_b)                                                                                           ### homojen dağılmıyor

""" Nonparametic t Test """
stats.mannwhitneyu(group_a,group_b)

## So, these biddings are not similar.
df = pd.DataFrame({"Groups":["A","B"],
                   "Mean":[group_a.mean(), group_b.mean()],
                   "Median":[group_a.median(), group_b.median()]})
if df.Mean[0]>df.Mean[1]:
    print("Mean of group A is bigger than group B",)
else:
    print("Mean of group B is bigger than group A")




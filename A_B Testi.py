import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro, levene, kruskal

""" Import Data and Some Setting"""
f.display()
plt.style.use('fivethirtyeight')

data_ = pd.read_csv("WA_Marketing-Campaign.csv", sep=",")
data = data_.copy()

""" Exploring Data"""
print(data.describe().T)

data.groupby("Promotion").agg({"SalesInThousands":["count","mean","median"]})
data.groupby(["MarketSize","Promotion"]).agg({"SalesInThousands":["count","mean","median"]})

"""  ANOVA (Analysis of Variance)"""                                                                                     
""" 1-) Normality assumption - Graphics """
## 1- Histogram and boxplot
data.loc[data["Promotion"]==1,"SalesInThousands"].plot.hist()
data.loc[data["Promotion"]==2,"SalesInThousands"].plot.hist()
data.loc[data["Promotion"]==3,"SalesInThousands"].plot.hist()

sns.boxplot(x=data.Promotion, y=data.SalesInThousands, data=data)

## 1- qqplot
fig , axs = plt.subplots(1,3,figsize=(15,5))

qqplot(np.array(data.loc[(data["Promotion"] == 1), "SalesInThousands"]), line="s", ax=axs[0])
qqplot(np.array(data.loc[(data["Promotion"] == 2), "SalesInThousands"]), line="s", ax=axs[1])
qqplot(np.array(data.loc[(data["Promotion"] == 3), "SalesInThousands"]), line="s", ax=axs[2])

axs[0].set_title("Promotion 1")
axs[1].set_title("Promotion 2")
axs[2].set_title("Promotion 3")

market_size = data["MarketSize"].unique()
for market_size in market_size:
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    qqplot(np.array(data.loc[(data["Promotion"] == 1) & (data["MarketSize"] == market_size), "SalesInThousands"]), line="s",
           ax=axs[0])
    qqplot(np.array(data.loc[(data["Promotion"] == 2) & (data["MarketSize"] == market_size), "SalesInThousands"]), line="s",
           ax=axs[1])
    qqplot(np.array(data.loc[(data["Promotion"] == 3) & (data["MarketSize"] == market_size), "SalesInThousands"]), line="s",
           ax=axs[2])

    axs[0].set_title("Promotion 1")
    axs[1].set_title("Promotion 2")
    axs[2].set_title("Promotion 3")

    fig.suptitle(f"QQ-Plot by Sales & Promotion Types - {market_size} Market Size")

""" 1-) Normality assumption - Shapiro Wilk Test """

for promotion in list (data["Promotion"].unique()):
    pvalue = shapiro(data.loc[data["Promotion"] == promotion, "SalesInThousands"])[1]
    print("Promotion:", promotion, "p-value: %.4f" % (pvalue))

## p_value is smaller than 0.05.So, Null Hypotesis is rejected and variables do not distribute normally.

""" 2-) Variance Homogeneity - Levene Test """
test_stat, pvalue = levene(data.loc[data["Promotion"] == 1, "SalesInThousands"],
                           data.loc[data["Promotion"] == 2, "SalesInThousands"],
                           data.loc[data["Promotion"] == 3, "SalesInThousands"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
## This is second assumption and p_value is bigger than 0.05. So, we can say that variance of variables is homogenise.

""" 3-) Nonparametrik ANOVA Test - Kruskal Wallis """

kruskal(data.loc[data["Promotion"] == 1, "SalesInThousands"],
        data.loc[data["Promotion"] == 2, "SalesInThousands"],
        data.loc[data["Promotion"] == 3, "SalesInThousands"])
## We use non parametric test because variables do not distribute normally.
## p_value is smaller than 0.05 and we can say that there is statistics important differences between promotions means.



data.groupby("Promotion").agg({"SalesInThousands":["count","mean","median"]})
data.groupby(["MarketSize","Promotion"]).agg({"SalesInThousands":["count","mean","median"]})
## When we investigate the means of variables promotion 1 and promotion 3, they effect to sales quantities approximately similar for all market size.
## Also, promotion 3 can represented by median value for large market size and so we can say that promotion 3 is more effectively for large market size.
## And also, promotions 2 is worst campaign for this new product.



import pandas as pd
import numpy as np
import os
import functions as f
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu, f_oneway, kruskal

path='C:\\Users\\hseym\\PycharmProjects\\pythonProject1\\Test\\A_B Testi'
os.chdir(path)
os.getcwd()
f.display()
plt.style.use('fivethirtyeight')

data_ = pd.read_csv("WA_Marketing-Campaign.csv", sep=",")
data = data_.copy()

""" Exploring Data"""
print(data.describe().T)

data.groupby("Promotion").agg({"SalesInThousands":["count","mean","median"]})
data.groupby(["MarketSize","Promotion"]).agg({"SalesInThousands":["count","mean","median"]})

"""  ANOVA (Analysis of Variance)"""                                                                                      #It is used to compare the mean of more than two groups.
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
#p value 0.05den küçük olduğu için null hipoteizimizi reddediyoruz. (null=dağılım noramldir)

""" 2-) Variance Homogeneity - Levene Test """
test_stat, pvalue = levene(data.loc[data["Promotion"] == 1, "SalesInThousands"],
                           data.loc[data["Promotion"] == 2, "SalesInThousands"],
                           data.loc[data["Promotion"] == 3, "SalesInThousands"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# varyansları arasında bir fark yoktur. p value 0.05den büyük olduğu için.

""" 3-) Nonparametrik ANOVA Test - Kruskal Wallis """

kruskal(data.loc[data["Promotion"] == 1, "SalesInThousands"],
        data.loc[data["Promotion"] == 2, "SalesInThousands"],
        data.loc[data["Promotion"] == 3, "SalesInThousands"])
#ortalamları arasında fark anlamlı derecede vardır.p küçük 0.05 olduğu için

""" 4-) Tukey Test """

from statsmodels.stats.multicomp import MultiComparison
comparison = MultiComparison(data["SalesInThousands"], data["Promotion"])
tukey = comparison.tukeyhsd(0.05)
print(comparison.tukeyhsd(0.05))

data.groupby("Promotion").agg({"SalesInThousands":["count","mean","median"]})



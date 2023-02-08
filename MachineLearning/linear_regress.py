import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文

import constants


def mul_lr():
    filename = constants.ml_data_dir + constants.filename_ml_data
    pd_data=pd.read_excel(filename)
    print('pd_data.head(10)=\n{}'.format(pd_data.head(10)))
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
    sns.pairplot(pd_data, x_vars=['中证500','沪深300','上证50','上证180'], y_vars='上证指数',kind="reg", size=5, aspect=0.7)
    plt.show()#注意必须加上这一句，否则无法显示。

mul_lr()
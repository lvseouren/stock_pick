import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
import constants
from sklearn.model_selection import train_test_split #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  #线性回归
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

def save_model(name, var_name_list, value_list):
    filename = constants.ml_data_dir + name
    fp = open(filename, 'w')
    for i in range(0, len(value_list)):
        fp.write('%s %s\n' %(var_name_list[i], value_list[i]))
    fp.close()

def mul_lr_3yang():
    filename = constants.ml_data_dir + constants.ml_excel_name
    pd_data=pd.read_excel(filename)
    print('pd_data.head(10)=\n{}'.format(pd_data.head(10)))
    mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
    sns.pairplot(pd_data, x_vars=['x1','x2','x3','x4','x5','x6','x7','x8','x9'], y_vars='y',kind="reg", aspect=0.7)
    plt.show()#注意必须加上这一句，否则无法显示。
    # 剔除日期数据，一般没有这列可不执行，选取以下数据http://blog.csdn.net/chixujohnny/article/details/51095817
    X = pd_data.loc[:, ('x1','x2','x3','x4','x5','x6','x7','x8','x9')]
    y = pd_data.loc[:, 'y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    print('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,
                                                                                              y_train.shape,
                                                                                              X_test.shape,
                                                                                              y_test.shape))
    linreg = LinearRegression()
    model = linreg.fit(X_train, y_train)
    print(model)
    # 训练后模型截距
    print(linreg.intercept_)
    # 训练后模型权重（特征个数无变化）
    print(linreg.coef_)

    feature_cols = ['x1','x2','x3','x4','x5','x6','x7','x8','x9', 'y']
    B=list(zip(feature_cols,linreg.coef_))
    print(B)
    save_model(constants.ml_model_file_name, feature_cols, linreg.coef_)
    #预测
    y_pred = linreg.predict(X_test)
    print (y_pred) #10个变量的预测结果
    #评价
    #(1) 评价测度
    # 对于分类问题，评价测度是准确率，但这种方法不适用于回归问题。我们使用针对连续数值的评价测度(evaluation metrics)。
    # 这里介绍3种常用的针对线性回归的测度。
    # 1)平均绝对误差(Mean Absolute Error, MAE)
    # (2)均方误差(Mean Squared Error, MSE)
    # (3)均方根误差(Root Mean Squared Error, RMSE)
    # 这里我使用RMES。
    sum_mean=0
    for i in range(len(y_pred)):
        sum_mean+=(y_pred[i]-y_test.values[i])**2
    sum_erro=np.sqrt(sum_mean/10)  #这个10是你测试级的数量
    # calculate RMSE by hand
    print ("RMSE by hand:",sum_erro)
    #做ROC曲线
    plt.figure()
    plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
    plt.plot(range(len(y_pred)),y_test,'r',label="test")
    plt.legend(loc="upper right") #显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()

def mul_lr_3yang1tiao():
    filename = constants.ml_data_dir + constants.ml_excel_name_3yang1tiao
    pd_data = pd.read_excel(filename)
    print('pd_data.head(10)=\n{}'.format(pd_data.head(10)))
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号，如果是plt画图，则将mlp换成plt
    sns.pairplot(pd_data, x_vars=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21'], y_vars='y', kind="reg",
                 aspect=0.7)
    plt.show()  # 注意必须加上这一句，否则无法显示。
    # 剔除日期数据，一般没有这列可不执行，选取以下数据http://blog.csdn.net/chixujohnny/article/details/51095817
    X = pd_data.loc[:, ('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21')]
    y = pd_data.loc[:, 'y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    print('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,
                                                                                              y_train.shape,
                                                                                              X_test.shape,
                                                                                              y_test.shape))
    linreg = LinearRegression()
    model = linreg.fit(X_train, y_train)
    print(model)
    # 训练后模型截距
    print(linreg.intercept_)
    # 训练后模型权重（特征个数无变化）
    print(linreg.coef_)

    feature_cols = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'y']
    B = list(zip(feature_cols, linreg.coef_))
    print(B)
    save_model(constants.ml_model_file_name_3yang1tiao, feature_cols, linreg.coef_)
    # 预测
    y_pred = linreg.predict(X_test)
    print(y_pred)  # 10个变量的预测结果
    # 评价
    # (1) 评价测度
    # 对于分类问题，评价测度是准确率，但这种方法不适用于回归问题。我们使用针对连续数值的评价测度(evaluation metrics)。
    # 这里介绍3种常用的针对线性回归的测度。
    # 1)平均绝对误差(Mean Absolute Error, MAE)
    # (2)均方误差(Mean Squared Error, MSE)
    # (3)均方根误差(Root Mean Squared Error, RMSE)
    # 这里我使用RMES。
    sum_mean = 0
    for i in range(len(y_pred)):
        sum_mean += (y_pred[i] - y_test.values[i]) ** 2
    sum_erro = np.sqrt(sum_mean / 10)  # 这个10是你测试级的数量
    # calculate RMSE by hand
    print("RMSE by hand:", sum_erro)
    # 做ROC曲线
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()

# mul_lr_3yang()
# mul_lr_3yang1tiao()
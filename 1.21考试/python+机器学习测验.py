## python选择题
# **1.** 下面4个程序片段，有 ___A_____ 个语法错误。


if { }:
    print("ok")

if ( ):
    print("ok")

if [ ]:
    print("ok")

if not "":
    print("ok")

# A) 0　 B) 1　 C) 2　 D) 3



# **2.** 以下程序共输出 ___b_____ 行 “ok”。


for i in range(8,2,-2):
    for j in range(i):
        print("ok")


# A) 0　 B) 12　 C) 18　 D) 20



# **3.** 以下程序中 print 执行的次数是 ____C____。


for i in range(1,3):
    for j in range(1,5):
        if i==j:
            continue
        print(i*j, end=" ")


# A) 15　 B) 8　 C) 6　 D) 1




# **4.** 以下程序的输出是 ____a____。


L = [1,2,3,4,5,6,7]
print(L[3:2], end=",")
print(L[-5:-3])


# A) [], [3,4]
#
# B) [3,4], []
#
# C) [3,4], [3,4]
#
# D) [], []



# **5.** 以下程序的输出是 ____c____。


b = sorted("This is a test string from Andrew".split(), key=str.lower)
print(b[-1])


# A) Andrew
#
# B) a
#
# C) This
#
# D) string



# **6.** 以下程序的输出是 ____b____。


x = 20
def f(a, b):
    x = b[0]
    b[0] = a
    a = x
c, d = 100, [1, 2]
f(c, d)
print(x, c, d[0])


# A) 1 100 100
#
# B) 20 100 100
#
# C) 20 100 1
#
# D) 1 100 1



# **7.** 以下程序的输出是 ____a____。


def change(x, i):
    x[0] = i
    x[i] = 0
x = list(range(100))
j = 7
print(x[j], end=',')
change(x, j)
print(x[j])


# A) 7,0
# B) 0,7
# C) 7,7
# D) 0,0



# **8.** 以下程序的输出是 ____C____。


def append_a(lst):
    t = lst
    t.append('a')
    return t

a = ['x', 'y', 'z']
b = append_a(a)
print(a, b)


# A) ['x','y','z'] ['x','y','z']
#
# B) ['x','y','z','a'] ['x','y','z','a']
#
# C) ['x','y','z'] ['x','y','z','a']
#
# D) ['x','y','z','a'] ['x','y','z']




## python程序分析
# **1.** 以下程序的功能是对随机产生的 1～100 之间的一个整数 n，利用二分法查找这个数并输出查找的次数。
# 请在横线上填写代码。


import random
import math
n = random.randint(1, 100)  # 函数 random.randint(a,b) 返回从 a 到 b 之间随机选出的一个整数
a, b, cnt = 1, 100, 0
while a<=b:
    cnt += 1
    m = math.ceil((a + b) / 2)  # 函数 math.ceil(x) 的返回值为数值 x 的向上取整
    if n < m:
        b = m - 1
    elif n>m:
        a = m + 1
    else:
        break
print(cnt)




# **2.** 以下程序读入正整数 n，计算
# S = 1! − 2! + 3! − 4! + 5! − …… ± n!
# 并输出。请在横线上填写代码。


n = int(input())
S = __________
sign = 1
k = __________
for i in range(_____________):
    k = __________
    S += sign * k
    sign = __________
print(S)


# **3.** 下面程序中的 `Change` 函数的功能是将十进制数转化 N 进制数（2 <= N <= 16）。
# 输入目标进制和待转换的数，函数返回转换后的目标进制数。
# 请在横线上填写代码并给出程序的输出结果。


def Change(radix, num):
    g = []
    while num != 0:
        r = num % radix
        num = num // radix
        g.append(r)
    ans = ''
    t = ('A', 'B', 'C', 'D', 'E', 'F')
    for x in range(len(g)):
        if g[x] >= 10:
            ans += t[j[x]-10]
        else:
            ans += str(g[x])
    return ans [::1]
print(Change(16, 12455))


程序输出：__________



# **4.** 给定一个整数的数字列表 L，判断 L 中是否存在相同数字，若存在返回 True，否则返回 False。
# 请在横线上补全代码。


def identical(L):
    flag = 0
    L.sort()
    for i in range(len(L-1)):
        if L[i] == L[i+1]:
            flag = 1
            break
    if flag:
        return True
    else:
        return False


# **5.** 程序填空。一个列表 `a` 中记录了连续多天的营业额，求其中最长的**连续增长（不含相等）**的子序列的长度。
# 例如 `[5, 1, 2, 3, 5, 9, 6, 7, 4, 6, 8]` 中最长的连续增长（不含相等）的子序列长度是 5（即 `[1, 2, 3, 5, 9]` 的长度）。


a = [5, 1, 2, 3, 5, 9, 6, 7, 4, 6, 8]
maxlen = 1
n = 1
for i in range(1,len(a) ):
    if a[i] > a[i-1]:
        n += 1
        if maxlen :
            maxlen =n
    else:
        n = 1
print(maxlen)

import pandas as pd

## Python数据分析（Pandas）

# 描述（Description）

# 你获得了一组包含出租车司机及其乘车信息的数据集。
# 你的任务是对这些数据进行一些基本分析，并将结果保存到一个 CSV 文件中。
#
# 数据包含在以下 CSV 文件中：

### `drivers.csv`

# * `driver_id`（类型：int）：司机唯一标识符
# * `age`（类型：int）：司机年龄
# * `second_language`（类型：str）：司机的第二语言。如果司机没有第二语言，值为 `"no"`
# * `rating`（类型：float）：司机的平均评分



### `rides_{i}.csv`

# 分成 4 个文件（`rides_1.csv` 到 `rides_4.csv`）：
#
# * `ride_id`（类型：int）：唯一的乘车标识符
# * `driver_id`（类型：int）：司机标识符
# * `passenger_id`（类型：int）：乘客标识符
# * `date`（类型：str）：乘车日期
# * `status`（类型：str）：乘车状态，可能的值包括
#
#   * `"Rejected by the driver"`（司机拒绝）
#   * `"Cancelled by the passenger"`（乘客取消）
#   * `"Success"`（成功）



### 你的任务如下：

### 1️⃣ 计算司机的平均评分（Average Driver Rating）

# * 从 `drivers.csv` 文件中计算 `rating` 列的平均值。
# * 将结果保存为：
#
#   * `insight_type`: `"average_driver_rating"`
#   * `value`: 计算出的平均评分
driver_csv = pd.read_csv('driver.csv')
driver_csv_mean = MT[rating].mean()



### 2️⃣ 计算拥有第二语言的司机比例（Percentage of Drivers with a Second Language）

# * 计算拥有第二语言的司机的比例（即 `second_language` 不为 `"no"` 的司机占总司机数的百分比）。
# * 将结果保存为：
#
#   * `insight_type`: `"percentage_drivers_with_second_language"`
#   * `value`: 计算出的百分比
no_second_lang_count = driver_csv['second_language'].isna().sum()
total_drivers = len(driver_csv)
has_second_lang_count = total_drivers - no_second_lang_count
second_lang_percent = round((has_second_lang_count / total_drivers) * 100, 2)
print(second_lang_percent)


### 3️⃣ 计算乘车成功率（Ride Success Rate）

# * 将所有 `rides_{i}.csv` 文件（从 1 到 4）合并为一个整体数据集。
# * 计算成功乘车（即 `status == "Success"`）的比例。
# * 将结果保存为：
#
#   * `insight_type`: `"ride_success_rate"`
#   * `value`: 计算出的百分比



### 输出要求（Output Requirements）

# * 将结果保存到一个名为 **`analysis_results.csv`** 的 CSV 文件中 （用代码保存）。
# * 该 CSV 文件应包含两列：
#
#   * `insight_type`
#   * `value`
# * 每一行对应一个任务结果，`insight_type` 为任务名称，`value` 为计算结果。
# * 所有数值在保留两位小数的范围内视为正确。
rides_1_csv = pd.read_csv('rides_1.csv')
rides_2_csv = pd.read_csv('rides_2.csv')
rides_3_csv = pd.read_csv('rides_3.csv')
rides_4_csv = pd.read_csv('rides_4.csv')
analysis_results_csv = pd.concat([rides_1_csv, rides_2_csv, rides_3_csv, rides_4_csv])
status_Success = analysis_results_csv[analysis_results_csv['status'] == 'Success']
status_len_bl = len(status_Success['status'])
status_len_bl_round = round(status_len_bl/len(analysis_results_csv)*100, 2)





## python机器学习

### 机器学习相关名词解释

# 1. 最常见的两种监督学习任务是什么？
# 2. 模型参数和模型超参数有什么区别？
# 3. 验证集的目的是什么？
# 4. 如果你的模型在训练数据上表现很好，但对新实例的泛化能力很差，这是怎么回事？你能说出三种可能的解决方案吗？
# 5. 交叉验证的过程是什么？


### 机器学习任务

# 任务：
# 使用线性回归 和决策树回归预测学生期末成绩，并比较模型性能。数据集采用UCI机器学习库中的"学生表现数据集"。  数据文件：student-mat.csv
#
# 实现步骤：
# 1. 将数据加载到Pandas DataFrame
student_mat_csv = pd.read_csv('student_mat.csv')
# 2. 分离特征(X)和目标变量(y)
# 3. 按80-20划分训练测试集(random_state=42)
# 4. 使用StandardScaler标准化特征
# 5. 训练以下模型：
#    - 线性回归
#    - 决策树回归
# 6. 计算各模型的MSE分数
# 7. 输出评估指标
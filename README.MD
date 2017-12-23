## 房屋租金预测模型

###我的思路是：
1.根据csv文件判断各类列表数据，挑选出与租金相关度最高的几个备用。
2.首先先清理数据 挑选出status=1的for rent进行计算，如果有时间再考虑status=[2,3,4,5]数据的rent, zetimate_rent列。
3.status=1一共有2239个数据，挑选前2000个进行建模，239个验证。
4.由于能力有限，我先挑选出了size, beds, bath三个重要类型，通过线性回归进行建模，得出各自的系数和截距。
5.将验证集代入模型计算模拟租金，与zetimate、rent列表分别进行方差分析，判断模型的误差。

----------
###结果如下：
test data lenth: 239					#测试集共239个数据
the variance sigma  :   263627.37		#模型的方差
the variance of rent:  1633624.44		#rent列与租金的方差

mine V.S. zetimate:						#对比模型与zetimate预估租金的方差
the variance of me      :  182238.44
the variance of zetimate: 2406692.62

----------

### 讨论
1.从方差结果来看，通过线性回归模型的预估，准确度是zestimate的13倍，是rent列的6倍。
2.但是结果远远不够准确，原始数据中仍有大量价值被浪费，还需要进一步优化。

### 改进思路
1.通过type列的数据，对于Apartment、Condo等不同类型进行分类，建立决策树模型，使租金的预估更加准确。
2.通过longitude、latitude经纬度数据，建立地价表，将不同地域的租金进行修正。
3.尝试利用year_built、year_refresh，对于房屋的建造、装修时间分析，但该类数据较少。
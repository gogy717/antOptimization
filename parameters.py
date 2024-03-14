import numpy as np
import matplotlib.pyplot as plt
from antOptimization import AntColony,AntTime

def generate_random_distance_matrix(size):
    # 生成一个随机的距离矩阵，矩阵大小为 size x size
    np.random.seed(42)  # 设置随机种子以确保结果的可重复性
    distances = np.random.uniform(1, 100, size=(size, size))  # 生成随机距离，范围1到100
    distances = np.round(distances, 2)

    distances = (distances + distances.T) / 2  # 使矩阵对称，确保距离的一致性
    np.fill_diagonal(distances, np.inf)  # 设置对角线为无穷大，表示自己到自己的距离
    return distances


# 生成80*80的随机距离矩阵
size = 80
distances = generate_random_distance_matrix(size)


excecution_time=[]
number_ants=[]
for i in range(1,100,5):
    ant_colony = AntTime(distances, n_ants=i, n_best=10,
                n_iterations=100, decay=0.5, alpha=1, beta=2)
    Time= ant_colony.run()
    number_ants.append(i)
    excecution_time.append(Time)

plt.figure()  # 设置图像大小
plt.bar(number_ants,excecution_time)  # 画柱状图，X轴是迭代次数，Y轴是距离值

# 设置图表标题和轴标签
plt.title(f'Iteration - number of ants')
plt.xlabel('number of Ants')
plt.ylabel('Excecution time')
# 显示图表
plt.show()


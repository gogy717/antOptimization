import numpy as np
import matplotlib.pyplot as plt
from antOptimization import AntColony

def generate_random_distance_matrix(size):
    # 生成一个随机的距离矩阵，矩阵大小为 size x size
    np.random.seed(42)  # 设置随机种子以确保结果的可重复性
    distances = np.random.randint(1, 100, size=(size, size))  # 生成随机距离，范围1到100
    distances = (distances + distances.T) / 2  # 使矩阵对称，确保距离的一致性
    np.fill_diagonal(distances, np.inf)  # 设置对角线为无穷大，表示自己到自己的距离
    return distances

# 生成80*80的随机距离矩阵
size = 80
distances = generate_random_distance_matrix(size)

# 打印生成的矩阵
print(distances)
# 设定迭代次数
iteration=50

ant_colony = AntColony(distances, n_ants=100, n_best=10,
                        n_iterations=iteration, decay=0.75, alpha=1, beta=2)
shortest_path,dis = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))

i = list(range(1,iteration+1))


plt.figure()  # 设置图像大小
plt.bar(i, dis)  # 画柱状图，X轴是迭代次数，Y轴是距离值

# 设置图表标题和轴标签
plt.title(f'Iteration ={iteration}')
plt.xlabel('Iteration')
plt.ylabel('Distance')
# 显示图表
plt.show()



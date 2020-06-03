# 首先导入包
import networkx as nx
import matplotlib.pyplot as plt


# 克隆
def clone_graph(G):
    cloned_graph = nx.Graph()
    for edge in G.edges():
        cloned_graph.add_edge(edge[0], edge[1])
    return cloned_graph


# 计算Q值
def cal_Q(partition, G):
    m = len(list(G.edges()))
    a = []
    e = []
    # 计算每个社区的a值
    for community in partition:
        t = 0
        for node in community:
            t += len(list(G.neighbors(node)))
        a.append(t / float(2 * m))

    # 计算每个社区的e值
    for community in partition:
        t = 0
        for i in range(len(community)):
            for j in range(len(community)):
                if i != j:
                    if G.has_edge(community[i], community[j]):
                        t += 1
        e.append(t / float(2 * m))
    # 计算Q
    q = 0
    for ei, ai in zip(e, a):
        q += (ei - ai ** 2)
    return q


class GN(object):
    def __init__(self, G):
        self._G_cloned = clone_graph(G)
        self._G = G
        self._partition = [[n for n in G.nodes()]]
        self._max_Q = 0.0

    # GN算法
    def execute(self):
        components = [list(c) for c in list(nx.algorithms.community.greedy_modularity_communities(G))]
        if len(components) != len(self._partition):
            # 3.计算Q值
            cur_Q = cal_Q(components, self._G_cloned)
            if cur_Q > self._max_Q:
                self._max_Q = cur_Q
                self._partition = components
        print("max Q:", self._max_Q)
        return self._partition


# 可视化划分结果


if __name__ == '__main__':
    # 加载网络并可视化
    G = nx.read_gml("homework_test.gml")
    T = nx.read_gml("homework_test.gml")


   #pos = nx.kamada_kawai_layout(T) #该布局需要下载额外的包scipy，同次运行时图布局不变
    pos = nx.spring_layout(T)

    # GN算法
    algo = GN(G)
    partition = algo.execute()
    print("community number:", len(partition))
    for i, nodes in zip(range(len(partition)), partition):
        print("community %d:" % i, nodes)

    # plotting

    plt.clf()

    colors = ['r', 'g', 'b', 'c', 'y', 'm']
    nx.draw(T, pos=pos, node_color='bisque', with_labels=True)
    for i in range(len(partition)):
        nx.draw(T, pos=pos, nodelist=partition[i], node_color=colors[i], node_shape='o')
    plt.show()
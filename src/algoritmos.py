NodeIndex = int
EdgeWeight = float
Edge = [NodeIndex, EdgeWeight]


class Grafo:
    adj: dict[NodeIndex, list[Edge]]
    n: NodeIndex

    def __init__(self):
        self.n = 0
        self.adj = {}

    def add_nodes(self, n: NodeIndex):
        for i in range(n):
            self.adj[i + self.n] = []
        self.n = self.n + n

    def add_edge(
        self,
        u: NodeIndex,
        v: NodeIndex,
        u_to_v: bool,
        v_to_u: bool,
        weight_u_to_v: float,
        weight_v_to_u: float,
    ):
        if u_to_v:
            edge: Edge = [v, weight_u_to_v]
            self.adj[u].append(edge)

        if v_to_u:
            edge: Edge = [u, weight_v_to_u]
            self.adj[v].append(edge)

    def get_distancia_dijkstra(u: NodeIndex, v: NodeIndex):
        pass

    def get_passos_dijkstra(u: NodeIndex, v: NodeIndex):
        pass

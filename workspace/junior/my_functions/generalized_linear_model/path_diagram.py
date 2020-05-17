import networkx as nx


def get():
    g = nx.DiGraph()
    g = nx.nx_agraph.to_agraph(g)

    g.add_node('x1', shape='box')
    g.add_node('x2', shape='box')
    g.add_node('…', shape='none')
    g.add_node('xk', shape='box')
    g.add_node('y', shape='box', label='f(z)->y')

    g.add_edges_from([['x1', 'y'], ['x2', 'y'], ['xk', 'y']])
    g.add_edge(['…', 'y'], color='white')

    return g.draw(format='png', prog='dot')
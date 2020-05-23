import networkx as nx


def get():
    g = nx.DiGraph()
    g = nx.nx_agraph.to_agraph(g)

    g.add_node('x', shape='box')
    g.add_node('y', shape='box')
    g.add_node('z', shape='box')

    g.add_edges_from([['z', 'x'], ['z', 'y']])
    g.add_edge(['x', 'y'], style='dashed')

    return g.draw(format='png', prog='dot')

import networkx as nx
from networkx.drawing.nx_pydot import to_pydot
from pydotplus import graph_from_dot_data
from IPython.display import Image


def get_png():
    g = nx.DiGraph()
    g = nx.nx_agraph.to_agraph(g)

    nodes_observed = ['身長', 'BMI', '会社規模', '収入', '年齢', '年齢', '既婚']
    nodes_unobserved = ['外見', '経済的能力']
    nodes_error = ['e']
    g.add_nodes_from(nodes_observed, shape='box')
    g.add_nodes_from(nodes_unobserved, shape='oval')
    g.add_nodes_from(nodes_error, shape='circle')
    g.add_subgraph(['経済的能力', '年齢'], rank='same')
    g.add_subgraph(['既婚', 'e'], rank='same')

    # correlation
    g.add_edge('経済的能力', '年齢', dir='both', label=0.4)
    # causal
    g.add_edge('身長', '外見', label=0.6)
    g.add_edge('BMI', '外見', label=0.7)
    g.add_edge('外見', '既婚', label=0.4)
    g.add_edge('経済的能力', '会社規模', label=0.5)
    g.add_edge('経済的能力', '収入', label=0.6)
    g.add_edge('会社規模', '既婚', label=0.6)
    g.add_edge('収入', '既婚', label=0.5)
    g.add_edge('年齢', '既婚', label=0.7)
    # error
    g.add_edge('e', '既婚', label=0.4)

    return g.draw(format='png', prog='dot')

# -*- coding: utf-8 -*-
import pydot_ng as pydot

###############################################################################
# hm2-1a
dot_object = pydot.Dot(graph_name="hm2_1a", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0')
dot_object.add_node(q0)
q1 = pydot.Node('q1')
dot_object.add_node(q1)
q2 = pydot.Node('q2')
dot_object.add_node(q2)
q3 = pydot.Node('q3', shape='doublecircle')
dot_object.add_node(q3)

dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q0, label='0'))
dot_object.add_edge(pydot.Edge(q0, q1, label='1'))
dot_object.add_edge(pydot.Edge(q1, q2, label='0'))
dot_object.add_edge(pydot.Edge(q2, q3, label='0'))
dot_object.add_edge(pydot.Edge(q3, q0, label='0'))

dot_object.write_png('hm2-1a.png', prog='dot')


###############################################################################
# hm2-1b
dot_object = pydot.Dot(graph_name="hm2_1b", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0', shape='doublecircle')
dot_object.add_node(q0)
q1 = pydot.Node('q1', shape='doublecircle')
dot_object.add_node(q1)
q2 = pydot.Node('q2')
dot_object.add_node(q2)

dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q1, label='b'))
dot_object.add_edge(pydot.Edge(q1, q1, label='b'))
dot_object.add_edge(pydot.Edge(q1, q2, label='a'))
dot_object.add_edge(pydot.Edge(q2, q1, label='b'))

dot_object.write_png('hm2-1b.png', prog='dot')

###############################################################################
# hm2-1c
dot_object = pydot.Dot(graph_name="hm2_1c", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0', shape='doublecircle')
dot_object.add_node(q0)
q1 = pydot.Node('q1')
dot_object.add_node(q1)
q2 = pydot.Node('q2')
dot_object.add_node(q2)

dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q0, label='b'))
dot_object.add_edge(pydot.Edge(q0, q1, label='a'))
dot_object.add_edge(pydot.Edge(q1, q1, label='b'))
dot_object.add_edge(pydot.Edge(q1, q2, label='a'))
dot_object.add_edge(pydot.Edge(q2, q0, label='b'))

dot_object.write_png('hm2-1c.png', prog='dot')

###############################################################################
# hm2-2a
dot_object = pydot.Dot(graph_name="hm2_2a", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0')
dot_object.add_node(q0)
q1 = pydot.Node('q1', shape='doublecircle')
dot_object.add_node(q1)

dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q1, label='1'))
dot_object.add_edge(pydot.Edge(q1, q1, label='1, d, _'))

dot_object.write_png('hm2-2a.png', prog='dot')

###############################################################################
# hm2-2b
dot_object = pydot.Dot(graph_name="hm2_2b", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0')
dot_object.add_node(q0)
q1 = pydot.Node('q1')
dot_object.add_node(q1)
q2 = pydot.Node('q2', shape='doublecircle')
dot_object.add_node(q2)

dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q1, label='-'))
dot_object.add_edge(pydot.Edge(q0, q2, label='d'))
dot_object.add_edge(pydot.Edge(q1, q2, label='d'))
dot_object.add_edge(pydot.Edge(q2, q2, label='d'))

dot_object.write_png('hm2-2b.png', prog='dot')

###############################################################################
# hm2-2c
dot_object = pydot.Dot(graph_name="hm2_2c", rankdir="LR", labelloc='b',
                       labeljust='r', ranksep=1)
dot_object.set_node_defaults(shape='circle', fixedsize='true',
                             height=.85, width=.85, fontsize=24)

st = pydot.Node('', shape='none')
dot_object.add_node(st)
q0 = pydot.Node('q0')
dot_object.add_node(q0)
q1 = pydot.Node('q1')
dot_object.add_node(q1)
q2 = pydot.Node('q2', shape='doublecircle')
dot_object.add_node(q2)
q3 = pydot.Node('q3')
dot_object.add_node(q3)
q4 = pydot.Node('q4', shape='doublecircle')
dot_object.add_node(q4)


dot_object.add_edge(pydot.Edge(st, q0))
dot_object.add_edge(pydot.Edge(q0, q1, label='-'))
dot_object.add_edge(pydot.Edge(q0, q2, label='d'))
dot_object.add_edge(pydot.Edge(q1, q2, label='d'))
dot_object.add_edge(pydot.Edge(q2, q3, label='.'))
dot_object.add_edge(pydot.Edge(q3, q4, label='d'))
dot_object.add_edge(pydot.Edge(q4, q4, label='d'))

dot_object.write_png('hm2-2c.png', prog='dot')
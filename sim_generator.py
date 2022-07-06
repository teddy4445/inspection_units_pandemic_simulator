# library imports
import os
import random
import pandas as pd

# project imports
from agent import Agent
from node import Node
from edge import Edge
from graph import Graph
from pips.pip import PIP
from sim import Simulator
from walks.walk import Walk
from population import Population
from walks.walk_random import WalkRandom
from pips.multi_aggressive_pip import PIPMultiAggressive
from walks.walk_random_with_stay import WalkRandomWithStay
from walks.walk_random_with_weighted_stay import WalkRandomWithWeightedStay


class SimulatorGenerator:
    """
    A class to generate simulation settings
    """

    def __init__(self):
        pass

    @staticmethod
    def sensativity_random(cu_portion: float = 0.1,
                           graph_density: float = 0.05,
                           population_density: float = 8,
                           population_mobility: float = 0.25,
                           min_node_count: int = 10,
                           max_node_count: int = 50,
                           max_time: int = 30):
        node_count = random.randint(min_node_count, max_node_count)
        edge_count = round(node_count * node_count * graph_density)
        graph = Graph.generate_random(node_count=node_count,
                                      edge_count=edge_count)
        population = Population(agents=[Agent.create_random(graph_size=node_count)
                                        for _ in range(round(population_density * node_count))])
        pip = PIPMultiAggressive(control_node_ids=random.sample(population=list(range(node_count)),
                                                                k=round(node_count * cu_portion)),
                                 found_exposed=True)
        walk_policy = WalkRandomWithWeightedStay(weight=population_mobility)
        return Simulator(graph=graph,
                         population=population,
                         pip=pip,
                         walk_policy=walk_policy,
                         max_time=max_time)

    @staticmethod
    def real_world(population_count: int = 1000,
                   max_time: int = 720):
        edge_weights = pd.read_csv(os.path.join(os.path.dirname(__file__), "real_data", "ariel_real_data.csv"))
        graph = Graph(nodes=[Node(id=i) for i in range(edge_weights.shape[0])],
                      edges=Graph.table_to_edges(edge_weights.values))
        population = Population.random(population_count=population_count,
                                       graph=graph)
        return Simulator(population=population,
                         graph=graph,
                         walk_policy=WalkRandomWithStay(),
                         pip=PIP(),
                         max_time=max_time)

    @staticmethod
    def simple_random(node_count: int = 50,
                      edge_count: int = 1000,
                      max_time: int = 200,
                      population_count: int = 1000,
                      control_units: int = 0):
        graph = Graph.generate_random(node_count=node_count,
                                      edge_count=edge_count)
        population = Population.random(population_count=population_count,
                                       graph=graph)
        return Simulator(population=population,
                         graph=graph,
                         walk_policy=WalkRandom(),
                         pip=PIP(),
                         max_time=max_time)

    @staticmethod
    def simple_random_aggressive_controled(node_count: int = 50,
                                           edge_count: int = 0,
                                           max_time: int = 200,
                                           population_count: int = 1000,
                                           control_units: int = 0,
                                           found_exposed: bool = False):
        sim = SimulatorGenerator.simple_random(node_count=node_count,
                                               edge_count=edge_count,
                                               max_time=max_time,
                                               population_count=population_count,
                                               control_units=control_units)
        sim.pip = PIPMultiAggressive(control_node_ids=list(range(control_units)),
                                     found_exposed=found_exposed)
        return sim

    @staticmethod
    def full_connected(node_count: int = 50,
                       edge_count: int = 0,
                       max_time: int = 200,
                       population_count: int = 1000,
                       control_units: int = 0):
        graph = Graph.fully_connected(node_count=node_count)
        population = Population.random(population_count=population_count,
                                       graph=graph)
        return Simulator(population=population,
                         graph=graph,
                         walk_policy=WalkRandom(),
                         pip=PIP(),
                         max_time=max_time)

    @staticmethod
    def full_connected_aggressive_controled(node_count: int = 50,
                                            edge_count: int = 0,
                                            max_time: int = 200,
                                            population_count: int = 1000,
                                            control_units: int = 0,
                                            found_exposed: bool = False):
        sim = SimulatorGenerator.full_connected(node_count=node_count,
                                                edge_count=edge_count,
                                                max_time=max_time,
                                                population_count=population_count,
                                                control_units=control_units)
        sim.pip = PIPMultiAggressive(control_node_ids=list(range(control_units)),
                                     found_exposed=found_exposed)
        return sim

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<SimulatorGenerator>"

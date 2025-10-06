"""
Тесты для алгоритмов DAG
"""

import unittest
import sys
import os

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dag_lib.core.graph import DAG
from dag_lib.core.node import Node
from dag_lib.core.edge import Edge
from dag_lib.algorithms.topological_sort import TopologicalSort
from dag_lib.algorithms.pathfinding import PathFinder
from dag_lib.algorithms.cycle_detection import CycleDetector
from dag_lib.algorithms.graph_metrics import GraphMetrics
from dag_lib.exceptions import CycleDetectedError, PathNotFoundError


class TestTopologicalSort(unittest.TestCase):
    """Тесты для топологической сортировки"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.dag = DAG("Test DAG")
        
        # Создаем простой DAG: A -> B -> C
        self.node_a = Node("A", "Узел A")
        self.node_b = Node("B", "Узел B")
        self.node_c = Node("C", "Узел C")
        
        self.dag.add_node(self.node_a)
        self.dag.add_node(self.node_b)
        self.dag.add_node(self.node_c)
        
        self.dag.add_edge(Edge("A", "B"))
        self.dag.add_edge(Edge("B", "C"))
    
    def test_kahn_algorithm(self):
        """Тест алгоритма Кана"""
        result = TopologicalSort.kahn_algorithm(self.dag)
        self.assertEqual(result, ["A", "B", "C"])
    
    def test_dfs_algorithm(self):
        """Тест DFS алгоритма"""
        result = TopologicalSort.dfs_algorithm(self.dag)
        self.assertEqual(result, ["A", "B", "C"])
    
    def test_lexicographical_sort(self):
        """Тест лексикографической сортировки"""
        result = TopologicalSort.lexicographical_sort(self.dag)
        self.assertEqual(result, ["A", "B", "C"])
    
    def test_empty_graph(self):
        """Тест пустого графа"""
        empty_dag = DAG("Empty")
        result = TopologicalSort.kahn_algorithm(empty_dag)
        self.assertEqual(result, [])
    
    def test_single_node(self):
        """Тест графа с одним узлом"""
        single_dag = DAG("Single")
        node = Node("X", "Узел X")
        single_dag.add_node(node)
        
        result = TopologicalSort.kahn_algorithm(single_dag)
        self.assertEqual(result, ["X"])
    
    def test_complex_dag(self):
        """Тест сложного DAG"""
        complex_dag = DAG("Complex")
        
        # Создаем узлы
        for i in range(6):
            node = Node(f"node_{i}", f"Узел {i}")
            complex_dag.add_node(node)
        
        # Создаем ребра: 0->1, 0->2, 1->3, 2->3, 3->4, 3->5
        edges = [
            ("node_0", "node_1"),
            ("node_0", "node_2"),
            ("node_1", "node_3"),
            ("node_2", "node_3"),
            ("node_3", "node_4"),
            ("node_3", "node_5")
        ]
        
        for source, target in edges:
            complex_dag.add_edge(Edge(source, target))
        
        result = TopologicalSort.kahn_algorithm(complex_dag)
        
        # Проверяем, что node_0 идет первым
        self.assertEqual(result[0], "node_0")
        
        # Проверяем, что node_3 идет после node_1 и node_2
        node_3_pos = result.index("node_3")
        node_1_pos = result.index("node_1")
        node_2_pos = result.index("node_2")
        self.assertGreater(node_3_pos, node_1_pos)
        self.assertGreater(node_3_pos, node_2_pos)
    
    def test_is_topological_order(self):
        """Тест проверки топологического порядка"""
        valid_order = ["A", "B", "C"]
        invalid_order = ["B", "A", "C"]
        
        self.assertTrue(TopologicalSort.is_topological_order(self.dag, valid_order))
        self.assertFalse(TopologicalSort.is_topological_order(self.dag, invalid_order))


class TestPathFinder(unittest.TestCase):
    """Тесты для поиска путей"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.dag = DAG("Path Test DAG")
        
        # Создаем DAG: A -> B -> C, A -> D -> C
        for i, node_id in enumerate(["A", "B", "C", "D"]):
            node = Node(node_id, f"Узел {node_id}")
            self.dag.add_node(node)
        
        self.dag.add_edge(Edge("A", "B", 1.0))
        self.dag.add_edge(Edge("B", "C", 2.0))
        self.dag.add_edge(Edge("A", "D", 1.5))
        self.dag.add_edge(Edge("D", "C", 1.0))
    
    def test_find_path(self):
        """Тест поиска пути"""
        path = PathFinder.find_path(self.dag, "A", "C")
        self.assertIn(path, [["A", "B", "C"], ["A", "D", "C"]])
    
    def test_find_path_same_node(self):
        """Тест поиска пути к самому себе"""
        path = PathFinder.find_path(self.dag, "A", "A")
        self.assertEqual(path, ["A"])
    
    def test_path_not_found(self):
        """Тест отсутствия пути"""
        with self.assertRaises(PathNotFoundError):
            PathFinder.find_path(self.dag, "C", "A")
    
    def test_find_all_paths(self):
        """Тест поиска всех путей"""
        paths = PathFinder.find_all_paths(self.dag, "A", "C")
        self.assertEqual(len(paths), 2)
        self.assertIn(["A", "B", "C"], paths)
        self.assertIn(["A", "D", "C"], paths)
    
    def test_find_shortest_paths(self):
        """Тест поиска кратчайших путей"""
        shortest_paths = PathFinder.find_shortest_paths(self.dag, "A")
        
        # Проверяем путь до C
        self.assertIn("C", shortest_paths)
        path, distance = shortest_paths["C"]
        self.assertEqual(distance, 2.5)  # A -> D -> C = 1.5 + 1.0
    
    def test_find_longest_path(self):
        """Тест поиска самого длинного пути"""
        path, length = PathFinder.find_longest_path(self.dag, "A", "C")
        self.assertEqual(length, 3.0)  # A -> B -> C = 1.0 + 2.0
    
    def test_find_reachable_nodes(self):
        """Тест поиска достижимых узлов"""
        reachable = PathFinder.find_reachable_nodes(self.dag, "A")
        self.assertEqual(reachable, {"A", "B", "C", "D"})
        
        reachable = PathFinder.find_reachable_nodes(self.dag, "B")
        self.assertEqual(reachable, {"B", "C"})


class TestCycleDetector(unittest.TestCase):
    """Тесты для обнаружения циклов"""
    
    def test_no_cycles(self):
        """Тест графа без циклов"""
        dag = DAG("No Cycles")
        
        node_a = Node("A", "Узел A")
        node_b = Node("B", "Узел B")
        node_c = Node("C", "Узел C")
        
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_node(node_c)
        
        dag.add_edge(Edge("A", "B"))
        dag.add_edge(Edge("B", "C"))
        
        self.assertFalse(CycleDetector.has_cycle(dag))
        cycles = CycleDetector.find_cycles(dag)
        self.assertEqual(cycles, [])
    
    def test_cycle_detection(self):
        """Тест обнаружения цикла"""
        # Создаем граф с циклом: A -> B -> C -> A
        dag = DAG("With Cycle")
        
        for node_id in ["A", "B", "C"]:
            node = Node(node_id, f"Узел {node_id}")
            dag.add_node(node)
        
        dag.add_edge(Edge("A", "B"))
        dag.add_edge(Edge("B", "C"))
        
        # Попытка добавить ребро, создающее цикл
        with self.assertRaises(CycleDetectedError):
            dag.add_edge(Edge("C", "A"))
    
    def test_validate_dag(self):
        """Тест валидации DAG"""
        dag = DAG("Valid DAG")
        
        node_a = Node("A", "Узел A")
        node_b = Node("B", "Узел B")
        
        dag.add_node(node_a)
        dag.add_node(node_b)
        dag.add_edge(Edge("A", "B"))
        
        is_valid, message = CycleDetector.validate_dag(dag)
        self.assertTrue(is_valid)
        self.assertIn("валидным DAG", message)


class TestGraphMetrics(unittest.TestCase):
    """Тесты для метрик графа"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.dag = DAG("Metrics Test")
        
        for i in range(4):
            node = Node(f"node_{i}", f"Узел {i}")
            self.dag.add_node(node)
        
        self.dag.add_edge(Edge("node_0", "node_1", 1.0))
        self.dag.add_edge(Edge("node_0", "node_2", 2.0))
        self.dag.add_edge(Edge("node_1", "node_3", 1.5))
        self.dag.add_edge(Edge("node_2", "node_3", 1.0))
    
    def test_basic_metrics(self):
        """Тест базовых метрик"""
        metrics = GraphMetrics.get_basic_metrics(self.dag)
        
        self.assertEqual(metrics['nodes'], 4)
        self.assertEqual(metrics['edges'], 4)
        self.assertEqual(metrics['roots'], 1)
        self.assertEqual(metrics['leaves'], 1)
    
    def test_density(self):
        """Тест вычисления плотности"""
        density = GraphMetrics.calculate_density(self.dag)
        # Для 4 узлов максимум 6 ребер, у нас 4, плотность = 4/6
        expected_density = 4 / 6
        self.assertAlmostEqual(density, expected_density, places=3)
    
    def test_node_degrees(self):
        """Тест степеней узлов"""
        degrees = GraphMetrics.get_node_degrees(self.dag)
        
        self.assertEqual(degrees['node_0']['out'], 2)
        self.assertEqual(degrees['node_0']['in'], 0)
        self.assertEqual(degrees['node_3']['in'], 2)
        self.assertEqual(degrees['node_3']['out'], 0)
    
    def test_degree_statistics(self):
        """Тест статистики степеней"""
        stats = GraphMetrics.get_degree_statistics(self.dag)
        
        self.assertIn('in_degree', stats)
        self.assertIn('out_degree', stats)
        self.assertIn('total_degree', stats)
        
        # Проверяем, что статистика содержит нужные поля
        for degree_type in stats.values():
            self.assertIn('min', degree_type)
            self.assertIn('max', degree_type)
            self.assertIn('mean', degree_type)
    
    def test_depth_statistics(self):
        """Тест статистики глубины"""
        stats = GraphMetrics.get_depth_statistics(self.dag)
        
        self.assertIn('max_depth', stats)
        self.assertIn('min_depth', stats)
        self.assertIn('levels', stats)
        self.assertIn('node_depths', stats)
    
    def test_connectivity_metrics(self):
        """Тест метрик связности"""
        metrics = GraphMetrics.get_connectivity_metrics(self.dag)
        
        self.assertIn('components_count', metrics)
        self.assertIn('is_connected', metrics)
        self.assertTrue(metrics['is_connected'])  # DAG связен
    
    def test_comprehensive_analysis(self):
        """Тест полного анализа"""
        analysis = GraphMetrics.get_comprehensive_analysis(self.dag)
        
        self.assertIn('basic_metrics', analysis)
        self.assertIn('degree_statistics', analysis)
        self.assertIn('path_statistics', analysis)
        self.assertIn('depth_statistics', analysis)
        self.assertIn('centrality_measures', analysis)
        self.assertIn('connectivity_metrics', analysis)


if __name__ == '__main__':
    unittest.main()

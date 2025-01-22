import yaml
import networkx as nx
import matplotlib.pyplot as plt

def load_config(config_file):
    """Загружает конфигурацию из YAML-файла."""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def parse_isis_adjacency(file_path):
    """Парсит файл с выводом ISIS adjacency и возвращает список соседей."""
    neighbors = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "Hostname" in lines[i]:
                system_id = lines[i].split(":")[1].strip()
                interface = lines[i + 2].split(":")[1].strip().split()[0]
                state = lines[i + 3].split(":")[1].strip().split()[0]
                level = lines[i + 6].split(":")[1].strip().split()[0]
                if state == "Up":
                    neighbors.append((system_id, interface, level))
                i += 12
            else:
                i += 1
    return neighbors

def parse_isis_database(file_path):
    """Парсит файл с выводом ISIS database и возвращает список LSP."""
    lsp_list = []
    current_level = None
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "Displaying Level" in lines[i]:
                current_level = lines[i].split("Level")[1].strip().split()[0]
            if "LSP ID" in lines[i]:
                lsp_id = lines[i].split(":")[1].strip().split(".")[0]
                if current_level:
                    lsp_list.append((lsp_id, current_level))
            i += 1
    return lsp_list

def parse_isis_topology(file_path):
    """Парсит файл с выводом ISIS topology и возвращает список путей."""
    paths = []
    current_level = None
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "IS-IS IP paths" in lines[i]:
                current_level = lines[i].split("Level")[1].strip().split()[0]
            if "Node      :" in lines[i]:
                node = lines[i].split(":")[1].strip().split(".")[0]
                nexthop = lines[i + 1].split(":")[1].strip().split(".")[0]
                if current_level:
                    paths.append((node, nexthop, current_level))
                i += 5
            else:
                i += 1
    return paths

def build_network_graph(lsp_list, neighbors, topology_paths, router_name):
    """Строит граф сети на основе списка LSP, соседей и путей, начиная с указанного роутера."""
    G = nx.Graph()

    # Добавляем центральный узел (router_name)
    G.add_node(router_name, color='red', size=800, level='both')

    # Добавляем узлы из LSP (маршрутизаторы) с указанием уровня
    for lsp, level in lsp_list:
        if lsp != router_name:  # Центральный узел уже добавлен
            if level == '1':
                G.add_node(lsp, color='blue', size=600, level='L1')
            elif level == '2':
                G.add_node(lsp, color='green', size=600, level='L2')

    # Добавляем связи из adjacency (соседи) с указанием уровня
    for system_id, interface, level in neighbors:
        if system_id not in G:
            if level == '1':
                G.add_node(system_id, color='blue', size=600, level='L1')
            elif level == '2':
                G.add_node(system_id, color='green', size=600, level='L2')

        if level == '1':
            G.add_edge(router_name, system_id, color='blue', level='L1')
        elif level == '2':
            G.add_edge(router_name, system_id, color='green', level='L2')

    # Добавляем связи из topology (пути между маршрутизаторами) с указанием уровня
    for node, nexthop, level in topology_paths:
        # Добавляем связь между router_name и nexthop
        if nexthop not in G:
            if level == '1':
                G.add_node(nexthop, color='blue', size=600, level='L1')
            elif level == '2':
                G.add_node(nexthop, color='green', size=600, level='L2')

        if level == '1':
            G.add_edge(router_name, nexthop, color='blue', level='L1')
        elif level == '2':
            G.add_edge(router_name, nexthop, color='green', level='L2')

        # Добавляем связь между node и nexthop, если node не является router_name
        if node != router_name:
            if node not in G:
                if level == '1':
                    G.add_node(node, color='blue', size=600, level='L1')
                elif level == '2':
                    G.add_node(node, color='green', size=600, level='L2')

            if level == '1':
                G.add_edge(node, nexthop, color='blue', level='L1')
            elif level == '2':
                G.add_edge(node, nexthop, color='green', level='L2')

    return G

# Тестовый запуск
if __name__ == "__main__":
    # Загружаем конфиг
    config = load_config("config.yaml")
    adjacency_file = config['adjacency_file']
    database_file = config['database_file']
    topology_file = config['topology_file']
    router_name = config['router_name']

    # Парсим данные из файлов
    neighbors = parse_isis_adjacency(adjacency_file)
    lsp_list = parse_isis_database(database_file)
    topology_paths = parse_isis_topology(topology_file)

    # Строим граф
    graph = build_network_graph(lsp_list, neighbors, topology_paths, router_name)

    # Инициализируем позиции узлов
    pos = nx.kamada_kawai_layout(graph)

    # Рисуем граф
    plt.figure(figsize=(12, 8))
    node_colors = [graph.nodes[node].get('color', 'lightblue') for node in graph]
    node_sizes = [graph.nodes[node].get('size', 1000) for node in graph]
    edge_colors = [graph.edges[edge].get('color', 'gray') for edge in graph.edges]

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')

    plt.title("IS-IS Topology (Level 1 and Level 2)")
    plt.show()
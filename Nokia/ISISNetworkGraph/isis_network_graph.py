import yaml
import networkx as nx
import matplotlib.pyplot as plt


class DraggableGraph:
    def __init__(self, graph, pos):
        self.graph = graph
        self.pos = pos
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.dragging = False
        self.dragged_node = None

        # Рисуем граф
        self.draw_graph()

        # Подключаем обработчики событий
        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def draw_graph(self):
        """Отрисовывает граф."""
        self.ax.clear()
        node_colors = [self.graph.nodes[node].get('color', 'lightblue') for node in self.graph]
        node_sizes = [self.graph.nodes[node].get('size', 1000) for node in self.graph]
        edge_colors = [self.graph.edges[edge].get('color', 'gray') for edge in self.graph.edges]
        edge_labels = {(u, v): f"{self.graph.edges[u, v]['weight']}" for u, v in self.graph.edges}

        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, edge_color=edge_colors)
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, self.pos, ax=self.ax, edge_labels=edge_labels, font_color='red')

        self.ax.set_title("IS-IS Topology (Level 1 and Level 2) with Metrics")
        plt.draw()

    def on_press(self, event):
        """Обрабатывает нажатие мыши."""
        if event.inaxes is None:
            return
        for node in self.graph.nodes:
            x, y = self.pos[node]
            if (x - event.xdata) ** 2 + (y - event.ydata) ** 2 < 0.01:  # Проверяем, близко ли нажатие к узлу
                self.dragging = True
                self.dragged_node = node
                break

    def on_release(self, event):
        """Обрабатывает отпускание мыши."""
        self.dragging = False
        self.dragged_node = None

    def on_motion(self, event):
        """Обрабатывает перемещение мыши."""
        if self.dragging and self.dragged_node is not None:
            self.pos[self.dragged_node] = (event.xdata, event.ydata)  # Обновляем позицию узла
            self.draw_graph()  # Перерисовываем граф


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
    """Парсит файл с выводом ISIS topology и возвращает список путей с метриками."""
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

                # Извлекаем метрику из строки SNPA
                if i + 3 < len(lines) and "Metric" in lines[i + 3]:
                    metric_part = lines[i + 3].split("Metric")[1].strip()
                    metric = int(''.join(filter(str.isdigit, metric_part)))
                else:
                    metric = 0  # Значение по умолчанию, если метрика не найдена

                if current_level:
                    paths.append((node, nexthop, current_level, metric))
                i += 5  # Переходим к следующей записи
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
            G.add_edge(router_name, system_id, color='blue', level='L1', weight=1)  # Метрика по умолчанию
        elif level == '2':
            G.add_edge(router_name, system_id, color='green', level='L2', weight=1)  # Метрика по умолчанию

    # Добавляем связи из topology (пути между маршрутизаторами) с указанием уровня и метрики
    for node, nexthop, level, metric in topology_paths:
        # Если Node и Nexthop совпадают, это прямой линк между router_name и Node
        if node == nexthop:
            # Добавляем связь между router_name и Node
            if node not in G:
                if level == '1':
                    G.add_node(node, color='blue', size=600, level='L1')
                elif level == '2':
                    G.add_node(node, color='green', size=600, level='L2')

            if level == '1':
                G.add_edge(router_name, node, color='blue', level='L1', weight=metric)
            elif level == '2':
                G.add_edge(router_name, node, color='green', level='L2', weight=metric)
        else:
            # Если Node и Nexthop не совпадают, добавляем связь между Node и Nexthop
            if node not in G:
                if level == '1':
                    G.add_node(node, color='blue', size=600, level='L1')
                elif level == '2':
                    G.add_node(node, color='green', size=600, level='L2')

            if nexthop not in G:
                if level == '1':
                    G.add_node(nexthop, color='blue', size=600, level='L1')
                elif level == '2':
                    G.add_node(nexthop, color='green', size=600, level='L2')

            if level == '1':
                G.add_edge(node, nexthop, color='blue', level='L1', weight=metric)
            elif level == '2':
                G.add_edge(node, nexthop, color='green', level='L2', weight=metric)

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
    pos = nx.spring_layout(graph, iterations=1000)

    # Создаем интерактивный граф
    draggable_graph = DraggableGraph(graph, pos)
    plt.show()
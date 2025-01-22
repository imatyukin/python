import yaml
import networkx as nx
import matplotlib.pyplot as plt

class DraggableGraph:
    def __init__(self, graph, pos):
        self.graph = graph
        self.pos = pos
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.dragging = None
        self.node_colors = [graph.nodes[node].get('color', 'lightblue') for node in graph]
        self.node_sizes = [graph.nodes[node].get('size', 1000) for node in graph]
        self.edge_colors = [graph.edges[edge].get('color', 'gray') for edge in graph.edges]

        # Рисуем граф
        self.nodes = nx.draw_networkx_nodes(graph, pos, ax=self.ax, node_color=self.node_colors, node_size=self.node_sizes)
        self.edges = nx.draw_networkx_edges(graph, pos, ax=self.ax, edge_color=self.edge_colors)
        self.labels = nx.draw_networkx_labels(graph, pos, ax=self.ax, font_size=10, font_weight='bold')

        # Подключаем обработчики событий
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        """Обработчик нажатия кнопки мыши."""
        if event.inaxes != self.ax:
            return
        for node, (x, y) in self.pos.items():
            if (x - event.xdata) ** 2 + (y - event.ydata) ** 2 < 0.01:  # Проверяем, близко ли нажатие к узлу
                self.dragging = node
                break

    def on_release(self, event):
        """Обработчик отпускания кнопки мыши."""
        self.dragging = None

    def on_motion(self, event):
        """Обработчик перемещения мыши."""
        if self.dragging is None or event.inaxes != self.ax:
            return
        # Обновляем позицию узла
        self.pos[self.dragging] = (event.xdata, event.ydata)
        # Очищаем и перерисовываем граф
        self.ax.clear()
        self.nodes = nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_color=self.node_colors, node_size=self.node_sizes)
        self.edges = nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, edge_color=self.edge_colors)
        self.labels = nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, font_size=10, font_weight='bold')
        self.fig.canvas.draw()

def load_config(config_file):
    """Загружает конфигурацию из YAML-файла."""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def parse_isis_adjacency(file_path):
    """Парсит файл с выводом ISIS adjacency (новый формат) и возвращает список соседей."""
    neighbors = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "Hostname" in lines[i]:  # Начало блока с информацией о соседе
                # Извлекаем Hostname (System ID)
                system_id = lines[i].split(":")[1].strip()

                # Извлекаем Interface
                interface_line = lines[i + 2]
                interface = interface_line.split(":")[1].strip().split()[0]  # Берем только первое слово

                # Извлекаем State
                state_line = lines[i + 3]
                state = state_line.split(":")[1].strip().split()[0]  # Берем только первое слово

                if state == "Up":  # Добавляем только активные соседи
                    neighbors.append((system_id, interface))

                i += 12  # Пропускаем оставшиеся строки блока
            else:
                i += 1
    return neighbors

def parse_isis_database(file_path):
    """Парсит файл с выводом ISIS database (новый формат) и возвращает список LSP."""
    lsp_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if "LSP ID" in lines[i]:  # Начало блока с информацией о LSP
                # Извлекаем LSP ID (System ID)
                lsp_id = lines[i].split(":")[1].strip().split(".")[0]  # Берем только System ID (без .00-00)
                # Извлекаем Level
                level_line = lines[i + 1]
                level = level_line.split(":")[1].strip()
                # Если уровень L1L2, добавляем в список
                if "L1L2" in level:
                    lsp_list.append(lsp_id)
                i += 1  # Переходим к следующей строке
            else:
                i += 1
    return lsp_list

def parse_isis_topology(file_path):
    """Парсит файл с выводом ISIS topology и возвращает список путей."""
    paths = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Ищем строки с данными о путях
        for line in lines:
            if "to_" in line:  # Фильтруем строки с интерфейсами
                parts = line.split()
                node = parts[0].split('.')[0]  # Берем только System ID (без .00-00)
                interface = parts[1]
                nexthop = parts[2]
                paths.append((node, nexthop))
    return paths

def build_network_graph(lsp_list, neighbors, topology_paths, router_name):
    """Строит граф сети на основе списка LSP, соседей и путей, начиная с указанного роутера."""
    G = nx.Graph()

    # Добавляем узлы из LSP (маршрутизаторы)
    for lsp in lsp_list:
        if lsp == router_name:
            G.add_node(lsp, color='red', size=3000)  # Выделяем роутер, с которого собраны данные
        else:
            G.add_node(lsp, color='lightblue', size=2000)

    # Добавляем связи из adjacency (соседи)
    for system_id, interface in neighbors:
        if system_id not in G:
            G.add_node(system_id, color='lightblue', size=2000)
        G.add_edge(router_name, system_id, color='black')  # Связь от router_name до соседа

    # Добавляем связи из topology (пути между маршрутизаторами)
    for node, nexthop in topology_paths:
        if node not in G:
            G.add_node(node, color='lightblue', size=2000)
        if nexthop not in G:
            G.add_node(nexthop, color='lightblue', size=2000)
        G.add_edge(node, nexthop, color='black')

    return G

def main():
    # Загружаем конфиг
    config = load_config("config.yaml")
    adjacency_file = config['adjacency_file']
    database_file = config['database_file']
    topology_file = config['topology_file']
    router_name = config['router_name']  # Имя роутера, с которого собраны данные

    # Парсим данные из файлов
    neighbors = parse_isis_adjacency(adjacency_file)
    lsp_list = parse_isis_database(database_file)
    topology_paths = parse_isis_topology(topology_file)

    # Строим граф
    graph = build_network_graph(lsp_list, neighbors, topology_paths, router_name)

    # Инициализируем позиции узлов
    pos = nx.spring_layout(graph)

    # Создаем интерактивный граф
    draggable_graph = DraggableGraph(graph, pos)
    plt.show()

if __name__ == "__main__":
    main()
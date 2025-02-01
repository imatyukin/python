import yaml
from PyQt5 import QtWidgets
from utils import (
    validate_ip_address, validate_port, validate_packet_size,
    validate_threads, validate_range
)

def save_config(config, parent_widget):
    """
    Сохранение конфигурации в YAML файл.
    """
    if not validate_config(config, parent_widget):  # Передаем parent_widget в validate_config
        return

    options = QtWidgets.QFileDialog.Options()
    file_name, _ = QtWidgets.QFileDialog.getSaveFileName(parent_widget, "Save YAML Config", "",
                                                         "YAML Files (*.yaml);;All Files (*)", options=options)
    if file_name:
        try:
            with open(file_name, 'w', encoding="utf-8") as file:
                yaml.dump(config, file, indent=2)
            parent_widget.statusBar.showMessage(f"Config saved to {file_name}")
        except Exception as e:
            parent_widget.statusBar.showMessage(f"Error saving config {e}")

def load_config(parent_widget):
    """
    Загрузка конфигурации из YAML файла.
    """
    options = QtWidgets.QFileDialog.Options()
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName(parent_widget, "Open YAML Config", "",
                                                         "YAML Files (*.yaml);;All Files (*)", options=options)
    if file_name:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                if not config:
                    raise ValueError("Empty or invalid YAML file.")
                if not validate_config(config, parent_widget):  # Передаем parent_widget в validate_config
                    return
                return config
        except Exception as e:
            parent_widget.statusBar.showMessage(f"Failed to load config: {e}")
    return None

def validate_config(config, parent_widget):
    """
    Валидация конфигурации.
    """
    try:
        validate_ip_address(config.get('source_address'))
        validate_ip_address(config.get('destination_address'))
        if config.get('protocol') == 'UDP':
            validate_port(config.get('destination_port'))
            validate_port(config.get('source_port'))

        validate_packet_size(config.get('packet_size'))
        validate_threads(config.get('threads'))
        float(config.get('speed_value'))

        dscp = config.get('qos', {}).get('dscp')
        if dscp:
            validate_range(dscp, 0, 63)

        ip_prec = config.get('qos', {}).get('ip_precedence')
        if ip_prec:
            validate_range(ip_prec, 0, 7)

        ecn = config.get('qos', {}).get('ecn')
        if ecn:
            validate_range(ecn, 0, 3)
        return True
    except Exception as e:
        parent_widget.statusBar.showMessage(f"Error in config: {e}")
        return False
# helpers/loader.py
import importlib
import os

def discover_algorithms(base_path="helpers/algorithms"):
    """
    Duyệt toàn bộ cây thư mục và trả về dict dạng:
    {
        "info/astar": "helpers.algorithms.info.astar",
        "noinfo/bfs": "helpers.algorithms.noinfo.bfs",
        ...
    }
    """
    algos = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), base_path)
                name = rel_path.replace("\\", "/")[:-3]
                module_path = f"helpers.algorithms.{name.replace('/', '.')}"
                algos[name] = module_path
    return algos

def load_algorithm(name):
    """
    name: ví dụ 'info-->astar' hoặc 'noinfo-->bfs'
    Trả về hàm find_path trong module tương ứng.
    """
    algos = discover_algorithms()
    if name not in algos:
        raise ValueError(f"Algorithm '{name}' not found")

    try:
        module = importlib.import_module(algos[name])
        if not hasattr(module, "find_path"):
            raise AttributeError(f"Module '{algos[name]}' không có hàm find_path")
        return module.find_path
    except Exception as e:
        raise ImportError(f"Lỗi khi load thuật toán '{name}': {e}")

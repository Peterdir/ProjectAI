import importlib
import os
from helpers.algorithm_names import ALGORITHM_DISPLAY_NAMES

_ALGO_CACHE = None

def discover_algorithms(base_path="helpers/algorithms"):
    global _ALGO_CACHE
    if _ALGO_CACHE is not None:
        return _ALGO_CACHE

    algos = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), base_path)
                name = rel_path.replace("\\", "/")[:-3]  # ví dụ: "Nhom 1/bfs"
                module_path = f"helpers.algorithms.{name.replace('/', '.')}"

                # Lấy tên file (bfs, dfs, v.v.)
                filename = os.path.splitext(file)[0]
                display_name = ALGORITHM_DISPLAY_NAMES.get(filename, filename.capitalize())

                algos[name] = {
                    "module": module_path,
                    "display": display_name,
                    "func": None
                }

    _ALGO_CACHE = algos
    return algos


def load_algorithm(name):
    algos = discover_algorithms()
    if name not in algos:
        raise ValueError(f"Algorithm '{name}' not found")

    algo_entry = algos[name]
    if algo_entry["func"] is not None:
        return algo_entry["func"]

    try:
        module = importlib.import_module(algo_entry["module"])
        if not hasattr(module, "find_path"):
            raise AttributeError(f"Module '{algo_entry['module']}' không có hàm find_path")
        algo_entry["func"] = module.find_path
        return algo_entry["func"]
    except Exception as e:
        raise ImportError(f"Lỗi khi load thuật toán '{name}': {e}")

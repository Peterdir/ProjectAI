from typing import Any, Callable, Dict, Optional, Tuple

# Types
Maze = list
Pos = Tuple[int, int]
Callback = Optional[Callable[[Pos], None]]


def run_search(algorithm: Callable[..., Any],
               maze: Maze,
               start: Pos,
               goal: Pos,
               on_expand: Callback = None) -> Any:
    """
    Execute an algorithm with an optional visualization callback (on_expand).
    This wrapper tries to pass the callback using the keyword 'callback'.
    If the algorithm doesn't accept it, it falls back gracefully.

    Returns the algorithm's raw result (path list or dict with 'path' and 'metrics').
    """
    try:
        # Try passing callback keyword if supported
        return algorithm(maze, start, goal, callback=on_expand)
    except TypeError:
        # Fallback: algorithm doesn't support callback
        return algorithm(maze, start, goal)


def normalize_result(result: Any) -> Tuple[Optional[list], Dict[str, Any]]:
    """
    Normalize the algorithm result to (path, metrics_dict).
    - If result is a dict with keys 'path' and optional 'metrics', extract them.
    - If result is a list (path), convert to (path, {"path_length": len(path)-1}).
    - If result is None, return (None, {}).
    """
    if result is None:
        return None, {}

    if isinstance(result, dict):
        path = result.get("path")
        metrics = result.get("metrics") or {}
        if path:
            metrics.setdefault("path_length", max(0, len(path) - 1))
        return path, metrics

    # Assume legacy path-only list
    if isinstance(result, (list, tuple)):
        path = list(result)
        metrics = {"path_length": max(0, len(path) - 1)}
        return path, metrics

    # Unknown format; best effort
    return None, {}

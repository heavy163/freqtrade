from typing import Any, Dict, List, Tuple


DEBUG_CALLBACKS: Dict[str, List[Tuple[Any]]] = {}


def register_hook(package, module, func_name, call):
    key = f"{package}:{module}:{func_name}"
    if key in DEBUG_CALLBACKS:
        DEBUG_CALLBACKS[key].append(call)
    else:
        DEBUG_CALLBACKS[key] = [call]


def callback(package, module, func_name, **kwargs):
    for key in DEBUG_CALLBACKS.keys():
        p, m, f = key.split(":")
        for callback in DEBUG_CALLBACKS[key]:
            if p == "*" or p == package:
                if m == "*" or m == module:
                    if f == "*" or f == func_name:
                        callback(package, module, func_name, **kwargs)

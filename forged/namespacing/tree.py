def render_namespace_tree(node, prefix: str = "", is_last: bool = True, depth: int = 0):
    """Recursively render a namespace tree from the root node."""
    lines = []

    connector = "└── " if is_last else "├── "
    symbol_str = " [symbol]" if node.symbol else ""

    if depth > 0:  # Skip root label
        lines.append(f"{prefix}{connector}{node.name}{symbol_str}")
        prefix += "    " if is_last else "│   "

    child_names = sorted(node.children.keys())
    for i, child in enumerate(child_names):
        child_node = node.children[child]
        is_child_last = i == len(child_names) - 1
        lines.extend(render_namespace_tree(child_node, prefix, is_child_last, depth + 1))

    return lines


def print_namespace(namespace):
    """Print the namespace starting from its root node."""
    print(namespace.name)  # e.g., 'root'
    lines = render_namespace_tree(namespace.root)
    for line in lines:
        print(line)

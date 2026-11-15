import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = ("agents", "channels")

def imported_modules(path):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module

def test_core_never_imports_agents_or_channels():
    offenders = []
    for path in sorted((ROOT / "core").rglob("*.py")):
        for mod in imported_modules(path):
            if mod.split(".")[0] in FORBIDDEN:
                offenders.append(f"{path.relative_to(ROOT)} imports {mod}")
    assert not offenders, "\n".join(offenders)

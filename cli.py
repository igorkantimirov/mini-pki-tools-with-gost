from __future__ import annotations

import importlib.util
import sys
from importlib import import_module
from pathlib import Path

_PKG = "mini_pki_tools"


def _bootstrap_package() -> None:
    root = Path(__file__).resolve().parent
    if _PKG in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(
        _PKG,
        root / "__init__.py",
        submodule_search_locations=[str(root)],
    )
    pkg = importlib.util.module_from_spec(spec)
    sys.modules[_PKG] = pkg
    assert spec.loader is not None
    spec.loader.exec_module(pkg)


if __name__ == "__main__":
    _bootstrap_package()
    import_module(f"{_PKG}.__main__").main()

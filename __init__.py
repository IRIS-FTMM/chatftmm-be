# file: backend/app/__init__.py

import sys
import pathlib

# Menambahkan direktori 'backend' (induk dari folder 'app' ini) ke dalam sys.path.
# Ini adalah perbaikan path yang paling awal dan paling kuat.
backend_root_path = str(pathlib.Path(__file__).resolve().parent.parent)
if backend_root_path not in sys.path:
    sys.path.insert(0, backend_root_path)
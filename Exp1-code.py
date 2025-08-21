import requests
import importlib.util
import sys
import os
import tempfile
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ipywidgets as w
from IPython.display import display, clear_output
from tabulate import tabulate

# Download and import .so module from GitHub
url = "https://github.com/Lab2Phys/module-resistance-distance/raw/refs/heads/main/module_resistance_distance.so"

try:
    r = requests.get(url)
    r.raise_for_status()
   
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.so', delete=False) as f:
        f.write(r.content)
        temp_path = f.name
   
    # Load module
    spec = importlib.util.spec_from_file_location("module_resistance_distance", temp_path)
    module_resistance_distance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_resistance_distance)
   
    print("Module loaded successfully")
   
except Exception as e:
    print(f"✗ Error: {e}")
    try:
        import ctypes
        module_resistance_distance = ctypes.CDLL(temp_path)
        print("Module loaded with ctypes")
    except:
        sys.exit(1)

# configuration
num_nodes = 9
decimal_precision = 3
r = 62
R = 1000

# Define edges as (node1, node2, resistance)
edges = [
    (1, 2, R),
    (1, 3, R),
    (1, 4, R),
    (2, 3, R),
    (2, 5, R),
    (2, 6, R),
    (3, 4, R),
    (3, 5, R),
    (3, 7, R),
    (4, 7, R),
    (4, 8, R),
    (5, 6, r),
    (5, 7, R),
    (5, 9, R),
    (6, 9, R),
    (7, 8, R),
    (7, 9, R),
    (8, 9, R)
]


# Run the main function from the downloaded module
try:
    module_resistance_distance.main(edges, num_nodes, decimal_precision)
except Exception as e:
    print(f"✗ Analysis error: {e}")

# Cleanup
try:
    os.unlink(temp_path)
except:
    pass
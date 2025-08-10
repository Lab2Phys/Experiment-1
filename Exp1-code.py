import networkx as nx, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ipywidgets as w
from IPython.display import display, clear_output
from tabulate import tabulate

# Graph data
r = 62
R = 1000

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

G = nx.Graph(); G.add_weighted_edges_from(edges)
n = max(max(u, v) for u, v, _ in edges)

# Resistances
res, total = [], 0
for i in range(1, n+1):
    for j in range(i+1, n+1):
        try: Rij = nx.resistance_distance(G, i, j, weight="weight"); total += Rij; res.append([f"R({i},{j})", f"{Rij:.3f}"])
        except: res.append([f"R({i},{j})", "N/A"])

# Table for console/PDF
mid = (len(res)+1)//2
table = [res[i] + (res[i+mid] if i+mid < len(res) else ["",""]) for i in range(mid)]

# Console output
print(tabulate(table, headers=["Resistance","Value (Ω)","Resistance","Value (Ω)"]))
print(f"\nTotal resistance kf(G) = {total:.3f} Ω")

# PDF output with centered text
with PdfPages("Resistance_Table.pdf") as pdf:
    fig, ax = plt.subplots(figsize=(8.3, 11.7)); ax.axis('off')
    plt.text(0.5, 0.81, f"Total resistance kf(G) = {total:.3f} Ω", ha='center', transform=ax.transAxes, fontsize=9)
    t = ax.table(cellText=[["Resistance","Value (Ω)","Resistance","Value (Ω)"]]+table, loc='center', bbox=[0.2,0.2,0.6,0.6])
    t.auto_set_font_size(False); t.set_fontsize(7)
    for (r,c),cell in t.get_celld().items():
        cell.set_text_props(ha='center', va='center')  # Center alignment for all cells
        if r == 0: cell.set_facecolor('#ccc')
    pdf.savefig(fig, bbox_inches='tight'); plt.close()

# Widgets
n1, n2, btn, out = w.IntText(1, description=f'Node 1 (1-{n}):', style={'description_width':'initial'}), \
                   w.IntText(1, description=f'Node 2 (1-{n}):', style={'description_width':'initial'}), \
                   w.Button(description='Calculate', button_style='success'), w.Output()

@out.capture(clear_output=True)
def calc(_):
    a, b = n1.value, n2.value
    if not (1<=a<=n and 1<=b<=n): print(f"Error: Nodes must be between 1 and {n}!")
    elif a==b: print("Error: Nodes must be different!")
    else:
        try: print(f"Equivalent resistance between nodes {a} and {b}: {nx.resistance_distance(G,a,b,weight='weight'):.3f} Ω")
        except: print("Error: No path exists between these nodes!")

btn.on_click(calc)
display(w.VBox([n1, n2, btn, out]))

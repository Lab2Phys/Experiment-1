import networkx as nx
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Define the graph and edges
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

# Create the graph
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Determine the number of nodes dynamically
n = max(max(u, v) for u, v, _ in edges)  # Find the maximum node index

# Calculate resistance for all pairs and print to console
resistances = []
total_resistance = 0
for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        try:
            R_ij = nx.resistance_distance(G, i, j, weight='weight')
            total_resistance += R_ij
            resistances.append([f"R({i},{j})", f"{R_ij:.3f}"])
            print(f"R({i},{j}) = {R_ij:.3f}")
        except nx.NetworkXError:
            resistances.append([f"R({i},{j})", "N/A"])
            print(f"R({i},{j}) = N/A")

print(f"\nTotal resistance kf(G) = {total_resistance:.3f} Ω")

# Prepare table data for PDF
midpoint = (len(resistances) + 1) // 2
table_data = [["Resistance", "Value (Ω)", "Resistance", "Value (Ω)"]]
for i in range(midpoint):
    left = resistances[i]
    right = resistances[i + midpoint] if i + midpoint < len(resistances) else ["", ""]
    table_data.append([left[0], left[1], right[0], right[1]])

# Save table to PDF
with PdfPages('Resistance_Table.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(8.3, 11.7))
    ax.axis('off')
    plt.text(0.5, 0.81, f"Total resistance kf(G) = {total_resistance:.3f} Ω",
            ha='center', va='bottom', transform=ax.transAxes, fontsize=9)
    table = ax.table(cellText=table_data, colLabels=None, loc='center', bbox=[0.2, 0.2, 0.6, 0.6])
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(ha='left' if col in [0, 2] else 'center', va='center')
        if row == 0:
            cell.set_facecolor('#cccccc')
            cell.set_height(0.05)
        else:
            cell.set_height(0.03)
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

# Create input fields and button
node1_input = widgets.IntText(value=1, description=f'Node 1 (1-{n}):', style={'description_width': 'initial'})
node2_input = widgets.IntText(value=1, description=f'Node 2 (1-{n}):', style={'description_width': 'initial'})
calc_button = widgets.Button(description='Calculate', button_style='success')
output = widgets.Output()

# Horizontal layout for input fields
input_box = widgets.VBox([node1_input, node2_input])

# Function to calculate resistance
def on_button_clicked(b):
    with output:
        clear_output()  # Clear previous output
        try:
            node1 = node1_input.value
            node2 = node2_input.value
            if node1 < 1 or node1 > n or node2 < 1 or node2 > n:
                print(f"Error: Nodes must be between 1 and {n}!")
                return
            elif node1 == node2:
                print("Error: Nodes must be different!")
                return
            else:
                try:
                    R_ij = nx.resistance_distance(G, node1, node2, weight='weight')
                    print(f"Equivalent resistance between nodes {node1} and {node2}: {R_ij:.3f} Ω")
                except nx.NetworkXError:
                    print(f"Error: No path exists between nodes {node1} and {node2}!")
                # Clear input fields for next entry
                node1_input.value = 1
                node2_input.value = 1
        except ValueError:
            print("Error: Please enter valid numbers!")

# Connect button to function
calc_button.on_click(on_button_clicked)

# Display widgets
display(input_box)
display(calc_button)
display(output)

import json
import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dijkstra import Network


class RoutingOptimizer:

    def __init__(self, root):
        self.root = root

        self.root.title("Internet Network Routing Optimizer")
        self.root.geometry("1100x850")
        self.root.minsize(900, 650)

        self.network = Network()
        self.graph = nx.Graph()

        self.load_data()
        self.create_gui()

    # Load network data
    def load_data(self):

        try:
            with open("data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for router in data["routers"]:

                router_id = router["id"]

                self.network.add_router(router_id)
                self.graph.add_node(router_id)

            for connection in data["connections"]:

                source = connection["router1"]
                destination = connection["router2"]
                latency = connection["latency"]

                self.network.add_connection(
                    source,
                    destination,
                    latency
                )

                self.graph.add_edge(
                    source,
                    destination,
                    weight=latency
                )

            self.positions = nx.spring_layout(
                self.graph,
                seed=42
            )

        except FileNotFoundError:
            messagebox.showerror(
                "File Error",
                "data.json file not found!"
            )
            raise

        except (KeyError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Data Error",
                f"Please check data.json:\n{error}"
            )
            raise

    # Create application interface
    def create_gui(self):

        title = tk.Label(
            self.root,
            text="INTERNET NETWORK ROUTING OPTIMIZER",
            font=("Arial", 18, "bold"),
            fg="darkblue"
        )

        title.pack(pady=10)

        # Network information
        info_frame = ttk.LabelFrame(
            self.root,
            text="Network Information"
        )

        info_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        router_count = self.graph.number_of_nodes()
        connection_count = self.graph.number_of_edges()

        info_text = (
            f"Total Routers: {router_count}     |     "
            f"Total Connections: {connection_count}     |     "
            f"Algorithm: Dijkstra's Algorithm"
        )

        self.info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 10)
        )

        self.info_label.pack(pady=8)

        # Router selection
        controls = ttk.Frame(self.root)
        controls.pack(pady=10)

        routers = sorted(self.graph.nodes)

        tk.Label(
            controls,
            text="Source Router:"
        ).grid(row=0, column=0, padx=5)

        self.source = ttk.Combobox(
            controls,
            values=routers,
            state="readonly",
            width=10
        )

        self.source.grid(row=0, column=1, padx=5)
        self.source.set("R1")

        tk.Label(
            controls,
            text="Destination Router:"
        ).grid(row=0, column=2, padx=5)

        self.destination = ttk.Combobox(
            controls,
            values=routers,
            state="readonly",
            width=10
        )

        self.destination.grid(row=0, column=3, padx=5)
        self.destination.set("R8")

        # Find shortest path button
        self.find_button = ttk.Button(
            controls,
            text="Find Shortest Path",
            command=self.find_path
        )

        self.find_button.grid(
            row=0,
            column=4,
            padx=5
        )

        # Reset button
        self.reset_button = ttk.Button(
            controls,
            text="Reset",
            command=self.reset_graph
        )

        self.reset_button.grid(
            row=0,
            column=5,
            padx=5
        )

        # Result display
        self.result = tk.Label(
            self.root,
            text="Select source and destination routers.",
            font=("Arial", 11),
            justify="center",
            wraplength=1000
        )

        self.result.pack(pady=8)

        # Graph
        self.figure, self.ax = plt.subplots(
            figsize=(10, 6)
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.root
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.draw_graph()

    # Draw network graph
    def draw_graph(self, path=None):

        self.ax.clear()

        nx.draw_networkx_edges(
            self.graph,
            self.positions,
            ax=self.ax,
            edge_color="lightgray",
            width=2
        )

        nx.draw_networkx_nodes(
            self.graph,
            self.positions,
            ax=self.ax,
            node_color="skyblue",
            node_size=1300
        )

        nx.draw_networkx_labels(
            self.graph,
            self.positions,
            ax=self.ax,
            font_size=10,
            font_weight="bold"
        )

        edge_labels = nx.get_edge_attributes(
            self.graph,
            "weight"
        )

        nx.draw_networkx_edge_labels(
            self.graph,
            self.positions,
            edge_labels=edge_labels,
            ax=self.ax,
            font_size=9
        )

        # Highlight shortest path
        if path:

            path_edges = list(
                zip(path, path[1:])
            )

            if path_edges:

                nx.draw_networkx_edges(
                    self.graph,
                    self.positions,
                    edgelist=path_edges,
                    ax=self.ax,
                    edge_color="red",
                    width=4
                )

            # Source router
            nx.draw_networkx_nodes(
                self.graph,
                self.positions,
                nodelist=[path[0]],
                ax=self.ax,
                node_color="green",
                node_size=1500
            )

            # Destination router
            if path[-1] != path[0]:

                nx.draw_networkx_nodes(
                    self.graph,
                    self.positions,
                    nodelist=[path[-1]],
                    ax=self.ax,
                    node_color="orange",
                    node_size=1500
                )

        self.ax.set_title(
            "Internet Network Topology",
            fontsize=13
        )

        self.ax.axis("off")

        self.figure.tight_layout()
        self.canvas.draw()

    # Validate input and find shortest path
    def find_path(self):

        source = self.source.get()
        destination = self.destination.get()

        # Validate selections
        if not source or not destination:

            messagebox.showwarning(
                "Input Error",
                "Please select both source and destination routers."
            )

            return

        if source not in self.graph or destination not in self.graph:

            messagebox.showerror(
                "Invalid Router",
                "The selected router does not exist in the network."
            )

            return

        if source == destination:

            self.result.config(
                text=(
                    f"Source: {source} | Destination: {destination}\n"
                    f"Shortest Route: {source}\n"
                    f"Total Latency: 0 units"
                ),
                fg="darkblue"
            )

            self.draw_graph([source])
            return

        # Calculate shortest path
        path, latency = self.network.shortest_path(
            source,
            destination
        )

        if path is None:

            messagebox.showwarning(
                "Route Not Found",
                "No route exists between the selected routers."
            )

            self.result.config(
                text="No route found.",
                fg="red"
            )

            self.draw_graph()
            return

        route = " -> ".join(path)

        self.result.config(
            text=(
                f"Source: {source}    "
                f"Destination: {destination}\n"
                f"Shortest Route: {route}\n"
                f"Total Latency: {latency} units"
            ),
            fg="darkblue"
        )

        self.draw_graph(path)

    # Reset graph and selections
    def reset_graph(self):

        self.source.set("R1")
        self.destination.set("R8")

        self.result.config(
            text="Select source and destination routers.",
            fg="black"
        )

        self.draw_graph()

    # End of class


if __name__ == "__main__":

    root = tk.Tk()

    app = RoutingOptimizer(root)

    root.mainloop()
import json
import sys
import networkx as nx
import matplotlib.pyplot as plt

from dijkstra import Network


def load_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def visualize_network(filename="data.json"):

    # Load JSON data
    data = load_data(filename)

    routers = data["routers"]
    connections = data["connections"]
    requests = data["requests"]

    # Create network graph
    graph = nx.Graph()
    network = Network()

    # Add routers
    for router in routers:
        router_id = router["id"]
        graph.add_node(router_id)
        network.add_router(router_id)

    # Add network connections
    for connection in connections:

        source = connection["router1"]
        destination = connection["router2"]
        latency = connection["latency"]

        graph.add_edge(
            source,
            destination,
            weight=latency
        )

        network.add_connection(
            source,
            destination,
            latency
        )

    # Display available requests
    print("\nAvailable Routing Requests")
    print("-" * 35)

    for request in requests:
        print(
            f"Request {request['id']}: "
            f"{request['source']} -> {request['destination']}"
        )

    # Select a request
    request_id = int(input("\nEnter Request ID to visualize: "))

    selected_request = next(
        (
            request for request in requests
            if request["id"] == request_id
        ),
        None
    )

    if selected_request is None:
        print("Invalid Request ID!")
        return

    source = selected_request["source"]
    destination = selected_request["destination"]

    # Calculate shortest path using Dijkstra
    path, total_latency = network.shortest_path(
        source,
        destination
    )

    if path is None:
        print("No route exists between these routers.")
        return

    # Identify shortest-path edges
    path_edges = list(zip(path, path[1:]))

    # Arrange routers visually
    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.5
    )

    # Draw complete network
    plt.figure(figsize=(13, 8))

    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="lightgray",
        width=2
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color="skyblue",
        node_size=1800
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=11,
        font_weight="bold"
    )

    # Highlight shortest route
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=path_edges,
        edge_color="red",
        width=4
    )

    # Highlight source and destination
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[source],
        node_color="green",
        node_size=2000
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[destination],
        node_color="orange",
        node_size=2000
    )

    # Display latency on every connection
    edge_labels = nx.get_edge_attributes(
        graph,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=10
    )

    # Display route information
    route_text = " -> ".join(path)

    plt.title(
        f"Internet Network Routing Optimizer\n"
        f"Source: {source} | Destination: {destination}\n"
        f"Shortest Route: {route_text}\n"
        f"Total Latency: {total_latency} units",
        fontsize=12
    )

    plt.axis("off")
    plt.tight_layout()

    print("\nRouting Result")
    print("-" * 35)
    print("Source:", source)
    print("Destination:", destination)
    print("Shortest Route:", route_text)
    print("Total Latency:", total_latency, "units")

    plt.show()


if __name__ == "__main__":

    filename = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "data.json"
    )

    try:
        visualize_network(filename)

    except (OSError, json.JSONDecodeError, ValueError, KeyError) as error:
        print("Error:", error)
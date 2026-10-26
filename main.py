import json
import sys

from dijkstra import Network


def load_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "data.json"

    try:
        data = load_data(filename)

        network = Network()

        for router in data["routers"]:
            network.add_router(router["id"])

        for connection in data["connections"]:
            network.add_connection(
                connection["router1"],
                connection["router2"],
                connection["latency"]
            )

        print("=" * 60)
        print("       INTERNET NETWORK ROUTING OPTIMIZER")
        print("=" * 60)

        print("\nNETWORK ROUTING RESULTS\n")

        for request in data["requests"]:
            source = request["source"]
            destination = request["destination"]

            path, total_latency = network.shortest_path(
                source,
                destination
            )

            print(f"Request ID: {request['id']}")
            print(f"Source Router: {source}")
            print(f"Destination Router: {destination}")

            if path is None:
                print("Status: No route available")
            else:
                print("Optimal Route:", " -> ".join(path))
                print(f"Total Latency: {total_latency} units")

            print("-" * 60)

    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
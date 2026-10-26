import heapq


class Network:

    def __init__(self):
        self.graph = {}

    def add_router(self, router):
        if router not in self.graph:
            self.graph[router] = {}

    def add_connection(self, source, destination, latency):
        self.add_router(source)
        self.add_router(destination)

        self.graph[source][destination] = latency
        self.graph[destination][source] = latency

    def shortest_path(self, source, destination):

        if source not in self.graph:
            return None, float("inf")

        if destination not in self.graph:
            return None, float("inf")

        distances = {}

        previous = {}

        for router in self.graph:
            distances[router] = float("inf")
            previous[router] = None

        distances[source] = 0

        priority_queue = [(0, source)]

        while priority_queue:

            current_distance, current_router = heapq.heappop(
                priority_queue
            )

            if current_distance > distances[current_router]:
                continue

            if current_router == destination:
                break

            for neighbor, latency in self.graph[current_router].items():

                new_distance = current_distance + latency

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance
                    previous[neighbor] = current_router

                    heapq.heappush(
                        priority_queue,
                        (new_distance, neighbor)
                    )

        if distances[destination] == float("inf"):
            return None, float("inf")

        path = []

        current_router = destination

        while current_router is not None:
            path.append(current_router)
            current_router = previous[current_router]

        path.reverse()

        return path, distances[destination]
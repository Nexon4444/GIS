import numpy as np
import queue
import collections

b = np.loadtxt(r'data.csv', dtype=str, delimiter='|', skiprows=1, usecols=np.r_[0:2])
data = []
for row in b:
    data.append((row[0], row[1].split("; ")))

publication_degrees = {}

for row in data:
    publication_degrees[len(row[1])] = publication_degrees.get(len(row[1]), 0) + 1

ordered_publication_degrees = collections.OrderedDict(sorted(publication_degrees.items()))

sum = 0
publications = len(data)
for item in ordered_publication_degrees:
    sum = sum + item * ordered_publication_degrees[item]

pub_degrees = []
for item in ordered_publication_degrees:
    for i in range(ordered_publication_degrees[item]):
        pub_degrees.append(item)

if publications % 2 == 1:
    median = pub_degrees[(publications - 1)/2 + 1]
else:
    index = int(publications/2)
    median = (pub_degrees[index] + pub_degrees[index + 1]) / 2

print('Publications: degrees, average, median')
print(ordered_publication_degrees)
print(sum/publications)
print(median)

authors_degrees = {}

for row in data:
    for author in row[1]:
        authors_degrees[author] = authors_degrees.get(author, 0) + 1

ordered_authors_degrees = {k: v for k, v in sorted(authors_degrees.items(), key=lambda item: item[1])}

author_degrees = {}
for item in ordered_authors_degrees:
    author_degrees[ordered_authors_degrees[item]] = author_degrees.get(ordered_authors_degrees[item], 0) + 1

degrees = []
for item in ordered_authors_degrees:
    degrees.append(ordered_authors_degrees[item])

sum_authors = 0
authors = len(ordered_authors_degrees.keys())
for item in ordered_authors_degrees:
    sum_authors = sum_authors + ordered_authors_degrees[item]

if int(authors) % 2 == 1:
    median = degrees[(authors - 1)/2 + 1]
else:
    index = int(authors/2)
    median = (degrees[index] + degrees[index + 1]) / 2

print('Authors: degrees, average, median')
print(author_degrees)
print(sum_authors/authors)
print(median)


# build collaboration_graph
class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.label] = node

    def add_edge(self, label1, label2):
        self.nodes[label1].add_neighbour(self.nodes[label2])
        self.nodes[label2].add_neighbour(self.nodes[label1])

    def count_edges(self):
        edges = 0
        for item in self.nodes.items():
            edges = edges + len(item[1].neighbours)
        return int(edges/2)

    def degrees_distribution(self):
        distribution = {}
        sum = 0
        for item in self.nodes.items():
            distribution[item[1].number_of_neighbours()] = distribution.get(item[1].number_of_neighbours(), 0) + 1
            sum = sum + len(item[1].neighbours)
        ordered_distribution = collections.OrderedDict(sorted(distribution.items()))
        average = sum / (2 * self.count_vertices())
        list_of_degrees = []
        for item in ordered_distribution:
            for i in range(ordered_distribution[item]):
                list_of_degrees.append(item)

        temp = len(list_of_degrees)
        if temp % 2 == 1:
            median = list_of_degrees[(temp - 1)/2 + 1]
        else:
            index = int(temp/2)
            median = (list_of_degrees[index] + list_of_degrees[index + 1]) / 2

        return (ordered_distribution, average, median)

    def count_vertices(self):
        return len(self.nodes.items())

    def density(self):
        return (2 * self.count_edges()) / (self.count_vertices() * (self.count_vertices() - 1))

    def count_inconsistent_subgraphs(self):
        visited = set()
        previous_visited = len(visited)
        size_distribution = {}
        subgraphs = 0
        max_size = 0
        while len(visited) != len(self.nodes):
            for node in self.nodes.items():
                if not visited.__contains__(node[0]):
                    (visited, dist) = self.bfs(node[1], visited)
                    subgraphs = subgraphs + 1
                    size = len(visited) - previous_visited
                    previous_visited = len(visited)
                    if size > max_size:
                        max_size = size
                        biggest_start_node = node
                    size_distribution[size] = size_distribution.get(size, 0) + 1

        ordered_distribution = collections.OrderedDict(sorted(size_distribution.items()))
        return (subgraphs, ordered_distribution, biggest_start_node)

    def bfs(self, starting_node, visited):
        q = queue.Queue()
        q.put(starting_node)
        visited.add(starting_node.label)
        distance = {}
        distance[starting_node.label] = 0
        while not q.empty():
            v = q.get()
            for node in v.neighbours:
                if not visited.__contains__(node.label):
                    distance[node.label] = distance[v.label] + 1
                    visited.add(node.label)
                    q.put(self.nodes[node.label])
        ordered_distance = collections.OrderedDict(sorted(distance.items()))
        return (visited, ordered_distance)

    def clasterization_factor(self):
        sum = 0
        clasterization_distribution = {}
        for node in self.nodes:
            temp = self.clasterization_for_node(self.nodes[node])
            clasterization_distribution[temp] = clasterization_distribution.get(temp, 0) + 1
            sum = sum + temp
        ordered_distribution = collections.OrderedDict(sorted(clasterization_distribution.items()))
        return (sum / self.count_vertices(), ordered_distribution)

    def clasterization_for_node(self, node):
        if node.number_of_neighbours() < 2:
            return 0
        neighbours_connections = 0
        for neighbour1 in node.neighbours:
            for neighbour2 in node.neighbours:
                if self.nodes[neighbour1.label].neighbours.__contains__(self.nodes[neighbour2.label]):
                    neighbours_connections = neighbours_connections + 1
        return neighbours_connections / (node.number_of_neighbours() * (node.number_of_neighbours() - 1))

    def clasterization_factor_4(self):
        sum = 0
        count_nodes = 0
        for node in self.nodes:
            if self.nodes[node].number_of_neighbours() >= 4:
                count_nodes = count_nodes + 1
                sum = sum + self.clasterization_for_node(self.nodes[node])
        return sum / count_nodes

    def clasterization_factor_for(self, labels):
        if len(labels) == 0:
            return 0
        sum = 0
        for label in labels:
            sum = sum + self.clasterization_for_node(self.nodes[label])
        return sum / len(labels)


class Node:
    def __init__(self, label):
        self.label = label
        self.neighbours = set()

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def number_of_neighbours(self):
        return len(self.neighbours)


graph = Graph()
for author in authors_degrees:
    graph.add_node(Node(author))

for row in data:
    for i in range(len(row[1])):
        for j in range(i+1, len(row[1])):
            graph.add_edge(row[1][i], row[1][j])

print("Collaboration graph: density, degree distribution, average degree, median degree")
print(graph.density())
(distribution, average, median) = graph.degrees_distribution()
print(distribution)
print(average)
print(median)

(subgraphs, subgraphs_distribution, biggest_start_node) = graph.count_inconsistent_subgraphs()
print("Number of subgraphs")
print(subgraphs)
print(subgraphs_distribution)
print(biggest_start_node[0])
(visited, distance) = graph.bfs(biggest_start_node[1], set())
dist = {}
for item in distance:
    dist[distance[item]] = dist.get(distance[item], 0) + 1
print(dist)

(clasterization, clasterization_distribution) = graph.clasterization_factor()
print("Clasterization factor")
print(clasterization)
print(clasterization_distribution)
# for item in clasterization_distribution:
#     print("{item},{count}".format(item=item, count=clasterization_distribution[item]))

clasterization4 = graph.clasterization_factor_4()
print("Clasterization factor for vertices with degree at least 4")
print(clasterization4)

top25 = list(ordered_authors_degrees.keys())[-25:]
clasterization_top25 = graph.clasterization_factor_for(top25)
print("Clasterization factor for top 25 authors")
print(clasterization_top25)

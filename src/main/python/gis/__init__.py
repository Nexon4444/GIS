import numpy as np
import queue
import collections
b = np.loadtxt(r'data.csv', dtype=str, delimiter=',', skiprows=1, usecols=np.r_[0:2])
data = []
for row in b:
    data.append((row[0].replace('"', ''), row[1].replace('"', '').split("; ")))

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
        average = sum / self.count_vertices()
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
        subgraphs = 0
        while len(visited) != len(self.nodes):
            for node in self.nodes.items():
                if not visited.__contains__(node[0]):
                    visited = self.bfs(node[1], visited)
                    subgraphs = subgraphs + 1
        return subgraphs

    def bfs(self, starting_node, visited):
        q = queue.Queue()
        q.put(starting_node)
        visited.add(starting_node.label)
        while not q.empty():
            v = q.get()
            for node in v.neighbours:
                if not visited.__contains__(node.label):
                    visited.add(node.label)
                    q.put(self.nodes[node.label])

        return visited



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

subgraphs = graph.count_inconsistent_subgraphs()
print("Number of subgraphs")
print(subgraphs)

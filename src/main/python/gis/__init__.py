import numpy as np
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


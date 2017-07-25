#!/usr/bin/env python3

cast = ["Cleese", 'Palin', 'Jones', "Idle"]
print(cast)
print(len(cast))
print(cast[1])
cast.append("Gilliam")
print(cast)
cast.pop()
print(cast)
cast.extend(["Gilliam", "Chapman"])
print(cast)
cast.remove("Chapman")
print(cast)
cast.insert(0, "Chapman")
print(cast)

movies = ["The Holy Grail", "The Life of Brian", "The Meaning of Life"]
print(movies[1])
movies.insert(1, 1975)
movies.insert(3, 1979)
movies.append(1983)
print(movies)
movies = ["The Holy Grail", 1975, "The Life of Brian", 1979, "The Meaning of Life", 1983]
print(movies)

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
print(movies)
print(movies[4][1][3])



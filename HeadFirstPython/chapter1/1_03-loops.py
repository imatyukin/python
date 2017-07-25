#!/usr/bin/env python3

fav_movies = ["The Holy Grail", "The Life of Brian"]

for each_flick in fav_movies:
    print(each_flick)
    

count = 0
while count < len(fav_movies):
    print(fav_movies[count])
    count = count+1
    

names = ['Michael', 'Terry']
print(names)
print(isinstance(names, list))
num_names = len(names)
print(num_names)
print(isinstance(num_names, list))


movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
print(movies)

for each_item in movies:
    if isinstance(each_item, list):
        for nested_item in each_item:
            if isinstance(nested_item, list):
                for deeper_item in nested_item:
                    print(deeper_item)
            else:
                print(nested_item)
    else:
        print(each_item)



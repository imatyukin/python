#!/usr/bin/env python3

my_foods = ['pizza', 'falafel', 'carrot cake'] 
friend_foods = my_foods[:] 
print(my_foods)
print(friend_foods)

my_foods.append('cannoli') 
friend_foods.append('ice cream') 

mylist = []
for x in my_foods:
    mylist.append(str(x))
print(mylist)

mylist = []
for x in friend_foods:
    mylist.append(str(x))
print(mylist)
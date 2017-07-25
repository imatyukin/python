#!/usr/bin/env python3

Animals = ["Mammal Class", "Bird Class", "Amphibian Class", "Reptila Class", "Bony Fish Class", \
           "Perissodactyla Class", "Proboscidea Class"]

myAnimals = Animals[:3]
print("The first three items in the list are:")
print(myAnimals)

myAnimals = Animals[3:6]
print("Three items from the middle of the list are:")
print(myAnimals)

myAnimals = Animals[-3:]
print("The last three items in the list are:")
print(myAnimals)
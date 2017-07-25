#!/usr/bin/env python3

Animals = ["Mammal Class", "Bird Class", "Amphibian Class", "Reptila Class", "Bony Fish Class", \
           "Perissodactyla Class", "Proboscidea Class"]

for Class in Animals:
    if Class == "Mammal Class":
        print(Class + ": These animals usually have hair/fur. " \
              "They give birth to live young and feed their young with milk. " \
              "Mammals are warm-blooded. " \
              "Includes: Rodents, Hoofed animals, Marsupials, Bats, Rabbits, Weasels, Raccoons, Bears, Dogs, and Cats.")
    elif Class == "Bird Class":
        print(Class + ': This class is also called "Aves." ' \
              'Birds are warm-blooded. ' \
              'They have hollow bones and feathers. ' \
              'Most can fly at least short distances. ' \
              'Birds are born from hard-shelled eggs. ' \
              'Includes: Raptors, Gulls, Songbirds, and Fowl.')
    elif Class == "Amphibian Class":
        print(Class + ": These animals have smooth skin, and most spend at least part of their life in water. " \
              "Amphibians are cold-blooded. " \
              "They usually have three life stages: egg, larva, adult. " \
              "Includes: Frogs, Toads, Salamanders, and Newts.")
    elif Class == "Reptila Class":
        print(Class + ": These animals have dry, scaly skin. " \
              "They are cold-blooded. " \
              "Most reptiles lay soft-shelled eggs, but some bear live young. " \
              "Includes: Lizards, Snakes, Turtles, and Crocodiles.")
    elif Class == "Bony Fish Class":
        print(Class + ': This class is also called "Osteichthyes." ' \
              'It includes almost all fish. ' \
              'Skeletons are made of mostly bone. ' \
              'Includes: Sunfish, Catfish, Minnows, Perch, Goldfish, and most others.')
    elif Class == "Perissodactyla Class":
        print(Class + ": includes horses, zebras. " \
              "Artiodactyla: includes those animals such as cows.")
    else:
        print(Class + ": includes elephants, among others.")
print("These animals are also called vertebrates.")

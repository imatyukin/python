#!/usr/bin/env python3
from fantasy_game_inventory import displayInventory


def main():
    inv = {'gold coin': 42, 'rope': 1}
    dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
    inv = addToInventory(inv, dragonLoot)
    displayInventory(inv)


def addToInventory(inventory, addedItems):
    for item in addedItems:
        for k in list(inventory.keys()):
            if item != k:
                inventory.setdefault(item, 1)
            else:
                inventory[k] += 1

    return inventory


if __name__ == "__main__":
    main()

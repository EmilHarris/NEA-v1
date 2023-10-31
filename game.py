import pygame as py

class Game:
    fullBlocks = []

    def __init__(self):
        pass

class Node:
    data = None
    pointer = 0

    def __init__(self, data, pointer):
        self.setData(data)
        self.setPointer(pointer)

    def setPointer(self, pointer):
        self.pointer = pointer

    def getPointer(self):
        return self.pointer

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

class linkedList:
    head = 0
    tail = 0
    vals = []

    def __init__(self, vals):
        for i, val in enumerate(vals):
            self.vals.append(Node(val, i))
        self.head = 0
        self.tail = len(vals) - 1

    def removeNode(self, position):
        delNode = self.findNode(self, position)
        for node in self.vals[position + 1:]:
            node.setPointer(node.getPointer() - 1)

    def findNode(self, pointer):
        if self.head <= pointer <= self.tail:
            for node in self.vals:
                if node.pointer == pointer:
                    return node
        return None



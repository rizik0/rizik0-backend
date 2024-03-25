class Player:
    def __init__(self, name, goal):
        self.name = name
        self.goal = goal

    def __str__(self):
        return f"Name: {self.name}, Goal: {self.goal}"
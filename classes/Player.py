class Player:
    def __init__(self, name, goal, color):
        self.name = name
        self.goal = goal
        self.color = color
        self.initial_units = 21

    def __str__(self):
        return f"{self.name} in {self.color} wins if conquer {self.goal}"
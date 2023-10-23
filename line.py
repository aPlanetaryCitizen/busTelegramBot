class Line:
    def __init__(self, number, places):
        self.number = number
        self.places = places

    def to_text(self):
        return f"{self.number}   " " - ".join(self.places)
class bi:
    def __init__(self, a):
        self.a = a
        self.b = 0

    def __ilshift__(self, other):
        self.b += 1
        return self


class Like:
    def __init__(self, something):
        self.something = something

    def __str__(self):
        return "LIKE"

    def __or__(self, other):
        if not self.something:
            self.something = other
            return self
        else:
            return ""



LIKE = Like()
a = 2
b = '%3%'

print(a |LIKE| b)

a |LIKE| b

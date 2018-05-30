class A:
    def __init__(self):
        self.a = 10

def chang(b):
    b.a = 20

c = A()
print(c.a)
chang(c)
print(c.a)
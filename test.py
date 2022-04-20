class hello:

    def __init__(self, a= 'weclome'):
        self.a = a
    def welcome(self, x):
        print(self.a+x)

h = hello()
h.welcome('turninr')

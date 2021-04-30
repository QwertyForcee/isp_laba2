class MyRange():
    def __init__(self,*args):
        if len(args)==1:
            self.start = 0
            self.end = args[0]
            self.step = 1 
        elif len(args)==2:
            self.start = args[0]
            self.end = args[1]
            self.step = 1
        elif len(args)==3:
            self.start = args[0]
            self.end = args[1]
            self.step = args[2]
        else:
            self.start = 0
            self.end = 0
            self.step = 0
        
        self.current = self.start

    def __repr__(self):
        return f"myrange(start={self.start},end={self.end},step={self.step})"

    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.current<self.end):
            temp = self.current
            self.current+=self.step
            return temp
        else:
            self.current=self.start
            raise StopIteration

r = MyRange(10,17,2)
for x in r:
    print(x)
print(r.current)


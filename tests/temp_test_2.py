def decorator_function(target):
    def wrap(self, *args, **kwargs):
        self.upd()
        return target(self, *args, **kwargs)

    return wrap



class Target:

    def upd(self):
        print(0)

    @decorator_function
    def qq(self):
        print(12)


a = Target()
a.qq()
a.qq()
a.qq()

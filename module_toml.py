from toml_serializer import TomlSerializer

class Engine:
    status=False
    def show(self):
        print('this is an engine')
    def start(self):
        if not self.status:
            self.status=True

    def kill(self):
        if self.status:
            self.status=False



data = TomlSerializer().dumps(Engine)
TomlSerializer().dump(Engine,open('somedata.toml','w'))
e = TomlSerializer().load(open('somedata.toml'))
e1 = e()
print(e1.status)
e1.show()
e1.start()
print(e1.status)

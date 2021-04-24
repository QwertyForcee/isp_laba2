from toml_serializer import TomlSerializer

class Engine:
    status=False
    def show(self):
        print('this is an engine')
    def Start(self):
        if not self.status:
            self.status=True

    def Kill(self):
        if self.status:
            self.status=False



data = TomlSerializer().dumps(Engine)
#TomlSerializer().dump(Engine,open('somedata.toml','w'))
e = TomlSerializer().loads(data)
e1 = e()
print(e1.status)
e.show(e1)
e1.Start
print(e1.status)

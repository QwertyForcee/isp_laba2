from toml_serializer import TomlSerializer

class Engine:
    status=False
    def Start(self):
        if not self.status:
            self.status=True

    def Kill(self):
        if self.status:
            self.status=False



data = TomlSerializer().dumps(Engine)
TomlSerializer().dump(Engine,open('somedata.toml','w'))
obj = TomlSerializer().loads(data)
print(obj())


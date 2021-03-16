import actors.actor


class RoleDescriptor(object):
    class_module: str
    class_name: str

    def __init__(self, name: str, module: str):
        self.class_name = name
        self.class_module = module

    @staticmethod
    def from_class(target) -> 'actors.actor.RoleDescriptor':
        return RoleDescriptor(target.__name__, target.__module__)

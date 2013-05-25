__author__ = 'SolPie'


def singleton(cls):
    instances = {}

    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
            # if cls.name not in instances:
        #     instances[cls.name] = cls()
        return instances[cls]

    return getInstance


def table(cls):
    instances = {}

    def getInstance(*args):
        if cls.name not in instances:
            instances[cls.name] = cls(*args)
        return instances[cls.name]

    return getInstance


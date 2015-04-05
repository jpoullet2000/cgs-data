class generalException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class createDataStructureException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class ReadingDataFileException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

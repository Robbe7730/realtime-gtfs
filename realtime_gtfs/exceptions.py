class InvalidKeyError(RuntimeError):
   def __init__(self, arg):
       self.args = ["Invalid key " + arg]

class MissingKeyError(RuntimeError):
   def __init__(self, arg):
       self.args = ["Missing key " + arg]
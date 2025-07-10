#Product object, for a possible change of input type
#class Product:
#    def __init__(self, id, model, price, rating=0):
#        self.id = id
#        self.model = model
#        self.price = price
#        self.rating = rating
#    def __str__(self):
#        return f"{self.id}, {self.model}, {self.price}, {self.rating}"

#Old id-assignment function
#def get_id(arr):
#    max_id = 0
#    for elem in arr:
#        if elem["id"] > max_id:
#            max_id = elem["id"]
#    return max_id + 1
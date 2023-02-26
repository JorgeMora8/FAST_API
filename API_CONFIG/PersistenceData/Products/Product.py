from ...resorces.getID import get_unique_id

class Product: 
    def __init__(self, name, price, inventory): 
        self._name = name
        self._price = price
        self._inventory = inventory

    def DTO(self): 
        product = { 
            "id": get_unique_id(),
            "name":self._name,
            "price":self._price,
            "inventory":self._inventory
        }

        return product
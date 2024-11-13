class Product:
    def __init__(self, name: str, product_id: int):
        self.name: str = name
        self.product_id: int = product_id

class Branch:
    def __init__(self, name: str, products: list[Product]):
        self.name: str = name
        self.products: list[Product] = products

class ProductTree:
    def __init__(self):
        self.branches: list[Branch] = []
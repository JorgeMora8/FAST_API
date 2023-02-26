class ProductRepository: 
    def __init__(self, DAO): 
        self.DAO = DAO

    def save(self, product): 
        product_DTO = product.DTO()
        self.DAO.save(product_DTO)
        return product_DTO

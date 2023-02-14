from fastapi import APIRouter, status, Request
from ..main import PostgresService
from ..models import Product

productsRouter = APIRouter(prefix="/products")

#Get all products
@productsRouter.get("/", tags=["products"], status_code=status.HTTP_200_OK)
async def get_products(request: Request): 
    return PostgresService.get_products()

#Get one product that match one id
@productsRouter.get("/{id}") 
async def get_product_by_id(id: int): 
    return PostgresService.get_product_by_id(id)

#Add one products filling the data required
@productsRouter.post("/", tags=["products"], status_code=status.HTTP_201_CREATED)
async def addProduct(productData: Product): 
        return PostgresService.add_product(productData)

#Update one product that match one Id
@productsRouter.put("/{id}", tags=["products"], status_code=status.HTTP_201_CREATED)
async def updateProduct(id:int, productData:Product): 
    return PostgresService.update_product(id, productData)


#Delete one product that match an ID
@productsRouter.delete("/{id}", tags=["products"], status_code=status.HTTP_204_NO_CONTENT)
async def deleteProduct(id:int): 
    return PostgresService.delete_product(id)

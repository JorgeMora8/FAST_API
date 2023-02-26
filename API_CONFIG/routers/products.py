from fastapi import APIRouter, status, Request, Depends
from ..DAO.productDAO import PostgresService
from ..Models.models import Product
from fastapi.exceptions import HTTPException
from sqlalchemy import insert

productsRouter = APIRouter(prefix="/products")


#SQL_ALCHEMY
from ..DAO.productDAO import get_db
from sqlalchemy.orm import Session
from ..Models.models import Product_SQL


#Get all products
@productsRouter.get("/", tags=["products"], status_code=status.HTTP_200_OK)
async def get_products(db:Session = Depends(get_db)): 

    data = db.query(Product_SQL).all()
    # return PostgresService.get_products()
    return data

#Get one product that match one id
@productsRouter.get("/{id}") 
async def get_product_by_id(id: str, db:Session = Depends(get_db)): 
     
    # try:
    #     return PostgresService.get_product_by_id(id)
    # except Exception as error: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product dont found")

#Add one products filling the data required
@productsRouter.post("/", tags=["products"], status_code=status.HTTP_201_CREATED)
async def addProduct(productData: Product, db:Session = Depends(get_db)): 
        # return PostgresService.add_product(productData)
        new_product = Product_SQL(name=productData.name, price=productData.price, inventory= productData.inventory)
        db.add(new_product)
        db.commit()
        return {"ok"}

#Update one product that match one Id
@productsRouter.put("/{id}", tags=["products"], status_code=status.HTTP_201_CREATED)
async def updateProduct(id:int, productData:Product): 
    return PostgresService.update_product(id, productData)


#Delete one product that match an ID
@productsRouter.delete("/{id}", tags=["products"], status_code=status.HTTP_204_NO_CONTENT)
async def deleteProduct(id:int): 
    return PostgresService.delete_product(id)

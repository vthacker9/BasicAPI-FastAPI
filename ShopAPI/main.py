import models
import schemas
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    The get_db function is a helper function that is used to create a database session.
    It will be called when the application needs to access the database, and it will return
    a database session that can be used to query for objects or collections of objects.
    
    :return: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"data": "Hello from FastAPI!"}


@app.post("/create_product")
def create_product(title:str, description:str, price:int, db:Session=Depends(get_db)):
    """
    The create_product function creates a new product in the database.
    It takes four parameters: title, description, price and db (the SQLAlchemy Session).
    The function creates a new Product object with the given data and adds it to the database.
    Finally, it returns that newly created Product object.
    
    :param title:str: Specify the title of the product
    :param description:str: Specify that the description parameter is a string
    :param price:int: Specify that the price should be an integer
    :param db:Session=Depends(get_db): Inject the database session into the function
    :return: A product object
    """
    product = models.Product(title=title, description=description, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/get_product/{product_id}")
def get_product(product_id:int, db:Session=Depends(get_db)):
    """
    The get_product function takes a product_id and returns the corresponding Product object.
    If no such Product exists, it raises an HTTPException with status code 404.
    
    :param product_id:int: Specify the id of the product we want to retrieve
    :param db:Session=Depends(get_db): Pass the database session to the function
    :return: The product with the given id
    """
    product = db.query(models.Product).get(product_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/list_products")
def get_all_products(db:Session=Depends(get_db)):
    """
    The get_all_products function is used to retrieve all products from the database.
    It takes a single argument, db, which is an instance of SessionLocal() and returns 
    a list of Product objects.
    
    :param db:Session=Depends(get_db): Inject the database session into the function
    :return: A list of all the products in the database
    """
    products = db.query(models.Product).all()
    if products:
        return products
    raise HTTPException(status_code=404, detail="No products found")


@app.patch('/update_product/{product_id}',response_model=schemas.Product)
def update_product(product_id: int, product_request: schemas.Product, db: Session = Depends(get_db)):
    """
    The update_product function updates a product in the database.
    It takes two arguments, product_id and the updated Product object.
    If a product with that ID exists, it updates it with the new data from the Product object.
    If not, it raises an HTTPException with status code 400
    
    :param product_id:int: Identify the product to be updated
    :param product_request:schemas.Product: Validate the data sent in the request
    :param db:Session=Depends(get_db): Get the database session
    :return: The updated product
    """
    #TODO partial update
    product = db.get(models.Product, product_id)
    if product:
        update_item_encoded = jsonable_encoder(product_request)
        product.title = update_item_encoded['title']
        product.price = update_item_encoded['price']
        product.description = update_item_encoded['description']
        db.commit()
        db.refresh(product)
        return product
    else:
        raise HTTPException(status_code=400, detail="Product not found with the given ID")
    

@app.delete("/deletet_product/{product_id}")
def delete_product(product_id:int, db:Session=Depends(get_db)):
    """
    The delete_product function deletes a product from the database.
    It takes in an integer representing the id of the product to be deleted, and returns a dictionary with one key: Success.
    The value for this key is a string that says Product deleted successfully with id. 
    
    :param product_id:int: Identify the product to be deleted
    :param db:Session=Depends(get_db): Inject the database session into the function
    """
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found with given id")
    db.delete(product)
    db.commit()
    return {"Success": f"Product deleted successfully with id of {product_id}"}
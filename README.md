# Ecommerce API with Flask & MySQL

A RESTful API for managing users, products, and orders. Built with Flask, SQLAlchemy, Marshmallow, and MySQL.

---

## Technologies Used
- Flask
- Flask-SQLAlchemy
- Marshmallow
- MySQL
- Postman (for testing)

## API Endpoints
- Users
    - GET /users
    - GET /users/<id>
    - POST /users
    - PUT /users/<id>
    - DELETE /users/<id>_
- Products
    - GET /products
    - GET /products/<id>
    - POST /products
    - PUT /products/<id>
    - DELETE /products/<id>
- Orders
    - POST /orders
    - PUT /orders/<order_id>/add_product/<product_id>
    - DELETE /orders/<order_id>/remove_product/<product_id>
    - GET /orders/user/<user_id>
    - GET /orders/<order_id>/products
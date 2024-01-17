# LittleLemonAPI
API
## URLS

> [!NOTE]
> All routes have a security layer so that only an Admin user can modify, delete, or add
### URLS Auth
- `auth/token/login` 
- `auth/token/logout`
- `auth/users`
### URLS Category
- `api/categories`
- `api/categories/{UUID-category_id}`
### URLS Product
- `api/products`
- `api/products/{UUID-product_id}`
### URLS Cart
- `api/carts`
- `api/carts/{UUID-cart_id}`
- `api/carts/{UUID-cart_id}/items`
- `api/carts/{UUID-cart_id}/items/{UUID-item_id}`
### URLS Order
- `api/orders`
- `api/orders/{UUID-order_id}`

## Package
> [!NOTE]
> List of packages used in the project
### Package Used
- `django`
- `djangorestframework`
- `djangorestframework-xml`
- `djoser`
- `uuid`
- `drf-nested-routers`

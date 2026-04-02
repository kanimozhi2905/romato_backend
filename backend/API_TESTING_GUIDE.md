# API Testing Guide

This guide provides examples for testing the Food Delivery API using curl or any API client like Postman.

## Base URL
```
http://127.0.0.1:8000
```

## 1. Authentication

### Register New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

Response will include:
- `access`: JWT access token
- `refresh`: JWT refresh token
- `user`: User information

### Get User Profile
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated"
  }'
```

## 2. Categories

### List All Categories
```bash
curl -X GET http://127.0.0.1:8000/api/categories/
```

### Get Category Details
```bash
curl -X GET http://127.0.0.1:8000/api/categories/1/
```

### Create Category (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pizza",
    "description": "Delicious pizzas from Italy"
  }'
```

## 3. Food Items

### List All Food Items
```bash
curl -X GET "http://127.0.0.1:8000/api/foods/?category_id=1&is_available=true&search=pizza&ordering=-price"
```

Query Parameters:
- `category_id`: Filter by category
- `is_available`: Filter availability (true/false)
- `search`: Search in name and description
- `ordering`: Order by field (prefix with `-` for descending)

### Get Food Item Details
```bash
curl -X GET http://127.0.0.1:8000/api/foods/1/
```

### Create Food Item (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/foods/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -F "name=Margherita Pizza" \
  -F "description=Classic pizza with tomato sauce, mozzarella, and basil" \
  -F "price=12.99" \
  -F "category_id=1" \
  -F "image=@/path/to/image.jpg" \
  -F "is_available=true"
```

### Update Food Item (Admin Only)
```bash
curl -X PUT http://127.0.0.1:8000/api/foods/1/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 14.99,
    "is_available": false
  }'
```

### Delete Food Item (Admin Only)
```bash
curl -X DELETE http://127.0.0.1:8000/api/foods/1/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

## 4. Cart

**Note**: All cart endpoints require authentication.

### Get User's Cart
```bash
curl -X GET http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Add Item to Cart
```bash
curl -X POST http://127.0.0.1:8000/api/cart/add/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "food_item_id": 1,
    "quantity": 2
  }'
```

### Update Cart Item Quantity
```bash
curl -X POST http://127.0.0.1:8000/api/cart/update/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3
  }'
```

### Remove Item from Cart
```bash
curl -X POST http://127.0.0.1:8000/api/cart/remove/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Clear Entire Cart
```bash
curl -X POST http://127.0.0.1:8000/api/cart/clear/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 5. Orders

**Note**: All order endpoints require authentication.

### Place New Order
```bash
curl -X POST http://127.0.0.1:8000/api/orders/place/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_name": "John Doe",
    "delivery_address": "123 Main St, Apt 4B",
    "delivery_city": "New York",
    "delivery_pincode": "100001",
    "delivery_phone": "9876543210"
  }'
```

This will:
1. Create an order from current cart items
2. Calculate total amount
3. Clear the cart
4. Return order details

### Get User's Orders
```bash
curl -X GET http://127.0.0.1:8000/api/orders/my-orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Order Details
```bash
curl -X GET http://127.0.0.1:8000/api/orders/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Order Status (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/update-status/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Preparing"
  }'
```

Available statuses:
- `Pending`
- `Preparing`
- `Out for Delivery`
- `Delivered`
- `Cancelled`

## Complete Testing Workflow

### 1. Register and Login
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login and save token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the `access` token from the response.

### 2. Browse Food
```bash
# Set token variable (Linux/Mac)
export TOKEN="your_access_token_here"

# Set token variable (Windows PowerShell)
$TOKEN = "your_access_token_here"

# View categories
curl -X GET http://127.0.0.1:8000/api/categories/

# View food items
curl -X GET http://127.0.0.1:8000/api/foods/
```

### 3. Add to Cart
```bash
curl -X POST http://127.0.0.1:8000/api/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "food_item_id": 1,
    "quantity": 2
  }'

curl -X POST http://127.0.0.1:8000/api/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "food_item_id": 2,
    "quantity": 1
  }'
```

### 4. View Cart
```bash
curl -X GET http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Place Order
```bash
curl -X POST http://127.0.0.1:8000/api/orders/place/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_name": "Test User",
    "delivery_address": "123 Test Street",
    "delivery_city": "Test City",
    "delivery_pincode": "123456",
    "delivery_phone": "9876543210"
  }'
```

### 6. View Order History
```bash
curl -X GET http://127.0.0.1:8000/api/orders/my-orders/ \
  -H "Authorization: Bearer $TOKEN"
```

## Using Postman

1. Import the API documentation from `/api/docs/`
2. Create an environment with variable `access_token`
3. Use `{{access_token}}` in Authorization headers
4. Save commonly used requests as collections

## Common Response Codes

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful resource creation
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid data or validation error
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server error

## Error Response Format

```json
{
  "success": false,
  "error": "Error message here",
  "errors": {
    "field_name": ["Specific field error"]
  }
}
```

Success Response Format

```json
{
  "success": true,
  "message": "Success message",
  "data": {
    // Response data
  }
}
```

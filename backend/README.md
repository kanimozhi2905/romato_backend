# Food Delivery Backend API

A complete, production-ready backend for a food delivery application built with Django and Django REST Framework.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration, login, and profile management
- **Food Management**: Browse food items by category, search, and filter
- **Cart Management**: Add, update, remove items from cart with real-time total calculation
- **Order Placement**: Complete order workflow with address validation
- **Order History**: Track current and past orders
- **Admin Panel**: Full-featured admin interface for managing food items, categories, and orders
- **API Documentation**: Auto-generated Swagger/ReDoc documentation

## 📁 Project Structure

```
backend/
├── food_delivery/          # Main Django project
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── apps/                   # Django applications
│   ├── authentication/     # User auth & JWT
│   ├── food/              # Food items & categories
│   ├── cart/              # Shopping cart
│   └── orders/            # Order management
├── manage.py
├── requirements.txt
└── .env
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

The `.env` file is already configured with default values. Update if needed:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Step 3: Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin account:
- Email address
- Name
- Password

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/token/refresh/` | Refresh JWT token | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT | `/api/auth/profile/` | Update user profile | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |

### Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| GET | `/api/categories/{id}/` | Get category details | No |
| POST | `/api/categories/` | Create category | Yes (Admin) |
| PUT | `/api/categories/{id}/` | Update category | Yes (Admin) |
| DELETE | `/api/categories/{id}/` | Delete category | Yes (Admin) |

### Food Items

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/foods/` | List all food items | No |
| GET | `/api/foods/{id}/` | Get food item details | No |
| POST | `/api/foods/` | Create food item | Yes (Admin) |
| PUT | `/api/foods/{id}/` | Update food item | Yes (Admin) |
| DELETE | `/api/foods/{id}/` | Delete food item | Yes (Admin) |

**Query Parameters for GET /api/foods/:**
- `category_id`: Filter by category
- `is_available`: Filter availability (default: true)
- `search`: Search by name or description
- `ordering`: Order by `price`, `name`, or `created_at`

### Cart

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart/` | Get user's cart | Yes |
| POST | `/api/cart/add/` | Add item to cart | Yes |
| POST | `/api/cart/update/{item_id}/` | Update cart item quantity | Yes |
| POST | `/api/cart/remove/{item_id}/` | Remove item from cart | Yes |
| POST | `/api/cart/clear/` | Clear entire cart | Yes |

**Request Body for POST /api/cart/add/:**
```json
{
  "food_item_id": 1,
  "quantity": 2
}
```

### Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/orders/place/` | Place new order | Yes |
| GET | `/api/orders/` | List user's orders | Yes |
| GET | `/api/orders/{id}/` | Get order details | Yes |
| GET | `/api/orders/my-orders/` | Get user's order history | Yes |
| POST | `/api/orders/{order_id}/update-status/` | Update order status | Yes (Admin) |

**Request Body for POST /api/orders/place/:**
```json
{
  "delivery_name": "John Doe",
  "delivery_address": "123 Main St, Apt 4B",
  "delivery_city": "New York",
  "delivery_pincode": "100001",
  "delivery_phone": "9876543210"
}
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. After logging in, include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Example Login Flow

1. **Register:**
```bash
POST /api/auth/register/
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

2. **Login:**
```bash
POST /api/auth/login/
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access": "<access_token>",
    "refresh": "<refresh_token>",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

3. **Use Access Token:**
```bash
GET /api/cart/
Authorization: Bearer <access_token>
```

## 🎯 Admin Panel

Access the Django admin panel at: `http://127.0.0.1:8000/admin/`

### Admin Capabilities:
- Manage users
- Create/edit/delete categories
- Manage food items (with image upload)
- View and update order status
- Monitor cart contents

## 📖 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`

## 🗄️ Database Models

### User Model
- Email (unique identifier)
- Name
- Password (hashed)
- Is Admin flag

### Category
- Name
- Description
- Image

### FoodItem
- Name
- Description
- Price
- Category (FK)
- Image
- Is Available

### Cart
- User (OneToOne)
- Created/Updated timestamps

### CartItem
- Cart (FK)
- Food Item (FK)
- Quantity

### Order
- User (FK)
- Total Amount
- Status (Pending, Preparing, Out for Delivery, Delivered, Cancelled)
- Delivery Address
- Delivery City
- Delivery Pincode
- Delivery Phone
- Delivery Name
- Timestamps

### OrderItem
- Order (FK)
- Food Item (FK)
- Quantity
- Price (at time of order)
- Subtotal

## 🔧 Development

### Running Tests

```bash
python manage.py test
```

### Creating Sample Data

You can create sample data through the admin panel or using Django shell:

```bash
python manage.py shell
```

```python
from apps.food.models import Category, FoodItem

# Create category
pizza = Category.objects.create(name="Pizza", description="Delicious pizzas")

# Create food item
margherita = FoodItem.objects.create(
    name="Margherita Pizza",
    description="Classic pizza with tomato sauce, mozzarella, and basil",
    price=12.99,
    category=pizza,
    is_available=True
)
```

## 🚢 Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Configure allowed hosts
4. Use PostgreSQL instead of SQLite
5. Set up static file serving
6. Configure HTTPS
7. Set up proper logging
8. Use environment variables for sensitive data

### Static Files

```bash
python manage.py collectstatic
```

## 🤝 Frontend Integration

The backend is configured to work with the React frontend running on `http://localhost:3000`.

CORS is enabled for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 📝 Notes

- All prices are in INR (₹)
- Passwords must be at least 8 characters
- Phone numbers must be 10 digits
- Pincodes must be 6 digits
- Cart is automatically cleared after successful order placement
- Orders can only be viewed by their owner (except admins)

## 🛡️ Security Features

- JWT token-based authentication
- Password hashing using Django's built-in system
- CORS protection
- CSRF protection
- Input validation and sanitization
- SQL injection protection via Django ORM

## 📄 License

This project is created for educational purposes.

## 💬 Support

For issues or questions, please check the API documentation or contact the development team.

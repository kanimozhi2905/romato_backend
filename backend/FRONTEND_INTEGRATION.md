# Frontend Integration Guide

This guide explains how to integrate your React frontend with the Django backend.

## 📡 Backend Configuration

### 1. Start the Backend Server

```bash
cd backend
python manage.py runserver
```

The backend runs on `http://127.0.0.1:8000/`

### 2. CORS Configuration

CORS is already configured in the backend to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

If your React app runs on a different port, update the `.env` file:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://your-port:3000
```

## 🔧 Frontend Setup

### 1. Create API Configuration File

Create a new file in your React app:

**File:** `client/src/config/api.js`

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const endpoints = {
  // Authentication
  REGISTER: `${API_BASE_URL}/auth/register/`,
  LOGIN: `${API_BASE_URL}/auth/login/`,
  TOKEN_REFRESH: `${API_BASE_URL}/auth/token/refresh/`,
  PROFILE: `${API_BASE_URL}/auth/profile/`,
  CHANGE_PASSWORD: `${API_BASE_URL}/auth/change-password/`,
  
  // Categories
  CATEGORIES: `${API_BASE_URL}/categories/`,
  
  // Food Items
  FOODS: `${API_BASE_URL}/foods/`,
  
  // Cart
  CART: `${API_BASE_URL}/cart/`,
  CART_ADD: `${API_BASE_URL}/cart/add/`,
  CART_UPDATE: (itemId) => `${API_BASE_URL}/cart/update/${itemId}/`,
  CART_REMOVE: (itemId) => `${API_BASE_URL}/cart/remove/${itemId}/`,
  CART_CLEAR: `${API_BASE_URL}/cart/clear/`,
  
  // Orders
  ORDERS_PLACE: `${API_BASE_URL}/orders/place/`,
  ORDERS: `${API_BASE_URL}/orders/`,
  ORDERS_MY: `${API_BASE_URL}/orders/my-orders/`,
};

export default API_BASE_URL;
```

### 2. Create API Utility Class

**File:** `client/src/utils/api.js`

```javascript
import API_BASE_URL, { endpoints } from '../config/api';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Get token from localStorage
  getToken() {
    return localStorage.getItem('access_token');
  }

  // Get authentication headers
  getAuthHeaders() {
    const token = this.getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
    };
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = typeof endpoint === 'function' ? endpoint() : endpoint;
    
    const config = {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...(options.headers || {}),
      },
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // HTTP methods
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Export singleton instance
export const api = new ApiClient();
export default api;
```

### 3. Update CartContext for Backend Integration

**File:** `client/src/Context/CartContext.js`

```javascript
import { createContext, useState, useEffect } from "react";
import api from "../utils/api";
import { endpoints } from "../config/api";

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load cart from backend on mount (if user is logged in)
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      loadCart();
    }
  }, []);

  // Load cart from backend
  const loadCart = async () => {
    try {
      setLoading(true);
      const response = await api.get(endpoints.CART);
      if (response.success) {
        setCart(response.data.items || []);
      }
    } catch (err) {
      console.error('Failed to load cart:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add item to cart (backend)
  const addToCart = async (item) => {
    try {
      setLoading(true);
      const response = await api.post(endpoints.CART_ADD, {
        food_item_id: item.id,
        quantity: 1,
      });
      
      if (response.success) {
        // Update local cart state from response
        setCart(response.data.items || []);
        return true;
      }
    } catch (err) {
      console.error('Failed to add to cart:', err);
      setError(err.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Remove item from cart (backend)
  const removeFromCart = async (itemId) => {
    try {
      setLoading(true);
      const response = await api.post(endpoints.CART_REMOVE(itemId));
      
      if (response.success) {
        setCart(response.data.items || []);
        return true;
      }
    } catch (err) {
      console.error('Failed to remove from cart:', err);
      setError(err.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Update item quantity (backend)
  const updateQuantity = async (itemId, newQuantity) => {
    try {
      setLoading(true);
      const response = await api.post(endpoints.CART_UPDATE(itemId), {
        quantity: newQuantity,
      });
      
      if (response.success) {
        setCart(response.data.items || []);
        return true;
      }
    } catch (err) {
      console.error('Failed to update quantity:', err);
      setError(err.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Clear cart (backend)
  const clearCart = async () => {
    try {
      setLoading(true);
      const response = await api.post(endpoints.CART_CLEAR);
      
      if (response.success) {
        setCart([]);
        return true;
      }
    } catch (err) {
      console.error('Failed to clear cart:', err);
      setError(err.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Helper functions
  const getTotalPrice = () => {
    return cart.reduce((sum, item) => sum + (item.food_item.price * item.quantity), 0);
  };

  const getTotalItems = () => {
    return cart.reduce((sum, item) => sum + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{ 
      cart, 
      loading,
      error,
      addToCart, 
      removeFromCart, 
      updateQuantity,
      clearCart,
      getTotalPrice,
      getTotalItems,
      loadCart,
    }}>
      {children}
    </CartContext.Provider>
  );
};
```

### 4. Create Auth Context for Backend Integration

**File:** `client/src/Context/AuthContext.js` (Create new file)

```javascript
import { createContext, useState, useContext, useEffect } from 'react';
import api from '../utils/api';
import { endpoints } from '../config/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  // Check if user is authenticated
  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const response = await api.get(endpoints.PROFILE);
        if (response.success) {
          setUser(response.data);
        } else {
          // Token might be expired, try to refresh
          await refreshToken();
        }
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
      }
    }
    setLoading(false);
  };

  // Refresh access token
  const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    try {
      const response = await api.post(endpoints.TOKEN_REFRESH, {
        refresh: refreshToken,
      });
      
      if (response.access) {
        localStorage.setItem('access_token', response.access);
        return true;
      }
    } catch (err) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return false;
    }
  };

  // Register user
  const register = async (userData) => {
    try {
      setError(null);
      const response = await api.post(endpoints.REGISTER, userData);
      
      if (response.success) {
        return { success: true, data: response.data };
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  // Login user
  const login = async (email, password) => {
    try {
      setError(null);
      const response = await api.post(endpoints.LOGIN, { email, password });
      
      if (response.success) {
        const { access, refresh, user } = response.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        setUser(user);
        return { success: true, user };
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  // Logout user
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  // Update profile
  const updateProfile = async (profileData) => {
    try {
      setError(null);
      const response = await api.put(endpoints.PROFILE, profileData);
      
      if (response.success) {
        setUser(response.data);
        return { success: true, data: response.data };
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      error,
      isAuthenticated: !!user,
      register,
      login,
      logout,
      updateProfile,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### 5. Update App.js to Use Auth Context

**File:** `client/src/App.js`

```javascript
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./Context/AuthContext";
import { CartProvider } from "./Context/CartContext";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/Loginpage";
import SignupPage from "./pages/Signuppage";
import CartPage from "./pages/CartPage";
import CheckoutPage from "./pages/CheckoutPage";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <Routes>
            <Route path="/" element={<><Navbar /><LandingPage /></>} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/cart" element={<><Navbar /><CartPage /></>} />
            <Route path="/checkout" element={<><Navbar /><CheckoutPage /></>} />
          </Routes>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
```

### 6. Update Login Page

**File:** `client/src/pages/Loginpage.jsx`

```javascript
import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Context/AuthContext';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error || 'Login failed');
    }
    
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p>
        Don't have an account? <Link to="/signup">Sign up</Link>
      </p>
    </div>
  );
};

export default LoginPage;
```

### 7. Update Products Page to Add to Cart

Update your ProductsPage to use the new CartContext with backend integration.

## 🧪 Testing the Integration

### 1. Test User Registration

```javascript
// In browser console or React component
const registerUser = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'Test User',
      email: 'test@example.com',
      password: 'testpass123',
      password_confirm: 'testpass123',
    }),
  });
  const data = await response.json();
  console.log(data);
};
```

### 2. Test Login

```javascript
const loginUser = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'test@example.com',
      password: 'testpass123',
    }),
  });
  const data = await response.json();
  console.log('Access Token:', data.data.access);
  localStorage.setItem('access_token', data.data.access);
};
```

### 3. Test Get Food Items

```javascript
const getFoods = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/foods/');
  const data = await response.json();
  console.log('Food Items:', data);
};
```

## 🔐 Handling Authentication

### Protected Routes

Create a Higher Order Component (HOC) for protected routes:

**File:** `client/src/components/ProtectedRoute.jsx`

```javascript
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../Context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useContext(AuthContext);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
```

Usage:

```javascript
<Route 
  path="/checkout" 
  element={
    <ProtectedRoute>
      <><Navbar /><CheckoutPage /></>
    </ProtectedRoute>
  } 
/>
```

## 📊 Common Issues and Solutions

### Issue: CORS Errors

**Solution:** 
- Ensure backend CORS settings include your frontend URL
- Check that both servers are running

### Issue: Token Expiration

**Solution:**
- Implement token refresh logic before API calls
- Store both access and refresh tokens

### Issue: Cart Not Syncing

**Solution:**
- Call `loadCart()` after login
- Update cart state after successful cart operations

## ✅ Integration Checklist

- [ ] Backend server running on http://127.0.0.1:8000
- [ ] API configuration file created
- [ ] API utility class implemented
- [ ] CartContext updated for backend
- [ ] AuthContext created and integrated
- [ ] Login/Register pages connected to backend
- [ ] Cart operations use backend API
- [ ] Order placement integrated
- [ ] Protected routes implemented
- [ ] Error handling added
- [ ] Loading states managed

## 🎉 Success!

Your React frontend is now fully integrated with the Django backend!

**Next Steps:**
1. Test all features end-to-end
2. Add proper error messages and notifications
3. Implement loading indicators
4. Add form validation
5. Test on different scenarios

Happy Coding! 🚀

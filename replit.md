# Adiseware - Agricultural Management Platform

## Overview
Adiseware is a comprehensive agricultural AI platform built with Python and Streamlit that empowers farmers with AI-powered disease detection, marketplace functionality, and community features while providing agrovets with complete business management tools.

## Project Status
- **Version**: 1.0.0
- **Status**: Fully Functional
- **Last Updated**: October 29, 2025

## Core Features

### For Farmers
1. **AI Plant Disease Detection** - Upload or capture plant photos using phone camera for instant disease analysis
2. **Treatment Recommendations** - Detailed disease information with medication suggestions
3. **Marketplace** - Browse and order agricultural products from local agrovets
4. **Order Tracking** - Monitor order status and delivery
5. **Community Forum** - Share experiences and learn from other farmers
6. **AI Agricultural Assistant** - 24/7 farming advice chatbot
7. **Weather & Crop Calendar** - Localized forecasts and planting schedules
8. **Personal Dashboard** - Track disease history and farm activities

### For Agrovets
1. **Point of Sale (POS) System** - Modern checkout interface for in-store sales
2. **Inventory Management** - Complete product catalog and stock tracking
3. **Order Management** - Process and fulfill farmer orders
4. **CRM System** - Customer relationship management and interaction tracking
5. **Analytics Dashboard** - Sales trends and business insights
6. **Product Management** - Add, edit, and manage product listings

### For Administrators
1. **System Dashboard** - Platform-wide overview and metrics
2. **User Management** - Create, edit, and manage all user accounts
3. **Order Monitoring** - View all orders across the platform
4. **Product Oversight** - Monitor all products in the system
5. **System Analytics** - Comprehensive platform analytics and trends

## Technology Stack

### Backend
- **Python 3.11**
- **SQLAlchemy** - ORM for database management
- **PostgreSQL** - Primary database (with SQLite fallback)
- **bcrypt** - Password hashing and authentication

### AI Integration
- **OpenAI GPT-5** - Plant disease detection via vision API
- **OpenAI GPT-5** - Agricultural chatbot assistant

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive charts and visualizations
- **Pandas** - Data manipulation and analysis

### Additional Libraries
- **streamlit-camera-input-live** - Real-time camera capture
- **Pillow (PIL)** - Image processing

## Architecture

### Database Models
- **User** - Multi-role user system (Farmer, Agrovet, Admin)
- **Product** - Agricultural product catalog
- **Order** - Order transactions with order items
- **OrderItem** - Individual items in orders
- **DiseaseDetection** - AI disease scan history
- **CommunityPost** - Forum posts with comments
- **Comment** - Post comments
- **CustomerInteraction** - CRM interaction tracking

### Key Files
```
.
├── app.py                      # Main application with routing
├── database.py                 # SQLAlchemy models and database setup
├── auth.py                     # Authentication and password management
├── ai_helper.py               # OpenAI integration for AI features
├── seed_data.py               # Sample data initialization
├── pages/                     # Page modules
│   ├── home.py                # Landing page
│   ├── login.py               # Login page
│   ├── register.py            # Registration page
│   ├── farmer_dashboard.py   # Farmer overview
│   ├── disease_detection.py  # AI disease scanning
│   ├── marketplace.py         # Product marketplace
│   ├── my_orders.py          # Order tracking
│   ├── community.py          # Community forum
│   ├── ai_assistant.py       # AI chatbot
│   ├── weather.py            # Weather and crop calendar
│   ├── agrovet_dashboard.py  # Agrovet overview
│   ├── pos_system.py         # Point of sale
│   ├── agrovet_orders.py     # Order processing
│   ├── inventory.py          # Product management
│   ├── crm.py                # Customer management
│   ├── analytics.py          # Business analytics
│   ├── admin_dashboard.py    # Admin overview
│   ├── user_management.py    # User administration
│   ├── all_orders.py         # System-wide orders
│   ├── all_products.py       # System-wide products
│   └── system_analytics.py   # Platform analytics
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL database (optional, uses SQLite as fallback)
- OpenAI API key for AI features

### Environment Variables
Required:
- `OPENAI_API_KEY` - For AI disease detection and chatbot

Optional:
- `DATABASE_URL` - PostgreSQL connection string (uses SQLite if not provided)
- `GEMINI_API_KEY` - Alternative to OpenAI (not currently used)

### Installation
1. Install dependencies (automatically handled by Replit)
2. Set up environment variables (OPENAI_API_KEY)
3. Run the application

### Demo Accounts
The system includes three pre-configured demo accounts:
- **Farmer**: Username: `farmer_demo`, Password: `demo123`
- **Agrovet**: Username: `agrovet_demo`, Password: `demo123`
- **Admin**: Username: `admin_demo`, Password: `demo123`

## Security Features
- Bcrypt password hashing
- SQLAlchemy ORM (SQL injection prevention)
- Role-based access control
- Session state management
- Environment-based secret management

## API Integration

### OpenAI Integration
The platform uses OpenAI's GPT-5 model for:
1. **Vision Analysis** - Plant disease detection from images
2. **Text Generation** - Agricultural advice and recommendations

Key functions in `ai_helper.py`:
- `analyze_plant_disease(image_bytes)` - Analyzes plant images for diseases
- `get_agricultural_advice(question, context)` - Provides farming advice

## Mobile Optimization
- Fully responsive Streamlit interface
- Phone camera integration for disease detection
- Mobile-friendly navigation and layouts
- Touch-optimized forms and buttons

## Future Enhancements
- Real-time notifications for order updates
- Payment gateway integration
- GPS-based agrovet locator
- Multi-language support
- Advanced analytics with ML predictions
- SMS/Email notifications
- Mobile app version

## Recent Changes (October 29, 2025)
- Initial platform development
- Implemented all core features
- Added admin role and functionality
- Created comprehensive database schema
- Integrated OpenAI for AI features
- Built multi-user role system
- Added demo accounts and seed data

## User Preferences
None recorded yet.

## Notes
- The application uses Streamlit session state for user authentication
- Database is automatically initialized on first run
- Sample data includes 5 products for testing
- AI features require valid OpenAI API key
- The platform supports unlimited users and transactions

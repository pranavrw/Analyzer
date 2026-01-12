# YOLO ML Training Platform

A comprehensive web-based platform for YOLO machine learning model training and dataset management. Built with FastAPI, PostgreSQL, and AWS S3 integration.

## Features

- 🔐 **User Authentication**: JWT-based authentication with secure password hashing
- 📁 **Dataset Management**: Upload, store, and manage datasets with S3 integration
- 🗄️ **Database Integration**: PostgreSQL database for data persistence
- 🔄 **Smart Fallback**: Automatic local storage fallback when S3 is unavailable
- 🚀 **REST API**: Full RESTful API with interactive documentation
- 🛡️ **Security**: Comprehensive error handling and credential protection

## Requirements

- Python 3.11 or higher
- PostgreSQL database
- (Optional) AWS S3 account for cloud storage

## Local Setup Instructions

### 1. Clone and Navigate
```bash
git clone <your-repository-url>
cd yolo-ml-platform
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Option 1: Using pip with requirements.txt
pip install -r requirements.txt

# Option 2: Using uv (if available)
uv sync

# Option 3: Manual installation
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] bcrypt python-multipart boto3 pyyaml
```

### 4. Set Up PostgreSQL Database

#### Option A: Local PostgreSQL
1. Install PostgreSQL on your system
2. Create a database:
```sql
CREATE DATABASE yolo_ml_platform;
CREATE USER yolo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE yolo_ml_platform TO yolo_user;
```

#### Option B: Use Docker
```bash
docker run --name postgres-yolo \
  -e POSTGRES_DB=yolo_ml_platform \
  -e POSTGRES_USER=yolo_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:13
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://yolo_user:your_password@localhost:5432/yolo_ml_platform
PGHOST=localhost
PGPORT=5432
PGUSER=yolo_user
PGPASSWORD=your_password
PGDATABASE=yolo_ml_platform

# JWT Secret (generate a secure random string)
SESSION_SECRET=your-super-secret-jwt-key-here

# AWS S3 Configuration (Optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### 6. Initialize Database
```bash
python init_db.py
```

### 7. Run the Application
```bash
# Start the FastAPI server
python -m uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload

# Alternative: Direct run
uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload
```

The application will be available at:
- **Web Interface**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/api/ping

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login

### Dataset Management
- `POST /api/datasets/upload` - Upload dataset
- `GET /api/datasets/` - List user datasets
- `GET /api/datasets/{dataset_id}` - Get specific dataset

### Utility
- `GET /api/ping` - Health check

## Testing the Setup

### 1. Health Check
```bash
curl http://localhost:5000/api/ping
```

### 2. Create User Account
```bash
curl -X POST "http://localhost:5000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 3. Login and Get Token
```bash
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

## Troubleshooting

### Database Issues
```bash
# Check database connection
python check_db.py

# Test database operations
python test_db.py
```

### Common Issues

1. **Database Connection Error**:
   - Verify PostgreSQL is running
   - Check DATABASE_URL in environment variables
   - Ensure database exists and user has permissions

2. **S3 Upload Failures**:
   - Check AWS credentials in environment variables
   - Verify S3 bucket exists and has proper permissions
   - Note: The system automatically falls back to local storage

3. **Port Already in Use**:
   - Change the port number in the uvicorn command
   - Kill existing processes: `pkill -f uvicorn`

### Development Utilities
```bash
# Check environment setup
python check_path.py

# View database records
python check_db.py

# Test database operations
python test_db.py
```

## Project Structure

```
yolo-ml-platform/
├── api/                    # FastAPI application
│   ├── main.py            # Main application entry point
│   ├── auth.py            # Authentication routes
│   ├── routes_dataset.py  # Dataset management routes
│   └── routes_analyzer.py # Analysis routes (placeholder)
├── src/                   # Core business logic
│   ├── config/            # Configuration modules
│   ├── user_db.py         # Database operations
│   └── s3_utils.py        # S3 integration utilities
├── config/                # Configuration files
│   ├── aws_config.yaml    # AWS settings
│   └── train_config.yaml  # Training configuration
├── data/                  # Data storage
│   ├── raw/              # Raw datasets
│   └── processed/        # Processed datasets
├── models/               # Model storage
│   └── runs/            # Training runs
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Next Steps

1. **Implement YOLO Training**: Add actual YOLO model training functionality
2. **Add Model Management**: Create endpoints for model versioning and deployment
3. **Enhance UI**: Build a web frontend for easier interaction
4. **Add Monitoring**: Implement logging and performance monitoring
5. **Deploy**: Set up production deployment with proper CI/CD

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]

# YOLO ML Training Platform

## Overview

This is a YOLO ML Training Platform that provides a comprehensive web-based solution for machine learning model training and dataset management. The platform allows users to upload datasets, manage training sessions, and perform YOLO-based object detection analysis. It features a FastAPI backend with PostgreSQL database storage and AWS S3 integration for file management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI with Python for REST API endpoints
- **Database**: PostgreSQL with SQLAlchemy ORM for data persistence
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **File Storage**: AWS S3 integration via boto3 for dataset and model storage
- **Session Management**: HTTP Bearer token-based authentication

### Database Schema
- **Users Table**: Stores user credentials with bcrypt-hashed passwords
- **Datasets Table**: Manages user-uploaded datasets with S3 paths and processing status
- **Training Logs Table**: Records training events and progress (referenced but not fully implemented)

### API Structure
- **Authentication Endpoints** (`/auth`): User registration and login
- **Dataset Management** (`/datasets`): Upload, list, and manage datasets
- **Analysis Endpoints** (`/analyze`): YOLO inference and evaluation (placeholder implementation)

### Data Flow
1. Users authenticate via JWT tokens
2. Dataset uploads are processed and stored in S3
3. Database tracks dataset metadata and user associations
4. Training configurations use YAML-based settings
5. YOLO models are trained using Ultralytics YOLO framework

### Security Design
- Password hashing with bcrypt
- JWT token-based API authentication
- Environment variable-based configuration for sensitive data
- S3 credential management through boto3 defaults

### Configuration Management
- Database connections through environment variables
- AWS S3 configuration via YAML files or environment variables
- Centralized database configuration in `src/config/db_config.py`

## External Dependencies

### Core Frameworks
- **FastAPI**: Web framework for REST API endpoints
- **SQLAlchemy**: ORM for PostgreSQL database interactions
- **Ultralytics YOLO**: Machine learning framework for object detection

### Database
- **PostgreSQL**: Primary database for user data, datasets, and logs
- **psycopg2**: PostgreSQL adapter for Python

### Cloud Services
- **AWS S3**: Object storage for datasets and trained models via boto3

### Authentication & Security
- **PyJWT (jose)**: JWT token creation and validation
- **Passlib**: Password hashing with bcrypt
- **python-multipart**: File upload handling

### Development Tools
- **uvicorn**: ASGI server for FastAPI
- **pydantic**: Data validation and serialization
- **pyyaml**: YAML configuration file parsing

### File Processing
- **zipfile**: Dataset archive extraction
- **pathlib**: Cross-platform path handling
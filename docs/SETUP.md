# TygrSecAcademy Development Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** and npm - [Download](https://nodejs.org/)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **PostgreSQL 15** (if not using Docker)
- **Redis 7** (if not using Docker)
- **Git** - [Download](https://git-scm.com/)

## Quick Start with Docker

The fastest way to get TygrSecAcademy running is using Docker Compose:

### 1. Clone the Repository and Navigate to Project

```bash
cd tygrsecacademy
```

### 2. Configure Environment Variables

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

**Required Configuration:**

Edit `.env` and update the following critical values:

```env
# Security - CHANGE THESE!
SECRET_KEY=your-secret-key-minimum-32-characters-change-this
JWT_SECRET_KEY=your-jwt-secret-key-minimum-32-characters-change-this

# Anthropic API
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Email (if using password reset)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** database (port 5432)
- **Redis** cache (port 6379)
- **Backend API** (port 8000)
- **Frontend** (port 3000)

### 4. Initialize Database

```bash
docker-compose exec backend python -c "from database.connection import init_db; init_db()"
```

### 5. Create Admin User (Optional)

```bash
docker-compose exec backend python scripts/create_admin.py
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend Health Check**: http://localhost:8000/health

## Manual Development Setup

If you prefer to run services locally without Docker:

### Backend Setup

1. **Create Virtual Environment**

```bash
cd backend
python -m venv venv
```

2. **Activate Virtual Environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment**

Create `.env` file in the backend directory with database connection:

```env
DATABASE_URL=postgresql://tygrsec:tygrsec_password@localhost:5432/tygrsecacademy
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=your-key-here
...
```

5. **Initialize Database**

```bash
# Start PostgreSQL and create database
python -c "from database.connection import init_db; init_db()"
```

6. **Run Development Server**

```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. **Install Dependencies**

```bash
cd frontend
npm install
```

2. **Configure Environment**

Create `.env.local` file:

```env
VITE_API_URL=http://localhost:8000
```

3. **Run Development Server**

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Database Migrations

We use Alembic for database migrations:

### Create a New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Common Issues

### Port Already in Use

If ports 3000, 5432, 6379, or 8000 are already in use:

1. Stop conflicting services
2. Or change ports in `docker-compose.yml` and `.env` files

### Database Connection Failed

1. Ensure PostgreSQL is running
2. Verify DATABASE_URL in `.env`
3. Check PostgreSQL logs: `docker-compose logs postgres`

### Anthropic API Errors

1. Verify ANTHROPIC_API_KEY is set correctly
2. Check API quota at https://console.anthropic.com/
3. Ensure API key has correct permissions

### Frontend Won't Connect to Backend

1. Check CORS_ORIGINS in backend `.env`
2. Verify VITE_API_URL in frontend environment
3. Check network tab in browser dev tools for errors

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| SECRET_KEY | App secret key | Yes | - |
| JWT_SECRET_KEY | JWT signing key | Yes | - |
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| REDIS_URL | Redis connection string | Yes | - |
| ANTHROPIC_API_KEY | Anthropic Claude API key | Yes | - |
| ANTHROPIC_MODEL | Claude model to use | No | claude-3-5-sonnet-20241022 |
| CORS_ORIGINS | Allowed CORS origins | No | http://localhost:3000 |
| DEBUG | Enable debug mode | No | True |

### Frontend (.env.local)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| VITE_API_URL | Backend API URL | No | http://localhost:8000 |

## Development Workflow

1. **Make Changes** - Edit code in your preferred editor
2. **Test Locally** - Backend and frontend auto-reload on changes
3. **Run Tests** - Ensure tests pass
4. **Commit** - Use meaningful commit messages
5. **Deploy** - Follow deployment guide

## Next Steps

- Review [API Documentation](API.md) for endpoint details
- Read [Security Documentation](SECURITY.md) for best practices
- Check [AI Integration Guide](AI_INTEGRATION.md) for AI features
- See [Deployment Guide](DEPLOYMENT.md) for production setup

## Getting Help

- Check existing documentation
- Review API docs at http://localhost:8000/docs
- Check Docker logs: `docker-compose logs backend` or `docker-compose logs frontend`
- Examine browser console for frontend errors

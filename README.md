# TygrSecAcademy

**Professional Cybersecurity Education Platform** - A comprehensive learning management system with AI-powered instruction, hands-on labs, and CTF challenges.

## 🚀 Features

- **Zero to Hero Curriculum**: 5-tier structured learning path (Foundations → AI in Cybersecurity → Hands-on Labs → CTF Challenges → Capstone Projects)
- **AI-Powered Learning**: Context-aware AI tutor using Anthropic Claude API
- **Hands-on Labs**: Docker-based isolated environments and browser terminals
- **CTF Challenges**: Multi-difficulty challenges with leaderboards
- **Role-Based Access**: Student, Tutor, and Admin interfaces
- **Progress Tracking**: Comprehensive analytics and achievement system
- **Capstone Publishing**: Internal blog and external sharing platform

## 🏗️ Architecture

- **Backend**: Python FastAPI (async, high-performance)
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **AI**: Anthropic Claude API
- **Labs**: Docker + xterm.js
- **Auth**: JWT with HTTP-only cookies
- **Deployment**: Docker Compose

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15
- Redis 7

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd tygrsecacademy
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start with Docker Compose

```bash
docker-compose up -d
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Initialize Database

```bash
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

### 4. Create Admin User

```bash
docker-compose exec backend python scripts/create_admin.py
```

## 🔧 Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API.md)
- [Security Model](docs/SECURITY.md)
- [AI Integration](docs/AI_INTEGRATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🔒 Security

- bcrypt password hashing (cost factor 12)
- JWT authentication with refresh tokens
- Role-based access control (RBAC)
- SQL injection protection via ORM
- XSS and CSRF protection
- Comprehensive audit logging
- Rate limiting on sensitive endpoints

## 📊 Project Structure

```
tygrsecacademy/
├── backend/               # FastAPI backend
│   ├── auth/             # Authentication & authorization
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── database/         # Schema & migrations
│   └── main.py           # Application entry point
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── components/  # Reusable components
│   │   ├── services/    # API clients
│   │   └── App.tsx      # Main app component
│   └── package.json
├── docs/                 # Documentation
├── docker-compose.yml    # Docker orchestration
└── .env.example          # Environment template
```

## 🎯 Curriculum Tiers

**Tier 0: Foundations**
- Introduction to Cybersecurity
- Linux Basics
- Networking Fundamentals
- Python for Cybersecurity
- AI Fundamentals

**Tier 1: AI in Cybersecurity**
- Machine Learning for Network Security
- LLMs for SOC Operations
- AI for Secure Coding
- AI for Digital Forensics

**Tier 2: Hands-on Labs**
- AI-Assisted Incident Response
- AI-Driven Threat Intelligence
- Safe Fuzzing Simulations
- Web Security with AI Helpers

**Tier 3: CTF Challenges**
- AI-Assisted OSINT Challenges
- AI-Driven Malware Classification
- Adversarial ML Challenges
- Difficulty: Easy → Medium → Hard → Insane

**Tier 4: Capstone & Publishing**
- Supervised Capstone Projects
- Progress Dashboards
- Internal Blog Publishing
- External Sharing (LinkedIn, etc.)

## 🤝 Contributing

This is a commercial cybersecurity education platform. For contribution guidelines, contact the development team.

## 📄 License

Proprietary - All rights reserved

## 👥 Team

TygrSecAcademy Development Team

---

**Built with ❤️ for the cybersecurity community**

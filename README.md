# Docker Django Backend Blueprint

A production-ready Django REST API blueprint with Docker, featuring Celery for async task processing, Redis for caching, Nginx as a reverse proxy, and WebSocket support through Django Channels.

## Features

- **Django 5.1.9** - Modern Python web framework
- **Django REST Framework** - Powerful API development toolkit
- **Celery 5.4.0** - Distributed task queue for async processing
- **Redis** - In-memory data store for caching and message brokering
- **Nginx** - High-performance reverse proxy and load balancer
- **Django Channels** - WebSocket and real-time communication support
- **PostgreSQL/PostGIS** - Spatial database support
- **Docker & Docker Compose** - Containerized development and deployment
- **JWT Authentication** - Secure token-based authentication
- **Firebase Admin** - Firebase integration capabilities
- **API Documentation** - Auto-generated API docs with drf-yasg (Swagger/OpenAPI)
- **Modeltranslation** - Multi-language model support
- **BDD Testing** - Behavior-driven development with Behave

## Architecture

```
┌─────────────────┐
│     Nginx       │  (Port 80/443)
│  Reverse Proxy  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │   Web    │  (Daphne ASGI Server)
    │ Django   │  (Port 8080)
    └─┬──────┬─┘
      │      │
      │      │
┌─────▼──┐ ┌▼────────┐
│ Redis  │ │ Celery  │
│ Cache  │ │ Workers │
└────────┘ └─────────┘
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd docker-django-backend-blueprint
   ```

2. **Create environment file**
   
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Database Configuration
   DB_Name=your_database_name
   DB_User=your_database_user
   DB_Password=your_secure_password
   DB_Host=db
   DB_Port=5432

   # Django Settings
   SECRET_KEY=your_super_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Redis Configuration
   REDIS_HOST=redis
   REDIS_PORT=6379

   # Additional settings as needed
   ```

3. **Build and run with Docker Compose (Local)**
   ```bash
   docker-compose -f docker.compose-local.yml up --build
   ```

   This will start:
   - PostgreSQL database with PostGIS extension
   - Django web application
   - Celery worker
   - Redis cache
   - Nginx reverse proxy

4. **Access the application**
   - API: http://localhost/
   - Admin Panel: http://localhost/admin/

### Production Deployment

1. **Build Docker images**
   ```bash
   # Build web image
   docker build -t template-web:latest ./src/web

   # Build celery image
   docker build -t template-celery:latest ./src/web
   ```

2. **Configure SSL certificates**
   
   Place your SSL certificates in the `certbot/conf/` directory or configure Let's Encrypt.

3. **Update production configuration**
   
   Modify `nginx.conf` with your domain and SSL settings.

4. **Deploy with production compose file**
   ```bash
   docker-compose up -d
   ```

## Configuration

### Environment Variables

Key environment variables you should configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_Name` | PostgreSQL database name | - |
| `DB_User` | Database username | - |
| `DB_Password` | Database password | - |
| `DB_Host` | Database host | `db` |
| `DB_Port` | Database port | `5432` |
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | - |
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |

### Django Settings

The Django settings are located in `src/web/settings.py`. Customize as needed for your specific use case.

## Usage

### Running Django Commands

Execute Django management commands inside the web container:

```bash
# Create migrations
docker exec -it web python manage.py makemigrations

# Apply migrations
docker exec -it web python manage.py migrate

# Create superuser
docker exec -it web python manage.py createsuperuser

# Collect static files
docker exec -it web python manage.py collectstatic

# Run tests
docker exec -it web python manage.py test
```

### Celery Tasks

Monitor Celery tasks:

```bash
# View Celery logs
docker logs -f celery

# Access Celery container
docker exec -it celery bash
```

### Redis Operations

Access Redis CLI:

```bash
docker exec -it redis redis-cli
```

### Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f celery
```

## Project Structure

```
.
├── docker-compose.yml              # Production Docker Compose configuration
├── docker.compose-local.yml        # Local development Docker Compose configuration
├── .dockerignore                   # Docker ignore file
├── .env                            # Environment variables (create this)
├── nginx.conf                      # Nginx production configuration
├── nginx-local.conf                # Nginx local configuration
├── certbot/                        # SSL certificates directory
├── src/
│   └── web/
│       ├── dockerfile              # Django application Dockerfile
│       ├── requirements.txt        # Python dependencies
│       └── settings.py             # Django settings
└── README.md                       # This file
```

## Technology Stack

### Backend
- **Django 5.1.9** - Web framework
- **Django REST Framework 3.15.2+** - REST API framework
- **Daphne 4.2.1** - ASGI server
- **Celery 5.4.0** - Task queue
- **Channels 4.3.1** - WebSocket support
- **PostgreSQL with PostGIS** - Database with spatial extensions

### Authentication & Security
- **djangorestframework-simplejwt 5.5.0** - JWT authentication
- **Firebase Admin 6.6.0** - Firebase integration

### Infrastructure
- **Redis 5.1.1** - Caching and message broker
- **Nginx** - Reverse proxy
- **Docker & Docker Compose** - Containerization

### Development Tools
- **behave-django 1.4.0** - BDD testing
- **coverage 7.6.1** - Code coverage
- **drf-yasg 1.21.7** - API documentation (Swagger/OpenAPI)

### Additional Libraries
- **Pillow 10.4.0** - Image processing
- **phonenumbers 8.13.31** - Phone number validation
- **GDAL 3.6.2** - Geospatial data processing
- **django-modeltranslation 0.19.12** - Model translation
- **django-filter 24.3** - Filtering support

## API Documentation

Once the application is running, you can access the auto-generated API documentation:

- **Swagger UI**: http://localhost/swagger/
- **ReDoc**: http://localhost/redoc/

## Development

### Adding Dependencies

1. Add the package to `src/web/requirements.txt`
2. Rebuild the Docker images:
   ```bash
   docker-compose -f docker.compose-local.yml up --build
   ```

### Database Migrations

```bash
# Create new migrations
docker exec -it web python manage.py makemigrations

# Apply migrations
docker exec -it web python manage.py migrate

# Show migrations
docker exec -it web python manage.py showmigrations
```

### Testing

Run the test suite:

```bash
# Run all tests
docker exec -it web python manage.py test

# Run with coverage
docker exec -it web coverage run --source='.' manage.py test
docker exec -it web coverage report
```

## Troubleshooting

### Container Issues

```bash
# Restart all services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up --build

# Check container status
docker-compose ps

# View resource usage
docker stats
```

### Database Issues

```bash
# Access PostgreSQL
docker exec -it db psql -U ${DB_User} -d ${DB_Name}

# Reset database (WARNING: destroys all data)
docker-compose down -v
docker-compose up
```

### Permission Issues

```bash
# Fix volume permissions
docker-compose run --rm web chown -R $(id -u):$(id -g) /code
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

## Acknowledgments

- Django Software Foundation
- Celery Project
- Redis Labs
- Docker, Inc.
- All open-source contributors

---

**Note**: This is a blueprint/template project. Customize it according to your specific needs and security requirements before deploying to production.

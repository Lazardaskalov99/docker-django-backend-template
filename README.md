# Docker Django Backend Template

A production-ready Django REST API template with Docker, featuring Celery for async task processing, Redis for caching, Nginx as a reverse proxy, and WebSocket support through Django Channels.

## Features

- **Python 3.12** - Latest Python runtime
- **Django 5.1.15** - Modern Python web framework
- **Django REST Framework 3.15.2+** - Powerful API development toolkit
- **Daphne 4.2.1** - ASGI server for async and WebSocket support
- **Celery 5.4.0** - Distributed task queue for async processing
- **Redis 5.1.1** - In-memory data store for caching and message brokering
- **Nginx** - High-performance reverse proxy and load balancer
- **Django Channels 4.3.1** - WebSocket and real-time communication support
- **PostgreSQL/PostGIS** - Spatial database support (local development)
- **Docker & Docker Compose** - Containerized development and deployment
- **JWT Authentication** - Secure token-based authentication via djangorestframework-simplejwt
- **Firebase Admin 6.6.0** - Firebase integration capabilities
- **API Documentation** - Auto-generated API docs with drf-yasg (Swagger/OpenAPI)
- **Modeltranslation** - Multi-language model support
- **BDD Testing** - Behavior-driven development with Behave
- **GDAL 3.6.2** - Geospatial data processing support

## Architecture

### Local Development
```
┌─────────────────┐
│     Nginx       │  (Port 80)
│  Reverse Proxy  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │   Web    │  (Daphne ASGI Server)
    │ Django   │  (Port 8080)
    └─┬──────┬─┘
      │      │
      │      └──────────────┐
┌─────▼──┐ ┌▼────────┐  ┌──▼──────┐
│ Redis  │ │ Celery  │  │   DB    │
│ Cache  │ │ Workers │  │PostGIS  │
└────────┘ └─────────┘  └─────────┘
```

### Production
```
┌─────────────────┐
│     Nginx       │  (Port 80/443 with SSL)
│  Reverse Proxy  │  + Flutter Web Hosting
└────────┬────────┘
         │
    ┌────▼─────┐
    │   Web    │  (Daphne ASGI Server)
    │ Django   │  (GHCR Image)
    └─┬────────┘
      │
┌─────▼──┐ ┌─────────┐
│ Redis  │ │ Celery  │
│ Cache  │ │ Workers │
└────────┘ └─────────┘
Note: External DB required
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
   cd docker-django-backend-template
   ```

2. **Create and configure environment file**
   
   Create a `.env` file in the root directory with the following variables:
   ```bash
   # Database Configuration
   DB_Name=your_database_name
   DB_User=your_database_user
   DB_Password=your_database_password
   DB_Host=db
   DB_Port=5432
   
   # Django Configuration
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   DJANGO_CSRF_TRUSTED=http://localhost,http://127.0.0.1
   
   # Redis Configuration
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

3. **Build and run with Docker Compose (Local)**
   ```bash
   docker-compose -f docker-compose-local.yml up --build
   ```

   This will start:
   - PostgreSQL database with PostGIS extension (port 5432)
   - Django web application (via Nginx on port 80)
   - Daphne ASGI server (internal port 8080)
   - Celery worker for async tasks
   - Redis cache and message broker
   - Nginx reverse proxy

4. **Access the application**
   - API: http://localhost/api/
   - Admin Panel: http://localhost/admin/
   - API Docs (Swagger): http://localhost/swagger/
   - API Docs (ReDoc): http://localhost/redoc/
   - Test endpoint: http://localhost/api/ping/

### Production Deployment

Production deployment uses pre-built images from GitHub Container Registry (GHCR).

1. **Prerequisites**
   - External PostgreSQL/PostGIS database configured
   - SSL certificates ready (Let's Encrypt or custom)
   - GHCR images built and pushed

2. **Configure environment variables**
   
   Update your `.env` file with production values:
   ```bash
   # GitHub Container Registry
   GHCR_OWNER=your-github-username
   GHCR_REPO=your-repo-name
   
   # Database (external)
   DB_Name=production_db
   DB_User=prod_user
   DB_Password=secure_password
   DB_Host=your-db-host
   DB_Port=5432
   
   # Django Production Settings
   DJANGO_SECRET_KEY=production-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DJANGO_CSRF_TRUSTED=https://yourdomain.com,https://www.yourdomain.com
   DJANGO_USE_X_FORWARDED_HOST=True
   DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
   ```

3. **Configure Nginx for production**
   
   Edit `nginx.conf` and replace placeholders:
   - `{{SERVER_NAME}}` → your domain (e.g., `example.com`)
   - `{{SERVER_NAME_WWW}}` → www version (e.g., `www.example.com`)
   - `{{DJANGO_SERVICE_NAME}}` → `web`
   - `{{DJANGO_PORT}}` → `8080`

4. **Set up SSL certificates**
   
   Place your SSL certificates in `./certbot/conf/live/yourdomain.com/`:
   - `fullchain.pem`
   - `privkey.pem`

5. **Deploy with production compose file**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - Django web application (from GHCR image)
   - Celery worker (from GHCR image)
   - Redis cache
   - Nginx with SSL on ports 80 and 443

## Configuration

### Environment Variables

The application uses `python-decouple` for configuration management. All settings can be configured via environment variables in the `.env` file.

#### Required Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DB_Name` | PostgreSQL database name | - | `myapp_db` |
| `DB_User` | Database username | - | `postgres` |
| `DB_Password` | Database password | - | `secretpass123` |
| `DB_Host` | Database host | `db` | `db` or `your-db-host.com` |
| `DB_Port` | Database port | `5432` | `5432` |
| `DJANGO_SECRET_KEY` | Django secret key | `change-me-in-prod` | Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |

#### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DJANGO_DEBUG` | Debug mode | `False` | `True` for dev, `False` for prod |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `*` | `localhost,yourdomain.com` |
| `DJANGO_CSRF_TRUSTED` | Comma-separated CSRF trusted origins | `http://127.0.0.1` | `https://yourdomain.com,https://www.yourdomain.com` |
| `DJANGO_USE_X_FORWARDED_HOST` | Use X-Forwarded-Host header | `False` | `True` for production behind proxy |
| `DJANGO_SECURE_PROXY_SSL_HEADER` | SSL header for proxy | `None` | `HTTP_X_FORWARDED_PROTO,https` |
| `REDIS_HOST` | Redis hostname | `redis` | `redis` |
| `REDIS_PORT` | Redis port | `6379` | `6379` |

#### GitHub Container Registry (Production Only)

| Variable | Description | Example |
|----------|-------------|---------|
| `GHCR_OWNER` | GitHub username or organization | `your-username` |
| `GHCR_REPO` | Repository name | `your-repo-name` |

### Django Settings

The Django settings are located in `src/web/web/settings.py` and use `python-decouple` for environment-based configuration. The main application is structured as:

- **Settings Module**: `web.settings`
- **ASGI Application**: `apps.gateway.asgi:application`
- **Celery App**: `web.celery:celery_app`
- **Main Gateway App**: `apps.gateway` (handles routing, WebSockets, and core API)

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
├── docker-compose.yml              # Production Docker Compose (GHCR images)
├── docker-compose-local.yml        # Local development Docker Compose
├── .dockerignore                   # Docker ignore file
├── .env                            # Environment variables (create this)
├── nginx.conf                      # Nginx production configuration (SSL, Flutter)
├── nginx-local.conf                # Nginx local development configuration
├── test.http                       # API test file (VS Code REST Client)
├── certbot/                        # SSL certificates directory
│   ├── conf/                       # Certificate files
│   └── data/                       # ACME challenge files
└── src/
    └── web/
        ├── dockerfile              # Django application Dockerfile
        ├── requirements.txt        # Python dependencies
        ├── manage.py               # Django management script
        ├── web/                    # Django project settings
        │   ├── settings.py         # Main settings (uses python-decouple)
        │   ├── settings_test.py    # Test settings
        │   ├── celery.py           # Celery configuration
        │   └── __init__.py
        ├── apps/                   # Django applications
        │   └── gateway/            # Main application
        │       ├── asgi.py         # ASGI application entry point
        │       ├── wsgi.py         # WSGI application entry point
        │       ├── routing.py      # WebSocket routing
        │       ├── urls.py         # URL configuration
        │       ├── views.py        # API views
        │       ├── models.py       # Database models
        │       ├── admin.py        # Django admin configuration
        │       ├── ping.py         # Health check endpoint
        │       ├── middleware.py   # Custom middleware
        │       └── ...
        └── features/               # BDD test features (Behave)
```

## Technology Stack

### Core Framework
- **Python 3.12** - Base runtime environment
- **Django 5.1.15** - Web framework
- **Django REST Framework 3.15.2+** - REST API framework
- **Daphne 4.2.1** - ASGI server for async and WebSocket support
- **Channels 4.3.1** - WebSocket and async support
- **Channels Redis 4.3.0** - Redis channel layer

### Task Processing
- **Celery 5.4.0** - Distributed task queue
- **Redis 5.1.1** - Message broker and cache backend

### Database
- **PostgreSQL with PostGIS** - Spatial database (local development)
- **psycopg2 2.9.9** - PostgreSQL adapter
- **GDAL 3.6.2** - Geospatial data abstraction library

### Authentication & Security
- **djangorestframework-simplejwt 5.5.0** - JWT authentication
- **Firebase Admin 6.6.0** - Firebase integration

### Infrastructure
- **Nginx** - Reverse proxy and static file server
- **Docker & Docker Compose** - Containerization
- **Supervisor** - Process control system (in Docker)

### Development & Testing Tools
- **behave 1.2.6** - BDD framework
- **behave-django 1.4.0** - Django integration for Behave
- **coverage 7.6.1** - Code coverage measurement
- **mock 5.1.0** - Mocking library
- **freezegun 0.3.4** - Time mocking

### API Documentation
- **drf-yasg 1.21.11** - Swagger/OpenAPI documentation generator

### Utilities & Additional Libraries
- **python-decouple 3.8** - Environment variable management
- **django-filter 24.3** - Dynamic QuerySet filtering
- **django-modeltranslation 0.19.12** - Model field translation
- **django-map-widgets 0.5.1** - Map widgets for Django admin
- **phonenumbers 8.13.31** - Phone number parsing and validation
- **Pillow** - Image processing (via Django)
- **Requests 2.32.3** - HTTP library
- **psutil 6.0.0** - System and process utilities

## API Documentation

Once the application is running, you can access the auto-generated API documentation:

- **Swagger UI**: http://localhost/swagger/
- **ReDoc**: http://localhost/redoc/

### Testing API Endpoints

A `test.http` file is included for quick API testing with VS Code REST Client extension:

```http
GET http://127.0.0.1:80/api/ping/
```

Install the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) in VS Code to use this file interactively.

## Development

### Adding Dependencies

1. Add the package to `src/web/requirements.txt`
2. Rebuild the Docker images:
   ```bash
   docker-compose -f docker-compose-local.yml up --build
   ```

### Building and Pushing Production Images

To build and push images to GitHub Container Registry:

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build images
docker build -t ghcr.io/USERNAME/REPO/web:latest ./src/web
docker build -t ghcr.io/USERNAME/REPO/celery:latest ./src/web

# Push images
docker push ghcr.io/USERNAME/REPO/web:latest
docker push ghcr.io/USERNAME/REPO/celery:latest
```

### WebSocket Development

WebSockets are configured in `apps/gateway/routing.py` and use Django Channels. The WebSocket endpoint is available at:

- Local: `ws://localhost/ws/...`
- Production: `wss://yourdomain.com/ws/...`

Nginx is pre-configured to proxy WebSocket connections with proper headers and long-lived connection support.

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

# Run BDD tests with Behave
docker exec -it web python manage.py behave

# Run with coverage
docker exec -it web coverage run --source='.' manage.py test
docker exec -it web coverage report

# Generate HTML coverage report
docker exec -it web coverage html
```

### Geospatial Features

The template includes PostGIS and GDAL support for geospatial data:

```bash
# Access PostgreSQL with PostGIS
docker exec -it db psql -U ${DB_User} -d ${DB_Name}

# Check PostGIS version
SELECT PostGIS_version();

# Enable PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Troubleshooting

### Container Issues

```bash
# Restart all services
docker-compose -f docker-compose-local.yml restart

# Rebuild from scratch
docker-compose -f docker-compose-local.yml down -v
docker-compose -f docker-compose-local.yml up --build

# Check container status
docker-compose -f docker-compose-local.yml ps

# View resource usage
docker stats

# Check logs for specific service
docker logs web
docker logs celery
docker logs nginx
docker logs redis
docker logs db
```

### Database Issues

```bash
# Access PostgreSQL
docker exec -it db psql -U ${DB_User} -d ${DB_Name}

# Check database connection
docker exec -it web python manage.py dbshell

# Reset migrations (WARNING: destroys all data)
docker exec -it web python manage.py migrate --fake app_name zero
docker exec -it web python manage.py migrate

# Reset database completely (WARNING: destroys all data)
docker-compose -f docker-compose-local.yml down -v
docker-compose -f docker-compose-local.yml up
```

### Celery Issues

```bash
# Check Celery worker status
docker exec -it celery celery -A web inspect active

# Purge all tasks
docker exec -it celery celery -A web purge

# Check registered tasks
docker exec -it celery celery -A web inspect registered
```

### Redis Issues

```bash
# Access Redis CLI
docker exec -it redis redis-cli

# Check Redis connection
docker exec -it redis redis-cli ping

# Clear all Redis data
docker exec -it redis redis-cli FLUSHALL
```

### Permission Issues

On Linux/Mac, if you encounter permission issues with volumes:

```bash
# Fix volume permissions
docker-compose -f docker-compose-local.yml run --rm web chown -R $(id -u):$(id -g) /src/web
```

### SSL Certificate Issues (Production)

```bash
# Test certificate paths
docker exec -it nginx ls -la /etc/nginx/ssl/live/yourdomain.com/

# Verify Nginx configuration
docker exec -it nginx nginx -t

# Reload Nginx configuration
docker exec -it nginx nginx -s reload
```

### Common Issues

**Issue**: Database connection refused
- **Solution**: Ensure the database container is healthy: `docker-compose ps`
- Wait for the healthcheck to pass before the web container starts

**Issue**: Static files not loading
- **Solution**: Run `docker exec -it web python manage.py collectstatic --noinput`

**Issue**: WebSocket connection fails
- **Solution**: Check Nginx WebSocket proxy configuration and ensure Daphne is running

**Issue**: Import errors or module not found
- **Solution**: Rebuild the containers: `docker-compose -f docker-compose-local.yml up --build`

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

**Note**: This is a template project. Customize it according to your specific needs and security requirements before deploying to production.

## Key Differences: Local vs Production

### Local Development (`docker-compose-local.yml`)
- Includes PostgreSQL/PostGIS database container
- Code mounted as volumes for live editing
- Automatic migrations on startup (`makemigrations` + `migrate`)
- Debug mode typically enabled
- Simple HTTP on port 80
- Builds images locally

### Production (`docker-compose.yml`)
- Uses pre-built GHCR images
- Requires external database
- No code volumes (baked into image)
- Manual migration control
- SSL/HTTPS support
- Rate limiting and security headers
- Can host Flutter web apps via Nginx
- Environment variable driven configuration

## Security Considerations

Before deploying to production:

1. **Change the Django secret key** - Generate a new one and never commit it to version control
2. **Disable DEBUG mode** - Set `DJANGO_DEBUG=False`
3. **Configure ALLOWED_HOSTS** - Restrict to your actual domains
4. **Set up HTTPS** - Configure SSL certificates properly
5. **Use strong database passwords** - Never use default or weak passwords
6. **Configure CSRF_TRUSTED_ORIGINS** - Set to your actual domains with HTTPS
7. **Review Nginx security headers** - Customize CSP policy for your needs
8. **Set up proper logging** - Configure log aggregation and monitoring
9. **Enable rate limiting** - Review and adjust Nginx rate limits
10. **Secure Redis** - Consider adding Redis password authentication
11. **Regular updates** - Keep dependencies updated for security patches

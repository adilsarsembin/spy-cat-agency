# Spy Cat Agency

A Django management application for Spy Cat Agency (SCA) to manage cats, missions, and targets.

## Project Structure

```
spy-cat-agency/
├── apps/
│   ├── config/        # Django project configuration (settings, wsgi, asgi)
│   ├── manage.py      # Django management script
│   ├── urls.py        # Root URL configuration
│   ├── spy_cats/      # Spy cats app (models, views, serializers, urls)
│   ├── missions/      # Missions app (models, views, serializers, urls)
│   ├── targets/       # Targets app (models, views, serializers, urls)
│   └── notes/         # Notes app (models, views, serializers, urls)
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker Compose configuration
```

## Setup

### Using Docker (Recommended)

1. Build and start containers:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python apps/manage.py migrate
```

3. Create a superuser (optional):
```bash
docker-compose exec web python apps/manage.py createsuperuser
```

The application will be available at `http://localhost:8000`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and configure environment variables:
```bash
export DB_NAME=spycatagency
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

3. Run migrations:
```bash
python apps/manage.py makemigrations
python apps/manage.py migrate
```

4. Create a superuser (optional):
```bash
python apps/manage.py createsuperuser
```

5. Run the development server:
```bash
python apps/manage.py runserver
```

## Apps

The project is organized into separate Django apps:

- **apps.spy_cats**: Manages spy cats (name, code name, availability)
- **apps.missions**: Manages missions assigned to cats
- **apps.targets**: Manages targets for missions (1-3 per mission)
- **apps.notes**: Manages notes written by cats on targets

Each app has its own:
- `models.py` - Database models
- `views.py` - View functions/classes
- `serializers.py` - API serializers
- `urls.py` - URL routing

## Models

- **Cat**: Represents a spy cat with name, code name, hire date, and availability status
- **Mission**: Represents a mission assigned to a cat (one cat per mission)
- **Target**: Represents a target to spy on (1-3 targets per mission)
- **Note**: Represents notes written by cats on targets (frozen when target is completed)

## Database

PostgreSQL is used as the database backend. Configure the connection via environment variables or docker-compose.yml.

## API Documentation

### Swagger UI

Interactive API documentation is available at: `http://localhost:8000/swagger/`

### Postman Collection

A Postman collection with all API endpoints is available in the repository: [postman_collection.json](postman_collection.json)

To import the collection:
1. Open Postman
2. Click "Import" button
3. Select the `postman_collection.json` file
4. The collection will be imported with all endpoints pre-configured

The collection includes:
- **Spy Cats**: List, Create, Get, Update Salary, Delete
- **Missions**: List, Create with Targets, Get, Assign Cat, Get/Update Target, Delete
- **Notes**: List, Create, Get, Update, Delete (with optional target filtering)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ConfigHub** — a full-stack configuration management platform. Supports JSON (with schema validation) and TOML formats, with version history, audit logging, and a dynamic role-based permission system.

## Development Commands

### Full Stack (Docker)
```bash
docker-compose up -d        # Start all services
docker-compose logs -f      # Tail logs
docker-compose down         # Stop all services
```

### Backend (Django)
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
python init_menus.py        # Seed menus/permissions (run once after migrate)
python manage.py test       # Run tests
```

### Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev      # Dev server at http://localhost:3000
npm run build    # Production build → dist/
npm run preview  # Preview production build
```

Default dev credentials: `admin` / `admin123`

## Architecture

### Backend (`backend/`)
Five Django apps with clear separation:
- `config_type/` — ConfigType model: defines format (JSON/TOML) and JSON Schema template
- `config_instance/` — ConfigInstance model: stores actual config content (text + parsed JSON), triggers versioning on save
- `smart_permission/` — Users, roles, permissions, and dynamic menu generation
- `audit/` — AuditLog: records every CREATE/UPDATE/DELETE/VIEW/EXPORT/IMPORT action
- `versioning/` — ConfigVersion snapshots; exposes rollback endpoint

API base: `http://localhost:8000/api/`

### Frontend (`frontend/src/`)
- **Dynamic routing**: Routes are generated at startup from backend menu data (`router/` + `permission/`), not statically defined
- **Permission system**: Global Vue mixin checks each button's permission against `missing_permissions` from the Pinia store — button visibility is permission-driven, not role-driven
- **Pinia stores**: `stores/user.js` (auth state), `stores/permission.js` (menu + permission state)
- **Key components**: `JsonSchemaEditor.vue` (form-based, uses `@json-editor/json-editor`), `CodeEditor.vue` (syntax highlighting via CodeMirror 6)
- **Vite proxy**: `/api` → `http://localhost:8000` in dev; Nginx reverse proxy in prod

### Environment Variables
| Variable | Dev Default | Notes |
|---|---|---|
| `DJANGO_DEBUG` | `True` | Set `False` in prod |
| `DJANGO_SECRET_KEY` | hardcoded | Change in prod |
| `DB_ENGINE` | `sqlite` | Use `mysql8` for prod |
| `DB_HOST` / `DB_PORT` | `localhost` / `3306` | MySQL only |
| `DB_NAME/USER/PASSWORD` | `confighub` / `confighub` / `confighub123` | MySQL only |

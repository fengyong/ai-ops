# Backend API Documentation

<cite>
**Referenced Files in This Document**
- [confighub/urls.py](file://backend/confighub/urls.py)
- [confighub/settings.py](file://backend/confighub/settings.py)
- [config_type/urls.py](file://backend/config_type/urls.py)
- [config_type/views.py](file://backend/config_type/views.py)
- [config_instance/urls.py](file://backend/config_instance/urls.py)
- [config_instance/views.py](file://backend/config_instance/views.py)
- [config_type/models.py](file://backend/config_type/models.py)
- [config_instance/models.py](file://backend/config_instance/models.py)
- [versioning/models.py](file://backend/versioning/models.py)
- [audit/models.py](file://backend/audit/models.py)
- [config_type/serializers.py](file://backend/config_type/serializers.py)
- [config_instance/serializers.py](file://backend/config_instance/serializers.py)
</cite>

## Update Summary
**Changes Made**
- Added new API Root Endpoint section documenting the centralized API discovery functionality
- Updated Architecture Overview to include the new API root endpoint
- Enhanced Project Structure diagram to show the new root endpoint integration
- Updated URL routing explanation to reflect the new centralized endpoint approach

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document provides comprehensive API documentation for the AI-Ops Configuration Hub backend REST APIs. It covers configuration type management, configuration instance management, version control, and audit log operations. For each endpoint, you will find HTTP methods, URL patterns, request/response schemas, authentication requirements, and error handling. It also documents pagination, filtering, and security considerations.

**Updated** The API now includes a centralized root endpoint that provides structured discovery of available endpoints for admin access and resource navigation.

## Project Structure
The backend is a Django application with Django REST Framework (DRF) providing automatic CRUD endpoints via ViewSets and routers. URL routing is organized under /api/, with separate routers for configuration types and instances. A new centralized API root endpoint provides discovery of available endpoints.

```mermaid
graph TB
Root["confighub/urls.py<br/>Root API endpoint + app routers"] --> APIRoot["api_root()<br/>Centralized API Discovery"]
Root --> Admin["Admin Interface<br/>/admin/"]
Root --> CT["config_type/urls.py<br/>Router for 'types'"]
Root --> CI["config_instance/urls.py<br/>Router for 'instances'"]
APIRoot --> Endpoints["Endpoints:<br/>- /admin/<br/>- /api/<br/>- /api/types/<br/>- /api/instances/"]
CT --> CTV["config_type/views.py<br/>ConfigTypeViewSet"]
CI --> CIV["config_instance/views.py<br/>ConfigInstanceViewSet"]
CIV --> VM["versioning/models.py<br/>ConfigVersion model"]
CIV --> AM["audit/models.py<br/>AuditLog model"]
```

**Diagram sources**
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)
- [confighub/urls.py:34-39](file://backend/confighub/urls.py#L34-L39)
- [config_type/urls.py:5-10](file://backend/config_type/urls.py#L5-L10)
- [config_instance/urls.py:5-10](file://backend/config_instance/urls.py#L5-L10)
- [config_type/views.py:8-39](file://backend/config_type/views.py#L8-L39)
- [config_instance/views.py:11-150](file://backend/config_instance/views.py#L11-L150)

**Section sources**
- [confighub/urls.py:21-39](file://backend/confighub/urls.py#L21-L39)
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)

## Core Components
- **API Root Endpoint**: Centralized endpoint providing structured discovery of available API endpoints for admin access and navigation.
- Configuration Type Management: Provides CRUD operations for configuration types with search and filter support.
- Configuration Instance Management: Provides CRUD operations for configuration instances, versioning, rollback, and content retrieval.
- Version Control: Tracks historical versions of configuration instances.
- Audit Logs: Records user actions on configuration instances.

Key implementation highlights:
- Centralized API discovery via dedicated root endpoint.
- Automatic endpoints via DRF ViewSet routers.
- Pagination configured globally.
- Filtering via query parameters.
- Transactional updates and version creation.
- Audit logging on create/update.

**Section sources**
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)
- [config_type/views.py:8-39](file://backend/config_type/views.py#L8-L39)
- [config_instance/views.py:11-150](file://backend/config_instance/views.py#L11-L150)
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)

## Architecture Overview
The API follows a layered architecture with centralized endpoint discovery:
- **Root API Endpoint**: Provides structured discovery of available endpoints.
- URL routing maps /api/types and /api/instances to respective ViewSets.
- ViewSets handle HTTP verbs and delegate to serializers and models.
- Versioning and audit models persist historical and activity data.

```mermaid
graph TB
subgraph "API Discovery Layer"
RootEndpoint["GET /<br/>API Root Endpoint"]
Endpoints["Endpoints Object:<br/>- admin: /admin/<br/>- api: /api/<br/>- types: /api/types/<br/>- instances: /api/instances/"]
end
subgraph "API Layer"
Types["GET /api/types/<name>/instances"]
Instances["GET /api/instances/{id}/versions<br/>POST /api/instances/{id}/rollback<br/>GET /api/instances/{id}/content"]
end
subgraph "Domain Layer"
VSetT["ConfigTypeViewSet"]
VSetI["ConfigInstanceViewSet"]
Versions["ConfigVersion model"]
Audit["AuditLog model"]
end
RootEndpoint --> Endpoints
Types --> VSetT
Instances --> VSetI
VSetI --> Versions
VSetI --> Audit
```

**Diagram sources**
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)
- [config_type/views.py:27-39](file://backend/config_type/views.py#L27-L39)
- [config_instance/views.py:92-149](file://backend/config_instance/views.py#L92-L149)
- [versioning/models.py](file://backend/versioning/models.py)
- [audit/models.py](file://backend/audit/models.py)

## Detailed Component Analysis

### API Root Endpoint
**New Feature** - Centralized API Discovery

Endpoints:
- GET /
  - Purpose: Provide centralized API discovery with structured endpoint information.
  - Response: JSON object containing API metadata and available endpoints.
  - Response Schema:
    ```json
    {
      "message": "ConfigHub API",
      "version": "1.0.0",
      "endpoints": {
        "admin": "/admin/",
        "api": "/api/",
        "types": "/api/types/",
        "instances": "/api/instances/"
      }
    }
    ```
  - Authentication: Not enforced by default settings.
  - Permissions: AllowAny by default.
  - Usage: Ideal for admin access and automated client initialization.

**Section sources**
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)

### Configuration Type Management API
Endpoints:
- GET /api/types
  - Purpose: List configuration types with optional filters.
  - Query parameters:
    - search: substring match on name or title.
    - format: filter by format.
  - Response: Paginated list of configuration types.
  - Authentication: Not enforced by default settings.
  - Permissions: AllowAny by default.
  - Pagination: PageNumberPagination, page size 20.

- GET /api/types/{name}
  - Purpose: Retrieve a configuration type by name.
  - Path parameter: name (lookup field).
  - Response: Single configuration type object.
  - Authentication: Not enforced by default.

- POST /api/types
  - Purpose: Create a configuration type.
  - Request body: Fields defined by ConfigTypeSerializer.
  - Response: Created configuration type object.
  - Authentication: Not enforced by default.

- PUT/PATCH /api/types/{name}
  - Purpose: Update a configuration type by name.
  - Path parameter: name.
  - Response: Updated configuration type object.
  - Authentication: Not enforced by default.

- DELETE /api/types/{name}
  - Purpose: Delete a configuration type by name.
  - Path parameter: name.
  - Response: Deletion result.
  - Authentication: Not enforced by default.

- GET /api/types/{name}/instances
  - Purpose: List instances belonging to this configuration type.
  - Path parameter: name.
  - Response: Array of instance summaries (id, name, version, updated_at).
  - Authentication: Not enforced by default.

Notes:
- Filtering and search are handled in the ViewSet's get_queryset method.
- Lookup by name is enabled via lookup_field.

**Section sources**
- [config_type/urls.py:5-10](file://backend/config_type/urls.py#L5-L10)
- [config_type/views.py:8-39](file://backend/config_type/views.py#L8-L39)
- [config_type/serializers.py](file://backend/config_type/serializers.py)
- [config_type/models.py](file://backend/config_type/models.py)
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)

### Configuration Instance Management API
Endpoints:
- GET /api/instances
  - Purpose: List configuration instances with optional filters.
  - Query parameters:
    - config_type: filter by configuration type name.
    - search: substring match on name.
    - format: filter by format.
  - Response: Paginated list of instances with related config_type.
  - Authentication: Not enforced by default.
  - Pagination: PageNumberPagination, page size 20.

- GET /api/instances/{id}
  - Purpose: Retrieve a configuration instance by ID.
  - Path parameter: id.
  - Response: Instance object with related config_type.
  - Authentication: Not enforced by default.

- POST /api/instances
  - Purpose: Create a configuration instance.
  - Request body: Fields defined by ConfigInstanceSerializer.
  - Behavior:
    - Creates initial version (version=1).
    - Records audit log for CREATE.
  - Response: Created instance object.
  - Authentication: Not enforced by default.

- PUT/PATCH /api/instances/{id}
  - Purpose: Update a configuration instance.
  - Path parameter: id.
  - Behavior:
    - Increments version number.
    - Creates new version record.
    - Records audit log for UPDATE.
  - Response: Updated instance object.
  - Authentication: Not enforced by default.

- DELETE /api/instances/{id}
  - Purpose: Delete a configuration instance.
  - Path parameter: id.
  - Response: Deletion result.
  - Authentication: Not enforced by default.

- GET /api/instances/{id}/versions
  - Purpose: Retrieve version history for an instance.
  - Path parameter: id.
  - Response: Array of version entries (version, format, change_reason, changed_by, changed_at).
  - Authentication: Not enforced by default.

- POST /api/instances/{id}/rollback
  - Purpose: Rollback to a previous version.
  - Path parameter: id.
  - Request body:
    - version: target version number.
  - Behavior:
    - Validates existence of target version.
    - Creates new version with rolled-back content.
  - Response: { message, new_version }.
  - Authentication: Not enforced by default.

- GET /api/instances/{id}/content
  - Purpose: Get content in a specified format.
  - Path parameter: id.
  - Query parameters:
    - format: requested output format (defaults to instance format).
  - Response: { format, content, parsed_data }.
  - Authentication: Not enforced by default.

Notes:
- Atomic transactions wrap create/update to ensure consistency.
- Versioning and audit models are used for persistence.
- Content retrieval supports format conversion via instance method.

**Section sources**
- [config_instance/urls.py:5-10](file://backend/config_instance/urls.py#L5-L10)
- [config_instance/views.py:11-150](file://backend/config_instance/views.py#L11-L150)
- [config_instance/serializers.py](file://backend/config_instance/serializers.py)
- [config_instance/models.py](file://backend/config_instance/models.py)
- [versioning/models.py](file://backend/versioning/models.py)
- [audit/models.py](file://backend/audit/models.py)
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)

### Version Control API
While there is no dedicated router for versions, the system exposes version history via the instance endpoint:
- GET /api/instances/{id}/versions
  - Returns historical versions of a configuration instance.
  - Each entry includes version number, format, change reason, who changed it, and when.

Rollback capability:
- POST /api/instances/{id}/rollback
  - Requires a version number in the request body.
  - On success, creates a new version reflecting the rollback and returns a message and new version number.

**Section sources**
- [config_instance/views.py:92-136](file://backend/config_instance/views.py#L92-L136)
- [versioning/models.py](file://backend/versioning/models.py)

### Audit Log API
There is no dedicated router for audit logs. However, the system records audit events during create and update operations:
- CREATE: Logged when a new instance is created.
- UPDATE: Logged when an instance is updated (including rollbacks).
Each audit event includes user, action, resource type, resource id/name, and details.

Note: There is no explicit endpoint to query audit logs in the current codebase.

**Section sources**
- [config_instance/views.py:36-60](file://backend/config_instance/views.py#L36-L60)
- [config_instance/views.py:62-90](file://backend/config_instance/views.py#L62-L90)
- [audit/models.py](file://backend/audit/models.py)

## Dependency Analysis
- URL routing:
  - Root includes dedicated API discovery endpoint and app routers for types and instances.
- ViewSets:
  - ConfigTypeViewSet handles types.
  - ConfigInstanceViewSet handles instances and delegates to versioning and audit models.
- Serializers:
  - Define request/response schemas for types and instances.
- Models:
  - ConfigType and ConfigInstance define domain entities.
  - ConfigVersion persists version history.
  - AuditLog persists audit events.

```mermaid
graph LR
Settings["confighub/settings.py<br/>REST defaults & pagination"] --> Root["confighub/urls.py<br/>API Root + Routers"]
Root --> Types["config_type/views.py"]
Root --> Instances["config_instance/views.py"]
Types --> CTModels["config_type/models.py"]
Instances --> CIModeuls["config_instance/models.py"]
Instances --> Versions["versioning/models.py"]
Instances --> Audit["audit/models.py"]
```

**Diagram sources**
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)
- [confighub/urls.py:21-39](file://backend/confighub/urls.py#L21-L39)
- [config_type/views.py:8-39](file://backend/config_type/views.py#L8-L39)
- [config_instance/views.py:11-150](file://backend/config_instance/views.py#L11-L150)
- [config_type/models.py](file://backend/config_type/models.py)
- [config_instance/models.py](file://backend/config_instance/models.py)
- [versioning/models.py](file://backend/versioning/models.py)
- [audit/models.py](file://backend/audit/models.py)

**Section sources**
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)
- [confighub/urls.py:21-39](file://backend/confighub/urls.py#L21-L39)
- [config_type/views.py:8-39](file://backend/config_type/views.py#L8-L39)
- [config_instance/views.py:11-150](file://backend/config_instance/views.py#L11-L150)

## Performance Considerations
- Pagination: PageNumberPagination with page size 20 is globally configured. Clients should implement cursor-based pagination for large datasets if needed.
- Select-related: Instance queries use select_related('config_type') to reduce database hits.
- Transactions: Create/update operations are wrapped in atomic transactions to maintain consistency.
- Filtering: Queries apply filters in Python for simplicity; consider adding database-level indexes for frequently filtered fields.
- **New** API Root Endpoint: Lightweight JSON response with minimal processing overhead for endpoint discovery.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- 404 Not Found on rollback:
  - Cause: Target version does not exist.
  - Resolution: Verify the version number exists via GET /api/instances/{id}/versions.
- Authentication:
  - Current settings allow any permission. If you enable authentication, ensure clients send credentials.
- CORS:
  - CORS is enabled for all origins. For production, restrict origins and configure credentials as needed.
- **New** API Root Endpoint Access:
  - The root endpoint is accessible without authentication and provides basic API discovery information.
  - Ensure clients handle the JSON response structure correctly.

**Section sources**
- [config_instance/views.py:112-116](file://backend/config_instance/views.py#L112-L116)
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)
- [confighub/settings.py:31](file://backend/confighub/settings.py#L31)
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)

## Conclusion
The AI-Ops Configuration Hub backend provides a clean REST API surface for managing configuration types and instances, with integrated versioning and audit logging. The APIs are generated via DRF ViewSets and routers, offering standard CRUD operations plus specialized actions for versions and content retrieval. **New** The addition of a centralized API root endpoint enhances discoverability and provides structured access to available endpoints. Pagination and filtering are supported out-of-the-box, while authentication and permissions are currently permissive by default.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### API Versioning Strategy
- No explicit API versioning is implemented in the current codebase. Clients should pin to the current base path (/api/) and expect backward-compatible changes unless documented otherwise.
- **New** The API root endpoint includes a version field that can be used for client-side version detection.

[No sources needed since this section provides general guidance]

### Pagination Implementation
- Global pagination settings:
  - DEFAULT_PAGINATION_CLASS: PageNumberPagination
  - PAGE_SIZE: 20
- Clients should rely on standard DRF pagination fields (page, page_size) when consuming lists.

**Section sources**
- [confighub/settings.py:33-39](file://backend/confighub/settings.py#L33-L39)

### Filtering Capabilities
- Configuration Types:
  - search: substring match on name or title.
  - format: filter by format.
- Configuration Instances:
  - config_type: filter by configuration type name.
  - search: substring match on name.
  - format: filter by format.

**Section sources**
- [config_type/views.py:14-25](file://backend/config_type/views.py#L14-L25)
- [config_instance/views.py:21-34](file://backend/config_instance/views.py#L21-L34)

### Authentication and Authorization
- Authentication:
  - Not enforced by default settings.
- Authorization:
  - DEFAULT_PERMISSION_CLASSES set to AllowAny.
- Recommendations:
  - Enable session or token-based authentication.
  - Define custom permissions to restrict access to sensitive operations.

**Section sources**
- [confighub/settings.py:33-36](file://backend/confighub/settings.py#L33-L36)

### Rate Limiting Information
- No rate limiting is configured in the current codebase. Consider integrating DRF Throttling for production deployments.

[No sources needed since this section provides general guidance]

### Security Considerations
- CORS: Enabled for all origins; restrict origins and configure credentials for production.
- CSRF: CSRF middleware is present; ensure proper handling for browser clients.
- Database: Supports SQLite and MySQL8 backends; configure secure credentials and network access.
- **New** API Root Endpoint: Minimal security risk as it only provides endpoint discovery information.

**Section sources**
- [confighub/settings.py:31](file://backend/confighub/settings.py#L31)
- [confighub/settings.py:94-117](file://backend/confighub/settings.py#L94-L117)
- [confighub/urls.py:21-32](file://backend/confighub/urls.py#L21-L32)

### Practical Examples

- **New** Get API Discovery Information
  - Method: GET
  - URL: /
  - Response: Structured endpoint information for admin access
  - Expected response: {
    "message": "ConfigHub API",
    "version": "1.0.0",
    "endpoints": {
      "admin": "/admin/",
      "api": "/api/",
      "types": "/api/types/",
      "instances": "/api/instances/"
    }
  }

- Create a configuration type
  - Method: POST
  - URL: /api/types
  - Body: Fields defined by ConfigTypeSerializer
  - Expected response: Created configuration type object

- List configuration instances with filters
  - Method: GET
  - URL: /api/instances?config_type=example-type&search=myapp&format=yaml
  - Expected response: Paginated list of instances with related config_type

- Retrieve version history
  - Method: GET
  - URL: /api/instances/{id}/versions
  - Expected response: Array of version entries

- Rollback to a specific version
  - Method: POST
  - URL: /api/instances/{id}/rollback
  - Body: { version: 2 }
  - Expected response: { message, new_version }

- Get content in a specific format
  - Method: GET
  - URL: /api/instances/{id}/content?format=json
  - Expected response: { format, content, parsed_data }

[No sources needed since this section provides general guidance]
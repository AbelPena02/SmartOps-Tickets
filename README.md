# SmartOps Tickets API

AI-powered incident and ticket management system for DevOps teams.
Monitors servers, classifies incidents, scores ticket priority, and exposes metrics for observability.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Environment Setup](#environment-setup)
5. [Running Locally](#running-locally)
6. [API Endpoints](#api-endpoints)
7. [Architecture Overview](#architecture-overview)
8. [Prometheus & Grafana](#prometheus--grafana)
9. [Contributing](#contributing)
10. [License](#license)

---

## Project Overview

SmartOps Tickets API allows DevOps teams to:

* Automatically classify tickets based on description.
* Score ticket priority based on severity.
* Simulate server states and lifecycle (BOOTING → RUNNING → FAILED).
* Expose Prometheus metrics for monitoring.
* Visualize system status via Grafana dashboards.

---

## Features

* **Ticket Management:** Create, read, update, delete tickets.
* **AI Classification:** Rule-based + optional ML model for ticket categorization.
* **Priority Scoring:** Automatic severity scoring (high / medium / low).
* **Server Lifecycle Simulation:** Tracks server states.
* **Monitoring & Metrics:** Prometheus + Grafana dashboards.
* **Dockerized:** Full stack in Docker Compose.

---

## Getting Started

### Prerequisites

* Docker & Docker Compose
* Python 3.13 (if running outside Docker)
* Git
* AWS CLI (optional for cloud deployment)

### Environment Variables (`.env`)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=smartops
POSTGRES_PORT=5432
```

---

## Running Locally

1. Build and start containers:

```bash
docker compose up --build
```

2. API will be available at:

```
http://localhost:8000
```

3. Prometheus metrics:

```
http://localhost:8000/metrics
```

4. Grafana dashboard:

```
http://localhost:3000
```

Default login for Grafana: `admin` / `admin`

---

## API Endpoints

### Tickets

| Endpoint               | Method | Description                | Request Example                                                   | Response Example                                                                              |
| ---------------------- | ------ | -------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `/tickets/`            | POST   | Create a new ticket        | `{"title":"Server down","description":"All servers unreachable"}` | `{ "id": 1, "title": "...", "priority": "high", "classification": "general", ... }`           |
| `/tickets/`            | GET    | List all tickets           | -                                                                 | `[ { "id": 1, "title": "...", ... } ]`                                                        |
| `/tickets/{ticket_id}` | GET    | Get ticket by ID           | -                                                                 | `{ "id": 1, "title": "...", ... }`                                                            |
| `/tickets/{ticket_id}` | PUT    | Update ticket              | `{"description":"Server still down"}`                             | `{ "id": 1, "description": "...", "priority":"high", ... }`                                   |
| `/tickets/{ticket_id}` | DELETE | Delete ticket              | -                                                                 | `{ "message": "Ticket 1 deleted successfully" }`                                              |
| `/tickets/analyze`     | POST   | Analyze ticket description | `{"description":"Server outage"}`                                 | `{ "description": "...", "predicted_classification":"general", "predicted_priority":"high" }` |

### Health

* `/health` (GET) → Basic health check

### Metrics

* `/metrics` (GET) → Prometheus metrics

### Analytics

* `/analytics/summary` (GET) → Ticket summary by classification & priority

---

## Architecture Overview

```
+--------------------+      +--------------------+
|   Users / Clients  | ---> |  FastAPI (API)     |
+--------------------+      +--------------------+
                                   |
                                   v
                          +--------------------+
                          | PostgreSQL Database|
                          +--------------------+
                                   |
                                   v
                        +-------------------------+
                        | Priority & Classifier   |
                        +-------------------------+
                                   |
                                   v
                  +-----------------------------+
                  | Prometheus Metrics Endpoint |
                  +-----------------------------+
                                   |
                                   v
                         +----------------+
                         | Grafana Dash   |
                         +----------------+
```

* **FastAPI** handles ticket CRUD, classification, and scoring.
* **PriorityScorer** auto-calculates severity.
* **TicketClassifier** uses rule-based or ML model.
* **Prometheus** scrapes metrics from `/metrics`.
* **Grafana** visualizes metrics.

---

## Prometheus & Grafana Setup (Local)

1. Prometheus configuration (`prometheus.yml`):

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'fastapi'
    metrics_path: /metrics
    static_configs:
      - targets: ['api:8000']
```

2. Start containers:

```bash
docker compose up -d
```

3. Access dashboards:

* Prometheus: `http://localhost:9090`
* Grafana: `http://localhost:3000`

4. Add Prometheus as a Grafana data source and create dashboards as needed.

---

## Contributing

* Fork repo & clone
* Create feature branch
* Test locally
* Open pull request

---

## License

MIT License

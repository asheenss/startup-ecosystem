# API Endpoints

## Startups

- `GET /api/startups`
- `POST /api/startups`
- `GET /api/startups/{startup_id}`
- `PUT /api/startups/{startup_id}`
- `DELETE /api/startups/{startup_id}`

## Investors

- `GET /api/investors`
- `POST /api/investors`
- `GET /api/investors/{investor_id}`
- `PUT /api/investors/{investor_id}`
- `DELETE /api/investors/{investor_id}`
- `GET /api/investors/match/{startup_id}`

## Events

- `GET /api/events`
- `POST /api/events`
- `POST /api/events/{event_id}/register?user_id={user_id}`

## Connections

- `GET /api/connections`
- `POST /api/connections/request`

## AI

- `POST /api/ai/analyze-pitch-deck`

## Dashboards

- `GET /api/dashboard/founder/{user_id}`
- `GET /api/dashboard/investor/{user_id}`
- `GET /api/dashboard/admin`

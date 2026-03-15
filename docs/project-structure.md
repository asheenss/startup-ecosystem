# Improved Project Structure

## Backend

```text
backend/
  app/
    api/
      routes/
    core/
    db/
    models/
    schemas/
    services/
    utils/
  tests/
    api/
    unit/
    integration/
  pyproject.toml
  ruff.toml
  mypy.ini
  pytest.ini
```

## Frontend

```text
frontend/
  app/
    dashboard/
      admin/
      founder/
      investor/
    startups/
    investors/
    events/
    connections/
  components/
    ui/
    dashboard/
      charts/
  lib/
  styles/
  eslint.config.mjs
  prettier.config.mjs
  tailwind.config.ts
```

## Scalable Recommendation

- Put generic building blocks in `components/ui`
- Put dashboard-domain widgets in `components/dashboard`
- Move route-specific fetchers into `lib/api`
- Add `features/<domain>/` when flows become stateful or interactive

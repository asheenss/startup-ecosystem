# Database Schema

## users

- `id`
- `name`
- `email`
- `role`

## startup_profiles

- `id`
- `startup_name`
- `description`
- `industry`
- `stage`
- `pitch_deck_url`
- `founders`
- `funding_needed`
- `owner_id`

## investor_profiles

- `id`
- `investor_name`
- `interests`
- `funding_range`
- `preferred_industries`
- `owner_id`

## events

- `id`
- `title`
- `description`
- `location`
- `event_date`
- `organizer_name`
- `capacity`

## event_registrations

- `id`
- `event_id`
- `user_id`

## connection_requests

- `id`
- `sender_id`
- `receiver_id`
- `status`
- `note`

## ai_analyses

- `id`
- `startup_id`
- `extracted_text`
- `score`
- `problem_clarity`
- `market_size`
- `traction`
- `team_strength`
- `financial_potential`
- `improvement_suggestions`

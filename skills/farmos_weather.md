---
name: farmos-weather
description: Query weather data and forecasts for farm fields via the Agronomy module.
author: brianppetty
version: 1.0.3
trigger: "what's the weather", "can we spray", "GDD for field X", "forecast", "will it rain this week?", "temperature and wind right now", "field conditions?"
---

# FarmOS Weather

Query farmos-tasks and farmos-observations alongside weather for any field operation question. This skill connects to the FarmOS Agronomy weather module to provide real-time conditions, forecasts, growing degree day calculations, and spray-condition evaluation for your farm fields.

## API Base

http://100.102.77.110:8012

## Endpoints

### Health Check

```
GET http://100.102.77.110:8012/api/weather/health
```

Verify the weather service is running. Call this first if you suspect connectivity issues.

### Current Conditions

```
GET http://100.102.77.110:8012/api/weather/field/{field_id}/current
```

Returns current temperature, humidity, wind speed, wind direction, precipitation, and dew point for the specified field.

### Forecast

```
GET http://100.102.77.110:8012/api/weather/field/{field_id}/forecast?days={days}
```

Returns hourly and daily forecast data. Default is 7 days. Use this for planning field operations.

**Parameters:**
- `field_id` (required) — the FarmOS field identifier
- `days` (optional, default: 7) — number of forecast days (1–14)

### Historical Data

```
GET http://100.102.77.110:8012/api/weather/field/{field_id}/historical?startDate={startDate}&endDate={endDate}
```

Returns historical weather observations for a date range. Useful for post-season analysis and record keeping.

**Parameters:**
- `field_id` (required)
- `startDate` (required, ISO 8601)
- `endDate` (required, ISO 8601)

### Growing Degree Days (GDD)

```
GET http://100.102.77.110:8012/api/weather/field/{field_id}/gdd?baseTemp={baseTemp}&startDate={startDate}
```

Calculates accumulated GDD from `startDate` to today using `baseTemp` as the base threshold.

**Parameters:**
- `field_id` (required)
- `baseTemp` (required, in Fahrenheit — e.g., 50 for corn)
- `startDate` (required, planting date in ISO 8601)

### Spray Conditions

```
GET http://100.102.77.110:8012/api/weather/field/{field_id}/spray-conditions
```

Returns a go/no-go evaluation for spraying based on wind speed, temperature inversion risk, rain forecast, and humidity. Includes a human-readable recommendation.

### Coordinate Lookup

```
GET http://100.102.77.110:8012/api/weather/coordinates?latitude={latitude}&longitude={longitude}&type={type}
```

Look up weather by raw GPS coordinates instead of a FarmOS field ID. Useful when a field hasn't been registered yet.

**Parameters:**
- `latitude` (required, decimal degrees)
- `longitude` (required, decimal degrees)
- `type` (optional) — one of `current`, `forecast`, `gdd`

### Integration Dashboard

```
GET http://100.102.77.110:8012/api/integration/dashboard
```

Returns a combined view of all registered fields with current conditions and active alerts. Good for a morning overview.

## Default Location

If no field is specified and you need a fallback, use central Indiana coordinates:
- Latitude: 40.25
- Longitude: -85.67

## Response Handling

- All responses are JSON.
- Display temperatures in Fahrenheit unless the user specifies otherwise.
- For spray conditions, always show the recommendation text prominently.
- When showing forecasts, summarize the next 3 days unless the user asks for more.

## Error Handling

If a weather endpoint fails or returns empty, say so: "The weather service isn't responding right now." Don't guess the weather.

## Cross-Module Usage

- When spray conditions are favorable, suggest creating a spray task via `farmos-tasks`.
- When GDD thresholds are reached, suggest creating a side-dress or harvest task.
- Include weather context when logging `farmos-observations` for any field visit.

## Notes

This skill is read-only — it does not modify any FarmOS data. All write operations should go through the appropriate FarmOS skill (farmos-tasks, farmos-observations, etc.).

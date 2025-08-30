-- SARDIN-AI Database Schema
-- Version: 1.0.0
-- PostgreSQL with PostGIS extension

-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vessels Table
CREATE TABLE vessels (
    id SERIAL PRIMARY KEY,
    mmsi VARCHAR(9) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    vessel_type VARCHAR(50),
    length_m NUMERIC(5, 2),
    beam_m NUMERIC(5, 2),
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ocean Data Table
-- This table can get very large. Consider partitioning strategies.
CREATE TABLE ocean_data (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL, -- Storing as geographic coordinates
    sea_surface_temperature_c NUMERIC(5, 2),
    salinity NUMERIC(5, 2),
    chlorophyll_mg_m3 NUMERIC(6, 3),
    wave_height_m NUMERIC(5, 2),
    current_speed_mps NUMERIC(5, 2),
    current_direction_deg INTEGER,
    source VARCHAR(50) -- e.g., 'NOAA', 'Copernicus'
);
CREATE INDEX idx_ocean_data_location ON ocean_data USING GIST (location);
CREATE INDEX idx_ocean_data_timestamp ON ocean_data (timestamp);


-- AI Predictions Table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    prediction_type VARCHAR(50) NOT NULL, -- e.g., 'fishing_hotspot', 'market_price'
    prediction_score NUMERIC(6, 4),
    model_version VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_predictions_location ON predictions USING GIST (location);
CREATE INDEX idx_predictions_timestamp ON predictions (timestamp);


-- Navigation Related Tables
CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    vessel_id INTEGER NOT NULL REFERENCES vessels(id),
    status VARCHAR(50) NOT NULL DEFAULT 'planned', -- e.g., planned, active, completed, aborted
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE waypoints (
    id SERIAL PRIMARY KEY,
    mission_id INTEGER NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    name VARCHAR(100),
    location GEOMETRY(Point, 4326) NOT NULL,
    sequence_order INTEGER NOT NULL,
    arrival_time TIMESTAMP WITH TIME ZONE,
    departure_time TIMESTAMP WITH TIME ZONE,
    UNIQUE(mission_id, sequence_order)
);

CREATE TABLE no_go_zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    zone_type VARCHAR(50), -- e.g., 'conservation', 'military', 'hazard'
    geometry GEOMETRY(Polygon, 4326) NOT NULL,
    risk_level INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    valid_from TIMESTAMP WITH TIME ZONE,
    valid_to TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_no_go_zones_geometry ON no_go_zones USING GIST (geometry);

-- Add more tables for catch logs, sensor data, etc. as needed.
-- ...

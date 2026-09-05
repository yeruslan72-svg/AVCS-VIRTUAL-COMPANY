# INS Architecture

## Overview

The Intelligence Navigation System (INS) is the operational navigation layer of AVCS.

## Components

### 1. AI Dispatcher
- Routes incoming information to appropriate departments
- Classifies events
- Creates task packets

### 2. Seven Departments
- **LOOKOUT** — Detection
- **CHARTS** — Context
- **GYRO** — Motion
- **NAVIGATOR** — Threat Assessment
- **COMPASS** — Action Recommendation
- **HELM** — Execution
- **CAPTAIN** — Authority Interface

### 3. Aggregator
- Consolidates department outputs
- Preserves evidence and conflicts

### 4. Conflict Detector
- Identifies conflicts between departments
- Preserves conflicts for visibility

### 5. Decision Engine
- Formulates decision proposals
- Identifies available options

### 6. Authority Gate
- Presents decisions to human authority
- Receives authorization

### 7. State Machine
- Manages decision states
- Enforces decision pathway

## Decision Flow

INFORMATION → DISPATCHER → DEPARTMENTS → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD

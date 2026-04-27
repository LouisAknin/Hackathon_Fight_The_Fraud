# Fight The Fraud - AI Detection System

[![Hackathon](https://img.shields.io/badge/Winner-Technical_Prize_2025-blue.svg)](https://github.com/LouisAknin/Hackathon_Fight_The_Fraud)
[![Python](https://img.shields.io/badge/Backend-Python-3776AB.svg?logo=python&logoColor=white)]()
[![React](https://img.shields.io/badge/Frontend-React%20%2F%20TypeScript-61DAFB.svg?logo=react&logoColor=black)]()

> **Technical Prize Winner - Hackathon Fight The Fraud 2025**

An AI-powered, real-time banking fraud detection system. This project provides a full-stack solution to monitor transactions, identify suspicious patterns, and trigger immediate alerts to prevent financial crimes.

## Table of Contents
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)

## Architecture & Tech Stack

The application is built on a decoupled architecture, ensuring clean separation of concerns between the user interface and the data processing engine.

### Frontend
* **Framework:** React
* **Language:** TypeScript
* **Role:** A responsive interface and dashboard for visualizing transaction data and monitoring alerts in real time.

### Backend
* **Language:** Python
* **Role:** Server-side logic handling data ingestion, running machine learning models for anomaly detection, and serving data to the client.

## Repository Structure

```text
Hackathon_Fight_The_Fraud/
├── Back/       # Python backend, APIs, and AI models
├── Front/      # React and TypeScript frontend application
└── .gitignore
```

## Getting Started

Follow these steps to run the project locally.

### Prerequisites
* Node.js and npm (or yarn)
* Python 3.8+

### 1. Clone the repository
```bash
git clone https://github.com/LouisAknin/Hackathon_Fight_The_Fraud.git
cd Hackathon_Fight_The_Fraud
```

### 2. Setup and run the Backend
```bash
cd Back
# Install dependencies 
pip install -r requirements.txt
# Start the server (adjust command based on your specific framework, e.g., FastAPI, Flask)
python main.py
```

### 3. Setup and run the Frontend
```bash
cd ../Front
# Install dependencies
npm install
# Start the development server
npm start
```

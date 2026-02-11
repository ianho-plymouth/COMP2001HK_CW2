# CW2 Guide
A REST micro‑service for Trails, LocationPoints and Users backed by ODBC Driver 18 for SQL Server, 
documented with OpenAPI (Swagger), and protected for write operations via the external Authenticator. 
This README walks you through setup, run and testing step by step.


## 1) Prerequisites
Python 3.10+
ODBC Driver 18 for SQL Server
Network access to the SQL Server
Base on database(COMP2001_HK_CHo), and Schema(CW2)
The project’s Swagger UI is served at `/ui`


## 2) Ready the environment
Download the code from GitHub to your own computer
Connect to the VPN(UoP)
Connect to SQL Server database


## 3) Configure the application
Database Credentials lives in `.env`
Update `server`, `database`, `username`, and `password` for your environment


## 4) Install dependencies
Run the following command for installs dependencies
`pip install -r requirements.txt`
This installs Flask, Connexion (Swagger UI), pyodbc, flask‑cors, and requests


## 5) Run locally
Run the following command for start the app
`python app.py`
Swagger UI: http://localhost:8000/ui
OpenAPI JSON: http://localhost:8000/openapi.json
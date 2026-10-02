\# Week 4 — Multi-Service Stack with Docker Compose



\## SkillAudit Internship



This project demonstrates how multiple services can be orchestrated together using Docker Compose.



The stack contains three services:



\- Flask Web Application

\- PostgreSQL Database

\- Redis Cache



The Flask application communicates with both PostgreSQL and Redis.



\## Architecture



```text

&#x20;               Browser

&#x20;                  |

&#x20;                  v

&#x20;           Flask Web App

&#x20;             /        \\

&#x20;            v          v

&#x20;     PostgreSQL       Redis

&#x20;       Database        Cache


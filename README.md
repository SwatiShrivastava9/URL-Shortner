# URL-Shortner with Microservices Architecture

Overview

This project implements a URL Shortener using a microservices architecture with three Virtual Machines (VMs). Each VM has a specific role, ensuring scalability, modularity, and efficient resource utilization.

Architecture

The system consists of three main components:

VM1: API Server (Flask)

Runs a Flask application to handle URL shortening and redirection.

Connects to Redis (VM2) for storing and retrieving URL mappings.

Exposes a RESTful API for communication with the frontend (VM3).

VM2: Redis Server

Stores URL mappings in-memory for fast retrieval.

Accepts connections from VM1 for read/write operations.

VM3: Frontend (Apache2 + HTML/JavaScript)

Hosts a simple HTML + JavaScript webpage for user interaction.

Calls the Flask API (VM1) to generate shortened URLs.

Displays shortened URLs and allows redirection.

Runs on an Apache2 web server

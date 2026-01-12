# Reverse Proxy & HTTPS Setup

## Overview
This project demonstrates using **NGINX as a reverse proxy** to route traffic to backend services and enable **HTTPS** using **self-signed certificates** generated with `mkcert`. It also includes **HTTP → HTTPS redirection** for secure access.

---

## Table of Contents
1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Generate Certificates](#generate-certificates)  
4. [NGINX Configuration](#nginx-configuration)  
5. [Docker Compose Setup](#docker-compose-setup)  
6. [Local Domain Setup](#local-domain-setup)  
7. [Running the Project](#running-the-project)  
8. [Testing HTTPS](#testing-https)  

---

## Prerequisites
- Docker & Docker Compose installed  
- `mkcert` installed (for locally-trusted certificates)  
- Node.js backend running on port `3000`  

---

## Project Structure


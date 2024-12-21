# Docker Compose Generator UI

A clean and professional Python-based application built with [Flet](https://flet.dev/), designed to generate and manage Docker Compose configurations. This application provides an intuitive UI for configuring services, enabling/disabling them, and editing service-specific details.

---

## Features

### 1. **Domain/IP Management**
- Easily input and manage the domain and IP address for your infrastructure.
- Save the values independently without affecting the main configuration file.

### 2. **Service Selection**
- Choose from a list of predefined services (e.g., MariaDB, MySQL, PostgreSQL, Redis, etc.).
- Enable or disable services with simple checkboxes.
- Save selected services into a configuration file (`config.yaml`).

### 3. **Service Configuration**
- Edit and manage the configurations of each selected service.
- Update service-specific parameters (e.g., ports, usernames, passwords) via the UI.
- Save all changes dynamically to the configuration file.

---

## How It Works

### **Step 1: Manage Domain and IP**
1. Input the domain and IP address in the first tab.
2. Click `Save` to store the values temporarily (outside the `config.yaml` file).

### **Step 2: Select Services**
1. Navigate to the second tab.
2. Select the services you want to include in your Docker Compose file.
3. Save your selections to `config.yaml`.

### **Step 3: Edit Service Configurations**
1. Navigate to the third tab.
2. View and edit the parameters for each selected service.
3. Save the updated configuration to `config.yaml`.

---

## Installation

### Prerequisites
- Python 3.10 or later
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/docker-compose-generator-ui.git
   cd docker-compose-generator-ui
   python main.py

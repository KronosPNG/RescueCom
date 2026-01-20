# RescueCom 🚨

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**A Resilient Emergency Communication System for Disaster Scenarios**

> Master's Software Project Management Course Project - Leading 7 bachelor students through the development of a decentralized emergency communication platform.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Management](#project-management)
- [Team](#team)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About the Project

RescueCom addresses a critical gap in emergency communications during disasters when traditional Internet infrastructure becomes unavailable. The system enables emergency message transmission between victims (Rescuees) and rescue personnel (Rescuers) using Bluetooth and Wi-Fi Direct, automatically synchronizing with a cloud server once connectivity is restored.

### Background

During natural disasters, power outages, or infrastructure failures, traditional communication networks often become inaccessible, making it impossible for victims to request help and for rescue operations to coordinate effectively. RescueCom solves this problem by creating a decentralized, self-organizing peer-to-peer network that operates completely offline.

### Project Context

This proof-of-concept was developed as part of a Software Project Management master's course, where I led a team of 7 bachelor students through a complete software development lifecycle over 4 months (October 2025 - January 2026). The project demonstrates both technical feasibility and effective project management practices in an educational setting.

---

## ✨ Key Features

### 🌐 Offline Communication
- **Bluetooth & Wi-Fi Direct**: Message transmission without Internet connectivity
- **Local Persistence**: All messages stored locally with automatic cloud sync when online
- **Mesh Network**: Self-organizing, dynamic network topology

### 📡 Relay Functionality
- **Every Device is a Node**: All devices function as relay nodes to extend network range
- **Smart Routing**: Efficient message forwarding with duplicate prevention
- **Automatic Discovery**: Periodic scanning for nearby devices

### 🆘 Emergency Messaging
- **Priority Levels**: Categorized emergency messages with timestamps
- **Proximity-Based Location**: Determines victim location through proximity to Rescuer devices
- **Quick SOS Activation**: Predefined message templates for rapid emergency signaling

### ☁️ Cloud Synchronization
- **Automatic Sync**: Seamless data synchronization when Internet becomes available
- **Conflict Resolution**: Smart algorithms for handling duplicates and modifications
- **RESTful API**: Complete REST API for device communication and data management

### 🖥️ User Interfaces
- **Rescuee Interface**: Simple, intuitive desktop UI for sending emergency requests
- **Rescuer Interface**: Advanced dashboard with message queue management, prioritization tools, and response capabilities

### 🔒 Security
- **No Authentication for Victims**: Immediate access during emergencies
- **Validated Rescuers**: Authorization and validation for rescue personnel
- **HTTPS Communications**: Secure API connections

---

## 🏗️ Architecture

RescueCom consists of three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloud Server                            │
│  - Flask REST API                                            │
│  - PostgreSQL Database                                       │
│  - Message Queue Management                                  │
│  - Conflict Resolution                                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTPS (when online)
                   │
┌──────────────────┴──────────────────────────────────────────┐
│              Offline Network (Bluetooth/Wi-Fi Direct)        │
│                                                               │
│  ┌───────────┐      ┌───────────┐      ┌───────────┐       │
│  │  Rescuee  │◄────►│  Rescuer  │◄────►│  Rescuee  │       │
│  │  Device   │      │  Device   │      │  Device   │       │
│  └───────────┘      └───────────┘      └───────────┘       │
│       ▲                   ▲                   ▲             │
│       │                   │                   │             │
│       └───────────────────┴───────────────────┘             │
│              Mesh Network with Relay                        │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

- **`client/`**: Desktop application for end users (both Rescuees and Rescuers)
  - Flask-based web interface
  - Offline message handling
  - Bluetooth/Wi-Fi Direct communication

- **`cloud/`**: Cloud server component
  - REST API endpoints
  - Message persistence and synchronization
  - Emergency queue management

- **`offline/`**: Offline networking module
  - Bluetooth communication protocols
  - Message relay logic
  - Device discovery and network management

- **`common/`**: Shared models and services
  - Data models (User, Emergency, EncryptedEmergency)
  - Cryptographic services
  - Emergency queue management

---

## 🛠️ Technology Stack

### Backend
- **Python 3.x**: Core programming language
- **Flask**: Web framework for both client and cloud components
- **Gunicorn**: Production WSGI server
- **SQLite/PostgreSQL**: Database systems

### Frontend
- **Jinja2**: Template engine
- **Bootstrap 5**: CSS framework
- **Vanilla JavaScript**: Client-side interactivity

### Communication
- **Bluetooth**: Short-range device-to-device communication
- **Wi-Fi Direct**: Extended range peer-to-peer networking
- **REST API**: Cloud synchronization interface

### Security
- **Cryptography Library**: Message encryption
- **HTTPS**: Secure cloud communications

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Git/GitHub**: Version control and collaboration

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for cloud deployment)
- Windows OS (proof-of-concept platform)
- Bluetooth and Wi-Fi Direct capable hardware

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KronosPNG/RescueCom.git
   cd RescueCom
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r cloud/requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in cloud/ directory
   cp cloud/.env.example cloud/.env
   # Edit .env with your configuration
   ```

### Running the Application

#### Start Cloud Server (Docker)
```bash
docker-compose up -d
```

#### Start Client Application
```bash
# On Windows
./start-client.sh

# Or manually
python -m client
```

#### Start Cloud Server (Development)
```bash
./start-cloud.sh

# Or manually
python -m cloud
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test suites
python -m pytest tests/tests_cloud/
python -m pytest tests/tests_common/
python -m pytest tests/tests_offline/
```

---

## 📊 Project Management

This project was managed following professional software project management practices:

### Documentation Deliverables
- [Business Case](management_deliverables/business_case.md)
- [Project Charter](management_deliverables/project_charter.md)
- [Project Scope Statement](management_deliverables/project_scope.md)
- [Work Breakdown Structure](management_deliverables/work_breakdown_structure.md)
- [Team Contract](management_deliverables/team_contract.md)
- [Risk Management Plan](management_deliverables/risk_management.md)
- [Financial Analysis](management_deliverables/financial_analysis.md)
- [Stakeholder Register](management_deliverables/stakeholder_register.md)

### Project Metrics
- **Duration**: 3.5 months (October 2025 - January 2026)
- **Team Size**: 8 members (1 PM + 7 developers)
- **Budget**: €165,000 initial investment
- **NPV (3 years)**: €118,480.67
- **Platform**: Windows (proof-of-concept)

### Development Process
- **Version Control**: GitHub with branching strategy (main, frontend, backend, feature branches)
- **Code Review**: Mandatory peer review (PM or 3+ peers) before merging to main
- **Communication**: Weekly meetings, Discord, email
- **Decision Making**: Unanimous resolution with PM final authority

---

## 👥 Team

### Project Manager
- **Luigi Turco** ([@KronosPNG](https://github.com/KronosPNG)) - *Project Manager & Course Lead*
  - Responsible for planning, coordination, deadline management, and critical decision-making

### Development Leaders
- ([@utox39](https://github.com/utox39)) - *Backend Lead*

- ([@mirkotermy](https://github.com/mirkotermy)) - *Frontend Lead*

### Development Team
- ([@vympel7](https://github.com/vympel7)) - *Developer*
- ([@toyo54](https://github.com/toyo54)) - *Developer*
- ([@cavv-dev](https://github.com/cavv-dev)) - *Developer*
- ([@MarcoDonatiello04](https://github.com/MarcoDonatiello04)) - *Developer*
- ([@francy310804](https://github.com/francy310804)) - *Developer*

*All team members actively contributed to development, testing, and documentation according to weekly assignments.*

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow Conventional Commits**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for testing
   - See [style guide](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)

3. **Make your changes** and test thoroughly

4. **Push your branch**
   ```bash
   git push -u origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md) and [CONTRIBUTING_FRONTEND.MD](CONTRIBUTING_FRONTEND.MD).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Academic Context

This project was developed as part of a Master's course in Software Project Management, demonstrating:
- ✅ Complete project lifecycle management
- ✅ Team leadership and coordination
- ✅ Stakeholder management
- ✅ Risk assessment and mitigation
- ✅ Budget planning and financial analysis
- ✅ Agile development practices
- ✅ Technical documentation
- ✅ Proof-of-concept delivery

---

## 🙏 Acknowledgments

- **Professors** Fabio Palomba and Filomena Ferrucci for guidance and support
- **Team Members** for their dedication and hard work
- **Open Source Community** for the tools and libraries used

---

## 📞 Contact

**Luigi Turco** - Project Manager
- GitHub: [@KronosPNG](https://github.com/KronosPNG)

---

<div align="center">
Made with ❤️ by the RescueCom Team
</div>
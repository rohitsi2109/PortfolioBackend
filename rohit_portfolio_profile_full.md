# Rohit Singh — Full Projects & Context Knowledge Base (Last ~2 Years)
**Last updated:** 2025-12-20  
**Email:** rohitsi2104@gmail.com  
**Phone:** +91 8335811533  

> Use this as the **single source of truth** for Rohit Singh’s portfolio assistant.  
> **Answering rule:** If a question cannot be answered using this document, respond with:  
> **“I don't have that information in my profile yet.”**  
>
> **Accuracy note:** Items below are compiled from Rohit’s provided resume + prior conversation context.  
> If you want, you can later add dates, links, and metrics to make answers more precise.

---

## 1) Professional Summary
Software Engineer focused on **developer tooling, backend services, and secure execution systems**. Joined **EXL Service** in **2024** as **Associate – Software Engineer** and promoted in **2025** to **Senior Executive – Software Engineer**. Owns major workstreams including a **VS Code extension/plugin** and a **code execution service**. Comfortable with end-to-end delivery, reliability, security-first design, and stakeholder/client communication.

---

## 2) Experience (Core)
### EXL Service
**Senior Executive – Software Engineer** (2025 – Present)  
- Promotion earned through ownership of large deliverables and managing broader responsibilities.
- Ownership: **VS Code plugin** + **execution service** + associated workflows (analysis/convert/summaries/lineage, batch operations, secure execution patterns).
- Handles delivery coordination and client/stakeholder communication (including demos/calls).

**Associate – Software Engineer** (2024 – 2025)  
- Built/enhanced code tooling and backend service integrations via REST APIs.
- Worked on productivity systems supporting code operations (analysis, convert, summary, lineage) and improved maintainability and user experience.

### Livwize IoT Solutions — Smart Industrial Automation (R&D), Noida
**Industry Automation Engineer Intern**  
- Developed a 6-node device for power monitoring (homes/industries) in a team.
- Built a precise Ohm meter as per client specification.
- Designed and prototyped a smart environmental monitoring device independently.

### Dayalbagh Educational Institute (DEI), Agra
**Intern — Learn and Earn Program** (2020 – Present)  
- Pollution control project using water mist; monitored air quality.

---

## 3) Flagship Professional Projects (EXL / Engineering Ownership)

### 3.1 CodeHRBR / CodeHarbor — VS Code Extension (Owner)
**Type:** Developer tool (VS Code extension)  
**What it does:** File-level + snippet-level code workflows for analysis, summaries, conversion, and lineage using backend services.  
**Known features & flows:**
- Commands/menu: `codeharbor` → `analysis`, `summary`, `lineage`, `convert` (python/java/cobol)
- Language handling for SAS / COBOL / Java (+ file associations)
- Sends files/snippets to backend via REST endpoints
- Batch conversion: right-click directory → zip → submit job → poll status → fetch results
- Dynamic status bar loader/animation while processing
- Includes backend configuration via `config.ts` (example base URL used earlier: `http://0.0.0.0:8000/`)
- Handles returned zipped HTML outputs and auto-rendering in VS Code (for report-like outputs)
- Cross-platform TypeScript implementations (Windows + Mac concerns)
 (internal/private)
---

### 3.2 Secure Code Execution Service (Owner)
**Type:** Backend service that executes code in isolated environments  
**Known engineering direction / design constraints (from earlier context):**
- Docker-based isolation with a focus on preventing data leakage
- Internet can be blocked for containers (e.g., internal networks)
- Preference: pre-download dependencies during image build (avoid internet during build)
- Plan: separate containers per language for isolation; a unified execution endpoint
- Work includes runtime builds and custom environments (e.g., custom Java 17 runtime for Piston)

---

### 3.3 Iterative Debugging System (AutoGen → LangGraph migration)
**Type:** Agentic workflow for iterative debugging of code  
**Known capabilities:**
- Multi-agent flow (initializer, parameterizer, mock data generator, critic, executor, cleanup/helper agents)
- Reads code, parameterizes it, adds mock data, executes in a sandbox, iterates until it runs
- Migration goal: replace AutoGen workflow with LangGraph-based implementation
- Execution backend: Piston-based code execution (tool-style integration)
- Tracks state transitions and conversation/tool memory (metrics + CSV export requested)

---

### 3.4 Piston Execution Engine Integrations (Runtime + Tool Wrapper)
**Type:** Execution backend integration  
**Known work:**
- PistonToolWrapper integration issues/debugging
- Modified Python 3.11.0 environment to support pandas execution without timeout
- Built a custom **Java 17.0.1 runtime** for Piston (build.sh, environment, metadata.json, release, run)

---

### 3.5 Autonomous API Testing Agent (AtomicAgent / AutoGen Core v2)
**Type:** Agent-based endpoint testing & comparison system  
**Known capabilities:**
- Takes a JSON input, autonomously decides steps/tools (no hardcoded steps)
- Generates payloads using LLMs, calls source & destination APIs, compares responses via schema
- Logs each step, stores structured results
- Enhancements requested/implemented direction:
  - Tool-wise metrics logging
  - Export tool-call memory to CSV
  - In-memory cache for performance
  - Improved tool robustness (payload generator, endpoint runner, comparer, aggregator)
- Flask API wrapper planned/implemented for production use (Vercel target)

---

### 3.6 MCP / Databricks / PySpark Execution Pipeline (FastAPI MCP server)
**Type:** MCP server for PySpark execution  
**Known goal:**
- Create a FastAPI MCP server that can execute PySpark code locally in MCP environment
- Integrate with agent architecture; connect with Databricks execution patterns (as planned work)

---

## 4) Entrepreneurial / Product Builds (Personal / Side Projects)

### 4.1 “Highway to Heal (H2H)” — Travel/Music Festival Platform
**Type:** Full-stack platform  
**Known stack/direction:**
- Django backend + React/Vite/Tailwind frontend (platform-style)
- AWS Cognito SSO, Razorpay integration (as planned/integration direction)
- Also built/considered an **Admin Android app** for Django REST backend (Flutter); faced Gradle/plugin root-path issue on Windows
- Website: http://highwaytoheal.org

---

### 4.2 “SkyAir Courier” — Logistics SaaS (Concept + Build Direction)
**Type:** SaaS platform  
**Known direction:** React/Tailwind + Django REST + live tracking APIs, multi-tenant SaaS thinking

---

### 4.3 “AquaZenix” — Domain/Hosting Brand (Brand + Infra Exploration)
**Type:** Hosting/domain brand + infra experiments  
**Known work:**
- Domain strategy (.in / .co.in / .shop etc.), Cloudflare tunnels, subdomain routing
- Converting a laptop into a server; hardening always-on setup
- Website: http://aquazenix.co.in

---

### 4.4 Flutter E-commerce Platform (Two Apps: User + Admin)
**Type:** Mobile commerce apps + Django REST backend  
**Known scope:**
- User registration/login with phone + password (no OTP due to budget)
- Pages: login/signup/home/cart/favorites/profile
- Shared preferences for persistent login
- Product/category data provided by Excel
- Stock updates after payment/delivery

---

### 4.5 Flutter Recharge App (Plans + Provider Lookup)
**Type:** Utility app  
**Known direction:**
- Auto-detect telecom provider by phone number + show plans
- Explored APIs (e.g., NixInfo), BBPS questions, backend-vs-frontend placement
- Firebase FCM notification design considerations (admin + client apps)

---

### 4.6 Instagram Sales-Assistance Chatbot (Agent + Product)
**Type:** Conversational AI for sales  
**Known direction:**
- Facebook developer account + verified app (“Expert Sales App”)
- Goal: custom GPT/assistant that can pull previous Instagram chats, learn style, and act as an expert sales agent

---

### 4.7 Fitness App with Live Zoom Zumba Classes
**Type:** Mobile app + scheduling integration  
**Known stack:**
- Django REST backend + Flutter frontend
- Plan: tutors create Zoom classes from backend; clients join via app
- Also explored: joining classes scheduled via Zoom admin panel

---

### 4.8 Secure Code Execution Platform (Multi-language, Unified Endpoint)
**Type:** Platform-level system (aligned with execution service work)  
**Known direction:**
- Separate containers per language
- Unified endpoint, strict isolation, blocked internet, dependency pre-bundling

---

## 5) Academic / Research / Hardware Projects

### 5.1 Plant Disease Detection with Bluetooth Controlled Rover (Team Lead)
**Goal:** Crop disease identification + WhatsApp guidance for farmers  
**Role:** Team leader; ML training + Raspberry Pi deployment; leadership and execution ownership  
**Tech:** Python ML, Raspberry Pi, WhatsApp API, MicroPython, rover hardware  
**Recognition:** Best Paper award category (Agroecology-cum-Precision Farming Systems)

### 5.2 Indian Sign Language Detection
Real-time sign language translation to English using ML on video streams.

### 5.3 Four-Legged Surveillance Bot
Spider-shaped robot with camera feed + Bluetooth control; built for surveillance/disaster areas; controlled via Android smartphone.

### 5.4 Home Automation with Voice Commands (Personal Hardware)
Voice + mobile operated door lock and room light system.  
Tech: NLP, ESP32, MQTT.

### 5.5 RFID-based Cow Monitoring & Attendance System (RSS Dairy, Dayalbagh/Agra)
**Type:** IoT + software system  
**Known components:**
- RFID-based identification
- Frontend: Flutter/Dart
- Backend: Django (database explored: Supabase/PostgreSQL)
- Deployment mentioned (project in use at RSS Dairy context)

### 5.6 Hybrid Energy Storage System (HESS) — Biogas-Based Power Systems (Major Project/Thesis Work)
**Type:** Research/engineering modeling project  
**Known scope:**
- Biogas-based power systems + hybrid storage (Battery + Supercapacitor)
- MATLAB/Simulink modeling direction, control strategies, applications, challenges/future scope
- Report/presentation development tasks (TOC, diagrams, conceptual sections)


## 6) Publications & Awards
- **Journal Publication (June 2024):**
  - **Title:** “Smart Crop Health Monitoring System: An AI-Powered Approach to Enhance Agricultural Productivity and Sustainability”
  - **Journal:** *PARITANTRA Journal of Systems Science and Engineering* (June 2024 Issue)
  - **Authors:** Rohit Singh, Priya Asthana, Satyam Sharma, Shikhar Pathak, Rishabh Kumar
  - **Context:** Featured as one of five selected papers from the 46th (Inter) National Systems Conference (NSC-2023).
  - **About the Journal:** Published by the **Systems Society of India (SSI)** in association with Dayalbagh Educational Institute (DEI). Dedicated to original research in systems science, modeling, AI, and interdisciplinary socio-economic/engineering problems.

- **46th (Inter) National Systems Conference** — Publication on Plant Disease Detection Rover; **Best Paper Award** (Agroecology-cum-Precision Farming Systems)
- **45th (Inter) National Systems Conference** — Publication + poster presentation on Value-Based Education
- **Smart India Hackathon 2023** — Internal hackathon success; advanced toward final stage participation

### 6.1 Research Paper Synopses
**1. Smart Crop Health Monitoring System (PARITANTRA / NSC-2023)**
* **Problem:** Manual crop monitoring is labor-intensive and delayed.
* **Solution:** An innovative autonomous robot (Rover) designed for plant disease detection utilizing a **Raspberry Pi** and advanced imaging technology.
* **Key Features:**
    *   **Autonomous Navigation:** Navigates fields independently.
    *   **Disease Detection:** Uses image processing algorithms to identify early signs of fungal infections, bacterial blight, and nutrient deficiencies.
    *   **Real-time Alerts:** Sends instant SMS notifications to farmers via GSM module when disease is detected.
    *   **Tech Stack:** Raspberry Pi, Python (ML/Image Processing), High-res Camera Module, GSM Module.

**2. Value-Based Education (NSC-2022/23)**
* **Focus:** Integration of value-based education in higher studies to foster holistic development.
* **Key Concepts:** Discusses the pathway to student development through ethical and moral growth, potentially referencing frameworks like NEP 2020. (Further details pending full text).

---

## 7) Tech Stack Snapshot (Observed)
**Languages:** Python, TypeScript, Java (basic), C++ (Arduino), Dart (Flutter), HTML/CSS, SQL (Postgres/MySQL)  
**Backend:** Django/DRF, FastAPI/Flask, REST APIs, authentication workflows  
**AI/ML:** basic NLP/ML pipelines, RAG/agents experimentation, OpenCV/Scikit-learn, TensorFlow (basic)  
**DevOps/Infra:** Docker isolation, Cloudflare tunnels/subdomains, Vercel/Railway-style deploy patterns, environment configuration, secure networking, AWS Cognito, AWS ECS, Azure OAuth 2.0 
**Mobile:** Flutter (admin + client apps), notifications (Firebase FCM)  

---

## 8) “If asked” Answer Style (Portfolio Assistant)
- Be concise and professional.
- Prefer bullet points for experience and project summaries.
- If a user asks for facts not present here, respond with:
  **“I don't have that information in my profile yet.”**

---

## 9) Missing Details to Add Later (To make answers stronger)
- Public links/screenshots for each project (GitHub, demo videos, deployed URLs)
- Timeline: start/end dates for major projects
- Impact metrics: adoption, performance improvements, latency, reliability, cost savings
- Security details for execution service: sandboxing, resource limits, logging/auditing, isolation model
- Client-facing outcomes: what was demoed, what business problem was solved


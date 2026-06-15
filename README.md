IoT Smart Agriculture Monitoring System


A complete Industry-Oriented Internet of Things (IoT) project that monitors environmental conditions, automates irrigation decisions, generates alerts, stores historical data, and visualizes everything through a real-time dashboard.


This project simulates a smart agriculture environment using ESP32 and Wokwi, communicates using MQTT, processes data through a Python backend, and visualizes insights through a Streamlit dashboard.


⸻


Project Overview


Modern agriculture relies heavily on data-driven decisions. Farmers need to know:


* Is the soil dry?
* Is the temperature too high?
* Is there enough water in the tank?
* Should irrigation be started?
* Are environmental conditions healthy for crops?


This project continuously monitors agricultural conditions and automatically decides whether irrigation should be activated.


The system provides:


* Real-time environmental monitoring
* Automated irrigation decision logic
* Alert generation
* Historical data storage
* Trend analysis
* Interactive dashboard visualization


⸻


Problem Statement


Traditional farming often depends on manual observation.


This creates problems such as:


* Delayed irrigation
* Water wastage
* Crop stress due to high temperatures
* Poor visibility into field conditions
* Lack of historical data


This project solves these problems by continuously monitoring the environment and providing automated insights.


⸻


Features


Environmental Monitoring


Monitors:


* Temperature
* Humidity
* Soil Moisture
* Water Tank Level
* Light Intensity


⸻


Smart Irrigation Logic


Automatically determines:


IF Soil Moisture < 30%
AND
Water Level > 20%
THEN
Pump ON


Otherwise:


Pump OFF


⸻


Alert System


Generates alerts for:


* Low Soil Moisture
* High Temperature
* Low Water Level


⸻


Real-Time Dashboard


Displays:


* Live sensor readings
* Active alerts
* System health
* Historical trends
* Pump activity
* Analytics


⸻


Historical Data Storage


Stores:


* Sensor data
* Alerts
* Pump events
* Daily summaries


⸻


System Architecture


DHT22
LDR Sensor
Soil Moisture Sensor (Simulated)
Water Level Sensor (Simulated)
          │
          ▼
      ESP32
          │
          ▼
 MQTT Publisher
          │
          ▼
 MQTT Broker
 (HiveMQ)
          │
          ▼
 Python Backend
          │
 ┌────────┼────────┐
 │        │        │
 ▼        ▼        ▼
Alerts  Logging Analytics
 │        │        │
 └────────┼────────┘
          ▼
      CSV Storage
          │
          ▼
 Streamlit Dashboard
          │
          ▼
 Real-Time Monitoring


⸻


Data Flow


The complete workflow is:


Sensor Reading
      ↓
ESP32 Processes Data
      ↓
Threshold Comparison
      ↓
Pump Decision Logic
      ↓
MQTT Publish
      ↓
Python MQTT Subscriber
      ↓
Data Validation
      ↓
CSV Storage
      ↓
Alert Generation
      ↓
Analytics Processing
      ↓
Dashboard Update


⸻


Technologies Used


Hardware (Simulated)


* ESP32
* DHT22
* LDR Module
* Relay Module
* Potentiometer (Soil Moisture Simulation)
* Potentiometer (Water Level Simulation)


⸻


Simulation


* Wokwi


⸻


Embedded Development


* PlatformIO
* Arduino Framework


⸻


Communication


* MQTT
* HiveMQ Public Broker


⸻


Backend


* Python


Libraries:


* paho-mqtt
* pandas
* numpy


⸻


Dashboard


* Streamlit
* Plotly


⸻


Why Potentiometers Were Used


Wokwi currently does not provide official Soil Moisture and Water Level sensors.


To simulate these sensors:


Agricultural Parameter	Simulated Using
Soil Moisture	Potentiometer
Water Level	Potentiometer


This works because both sensors produce analog values in real-world systems.


The ESP32 reads them exactly like actual sensors.


⸻


Project Structure


IoT-Smart-Agriculture-Monitoring-System/
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   ├── charts.py
│   └── metrics.py
│
├── mqtt_backend/
│   ├── subscriber.py
│   ├── alerts.py
│   ├── analytics.py
│   ├── logger.py
│   └── system_health.py
│
├── data/
│   ├── sensor_data.csv
│   ├── alerts.csv
│   ├── pump_history.csv
│   └── daily_summary.csv
│
├── outputs/
│   ├── system_log.txt
│   ├── alert_log.txt
│   └── analytics_report.txt
│
├── smart-agriculture-monitoring/
│   ├── src/
│   │   └── main.cpp
│   │
│   ├── include/
│   │   └── config.h
│   │
│   ├── platformio.ini
│   ├── diagram.json
│   └── wokwi.toml
│
├── images/
│
├── docs/
│
├── requirements.txt
│
└── README.md


⸻


Sensor Mapping


Sensor	ESP32 Pin
DHT22	GPIO4
Soil Moisture	GPIO34
Water Level	GPIO32
LDR Module	GPIO35
Relay	GPIO26


⸻


Pump Decision Logic


The irrigation system follows:


Soil Moisture < 30%
        ↓
Check Water Level
        ↓
Water Level > 20%
        ↓
Pump ON


Otherwise:


Pump OFF


This prevents running the pump when the water tank is empty.


⸻


Installation Guide


This section is written for complete beginners.


No prior experience is required.


⸻


Step 1: Install Visual Studio Code


Download:


https://code.visualstudio.com


Install using the default settings.


⸻


Step 2: Install PlatformIO


Open VS Code.


Go to:


Extensions


Search:


PlatformIO IDE


Install it.


⸻


Step 3: Install Python


Check if Python is already installed.


Windows


Open Command Prompt:


python --version


⸻


macOS


Open Terminal:


python3 --version


⸻


Linux


Open Terminal:


python3 --version


⸻


If Python is missing:


Download from:


https://www.python.org/downloads


⸻


Step 4: Clone Repository


Windows


git clone <repository-url>
cd IoT-Smart-Agriculture-Monitoring-System


⸻


macOS


git clone <repository-url>
cd IoT-Smart-Agriculture-Monitoring-System


⸻


Linux


git clone <repository-url>
cd IoT-Smart-Agriculture-Monitoring-System


⸻


Step 5: Create Virtual Environment


Windows


python -m venv venv
venv\Scripts\activate


⸻


macOS


python3 -m venv venv
source venv/bin/activate


⸻


Linux


python3 -m venv venv
source venv/bin/activate


⸻


Step 6: Install Python Dependencies


pip install -r requirements.txt


⸻


Step 7: Start MQTT Backend


Navigate to:


mqtt_backend


Run:


Windows


python subscriber.py


⸻


macOS


python3 subscriber.py


⸻


Linux


python3 subscriber.py


⸻


Expected:


MQTT Connected
Receiving Sensor Data...


⸻


Step 8: Run Dashboard


Open a new terminal.


Run:


streamlit run dashboard/app.py


Browser opens automatically.


If not:


Visit:


http://localhost:8501


⸻


Step 9: Start Wokwi Simulation


Open:


smart-agriculture-monitoring


Start:


Wokwi Simulator


The ESP32 begins sending data automatically.


⸻


Testing Scenarios


Scenario 1


Normal Conditions


Expected:


Pump OFF
No Alerts


⸻


Scenario 2


Dry Soil


Set:


Soil Moisture < 30


Expected:


Pump ON
Low Soil Moisture Alert


⸻


Scenario 3


Low Water Tank


Set:


Water Level < 20


Expected:


Pump OFF
Low Water Level Alert


⸻


Scenario 4


High Temperature


Set DHT22 Temperature:


> 35°C


Expected:


High Temperature Alert


⸻


Dashboard Pages


Main Dashboard


Displays:


* Live Metrics
* Alerts
* System Health
* Sensor Trends


⸻


Alerts Page


Displays:


* Active Alerts
* Alert History


⸻


Analytics Page


Displays:


* Average Temperature
* Average Humidity
* Average Soil Moisture
* Average Water Level
* Pump Statistics


⸻


Pump History


Displays:


* Pump ON Events
* Pump OFF Events


⸻


System Health


Displays:


* MQTT Status
* Backend Status
* CSV Storage Status
* Last MQTT Message


⸻


Screenshots


Add screenshots to:


images/


Recommended screenshots:


wokwi_circuit.png
sensor_readings.png
dashboard_home.png
alerts_page.png
analytics_page.png
pump_history.png
system_health.png


⸻


Future Improvements


Possible future enhancements:


* Mobile App Integration
* SMS Alerts
* Email Notifications
* Weather API Integration
* Machine Learning Predictions
* Crop Recommendation System
* Cloud Database
* Multi-Farm Monitoring
* LoRaWAN Communication
* Solar Power Monitoring


⸻


Learning Outcomes


This project demonstrates:


* Internet of Things (IoT)
* Embedded Systems
* ESP32 Programming
* MQTT Communication
* Sensor Integration
* Automation Logic
* Data Logging
* Python Backend Development
* Streamlit Dashboard Development
* Real-Time Monitoring Systems


⸻


Author


Aniket Satpathy


Industry-Oriented IoT Project


Smart Agriculture Monitoring Platform


Built using ESP32, Wokwi, MQTT, Python, and Streamlit.

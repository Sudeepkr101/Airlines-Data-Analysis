# Airlines Data Analysis for Profit Maximization

An interactive data analysis dashboard built with **Streamlit** to explore airline database metrics and propose data-driven strategies for profit maximization.

Developed by: **Sudeep**  
GitHub Repository: [Sudeepkr101/Airlines-Data-Analysis](https://github.com/Sudeepkr101/Airlines-Data-Analysis.git)

---

## 📌 Project Overview

The airline industry faces significant pressure due to:
1. **Stricter environmental regulations** which raise operating costs and restrict expansion.
2. **Higher flight taxes** which increase the overall cost of flying and subsequently reduce demand.
3. **Tight labor market** leading to increased labor costs and higher turnover rates.

This application connects to an SQLite database (`travel.sqlite`) to analyze key operational metrics and simulate financial strategies (like boosting the load factor by 10%) to optimize and maximize total annual turnover.

---

## 🛠️ Key Features & Analyses

The dashboard is organized into several modules:
- **Problem Statement**: Overview of the current challenges in the aviation industry.
- **Model Ranges**: Explores the relation between airplane models and their maximum travel ranges. Highlights aircraft with more than 120 seats (e.g., Boeing 777-300).
- **Revenue Earned**: Time-series visualization of ticket sales and total amount earned over time.
- **Flight Prices**: Explores fare distributions and average prices across Cabin classes (Economy, Comfort, Business) for different aircraft.
- **Booked Seats and Occupancy Rate**: Details the correlation between the number of booked seats and the overall occupancy rate of flights.
- **Profit Maximization**: Calculates and plots the potential increase in annual turnover if aircraft occupancy rates are increased by 10%.
- **Audio Narratives**: Includes a Google Text-to-Speech (gTTS) narrator to read out analytical conclusions directly from the UI.

---

## 🚀 Getting Started

### 📋 Prerequisites

Make sure you have Python (version 3.10 or higher) installed.

### ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Sudeepkr101/Airlines-Data-Analysis.git
   cd Airlines-Data-Analysis
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run Airlines_analysis.py
   ```

4. **Access the App:**
   Open your browser and navigate to `http://localhost:8501`.

---

## 🐳 Docker Deployment

You can also run the application inside a container:

1. **Build the Docker Image:**
   ```bash
   docker build -t airlines-data-analysis .
   ```

2. **Run the Container:**
   ```bash
   docker run -p 8501:8501 airlines-data-analysis
   ```

---

## 🗄️ Database Schema

The analysis uses an SQLite database `travel.sqlite` composed of the following tables:
- **`aircrafts_data`**: Aircraft code, model names, and travel range.
- **`airports_data`**: Airport code, airport name, and city.
- **`seats`**: Aircraft seat layout configurations.
- **`bookings`**: Booking reference, booking dates, and total booking amount.
- **`tickets`**: Ticket numbers associated with booking references.
- **`flights`**: Scheduled flight details and aircraft codes.
- **`boarding_passes`**: Boarding passes associated with tickets and flights.
- **`ticket_flights`**: Ticket flight fares, amounts, and cabin classes.

---

## 📊 Technologies Used

- **UI / Dashboard**: Streamlit
- **Database**: SQLite3
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn, Plotly
- **Narrations**: gTTS (Google Text-to-Speech)
- **Deployment**: Docker

---

## 👤 Author

- **Sudeep**
- GitHub: [@Sudeepkr101](https://github.com/Sudeepkr101)

# CourierBot AI - Courier & Inventory Management Chatbot

A professional AI-powered chatbot specialized in Courier Services and Inventory Management for Pakistan and worldwide logistics.

## Features

- Multi-model AI support (25+ free models via OpenRouter)
- Real-time model switching with Auto mode
- Chat history with search, rename, and delete
- Dark/Light theme toggle
- PDF export of conversations
- Voice input support
- Image/file attachment
- Usage statistics
- PostgreSQL database for conversation storage

## Tech Stack

- **Frontend:** React.js
- **Backend:** Django REST Framework
- **Database:** PostgreSQL
- **AI Models:** OpenRouter API (Free models)

## AI Models Available

- Google: Gemma 4 31B
- Meta: Llama 3.3 70B
- NVIDIA: Nemotron series
- Cohere: North Mini
- LiquidAI: LFM2.5
- And 20+ more free models

## Domain Knowledge

- Pakistan Couriers: TCS, Leopards, PostEx, BlueEx, M&P, Trax
- International: DHL, FedEx, UPS
- Inventory: FIFO, LIFO, EOQ, ABC Analysis, Safety Stock
- COD (Cash on Delivery) operations
- Warehouse management

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in backend folder:
```
OPENROUTER_API_KEY=your_api_key_here
DB_NAME=courier_chatbot_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

```bash
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Access
Open browser: `http://localhost:3000`

## How to Run

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Screenshots

CourierBot AI provides intelligent responses about:
- Parcel tracking and courier rates
- COD service operations
- Inventory stock management
- EOQ calculations
- Warehouse operations

## Developer

- **GitHub:** javariaazeemkhan478-crypto
- **Project:** Courier & Inventory Management AI Chatbot
- **Stack:** React + Django + PostgreSQL + OpenRouter


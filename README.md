# Vehicle Rental Manager

Vehicle management system prototype for Car Go – brought to you by SmartMotion.

## Project Structure

```

vehicle-rental-manager/
├── backend/   # Flask backend API
└── frontend/  # Vue 3 frontend dashboard

```

---

## How to Run

### Running the Backend

#### Prerequisites

- **Python 3.10+**
- **pip** for Python dependencies

#### Steps

1. Open a terminal and navigate to the backend folder:

```bash
cd vehicle-rental-manager/backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Flask server:

```bash
flask run
```

**Important:** Keep this terminal running so the frontend can connect to the backend.

---

### Running the Frontend

#### Prerequisites

- **Node.js**
- **npm** (comes with Node.js)

#### Steps

1. Open another terminal and navigate to the frontend folder:

```bash
cd vehicle-rental-manager/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

**Reminder:** The backend must also be running in another terminal.

---

## Access the App

Once both backend and frontend are running, open your browser at:

```
http://localhost:5173
```

- Backend API endpoints are documented in `backend/README.md`.
- Frontend instructions are documented in `frontend/README.md`.

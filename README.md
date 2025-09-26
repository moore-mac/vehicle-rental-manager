# Vehicle Rental Manager

Vehicle mangement system prototype for Car Go - brought to you by SmartMotion.

## Project Structure

```
vehicle-rental-manager/
├── backend/   # Flask backend API
└── frontend/  # Vue 3 frontend dashboard
```

## How to Run

### Running the Backend

#### Prerequisites

Make sure you have:

- **Python 3.10+**
- **pip** for Python dependencies

---

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

- Ensure the backend is running before starting the frontend so the Vue app can fetch data.

### Running the Frontend

#### Prerequisites

Make sure you have:

- **Node.js**
- **npm** (comes with Node.js)

---

1. Open a terminal and navigate to the frontend folder:

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

- Ensure the backend is running in another terminal as well, so the frontend can fetch data (refer to backend README.md).

---

## Access the App

- Open your browser and go to:

```
http://localhost:5173
```

> Make sure both backend and frontend are running simultaneously for full functionality.

---

## Accessing the App

- Open your browser and go to the frontend URL (see `frontend/README.md`)
- Backend API endpoints are documented in `backend/README.md`

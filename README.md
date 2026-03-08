# LifeDrops - Blood Donation Camp App

A full-stack, responsive web application for managing blood donation camps, featuring user registration, authentication, and personalized dashboards.

## Technologies Used
- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML5, CSS3 (Modern Flexbox/Grid)
- **Styling:** Custom Vanilla CSS with a clean white and deep red aesthetic.

## Setup Instructions

1. **Install Dependencies**
   Ensure you have Python installed. Then configure your virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**
   Run the initialization script to create the SQLite schema and seed it with dummy users and upcoming camps:
   ```bash
   python init_db.py
   ```
   **Seed User Accounts for Testing:**
   - john@example.com / password123
   - jane@example.com / password123
   - alice@example.com / password123

3. **Run the Application**
   Start the Flask development server:
   ```bash
   python app.py
   ```
   The application will be accessible at `http://localhost:5000` or `http://127.0.0.1:5000`.

## Running the Project

### Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.6+
- pip
- Git
- Docker (optional but recommended)

### Setting Up the Environment

1. Clone the repository:
   ```
   git clone https://github.com/vkmechit/social_network_app.git
   cd aknx_social_network_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuring the Database

1. Set up your database credentials in the `.env` file:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=true
   DB_ENGINE=django.db.backends.sqlite3
   ALLOWED_HOSTS=*  # For local development only
   ```

2. Create the database tables:
   ```bash
   python manage.py migrate
   ```

### Running the Development Server

To run the development server:

```bash
python manage.py runserver
```

Your application will now be accessible at `http://localhost:8000`.


### Deploying

For deployment, we recommend using Docker. To build and run the Docker container:

```bash
docker-compose up --build
```

This will create and start the necessary services.

### API Endpoints

The project provides several API endpoints:
# For detailed API structure please refer to the postman collection file named ```Accuknox.postman_collection.json```
# Please refer to https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/ to import the collection

1. Send a friend request:
   ```
   POST http://127.0.0.1:8000/api/social/send-request/
   ```

2. Update friend request status:
   ```
   POST http://127.0.0.1:8000/api/social/update-request-status/<int:pk>/
   ```

3. Get friend list:
   ```
   GET http://127.0.0.1:8000/api/social/get-friend-list/
   ```

4. Get pending friend requests:
   ```
   GET http://127.0.0.1:8000/api/social/get-pending-friend-requests/
   ```

### Additional Notes

- Make sure to configure your firewall to allow connections to the specified ports.
- For production environments, consider setting up HTTPS and configuring proper security measures.
- Regularly backup your database to prevent data loss.
```


Certainly! I'll provide you with detailed information about each API endpoint, including sample calls. Here's how you can structure this information in your README.md file:

```

# API Connection Fix

This document explains the issues that were causing the API connection problems between the frontend and backend, and how they were fixed.

## Issues Identified

1. **Missing Vite Proxy Configuration**: The frontend was not properly configured to proxy API requests to the backend during development.
2. **Database Configuration**: The backend was configured to use PostgreSQL, but SQLite was required.
3. **API URL Mismatch**: There was a potential mismatch between the API URL formats used by the frontend and backend.

## Fixes Applied

### 1. Vite Proxy Configuration

The Vite development server needs to be configured to proxy API requests to the backend. This was fixed by uncommenting and updating the proxy configuration in `svelte@latest/vite.config.ts`:

```javascript
proxy: {
  '/api/v1': {
    target: 'http://localhost:5000',
    changeOrigin: true,
    secure: false,
    rewrite: (path) => path
  }
}
```

This configuration forwards all requests to `/api/v1/*` from the frontend to `http://localhost:5000/api/v1/*` on the backend.

### 2. Database Configuration

The backend was configured to use PostgreSQL, but SQLite is preferred for development. The `.env` file was updated to use SQLite:

```
# Using SQLite for development and testing
DEV_DATABASE_URL="sqlite:///instance/dev.sqlite"
TEST_DATABASE_URL="sqlite:///instance/test.sqlite"
```

### 3. Database Initialization

A script was created to initialize the SQLite database with the necessary tables and sample data:

```
python init_db.py
```

## Testing the Fix

Two test scripts were created to verify the API connection:

1. **API Connection Test**: Tests the basic connectivity between frontend and backend.
   ```
   python api_connection_test.py
   ```

2. **API Endpoint Test**: Tests all the API endpoints to ensure they're working correctly.
   ```
   python test_api_endpoints.py
   ```

## Steps to Apply the Fix

1. **Update Vite Configuration**:
   - The `vite.config.ts` file has been updated to enable the proxy configuration.
   - No action needed if you've already pulled the latest changes.

2. **Update Database Configuration**:
   - The `.env` file has been updated to use SQLite instead of PostgreSQL.
   - No action needed if you've already pulled the latest changes.

3. **Initialize the Database**:
   - Run the database initialization script:
     ```
     cd backend
     python init_db.py
     ```

4. **Start the Backend Server**:
   - Start the Flask backend server:
     ```
     cd backend
     python run.py
     ```

5. **Start the Frontend Development Server**:
   - Start the Svelte frontend development server:
     ```
     cd svelte@latest
     npm run dev
     ```

6. **Test the Connection**:
   - Run the API connection test script:
     ```
     python api_connection_test.py
     ```
   - Run the API endpoint test script:
     ```
     python test_api_endpoints.py
     ```

## Troubleshooting

If you still encounter issues after applying the fixes:

1. **Check Server Ports**:
   - Ensure the backend is running on port 5000
   - Ensure the frontend is running on port 5173

2. **Check CORS Configuration**:
   - The backend has CORS enabled for all origins during development
   - If you're still seeing CORS errors, check the browser console for details

3. **Check API URL Format**:
   - The frontend expects API endpoints at `/api/v1/*`
   - The backend serves API endpoints at `/api/v1/*`
   - Ensure all API calls in the frontend code use this format

4. **Database Issues**:
   - If you encounter database errors, try deleting the SQLite database file and running the initialization script again:
     ```
     rm backend/instance/dev.sqlite
     python backend/init_db.py
     ```

5. **Authentication Issues**:
   - If you're having trouble with authenticated endpoints, ensure you're properly storing and using the JWT token
   - Check that the token is being included in the Authorization header for API requests

## Additional Notes

- The frontend is configured to use a relative URL for the API (`/api/v1`), which is proxied to the backend during development.
- The backend is configured to use SQLite for development, which is a file-based database that doesn't require a separate database server.
- The test scripts provide detailed information about the API connection and endpoints, which can help identify any remaining issues.

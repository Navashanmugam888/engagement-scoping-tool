# FCCS Scoping Tool - Backend API Requirements

## Overview
The frontend sends scoping data to your backend, and your backend returns calculation results. The backend URL is configured in `.env` file.

## Environment Configuration

Add to `.env` file:
```
NEXT_PUBLIC_BACKEND_API_URL=http://your-backend-url:port
```

Example:
```
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:5000
NEXT_PUBLIC_BACKEND_API_URL=https://api.yourcompany.com
```

## Required Backend API Endpoints

### 1. Submit Scoping Data
**Endpoint:** `POST /api/scoping/submit`

**Request Body:**
```json
{
  "userEmail": "user@example.com",
  "userName": "John Doe",
  "scopingData": {
    "dim_1": { "value": "YES", "count": 5 },
    "dim_2": { "value": "NO", "count": null },
    "feature_1": { "value": "YES", "count": 3 },
    // ... all scoping form fields
  },
  "selectedRoles": [
    "PM USA", 
    "Architect USA", 
    "App Developer India"
  ],
  "comments": "Optional user comments about the project",
  "submittedAt": "2025-12-03T10:30:00.000Z"
}
```

**Response (Success):**
```json
{
  "success": true,
  "submissionId": 123,
  "id": 123,
  "message": "Submission received successfully",
  "status": "COMPLETED"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Error message here",
  "error": "Detailed error description"
}
```

---

### 2. Get Submission History
**Endpoint:** `GET /api/scoping/history?email={userEmail}`

**Query Parameters:**
- `email` (required): User's email address

**Response:**
```json
{
  "success": true,
  "submissions": [
    {
      "id": 123,
      "user_name": "John Doe",
      "user_email": "user@example.com",
      "submitted_at": "2025-12-03T10:30:00.000Z",
      "status": "COMPLETED",
      "calculation_result": {
        "weeks": 24,
        "complexity": "High",
        "cost": "$250,000"
      }
    },
    {
      "id": 122,
      "user_name": "John Doe", 
      "submitted_at": "2025-12-02T14:20:00.000Z",
      "status": "PENDING",
      "calculation_result": null
    }
  ]
}
```

**Status Values:**
- `PENDING` - Calculation in progress
- `COMPLETED` - Calculation finished, results available
- `FAILED` - Calculation failed

---

### 3. Get Submission Result
**Endpoint:** `GET /api/scoping/result/{id}`

**Path Parameters:**
- `id` (required): Submission ID

**Response:**
```json
{
  "success": true,
  "submission": {
    "id": 123,
    "user_name": "John Doe",
    "user_email": "user@example.com",
    "submitted_at": "2025-12-03T10:30:00.000Z",
    "calculated_at": "2025-12-03T10:35:00.000Z",
    "status": "COMPLETED",
    "comments": "User comments here",
    "scoping_data": {
      // Original form data submitted
    },
    "selected_roles": ["PM USA", "Architect USA"],
    "calculation_result": {
      "weeks": 24,
      "complexity": "High",
      "cost": "$250,000",
      "breakdown": {
        "development": 18,
        "testing": 4,
        "deployment": 2
      },
      "roleAllocation": {
        "PM USA": 0.5,
        "Architect USA": 1.0,
        "App Developer India": 3.0
      },
      "phases": [
        {
          "name": "Phase 1 - Setup",
          "duration": 4,
          "tasks": ["Environment setup", "Data migration"]
        }
      ],
      "risks": ["Complex integrations", "Legacy dependencies"],
      "assumptions": ["All APIs available", "Test environment ready"],
      "additionalNotes": "Any extra information"
    }
  }
}
```

## Calculation Result Format

The `calculation_result` object should include:

### Required Fields:
```json
{
  "weeks": 24,              // Total duration in weeks (number)
  "complexity": "High",     // Complexity level (string)
  "cost": "$250,000"        // Estimated cost (string)
}
```

### Optional Fields (add as needed):
```json
{
  "breakdown": {
    "development": 18,
    "testing": 4,
    "deployment": 2,
    "training": 1
  },
  "roleAllocation": {
    "PM USA": 0.5,
    "Architect USA": 1.0,
    "App Developer India": 3.0
  },
  "phases": [],
  "risks": [],
  "assumptions": [],
  "additionalNotes": "..."
}
```

## Testing

### 1. Update `.env` file:
```
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:5000
```

### 2. Start your backend server on port 5000

### 3. Test submission:
- Fill out the scoping form
- Click "Calculate & Submit"
- Frontend will call: `POST http://localhost:5000/api/scoping/submit`

### 4. Test history:
- Click "History" in sidebar  
- Frontend will call: `GET http://localhost:5000/api/scoping/history?email=user@example.com`

### 5. Test view result:
- Click "View Result" on a submission
- Frontend will call: `GET http://localhost:5000/api/scoping/result/{id}`

## Error Handling

Your backend should return proper HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid data)
- `404` - Resource not found
- `500` - Server error

Always include error messages in the response:
```json
{
  "success": false,
  "message": "User-friendly error message",
  "error": "Technical error details (optional)"
}
```

## CORS Configuration

Your backend must allow CORS requests from the frontend:

```javascript
// Example for Express.js
const cors = require('cors');
app.use(cors({
  origin: 'http://localhost:3001', // Frontend URL
  credentials: true
}));
```

## Notes

1. **Asynchronous Processing**: If your calculations take time, you can:
   - Return immediately with `status: "PENDING"`
   - Process in background
   - Frontend will show "Processing" status in history

2. **Data Storage**: Store submissions in your database with all fields

3. **Authentication**: You may want to add authentication headers if needed

4. **Validation**: Validate all incoming data before processing

## Questions?
Contact the frontend team for any questions about the integration.

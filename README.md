# TODO Manager CLI

A command-line task management application built with Python that uses the **Airtable REST API** as a remote backend.

The application supports complete CRUD operations—creating, reading, updating, and deleting tasks—while also implementing practical API concepts such as **pagination, rate-limit handling, retries, request timeouts, and centralized HTTP request management**.

This project demonstrates how a Python CLI application can communicate reliably with a remote REST API rather than relying on local file storage.

## How It Works

```text
User
 ↓
CLI Menu
 ↓
Python Application
 ↓
HTTP Request Layer
 ↓
Airtable REST API
 ↓
Remote Task Database
```

The application sends HTTP requests to Airtable to manage task records.

### Task Workflow

```text
Create Task
     ↓
POST Request
     ↓
Airtable Record

View Tasks
     ↓
GET Request
     ↓
Paginated Records
     ↓
All Tasks

Update Task
     ↓
PATCH Request
     ↓
Updated Record

Delete Task
     ↓
DELETE Request
     ↓
Removed Record
```

---

## Features

* Create new tasks
* View all tasks
* Update task names
* Update task statuses
* Update task notes
* Delete tasks
* Persistent remote storage using Airtable
* Airtable REST API integration
* CRUD operations
* Pagination support
* Rate-limit handling
* Automatic retries for rate-limited requests
* Centralized request handling
* Request timeouts
* HTTP error handling
* Network connection error handling
* Secure API authentication using environment variables
* Interactive command-line interface

---

## CRUD Operations

This project implements the four fundamental CRUD operations:

| Operation | HTTP Method | Purpose                 |
| --------- | ----------- | ----------------------- |
| Create    | `POST`      | Create a new task       |
| Read      | `GET`       | Retrieve tasks          |
| Update    | `PATCH`     | Modify an existing task |
| Delete    | `DELETE`    | Remove a task           |

### Create

A `POST` request creates a new Airtable record:

```text
POST → Create a task
```

### Read

A `GET` request retrieves tasks from Airtable:

```text
GET → Retrieve tasks
```

### Update

A `PATCH` request updates a specific record:

```text
PATCH → Modify a task
```

### Delete

A `DELETE` request removes a specific record:

```text
DELETE → Delete a task
```

---

## Rate Limiting and Retries

The application handles HTTP `429 Too Many Requests` responses.

When Airtable rate-limits the application, the request manager:

1. Detects the `429` response.
2. Waits for 30 seconds.
3. Retries the request.
4. Repeats the process up to three times.

```text
Request
  ↓
429 Rate Limited
  ↓
Wait 30 Seconds
  ↓
Retry
  ↓
Success or Maximum Retries Reached
```

The maximum number of retry attempts is:

```python
max_retries = 3
```

This prevents the application from continuously sending requests when the API has temporarily limited access.

---

## Pagination

The `get_tasks()` function supports Airtable pagination.

Airtable may return records in multiple pages instead of returning every record in a single response.

The application checks for an `offset` value:

```python
if "offset" not in data:
    break
```

If an offset exists, it is sent with the next request:

```text
Request 1
    ↓
Records + Offset
    ↓
Request 2
    ↓
More Records + Offset
    ↓
Request 3
    ↓
All Records Retrieved
```

All records are collected into a single list:

```python
all_records.extend(data["records"])
```

This allows the application to retrieve all available tasks even when the database contains more records than can be returned in a single API response.

---

## Centralized Request Handling

Instead of duplicating request and error-handling logic inside every function, the project uses a centralized:

```python
make_request()
```

function.

All API requests pass through this function:

```python
response = make_request(
    "GET",
    BASE_URL,
    headers=headers,
    params=params,
    timeout=10
)
```

This creates a single location for handling:

* HTTP requests
* Rate limiting
* Retries
* Connection errors
* Timeouts
* HTTP errors

This makes the application more consistent and reduces duplicated code.

---

## Error Handling

The application handles several common request failures.

### Rate Limit Errors

```text
429 Too Many Requests
```

The application waits and retries the request.

### Connection Errors

Handles situations where the application cannot connect to the API.

### Timeout Errors

Every request has a 10-second timeout:

```python
timeout=10
```

This prevents the program from waiting indefinitely for a response.

### HTTP Errors

The application uses:

```python
response.raise_for_status()
```

to detect unsuccessful HTTP responses, including:

* `400 Bad Request`
* `401 Unauthorized`
* `403 Forbidden`
* `404 Not Found`
* `500 Server Error`

---

## How To Run

Install the required dependencies:

```bash
pip install requests python-dotenv
```

Create a `.env` file in the project directory:

```env
AIRTABLE_TOKEN=your_airtable_personal_access_token
```

Then run:

```bash
python main.py
```

---

## Example Menu

```text
============== TODO MANAGER ==============
1. Create Task
2. Show Tasks
3. Update Task
4. Delete Task
5. Exit
```

---

## Example Usage

### Creating a Task

```text
Enter task name: Learn REST APIs
Enter task status (Started/Pending/Completed): Started
Add notes: Practice CRUD operations with Airtable

Task created: Learn REST APIs
```

### Viewing Tasks

```text
1. ID: rec123456
   - Name: Learn REST APIs
   - Status: Started
   - Notes: Practice CRUD operations with Airtable
====================
```

### Updating a Task

```text
Which record id would you like to update?: rec123456
Which field would you like to update(Name, Status, Notes): Status
Which status are you now?: Completed

Data updated
```

### Deleting a Task

```text
Which record id would you like to delete?: rec123456

Data deleted!
```

---

## API Authentication

The application authenticates with Airtable using a Bearer token:

```python
headers = {
    "Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"
}
```

The token is loaded from an environment variable using `python-dotenv`.

The `.env` file should **never** be committed to GitHub.

Your `.gitignore` should include:

```gitignore
.env
```

---

## Project Structure

```text
airtable-todo-manager/
│
├── main.py
├── .env
├── .gitignore
└── README.md
```

### `main.py`

Contains the complete application logic, including:

* API communication
* CRUD operations
* Pagination
* Rate-limit handling
* Retry logic
* Error handling
* User input
* CLI menu management

### `.env`

Stores the Airtable API token locally.

### `.gitignore`

Prevents sensitive files such as `.env` from being tracked by Git.

---

## Topics Covered

* Python
* REST APIs
* HTTP requests
* CRUD operations
* `GET`, `POST`, `PATCH`, and `DELETE` requests
* API authentication
* Bearer tokens
* Environment variables
* `python-dotenv`
* JSON request bodies
* JSON responses
* HTTP status codes
* `response.raise_for_status()`
* Request timeouts
* Rate limiting
* HTTP `429` responses
* Retry logic
* API pagination
* `offset`-based pagination
* Exception handling
* Remote data storage
* Command-line interfaces
* Centralized request handling

---

## Key Concepts Demonstrated

This project goes beyond simply making API requests. It demonstrates how to build a more reliable API client.

A basic API client might look like:

```text
Send Request
     ↓
Receive Response
```

This project adds real-world reliability:

```text
Send Request
     ↓
Check for Rate Limiting
     ↓
Retry if Necessary
     ↓
Handle Connection Errors
     ↓
Handle Timeouts
     ↓
Handle HTTP Errors
     ↓
Process Response
```

It also handles large datasets through pagination:

```text
API Page 1
    ↓
API Page 2
    ↓
API Page 3
    ↓
All Records Combined
```

This makes the project a practical example of building a Python application that interacts with an external API while accounting for common production concerns such as **rate limits, transient failures, timeouts, and paginated data**.

# TODO Manager CLI

A command-line task management application built with Python and the Airtable REST API. The application allows users to create, view, update, and delete tasks stored remotely in an Airtable database.

Unlike a traditional local TODO application that stores data in a file on the user's computer, this project uses Airtable as a remote backend and communicates with it through HTTP requests.

## How It Works

The application communicates with an Airtable database using the following workflow:

```text
User
 ↓
CLI Menu
 ↓
Python Application
 ↓
HTTP Request
 ↓
Airtable REST API
 ↓
Remote Task Database
```

Users can perform CRUD operations:

* **Create** new tasks
* **Read** existing tasks
* **Update** task information
* **Delete** tasks

The task data is stored remotely in Airtable.

## Features

* Create new tasks
* View all stored tasks
* Update task names
* Update task statuses
* Update task notes
* Delete tasks
* Persistent remote data storage through Airtable
* API authentication using a Bearer token
* Request timeouts
* HTTP error handling
* Network connection error handling
* Interactive command-line menu

## Task Fields

Each task contains the following fields:

| Field    | Description                           |
| -------- | ------------------------------------- |
| `Name`   | The name of the task                  |
| `Status` | The current status of the task        |
| `Notes`  | Additional information about the task |

Example:

```text
Name: Complete Python project
Status: Started
Notes: Finish the README and push to GitHub
```

## CRUD Operations

This project demonstrates the four fundamental CRUD operations:

### Create

Uses an HTTP `POST` request to create a new Airtable record.

```text
POST → Create a new task
```

### Read

Uses an HTTP `GET` request to retrieve existing tasks.

```text
GET → Retrieve all tasks
```

### Update

Uses an HTTP `PATCH` request to modify a specific task.

```text
PATCH → Update an existing task
```

### Delete

Uses an HTTP `DELETE` request to remove a specific task.

```text
DELETE → Remove a task
```

## How To Run

Install the required dependency:

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

## Example Menu

```text
==============TODO MANAGER==============
1. Create Task
2. Show Tasks
3. Update Task
4. Delete Task
5. Exit
```

## Example Usage

### Creating a Task

```text
Enter task name: Learn REST APIs
Enter task status(Started/Pending/Completed): Started
Add notes: Practice CRUD operations with Airtable

Task created: Learn REST APIs
```

### Viewing Tasks

```text
1. ID: rec123456
   - Name: Learn REST APIs
   - Status: Started
   - Notes: Practice CRUD operations with Airtable
```

### Updating a Task

The user provides the Airtable record ID and chooses which field to modify:

```text
Which record id will you like to update?: rec123456
Which field will you like to update(Name,Status, Notes): Status
Which status are you now: Completed

Data updated
```

## API Authentication

The application authenticates with Airtable using a Bearer token:

```python
headers = {
    "Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"
}
```

The token is stored in a `.env` file instead of being written directly in the Python source code.

This is important because API tokens are sensitive credentials and should not be committed to GitHub.

Your `.gitignore` should include:

```gitignore
.env
```

## Error Handling

The application handles several types of request failures:

### Connection Errors

```python
requests.exceptions.ConnectionError
```

Handles situations where the application cannot connect to the API.

### Timeout Errors

```python
requests.exceptions.Timeout
```

Handles requests that take too long to receive a response.

### HTTP Errors

```python
response.raise_for_status()
```

Detects unsuccessful HTTP responses such as:

* `400 Bad Request`
* `401 Unauthorized`
* `403 Forbidden`
* `404 Not Found`
* `500 Server Error`

The application also uses:

```python
timeout=10
```

to prevent requests from waiting indefinitely.

## Topics Covered

* Python
* REST APIs
* HTTP requests
* CRUD operations
* `GET`, `POST`, `PATCH`, and `DELETE` requests
* API authentication
* Bearer tokens
* Environment variables
* `.env` files
* `python-dotenv`
* JSON request bodies
* JSON responses
* HTTP status codes
* `requests.raise_for_status()`
* Exception handling
* API timeouts
* Remote data storage
* Command-line interfaces

## Project Structure

```text
todo-manager/
│
├── main.py
├── .env
├── .gitignore
└── README.md
```

### `main.py`

Contains the application logic for:

* Communicating with the Airtable API
* Managing tasks
* Handling user input
* Processing API responses
* Displaying information in the terminal

### `.env`

Stores the Airtable API token securely.

### `.gitignore`

Prevents sensitive files such as `.env` from being tracked by Git.

## Key Concepts Demonstrated

This project demonstrates how a Python application can communicate with a remote database through a REST API.

Instead of directly manipulating a local CSV or JSON file:

```text
Python Application
       ↓
Local File
```

this project communicates with an external service:

```text
Python Application
       ↓
HTTP Request
       ↓
Airtable REST API
       ↓
Remote Database
```


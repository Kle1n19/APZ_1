# LAB 1
## Installation

### Prerequisites

- Python 3
- pip

### Install Dependencies

Run the following command to install required packages:

```sh
pip install fastapi uvicorn requests
```

---

## Running the Services

Each service must run independently in different terminals.

### **1. Start the Logging Service**

```sh
uvicorn logging_service:app --port 8001 --reload
```

### **2. Start the Facade Service**

```sh
uvicorn facade_service:app --port 8000 --reload
```

### **3. Start the Messages Service**

```sh
uvicorn messages_service:app --port 8002 --reload
```

---

## API Endpoints

#### `POST /send`

Send a message to be logged.

```sh
curl -X 'POST' 'http://127.0.0.1:8000/send' \
-H 'Content-Type: application/json' \
-d '{"msg": "Hello World"}'
```

**Response:**

```json
{"message":"Message sent"}
```

#### `GET /fetch`

Retrieve all stored messages and the static response from `messages-service`.

```sh
curl -X 'GET' 'http://127.0.0.1:8000/fetch'
```

**Response:**

```json
{"logs":["Hllo World"],"message":{"message":"not implemented yet"}}
```

---

## Additional Features

- **Retry Mechanism**: Retries failed requests to `logging-service` up to **3 times**.
- **Deduplication**: Prevents duplicate messages in the logging service.

---

## Notes

- Ensure all services are running before testing.
- If `logging-service` is down, `facade-service` retries automatically.
- Logs are stored in memory, so restarting `logging-service` will reset stored logs.

---

## Author

Developed for **Microservices Basics Task**.


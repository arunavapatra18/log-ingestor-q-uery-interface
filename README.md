<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python v3.12

  Get it here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dyte-submissions/november-2023-hiring-arunavapatra18.git
   ```
2. cd into **src/**
   ```sh
    cd src
   ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your database credentials in **.env**
   ```
    DB_USERNAME = USER
    DB_PASSWORD = PASSWORD
    DB_NAME = PG_DB_NAME
    MONGO_DB_USERNAME = USER
    MONGO_DB_PASSWORD = PASSWORD
   ```
5. Enter your database urls in **db.py**
   ```py
    POSTGRES_DB_URL = f"postgres://{getenv('DB_USERNAME')}:{getenv('DB_PASSWORD')}@localhost:5432/{getenv('DB_NAME')}"

    MONGO_DB_URL = f"mongodb+srv://{getenv('MONGO_DB_USERNAME')}:{getenv('MONGO_DB_PASSWORD')}@cluster0.u2ntfqh.mongodb.net/?retryWrites=true&w=majority"
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Start the Log Ingestor server
   ```sh
    $ python run.py
   ```

    ![System Design](/images/LogIngestor%20Running.png)

2. The API will be avaialbe at http://localhost:3000/ 
   
   The application will ingest logs on port 3000.

3. Run the CLI application to search and filter logs
   
   Examples:
   ```sh
    $ python cli.py -q "Failed to connect"

    Search Results:
    {'level': 'success', 'message': 'Failed to connect to DB', 'resourceId': 'server-1234', 'timestamp': '2023-09-15T08:00:00', 'traceId': 'abc-xyz-123', 'spanId': 'span-456', 'commit': '5e5342f', 'metadata': {'parentResourceId': 'server-0987'}}

    {'level': 'error', 'message': 'Failed to connect to DB', 'resourceId': 'server-1234', 'timestamp': '2023-09-15T08:00:00', 'traceId': 'abc-xyz-123', 'spanId': 'span-456', 'commit': '5e5342f', 'metadata': {'parentResourceId': 'server-0987'}}
    
    $ python cli.py -l "success"

    Search Results:
    {'level': 'success', 'message': 'Failed to connect to DB', 'resourceId': 'server-1234', 'timestamp': '2023-09-15T08:00:00', 'traceId': 'abc-xyz-123', 'spanId': 'span-456', 'commit': '5e5342f', 'metadata': {'parentResourceId': 'server-0987'}}
   ```

4. CLI interface usage:
    ```
      $ python cli.py --help
      Usage: cli.py [OPTIONS]

      Function to search and filter logs from CLI

      Options:
        -q, --query TEXT               Search query string.
        -l, --level TEXT               Log level.
        -m, --message TEXT             Log message.
        -ri, --resource-id TEXT        Resource ID.
        -t, --timestamp TEXT           Log timestamp.
        -tr, --trace-id TEXT           Trace ID.
        -s, --span-id TEXT             Span ID.
        -c, --commit TEXT              Git commit hash.
        -p, --parent-resource-id TEXT  Parent resource ID.
        --help                         Show this message and exit.
    ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- SYSTEM DESIGN -->
## System Design

### Overview

![System Design](/images/System%20Design.png)

**Key Components**:

- FastAPI for ingestion API
- MongoDB and Postgres for storage
- Pydantic models for validation
- CLI using Click for search and filter interface

### Features

- Clients send logs to FastAPI server for ingestion
- Pydantic models validate logs
- Logs inserted into both MongoDB and Postgres databases
- CLI makes search requests to API
- API queries MongoDB to perform full-text search and filtering
- Results returned to CLI for display

<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




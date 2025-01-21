```mermaid
graph TD
    A[Checkout code] --> B[Set up Python 3.11]
    B --> C[Install dependencies]
    C --> D[Run cargohub_db.py to create test database]
    D --> E[Lint with flake8]
    E --> F[Check cargohub_test.db existence]
    F --> G[Run tests]

    subgraph build
        A[Checkout code]
        B[Set up Python 3.11]
        C[Install dependencies]
        D[Run cargohub_db.py to create test database]
        E[Lint with flake8]
        F[Check cargohub_test.db existence]
        G[Run Pytest on unit tests]
    end
```
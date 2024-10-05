
# Mock Social API

## Overview

This project is built using FastAPI and allows you to track user activity and check follow status on Instagram accounts. 

## Prerequisites

Before running the project, you need to have [Poetry](https://python-poetry.org/docs/#installation) installed. Poetry is a dependency management tool for Python.

### Install Poetry

To install Poetry, follow the instructions provided on their [official installation page](https://python-poetry.org/docs/#installation). 

For most systems, you can use the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, ensure that Poetry is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Getting Started

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone https://github.com/jonra1993/mock-social-api.git
   cd mock-social-api
   ```

2. **Install dependencies**:

   ```bash
   poetry install
   ```

3. **Activate the Poetry environment**:

   ```bash
   poetry shell
   ```

4. **Run the FastAPI project**:

   Use the following command to start the FastAPI server:

   ```bash
   fastapi dev mock_social_api/main.py
   ```

5. **Access the API**:

   Open your web browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI documentation and test the endpoints.

## Project Structure

- `mock_social_api/`: Contains the main application logic.
- `main.py`: Entry point for the FastAPI application.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Endava Testing Solution

This project contains the solutions for the endava REST API task and Web UI task v1 and v2

---

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/AlexanderTerezov/endava_testing_solution.git
cd endava_testing_solution
```

### 2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the tests

### REST API Tests

```bash
cd Rest_Api_Task
python rest_api_test.py
```

### Web UI Version 1

```bash
cd Web_UI_Task
python -m tests.test_version1
```

### Web UI Version 2

```bash
python -m tests.test_version2  {chrome|firefox} <enviroment> <tests>
```

#### Example:

```bash
python -m tests.test_version2 firefox dev test_scenario_1 test_scenario_2
```


# Flask event scheduler web application

<!-- TOC -->
* [Flask web application](#Flask-event-scheduler-web-application)
    * [Prerequisites](#prerequisites)
    * [Setup](#setup)
    * [How to Run](#how-to-run)
<!-- TOC -->

### Prerequisites
Before you begin, make sure you have the following requirements:

- Python installed (version 3.10)
- Poetry installed

### Setup
Clone the repository:

```bash
git clone https://github.com/AwfulIceCream/events.git
cd events
```
Activate virtual environment:
```bash
python -m venv venv
#For windows:
.\venv\Scripts\activate
#For UNIX-like(Linux\MacOs):
source venv/bin/activate
```
Install Poetry and dependencies:
```bash
pip install poetry
poetry install
```

### How to Run
To run the project, follow these steps:

1. Run the Flask application:

```bash
poetry run python app.py
```

Note:
If you encounter any issues or have specific questions about the Flask Events Scheduler project, feel free to contact the author at <andriymyrosh@gmail.com>.

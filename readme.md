# Rule Engine Application

## Overview

This Rule Engine Application allows users to create and evaluate rules based on provided data. The rules are represented as an Abstract Syntax Tree (AST) and can be evaluated using logical operations such as AND and OR. The application is built using Flask and SQLite.

## Features

- Create rules using a simple syntax
- Save rules to a SQLite database
- Evaluate rules against JSON-formatted data
- Returns the evaluation result and rule ID

## Technologies Used

- Python
- Flask
- SQLite
- HTML/CSS/JavaScript for the front-end

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lokeshgonthina/RuleEngineApp.git
   cd RuleEngineApp

## Set up a virtual environment:

python -m venv venv

## Activate the virtual environment:

source venv/Scripts/activate

## Install required packages:
pip install Flask

## Run the application:

python app.py

Enter following URL in the browser:

http://127.0.0.1:5000/static/index.html



## Usage
Create a Rule:

  "rule_string": "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

Evaluate :

  "data": {
    "age": 32,
    "department": "Marketing",
    "salary": 30000,
    "experience": 7
  }

Check the Response:

The response will include the rule_id and the evaluation result.




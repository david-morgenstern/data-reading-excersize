# Questions / tasks
    • Provide a high-level architecture for the solution
    • What kind of technologies would you use?
    • Please explain your decisions and describe your assumptions if any

### High level architecture:
- Control Flow:
  1. Acquire data
  2. Clean data with pandas
  3. Save to database
  4. Use sql for precise queries and pandas.DataFrame for data manipulation
  5. matplotlib, seaborn, streamlit.io for visualization (not shown in this example)

### Technologies I'd use:
- Python3
- pandas
- numpy
- MySql
- mongodb
- streamlit.io
- fastApi

### Explanation:
- It would've been alot easier to just generate json data with a site like https://www.mockaroo.com/
but of course I wanted to show some of my numpy skills.
- Made two types of files to make sure I'll need to get information from more than one places/tables.
- This example does not reflect OOP principles
- I focused more on this task and not so much on the "refactoring", to be honest
I'm not sure if I even understood that task.

## Instructions:
  - Refactoring Python:
    - Check interview_refactoring.py file
    - I left the old code after the refactored to make it easier to compare. No idea if this is what you meant by refactoring it.
  - Building database and the rest:
    1. Optional(create a virtualenv)
    2. Install packages listed in requirements.txt (or just pip install pandas, should be enough)
    3. Run create_data.py
    4. Run read_data.py
    5. See terminal output.

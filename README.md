# Recurly to Postgres
Get data from Recurly and save to the Postgres database.

## Prerequisites
* Python 3.6.x (for f-strings)
* Knowledge of Python
* Install the dependencies: `pip install -r requirements.txt`

## Usage
1. Add new ORM mappings to: `mapping.py`
2. Modify `main.py` as needed
3. Run `python main.py`
4. Profit!

## Connect to Recurly
An API Key is required to access Recurly's data. Following this [instruction](https://docs.recurly.com/docs/api-keys) to get yours then set it to the environment variable `RECURLY_API_KEY`.

## Connect to the database
Please set the following environment variables as needed:
| Environment variable | Description | Default value |
| -------------------- | ----------- | ------------- |
| PG_USERNAME  | the username | postgres |
| PG_PASSWORD  | the password | postgres |
| PG_HOST  | the database hostname | localhost |
| PG_PORT  | the database port | 5432 |
| PG_DATABASE  | the database name | recurly |

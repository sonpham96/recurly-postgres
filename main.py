"""
Install dependencies: pip install -r requirements.txt
How to get the Recurly API Key: https://docs.recurly.com/docs/api-keys
Recurly Python docs:
    https://recurly-client-python.readthedocs.io/en/latest/
    https://recurly-client-python.readthedocs.io/en/latest/recurly.html?highlight=clientpy#recurly-package
"""

from os import getenv

import recurly
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from mapping import (Account, Invoice, Plan, Subscription, create_all, get,
                     get_or_create)

# RECURLY
api_key = getenv('RECURLY_API_KEY')
client = recurly.Client(api_key)

# DATABASE
engine = sqlalchemy.create_engine('postgresql://{username}:{password}@{host}:{port}/{database}'.format(
    username=getenv('PG_USERNAME', 'postgres'),
    password=getenv('PG_PASSWORD', 'postgres'),
    host=getenv('PG_HOST', 'localhost'),
    port=getenv('PG_PORT', 5432),
    database=getenv('PG_DATABASE', 'recurly'),
))
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables if not exists
create_all(engine)


def get_first(fetch_method, *args, **kwargs):
    pager = fetch_method(*args, **kwargs)
    return next(pager.items())


def create_helper(fetch_method, model, *args, **kwargs):
    pager = fetch_method(*args, **kwargs)
    return [get_or_create(session, model, **item.__dict__) for item in pager.items()]


def create_accounts():
    return create_helper(client.list_accounts, Account)


def create_plans():
    return create_helper(client.list_plans, Plan)


def create_subscriptions():
    return create_helper(client.list_subscriptions, Subscription)


def create_invoices():
    pager = client.list_invoices()

    def get_subscriptions(item):
        return [get(session, Subscription, subscription_id) for subscription_id in item.subscription_ids]

    return [get_or_create(session, Invoice, **item.__dict__, subscriptions=get_subscriptions(item)) for item in pager.items()]


# Debug
# print(get_first(client.list_accounts))
# print(get_first(client.list_plans))
# print(get_first(client.list_subscriptions))
# print(get_first(client.list_invoices))

# Populate data
create_accounts()
create_plans()
create_subscriptions()
create_invoices()

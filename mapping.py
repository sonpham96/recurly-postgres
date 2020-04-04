from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def create_all(engine):
    Base.metadata.create_all(engine)


def get(session, model, id):
    return session.query(model).filter_by(id=id).first()


def create(session, model, **kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def get_or_create(session, model, **kwargs):
    instance = get(session, model, id=kwargs['id'])

    if instance:
        return instance
    else:
        instance = create(session, model, **kwargs)
        return instance


class BaseEntity(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{k}={v}" for k, v in sorted(self.__dict__.items()))})'


class Account(BaseEntity):
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True)
    code = Column(String, unique=True)
    bill_to = Column(String)
    state = Column(String)
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    tax_exempt = Column(Boolean)
    has_live_subscription = Column(Boolean)
    has_active_subscription = Column(Boolean)
    has_future_subscription = Column(Boolean)
    has_canceled_subscription = Column(Boolean)
    has_paused_subscription = Column(Boolean)
    has_past_due_invoice = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    subscriptions = relationship('Subscription')


class Plan(BaseEntity):
    __tablename__ = 'plans'

    id = Column(String, primary_key=True)
    code = Column(String, unique=True)
    state = Column(String)
    name = Column(String)
    description = Column(String)
    interval_unit = Column(String)
    interval_length = Column(Integer)
    trial_unit = Column(String)
    trial_length = Column(Integer)
    total_billing_cycles = Column(Integer)
    revenue_schedule_type = Column(String)
    setup_fee_revenue_schedule_type = Column(String)
    auto_renew = Column(Boolean)
    accounting_code = Column(String)
    setup_fee_accounting_code = Column(String)
    tax_code = Column(String)
    tax_exempt = Column(Boolean)
    unit_amount = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __init__(self, **kwargs):
        currencies = kwargs.pop('currencies')
        if len(currencies) > 0:
            kwargs['unit_amount'] = currencies[0].unit_amount

        super().__init__(**kwargs)


class Subscription(BaseEntity):
    __tablename__ = 'subscriptions'

    id = Column(String, primary_key=True)
    uuid = Column(String, unique=True)
    account_id = Column(String, ForeignKey('accounts.id'))
    account = relationship('Account')
    plan_id = Column(String, ForeignKey('plans.id'))
    plan = relationship('Plan')
    state = Column(String)
    current_period_started_at = Column(DateTime)
    current_period_ends_at = Column(DateTime)
    current_term_started_at = Column(DateTime)
    current_term_ends_at = Column(DateTime)
    trial_started_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    remaining_billing_cycles = Column(Integer)
    total_billing_cycles = Column(Integer)
    renewal_billing_cycles = Column(Integer)
    revenue_schedule_type = Column(String)
    auto_renew = Column(Boolean)
    paused_at = Column(DateTime)
    remaining_pause_cycles = Column(Integer)
    currency = Column(String)
    unit_amount = Column(Float)
    quantity = Column(Integer)
    subtotal = Column(Float)
    collection_method = Column(String)
    po_number = Column(String)
    net_terms = Column(Integer)
    bank_account_authorized_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    activated_at = Column(DateTime)
    canceled_at = Column(DateTime)
    invoices = relationship('Invoice', secondary='invoice_subscription')

    def __init__(self, **kwargs):
        account = kwargs.pop('account')
        kwargs['account_id'] = account.id

        plan = kwargs.pop('plan')
        kwargs['plan_id'] = plan.id

        super().__init__(**kwargs)


class Invoice(BaseEntity):
    __tablename__ = 'invoices'

    id = Column(String, primary_key=True)
    type = Column(String)
    origin = Column(String)
    state = Column(String)
    account_id = Column(String, ForeignKey('accounts.id'))
    account = relationship('Account')
    previous_invoice_id = Column(String)
    number = Column(String)
    collection_method = Column(String)
    po_number = Column(String)
    net_terms = Column(Integer)
    currency = Column(String)
    balance = Column(Float)
    paid = Column(Float)
    total = Column(Float)
    subtotal = Column(Float)
    refundable_amount = Column(Float)
    discount = Column(Float)
    tax = Column(Float)
    vat_number = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    due_at = Column(DateTime)
    closed_at = Column(DateTime)
    subscriptions = relationship('Subscription', secondary='invoice_subscription')

    def __init__(self, **kwargs):
        account = kwargs.pop('account')
        kwargs['account_id'] = account.id

        subscriptions = kwargs.pop('subscriptions')

        super().__init__(**kwargs)
        for s in subscriptions:
            self.subscriptions.append(s)


class InvoiceSubscription(BaseEntity):
    __tablename__ = 'invoice_subscription'

    invoice_id = Column(String, ForeignKey('invoices.id'), primary_key=True)
    subscription_id = Column(String, ForeignKey('subscriptions.id'), primary_key=True)

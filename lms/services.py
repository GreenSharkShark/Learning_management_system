import stripe
from config.settings import STRIPE_SECRET_KEY_TEST


def generate_payment_intent(amount):
    stripe.api_key = STRIPE_SECRET_KEY_TEST
    currency = 'usd'
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        description='Payment for course',
        statement_descriptor='Course Payment',
    )
    return intent


def get_payment_status(payment_id):
    stripe.api_key = STRIPE_SECRET_KEY_TEST
    retrieve = stripe.PaymentIntent.retrieve(payment_id)
    return retrieve

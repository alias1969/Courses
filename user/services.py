import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(amount):
    """Создаем цену в Stripe"""
    return stripe.Price.create(
        currency="RUB",
        unit_amount=amount * 100,
        product_data={"name": "payment"},
    )


def create_stripe_session(price):
    """Создаем сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/course/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

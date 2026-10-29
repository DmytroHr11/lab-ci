import pytest

from shop.cart import Cart


@pytest.fixture
def empty_cart() -> Cart:
    """Фікстура, що повертає новий порожній кошик перед кожним тестом."""
    return Cart()


@pytest.fixture
def cart_with_items() -> Cart:
    """Фікстура, що повертає кошик із трьома товарами для перевірки розрахунків."""
    cart = Cart()
    cart.add("Книга", price=250.0, qty=2)  # 500.0 грн
    cart.add("Ручка", price=25.0, qty=4)  # 100.0 грн
    cart.add("Зошит", price=50.0, qty=1)  # 50.0 грн
    return cart

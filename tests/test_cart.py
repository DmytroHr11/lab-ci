from unittest.mock import Mock

import pytest

from shop.cart import Cart, Item


def test_empty_cart_initialization(empty_cart: Cart) -> None:
    assert empty_cart.items_count() == 0
    assert empty_cart.total() == 0.0


def test_add_single_item(empty_cart: Cart) -> None:
    empty_cart.add("Ноутбук", price=30000.0, qty=1)
    assert empty_cart.items_count() == 1
    assert empty_cart.total() == 30000.0


def test_add_multiple_quantity(empty_cart: Cart) -> None:
    empty_cart.add("Мишка", price=500.0, qty=3)
    assert empty_cart.items_count() == 3
    assert empty_cart.total() == 1500.0


def test_add_existing_item_updates_qty_and_price(empty_cart: Cart) -> None:
    empty_cart.add("Кава", price=120.0, qty=1)
    empty_cart.add("Кава", price=130.0, qty=2)
    assert empty_cart.items_count() == 3
    assert empty_cart.total() == 390.0


def test_remove_existing_item(cart_with_items: Cart) -> None:
    cart_with_items.remove("Зошит")
    assert cart_with_items.items_count() == 6
    assert cart_with_items.total() == 600.0


def test_remove_nonexistent_item_raises(empty_cart: Cart) -> None:
    with pytest.raises(KeyError, match="Флешка"):
        empty_cart.remove("Флешка")


def test_add_negative_price_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="price must be non-negative"):
        empty_cart.add("Товар", price=-10.0, qty=1)


def test_add_zero_or_negative_qty_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("Товар", price=100.0, qty=0)
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("Товар", price=100.0, qty=-2)


@pytest.mark.parametrize(
    ("discount", "expected_total"),
    [
        (0.0, 650.0),
        (10.0, 585.0),
        (50.0, 325.0),
        (100.0, 0.0),
    ],
)
def test_total_with_valid_discounts(
    cart_with_items: Cart, discount: float, expected_total: float
) -> None:
    assert cart_with_items.total(discount_percent=discount) == pytest.approx(expected_total)


@pytest.mark.parametrize("invalid_discount", [-1.0, 100.1, -15.0, 150.0])
def test_total_with_invalid_discount_raises(cart_with_items: Cart, invalid_discount: float) -> None:
    with pytest.raises(ValueError, match=r"discount_percent must be in \[0, 100\]"):
        cart_with_items.total(discount_percent=invalid_discount)


def test_total_in_currency_with_mock(cart_with_items: Cart) -> None:
    mock_rates = Mock()
    mock_rates.get_rate.return_value = 41.50
    total_usd = cart_with_items.total_in("USD", rates=mock_rates)
    assert total_usd == pytest.approx(15.66)
    mock_rates.get_rate.assert_called_once_with("USD")


def test_total_in_currency_invalid_rate_raises(cart_with_items: Cart) -> None:
    mock_rates = Mock()
    mock_rates.get_rate.return_value = 0.0
    with pytest.raises(ValueError, match="rate must be positive"):
        cart_with_items.total_in("EUR", rates=mock_rates)


def test_most_expensive_empty_cart(empty_cart: Cart) -> None:
    assert empty_cart.most_expensive() is None


def test_most_expensive_with_items(cart_with_items: Cart) -> None:
    most_exp = cart_with_items.most_expensive()
    assert isinstance(most_exp, Item)
    assert most_exp.name == "Книга"
    assert most_exp.price == 250.0

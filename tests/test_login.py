# -*- coding: utf-8 -*-
"""UI-автотесты авторизации и корзины Swag Labs (Playwright + pytest)."""

BASE = "https://www.saucedemo.com/"


def login(page, user, password="secret_sauce"):
    """Вспомогательная функция: вход на сайт."""
    page.goto(BASE)
    page.fill("#user-name", user)
    page.fill("#password", password)
    page.click("#login-button")


def test_successful_login(page):
    """Вход под standard_user открывает каталог с 6 товарами."""
    login(page, "standard_user")
    assert "/inventory.html" in page.url
    assert page.locator(".inventory_item").count() == 6


def test_locked_out_user(page):
    """Заблокированный пользователь видит сообщение об ошибке."""
    login(page, "locked_out_user")
    error = page.locator("[data-test='error']")
    assert error.is_visible()
    assert "locked out" in error.inner_text()


def test_invalid_credentials(page):
    """Неверный пароль -> сообщение об ошибке."""
    login(page, "standard_user", "wrong_password")
    error = page.locator("[data-test='error']")
    assert "do not match" in error.inner_text()


def test_add_to_cart(page):
    """После добавления товара счётчик корзины показывает 1."""
    login(page, "standard_user")
    page.click("button[data-test^='add-to-cart']")
    assert page.locator(".shopping_cart_badge").inner_text() == "1"

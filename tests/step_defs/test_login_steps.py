"""
Step definitions for Login feature.

This module implements the steps from login.feature using pytest-bdd.
Each step is a Python function that connects Gherkin steps to actual code.
"""

import allure
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from lib.pages.login_page import LoginPage


# ============================================================================
# LOAD SCENARIOS
# ============================================================================
# This line tells pytest-bdd to load all scenarios from login.feature
scenarios('../features/login.feature')


# ============================================================================
# GIVEN STEPS (Preconditions)
# ============================================================================

@given('I am on the login page', target_fixture='login_page')
def navigate_to_login_page(page: Page) -> LoginPage:
    """
    Navigate to the login page and return a LoginPage object.
    
    This step:
    1. Creates a LoginPage instance
    2. Navigates to the login URL
    3. Returns the page object for use in other steps
    
    The 'target_fixture' parameter makes this step return a fixture
    that can be used by subsequent steps.
    """
    with allure.step("Navigate to the login page"):
        login_page = LoginPage(page)
        login_page.goto()
        return login_page


# ============================================================================
# WHEN STEPS (Actions)
# ============================================================================

@when(parsers.parse('I enter username "{username}"'))
def enter_username(login_page: LoginPage, username: str) -> None:
    """
    Enter a username in the username field.
    
    Args:
        login_page: The LoginPage fixture from the Given step
        username: The username to enter (from the Gherkin step)
    
    The parsers.parse() allows us to extract "{username}" from the step text.
    """
    with allure.step(f"Enter username: {username}"):
        login_page.username_input.fill(username)


@when(parsers.parse('I enter password "{password}"'))
def enter_password(login_page: LoginPage, password: str) -> None:
    """
    Enter a password in the password field.
    
    Note: We use allure.step but don't show the actual password value
    for security reasons in the report.
    """
    with allure.step("Enter password"):
        login_page.password_input.fill(password)


@when('I click the login button')
def click_login_button(login_page: LoginPage) -> None:
    """
    Click the login button to submit the form.
    """
    with allure.step("Click the login button"):
        login_page.login_button.click()


# ============================================================================
# THEN STEPS (Assertions/Verifications)
# ============================================================================

@then('I should be redirected to the inventory page')
def verify_redirect_to_inventory(page: Page) -> None:
    """
    Verify that we were redirected to the inventory page.
    
    This checks that 'inventory.html' is in the URL.
    """
    with allure.step("Verify redirect to inventory page"):
        page.wait_for_load_state("domcontentloaded")
        assert "inventory.html" in page.url, \
            f"Expected 'inventory.html' in URL, but got: {page.url}"


@then(parsers.parse('I should see the "{title}" title'))
def verify_title_visible(page: Page, title: str) -> None:
    """
    Verify that a specific title is visible on the page.
    
    Args:
        title: The title text to look for (extracted from step)
    """
    with allure.step(f"Verify '{title}' title is visible"):
        title_element = page.get_by_text(title)
        assert title_element.is_visible(), \
            f"Expected '{title}' to be visible, but it was not found"


@then('I should see an error message')
def verify_error_message_visible(login_page: LoginPage) -> None:
    """
    Verify that an error message is displayed.
    """
    with allure.step("Verify error message is visible"):
        assert login_page.error_message.is_visible(), \
            "Expected error message to be visible, but it was not"


@then(parsers.parse('the error message should contain "{text}"'))
def verify_error_message_contains(login_page: LoginPage, text: str) -> None:
    """
    Verify that the error message contains specific text.
    
    Also attaches the actual error message to the Allure report.
    """
    with allure.step(f"Verify error message contains: '{text}'"):
        error_text = login_page.get_error_text()
        assert text in error_text, \
            f"Expected '{text}' in error message, but got: {error_text}"
        
        # Attach the full error message to the Allure report
        allure.attach(
            error_text,
            name="Error Message",
            attachment_type=allure.attachment_type.TEXT
        )

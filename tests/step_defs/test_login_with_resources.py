"""
Example: Using ResourceLoader in BDD tests.

This demonstrates how to integrate environment-based resources with pytest-bdd.
"""

import allure
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from lib.resource_loader import ResourceLoader


# Load scenarios from feature file
scenarios('../features/login.feature')


@given('I am on the login page', target_fixture='test_context')
def navigate_to_login_page(page: Page, environment: str):
    """
    Navigate to login page using ResourceLoader.
    
    This step demonstrates loading locators from environment-specific resources.
    """
    # Create ResourceLoader for current environment
    loader = ResourceLoader(environment=environment)
    
    with allure.step(f"Initialize ResourceLoader for {environment}"):
        # Load page locators
        locators = loader.load_locators("login_page")
        
        allure.attach(
            f"Environment: {environment}\nLocators loaded: {len(locators)} elements",
            name="Resource Info",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Navigate to login page"):
        page.goto("https://www.saucedemo.com/")
        page.wait_for_load_state("domcontentloaded")
    
    # Return context with loader and locators for next steps
    return {
        'loader': loader,
        'locators': locators,
        'page': page
    }


@when(parsers.parse('I enter credentials for "{user_key}"'))
def enter_credentials(test_context: dict, user_key: str):
    """Enter username and password for a specific user key."""
    page = test_context['page']
    loader = test_context['loader']
    locators = test_context['locators']
    
    with allure.step(f"Load credentials for '{user_key}'"):
        # Load user data
        users_data = loader.load_test_data("users")
        if user_key not in users_data:
            raise KeyError(f"User '{user_key}' not found in users.json")
        
        user = users_data[user_key]
        username = user["username"]
        password = user["password"]
    
    with allure.step(f"Enter credentials for {username}"):
        # Get locators
        username_locator = locators["username_input"]["value"]
        password_locator = locators["password_input"]["value"]
        
        # Fill fields
        page.locator(username_locator).fill(username)
        page.locator(password_locator).fill(password)


@when('I click the login button')
def click_login_button(test_context: dict):
    """Click login button using locator from ResourceLoader."""
    page = test_context['page']
    locators = test_context['locators']
    
    with allure.step("Click login button"):
        login_btn_locator = locators["login_button"]["value"]
        page.locator(login_btn_locator).click()


@then('I should be redirected to the inventory page')
def verify_redirect_to_inventory(test_context: dict):
    """Verify redirect to inventory page."""
    page = test_context['page']
    
    with allure.step("Verify redirect to inventory"):
        page.wait_for_load_state("domcontentloaded")
        assert "inventory.html" in page.url


@then(parsers.parse('I should see the "{title}" title'))
def verify_title_visible(test_context: dict, title: str):
    """Verify title is visible."""
    page = test_context['page']
    
    with allure.step(f"Verify '{title}' title visible"):
        assert page.get_by_text(title).is_visible()


@then('I should see an error message')
def verify_error_message_visible(test_context: dict):
    """Verify error message using locator from ResourceLoader."""
    page = test_context['page']
    locators = test_context['locators']
    
    with allure.step("Verify error message visible"):
        error_locator = locators["error_message"]["value"]
        assert page.locator(error_locator).is_visible()


@then(parsers.parse('the error message should contain "{text}"'))
def verify_error_contains(test_context: dict, text: str):
    """Verify error message content using locator from ResourceLoader."""
    page = test_context['page']
    locators = test_context['locators']
    
    with allure.step(f"Verify error contains: '{text}'"):
        error_locator = locators["error_message"]["value"]
        error_text = page.locator(error_locator).inner_text()
        assert text in error_text
        
        allure.attach(error_text, name="Error Message", attachment_type=allure.attachment_type.TEXT)

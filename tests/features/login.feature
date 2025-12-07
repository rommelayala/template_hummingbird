# language: en
Feature: User Authentication
  As a user of the system
  I want to be able to authenticate
  So that I can access the application

  Background:
    Given I am on the login page

  @smoke @critical @login
  @smoke @critical @login
  Scenario: Successful login with valid credentials
    When I enter credentials for "valid_user"
    And I click the login button
    Then I should be redirected to the inventory page
    And I should see the "Products" title

  @smoke @critical @login
  Scenario: Failed login with invalid credentials
    When I enter credentials for "invalid_user"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Epic sadface"

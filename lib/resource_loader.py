"""
Resource Loader for Environment-Based Resources.

Loads JSON templates, payloads, locators (JSON or .properties), and test data 
based on the current environment.
Supports fallback to common resources and caching for performance.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from functools import lru_cache
from configparser import ConfigParser


class ResourceLoader:
    """
    Load resources based on environment (DEV, QA, STAG, PP).
    
    Usage:
        loader = ResourceLoader(environment="QA")
        
        # Load different resource types
        template = loader.load_json_template("login_response")
        payload = loader.load_payload("create_user")
        locators = loader.load_locators("login_page")
        users = loader.load_test_data("users")
        
        # Quick access methods
        locator_value = loader.get_locator("login_page", "username_input")
        user = loader.get_test_user("standard")
    """
    
    def __init__(self, environment: str, resources_dir: str = "resources"):
        """
        Initialize ResourceLoader.
        
        Args:
            environment: Environment name (DEV, QA, STAG, PP)
            resources_dir: Base resources directory (default: "resources")
        """
        self.environment = environment.upper()
        self.base_path = Path(resources_dir)
        self.env_path = self.base_path / self.environment
        self.common_path = self.base_path / "common"
        
        # Validate environment exists
        if not self.env_path.exists():
            raise ValueError(
                f"Environment '{self.environment}' not found. "
                f"Available: {self._list_environments()}"
            )
    
    def _list_environments(self) -> list:
        """List available environments."""
        if not self.base_path.exists():
            return []
        return [
            d.name for d in self.base_path.iterdir() 
            if d.is_dir() and d.name != "common"
        ]
    
    def _load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Resource file not found: {file_path}")
    
    def _load_properties_file(self, file_path: Path) -> Dict[str, str]:
        """
        Load and parse .properties file.
        
        Format: key=type:value
        Example: user_login=css:#user-name
        """
        properties = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        properties[key.strip()] = value.strip()
            
            return properties
        except FileNotFoundError:
            raise FileNotFoundError(f"Properties file not found: {file_path}")
    
    def _find_resource(self, resource_type: str, name: str, extensions: list = None) -> Path:
        """
        Find resource file, with fallback to common.
        
        Args:
            resource_type: Type of resource (json_templates, payloads, etc.)
            name: Resource name (without extension)
            extensions: List of extensions to try (default: ['.json'])
        
        Returns:
            Path to the resource file
        
        Raises:
            FileNotFoundError: If resource not found in env or common
        """
        if extensions is None:
            extensions = ['.json']
        
        # Try environment-specific first
        for ext in extensions:
            env_file = self.env_path / resource_type / f"{name}{ext}"
            if env_file.exists():
                return env_file
        
        # Fallback to common
        for ext in extensions:
            common_file = self.common_path / resource_type / f"{name}{ext}"
            if common_file.exists():
                return common_file
        
        raise FileNotFoundError(
            f"Resource '{name}' not found in {self.environment}/{resource_type} "
            f"or common/{resource_type} with extensions {extensions}"
        )
    
    @lru_cache(maxsize=128)
    def load_json_template(self, name: str) -> Dict[str, Any]:
        """
        Load JSON template for assertions.
        
        Args:
            name: Template name (without .json extension)
        
        Returns:
            Dictionary with template structure
        
        Example:
            expected = loader.load_json_template("login_response")
            assert_json_match(actual, expected)
        """
        file_path = self._find_resource("json_templates", name)
        return self._load_json_file(file_path)
    
    @lru_cache(maxsize=128)
    def load_payload(self, name: str) -> Dict[str, Any]:
        """
        Load request payload.
        
        Args:
            name: Payload name (without .json extension)
        
        Returns:
            Dictionary with payload data
        
        Example:
            payload = loader.load_payload("create_user")
            response = api.post("/users", json=payload)
        """
        file_path = self._find_resource("payloads", name)
        return self._load_json_file(file_path)
    
    @lru_cache(maxsize=128)
    def load_locators(self, page_name: str) -> Dict[str, Any]:
        """
        Load page locators/web elements from .properties or .json file.
        
        Args:
            page_name: Page name (without extension)
        
        Returns:
            Dictionary with locator definitions
        
        Examples:
            # .properties format:
            user_login=css:#user-name
            
            # .json format:
            {"user_login": {"type": "css", "value": "#user-name"}}
            
        Usage:
            locators = loader.load_locators("login_page")
            
            # If .properties:
            selector = locators["user_login"]  # "css:#user-name"
            
            # If .json:
            selector = locators["user_login"]["value"]  # "#user-name"
        """
        # Try .properties first, then .json
        file_path = self._find_resource("locators", page_name, ['.properties', '.json'])
        
        if file_path.suffix == '.properties':
            return self._load_properties_file(file_path)
        else:
            return self._load_json_file(file_path)
    
    @lru_cache(maxsize=128)
    def load_test_data(self, data_name: str) -> Dict[str, Any]:
        """
        Load test data.
        
        Args:
            data_name: Data file name (without .json extension)
        
        Returns:
            Dictionary with test data
        
        Example:
            users = loader.load_test_data("users")
            user = users["valid_users"][0]
        """
        file_path = self._find_resource("test_data", data_name)
        return self._load_json_file(file_path)
    
    def get_locator(self, page: str, element: str) -> str:
        """
        Get locator value for a specific element.
        
        Handles both .properties and .json formats automatically.
        
        Args:
            page: Page name
            element: Element name
        
        Returns:
            Locator value (CSS selector, XPath, etc.)
        
        Examples:
            # .properties format: user_login=css:#user-name
            selector = loader.get_locator("login_page", "user_login")
            # Returns: "css:#user-name" or just "#user-name"
            
            # .json format: {"user_login": {"value": "#user-name"}}
            selector = loader.get_locator("login_page","user_login")
            # Returns: "#user-name"
        """
        locators = self.load_locators(page)
        if element not in locators:
            raise KeyError(f"Element '{element}' not found in {page} locators")
        
        element_config = locators[element]
        
        # Handle .properties format (string value)
        if isinstance(element_config, str):
            # Format: "css:#selector" or "xpath://path"
            # Return full value or just the selector part
            if ':' in element_config:
                # Split and return just the selector
                _, selector = element_config.split(':', 1)
                return selector
            return element_config
        
        # Handle .json format (dict with 'value' key)
        return element_config.get("value", element_config)
    
    def get_test_user(self, user_type: str = "standard") -> Dict[str, str]:
        """
        Get test user credentials.
        
        Args:
            user_type: Type of user (standard, problem, locked, etc.)
        
        Returns:
            Dictionary with username and password
        
        Example:
            user = loader.get_test_user("standard")
            login(user["username"], user["password"])
        """
        users = self.load_test_data("users")
        
        # Try to find user in valid_users list
        if "valid_users" in users:
            for user in users["valid_users"]:
                if user.get("type") == user_type or user.get("username") == user_type:
                    return user
        
        # Fallback to direct key access
        if user_type in users:
            return users[user_type]
        
        raise KeyError(f"User type '{user_type}' not found in test data")
    
    def clear_cache(self):
        """Clear the resource cache."""
        self.load_json_template.cache_clear()
        self.load_payload.cache_clear()
        self.load_locators.cache_clear()
        self.load_test_data.cache_clear()
    
    def __repr__(self) -> str:
        return f"ResourceLoader(environment='{self.environment}')"

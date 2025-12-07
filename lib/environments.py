# environments.py
"""
Environment configuration for different test environments.
Similar to Maven profiles.
"""

ENVIRONMENTS = {
    "DEV": {
        "base_url": "https://www.saucedemo.com/",
        "username": "standard_user",
        "password": "secret_sauce",
        "timeout": 30000,
        "description": "Development environment",
    },
    "QA": {
        "base_url": "https://www.saucedemo.com/",  # Change to your QA URL
        "username": "standard_user",
        "password": "secret_sauce",
        "timeout": 30000,
        "description": "QA environment",
    },
    "STAG": {
        "base_url": "https://www.saucedemo.com/",  # Change to your STAG URL
        "username": "standard_user",
        "password": "secret_sauce",
        "timeout": 45000,
        "description": "Staging/Pre-production environment",
    },
    "PP": {
        "base_url": "https://www.saucedemo.com/",  # Change to your PP URL
        "username": "standard_user",
        "password": "secret_sauce",
        "timeout": 60000,  # Longer timeout for production-like
        "description": "Pre-production environment",
    },
}


def get_environment(env_name):
    """Get environment configuration."""
    if env_name not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {env_name}. Available: {list(ENVIRONMENTS.keys())}")
    return ENVIRONMENTS[env_name]

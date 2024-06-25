#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # Set the Environment for deployment
    DJANGO_ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')
    
    # Set the DJANGO_SETTINGS_MODULE based on DJANGO_ENVIRONMENT
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"project.settings.{DJANGO_ENVIRONMENT}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

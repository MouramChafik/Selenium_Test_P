import os
import sys
import pytest


# Ajouter le répertoire courant au PYTHONPATH
@pytest.fixture(autouse=True)
def add_project_root_to_pythonpath():
    """Ajoute automatiquement le répertoire racine du projet au PYTHONPATH."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    yield

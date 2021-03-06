from unittest import TestCase

from app.api import create_api
from app.utils.exts import db


class ApiBaseTestCase(TestCase):
    """Setups the Base configs for testing
    """

    def setUp(self) -> None:
        self. api = create_api("testing")
        self.api_context = self.api.app_context()
        self.api_context.push()
        self.client  = self.api.test_client()
        db.create_all()
    
    def tearDown(self) -> None:
        db.drop_all()
        self.api_context.pop()
        
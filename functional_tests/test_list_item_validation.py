from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        self.fail('write me!')
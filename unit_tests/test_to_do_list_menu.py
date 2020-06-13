from to_do_list_menu import *
import unittest

class PrintMenuTest(unittest.TestCase):
    def test_case_01(self):
        display_text = "1) Today's tasks\n" \
                       "2) Add task\n" \
                       "0) Exit"
        self.assertEqual(get_menu_text(), display_text)
import unittest
import tkinter as tk
from tkinter import Tk
from unittest.mock import patch, MagicMock
from SimpleRecipeManager import RecipeGUI
from unittest import TestCase, mock



class TestRecipeGUI(unittest.TestCase):
    def setUp(self):
        # Patching Tkinter's Tk() instance
        self.patcher = patch('tkinter.Tk')
        self.mock_tk = self.patcher.start()
        self.app = RecipeGUI(self.mock_tk.return_value)
       

    @patch('tkinter.Tk.mainloop')
    def test_app_doesnt_open(self, mock_mainloop):
        mock_mainloop.assert_not_called()


if __name__ == '__main__':
    unittest.main()

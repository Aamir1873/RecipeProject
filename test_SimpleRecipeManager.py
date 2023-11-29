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
    def test_add_recipe(self):
            # Mocking the open_form method
            with patch.object(self.app, 'open_form') as mock_open_form:
                # Trigger the Add Recipe button
                try:
                    self.app.add_recipe()
                except Exception as e:
                    self.fail(f"Error encountered: {e}")

                # Ensure the open_form method is called with the correct parameters
                mock_open_form.assert_called_once_with()
    @patch("tkinter.filedialog.asksaveasfilename", return_value="./TestTemp/test_export.json")
    @patch("tkinter.messagebox.showinfo")
    def test_export_recipes(self, mock_showinfo, mock_file_dialog):
        # Test exporting recipes
        self.app.recipes = {
    "Guacamole": {
        "recipe_name": "Guacamole",
        "ingredients": "Avocado\nTomato\nOnion\nLime Juice\nSalt\nCilantro",
        "instructions": "1. Mash avocados in a bowl. \n2. Add diced tomatoes, finely chopped onions, lime juice, salt, and chopped cilantro. \n3. Mix ingredients thoroughly. \n4. Serve with chips or use as a topping.",
        "category": "appetizer",
        "rating": 4
    }}
        initial_recipe_count = len(self.app.recipes)
        

        self.app.export_recipes()
        exported_recipe_count = len(self.app.recipes)

        mock_file_dialog.assert_called_once()  # Ensure file dialog was opened
        mock_showinfo.assert_called_once()  # Ensure showinfo was called

        self.assertEqual(exported_recipe_count, initial_recipe_count)
        # ...

            

if __name__ == '__main__':
    unittest.main()

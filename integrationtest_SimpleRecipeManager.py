import unittest
from unittest.mock import patch, MagicMock
from SimpleRecipeManager import RecipeGUI


class TestRecipeGUIIntegration(unittest.TestCase):
    def setUp(self):
        # Patching Tkinter's Tk() instance
        self.patcher = patch('tkinter.Tk')
        self.mock_tk = self.patcher.start()
        self.app = RecipeGUI(self.mock_tk.return_value)

##hi
    @patch('tkinter.messagebox.askyesno', return_value=True)
    def test_add_and_delete_recipe(self, mock_askyesno):
        # Add a recipe
        new_recipe = {
            "recipe_name": "Integration Test Recipe",
            "ingredients": "Ingredient 1, Ingredient 2",
            "instructions": "Step 1, Step 2",
            "category": "test",
            "rating": 4
        }

        # Add the recipe to the GUI
        self.app.add_to_database(new_recipe)
        self.app.initialize_data()
        # Verify that the recipe was added successfully
        self.assertIn("Integration Test Recipe", self.app.recipes)
        self.assertEqual(new_recipe, self.app.recipes["Integration Test Recipe"])
        intial_count = len(self.app.recipes)
        # Delete the added recipe
        with patch.object(self.app.recipe_list, 'get', return_value="Integration Test Recipe"):
            
            self.app.delete_recipe()
        current_count = len(self.app.recipes)
        # # Verify that the recipe was deleted
        self.assertNotEqual(current_count,intial_count)
 
    @patch("tkinter.filedialog.asksaveasfilename", return_value="./TestTemp/test_export.json")
    @patch("tkinter.filedialog.askopenfilename", return_value="./TestTemp/test_export.json")
    @patch("tkinter.messagebox.showinfo")
    def test_export_and_import_recipes(self, mock_showinfo, mock_open_file_dialog, mock_save_file_dialog):
        # Mock the return values for file dialogs
        self.app.recipes = {
            "Guacamole": {
                "recipe_name": "Guacamole",
                "ingredients": "Avocado\nTomato\nOnion\nLime Juice\nSalt\nCilantro",
                "instructions": "1. Mash avocados in a bowl. \n2. Add diced tomatoes, finely chopped onions, lime juice, salt, and chopped cilantro. \n3. Mix ingredients thoroughly. \n4. Serve with chips or use as a topping.",
                "category": "appetizer",
                "rating": 4
            }
        }
        initial_recipe_count = len(self.app.recipes)

        self.app.export_recipes()
        exported_recipe_count = len(self.app.recipes)

        mock_save_file_dialog.assert_called_once()  # Ensure file dialog was opened for export
        mock_showinfo.assert_called_with('Success', 'Recipes exported to JSON file.')
        self.assertEqual(exported_recipe_count, initial_recipe_count)

        # Import recipes
        self.app.import_recipes()
        self.app.initialize_data()
        imported_recipe_count = len(self.app.recipes)

        mock_open_file_dialog.assert_called_once()  # Ensure file dialog was opened for import
        mock_showinfo.assert_called_with('Success', 'Recipes imported from JSON file.')
        self.assertNotEqual(imported_recipe_count, initial_recipe_count)

if __name__ == '__main__':
    unittest.main()

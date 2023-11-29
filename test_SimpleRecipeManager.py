import unittest
import tkinter as tk
from tkinter import Tk
import json
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
    def test_add_recipe_to_database(self):
            # Mock a recipe to add to the database
            new_recipe = {
                "recipe_name": "Test Recipe",
                "ingredients": "Ingredient 1, Ingredient 2",
                "instructions": "Step 1, Step 2",
                "category": "test",
                "rating": 4
            }

            # Add the recipe to the database
            added_recipe = self.app.add_to_database(new_recipe)
            # Check if the recipe was added successfully by reading the database file
            with open("Recipe_database.json", "r") as data_file:
                data = json.load(data_file)
                self.assertIn("Test Recipe", data)  # Check if the recipe name exists in the database
                self.assertEqual(data["Test Recipe"], new_recipe)  # Check if the added recipe matches the expected one
            with open("Recipe_database.json", "w") as data_file:
                 json.dump(self.app.recipes, data_file, indent=4)
    
    # def test_view_recipe(self):
    #         # Mocking the open_form method
    #         with patch.object(self.app, 'open_form') as mock_open_form:
    #             # Trigger the View Recipe button
    #             try:
    #                 self.app.view_recipe()
    #             except Exception as e:
    #                 self.fail(f"Error encountered: {e}")

    #             # Ensure the open_form method is called with the correct parameters
    #             mock_open_form.assert_called_once_with(self.app.recipes["Guacamole"])

    # def test_edit_recipe(self):
    #         # Mocking the open_form method
    #         with patch.object(self.app, 'open_form') as mock_open_form:
    #             # Trigger the Edit Recipe button
    #             try:
    #                 self.app.edit_recipe()
    #             except Exception as e:
    #                 self.fail(f"Error encountered: {e}")

    #             # Ensure the open_form method is called with the correct parameters
    #             mock_open_form.assert_called_once_with()

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
    
    @patch("tkinter.filedialog.askopenfilename", return_value="./TestTemp/test_export.json")
    @patch("tkinter.messagebox.showinfo")
    def test_import_recipes(self, mock_showinfo, mock_file_dialog):
        # Test importing recipes
        self.app.recipes = {"Test Recipe":{
            "recipe_name": "Test Recipe",
            "ingredients": "Ingredient 1, Ingredient 2",
            "instructions": "Step 1, Step 2",
            "rating": 4
        }}
        initial_recipe_count = len(self.app.recipes)


        # Import recipes
        self.app.import_recipes()
        imported_recipe_count = len(self.app.recipes)

        mock_file_dialog.assert_called_once()  # Ensure file dialog was opened
        mock_showinfo.assert_called_once()  # Ensure showinfo was called
        self.assertNotEqual(imported_recipe_count, initial_recipe_count)
    
    @patch('tkinter.messagebox.askyesno', return_value=True)
    def test_delete_recipe_successful(self, mock_askyesno):
        # Setup initial conditions
        self.app.recipes = {
            "Recipe1": {
                "recipe_name": "Recipe1",
                "ingredients": "Ingredient1",
                "instructions": "Step1",
                "rating": 5
            },
            # Add more recipes as needed for testing scenarios
        }
        initial_recipe_count = len(self.app.recipes)

        # Patching del_from_database method
        with patch.object(self.app, 'del_from_database', new=MagicMock()) as mock_del_from_database:
            # Trigger the delete_recipe method with a valid recipe
            with patch.object(self.app.recipe_list, 'get', return_value="Recipe1"):
                self.app.delete_recipe()

        # Check if the recipe was deleted and the necessary methods were called
        self.assertEqual(len(self.app.recipes), initial_recipe_count - 1)
        mock_del_from_database.assert_called()  


            

if __name__ == '__main__':
    unittest.main()

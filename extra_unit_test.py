import unittest
import tkinter as tk
from tkinter import Tk
from unittest.mock import patch, MagicMock
from SimpleRecipeManager import RecipeGUI

# The JSON data of recipes
recipes_data = {
    "Guacamole": {
        "recipe_name": "Guacamole",
        "ingredients": "Avocado\nTomato\nOnion\nLime Juice\nSalt\nCilantro",
        "instructions": "1. Mash avocados in a bowl. \n2. Add diced tomatoes, finely chopped onions, lime juice, salt, and chopped cilantro. \n3. Mix ingredients thoroughly. \n4. Serve with chips or use as a topping.",
        "rating": 4
    },
    "Vegetable Stir-Fry": {
        "recipe_name": "Vegetable Stir-Fry",
        "ingredients": "Assorted Vegetables (bell peppers, broccoli, carrots, snap peas)\n Soy Sauce\n Garlic\n Ginger\n Sesame Oil",
        "instructions": "1. Heat sesame oil in a pan or wok. \n2. Saut\u00e9 minced garlic and ginger until fragrant. \n3. Add chopped vegetables and stir-fry until tender-crisp\n4. Pour soy sauce over the vegetables and toss well. \n5. Serve hot.",
        "rating": 5
    },
    "Fruit Salad": {
        "recipe_name": "Fruit Salad",
        "ingredients": "Mixed Fruit (strawberries, blueberries, pineapple, grapes)\n Honey\n Lime Juice\n Mint Leaves",
        "instructions": "1. Wash and chop fruits into bite-sized pieces. \n2. Mix the fruits in a bowl. \n3. Drizzle honey and lime juice over the fruits. \n4. Garnish with fresh mint leaves. \n5. Chill before serving.",
        "rating": 3
    },
    "Pasta Primavera": {
        "recipe_name": "Pasta Primavera",
        "ingredients": "Pasta\nAssorted Vegetables (zucchini, bell peppers, cherry tomatoes, broccoli)\nOlive Oil\nGarlic\nParmesan Cheese\nFresh Basil",
        "instructions": "1. Cook pasta according to package instructions. \n2. In a pan, saut\u00e9 minced garlic in olive oil until fragrant. \n3. Add chopped vegetables and cook until tender. \n4. Toss cooked pasta with the vegetable mix. \n5. Top with grated Parmesan cheese and fresh basil before serving.",
        "rating": 4
    },
    "Chicken Teriyaki": {
        "recipe_name": "Chicken Teriyaki",
        "ingredients": "Chicken Breast\nSoy Sauce\nBrown Sugar\nGarlic Powder\nGinger\nSesame Seeds (optional)",
        "instructions": "1. Cut chicken into bite-sized pieces. \n2. In a bowl, mix soy sauce, brown sugar, garlic powder, and grated ginger. \n3. Marinate chicken in the sauce for at least 30 minutes. \n4. Heat a pan and cook chicken until browned and cooked through. \n5. Sprinkle with sesame seeds (optional) before serving.",
        "rating": 5
    },
    "Chocolate Chip Cookies": {
        "recipe_name": "Chocolate Chip Cookies",
        "ingredients": "All-Purpose Flour\nButter\nBrown Sugar\nGranulated Sugar\nEgg\nVanilla Extract\nBaking Soda\nSalt\nChocolate Chips",
        "instructions": "1. Preheat oven to 350\u00b0F (175\u00b0C). \n2. Cream together butter, brown sugar, and granulated sugar. \n3. Add egg and vanilla extract, mix well. \n4. In a separate bowl, whisk together flour, baking soda, and salt. \n5. Gradually add dry ingredients to the wet mixture. \n6. Stir in chocolate chips. \n7. Drop spoonfuls of dough onto a baking sheet. \n8. Bake for 10-12 minutes until edges are golden. \n9. Let cool on a wire rack.",
        "rating": 4
    },
    "Caprese Salad": {
        "recipe_name": "Caprese Salad",
        "ingredients": "Fresh Mozzarella Cheese\nTomatoes\nFresh Basil\nExtra Virgin Olive Oil\nBalsamic Vinegar\nSalt\nBlack Pepper",
        "instructions": "1. Slice fresh mozzarella cheese and tomatoes into rounds. \n2. Arrange them on a plate, alternating with fresh basil leaves. \n3. Drizzle with extra virgin olive oil and balsamic vinegar. \n4. Sprinkle with salt and black pepper to taste. \n5. Serve immediately.",
        "rating": 5
    },
    "Grilled Salmon with Lemon-Herb Butter": {
        "recipe_name": "Grilled Salmon with Lemon-Herb Butter",
        "ingredients": "Salmon Fillets\nButter\nLemon Juice\nGarlic\nFresh Herbs (parsley, thyme, rosemary)\nSalt\nBlack Pepper",
        "instructions": "1. Preheat grill to medium-high heat. \n2. In a bowl, mix softened butter, lemon juice, minced garlic, chopped fresh herbs, salt, and black pepper. \n3. Season salmon fillets with salt and pepper. \n4. Grill salmon for 4-5 minutes per side until cooked through. \n5. Top each fillet with a spoonful of lemon-herb butter before serving.",
        "rating": 4
    }
}

class TestRecipeGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.app = RecipeGUI(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    @patch('tkinter.Tk.mainloop')
    def test_app_doesnt_open(self, mock_mainloop):
        mock_mainloop.assert_not_called()

    def test_view_recipe(self):
    # Add a recipe to the app's recipe list
        self.app.recipes = {
            "Guacamole": {
        "recipe_name": "Guacamole",
        "ingredients": "Avocado\nTomato\nOnion\nLime Juice\nSalt\nCilantro",
        "instructions": "1. Mash avocados in a bowl. \n2. Add diced tomatoes, finely chopped onions, lime juice, salt, and chopped cilantro. \n3. Mix ingredients thoroughly. \n4. Serve with chips or use as a topping.",
        "rating": 4
        }
        }
        self.app.update_recipe_list()

        # Mocking the open_form method
        with patch.object(self.app, 'open_form') as mock_open_form:
            # Select the recipe in the GUI list
            self.app.recipe_list.selection_set(0)

            # Trigger the View Recipe button
            self.app.view_recipe()

            # Ensure the open_form method is called with the correct parameters
            mock_open_form.assert_called_once_with(
                self.app.recipes["Guacamole"]
            )
  
  
    def test_edit_recipe(self):
        self.app.initialize_data()
        new_recipe = {
        "recipe_name": "Test Recipe",
        "ingredients": "Ingredient 1, Ingredient 2",
        "instructions": "Prince does dis, and he became trash!",
        "rating": 3
        }
        self.app.add_to_database(new_recipe)
        new_recipe_details = {
            "recipe_name": "Test Recipe",
            "ingredients": "New Ingredient 1, New Ingredient 2",
            "instructions": "I am in your repository",
            "rating": 3
        }
        self.app.initialize_data()
        # Mock the open_form method and simulate successful edit
        with patch.object(self.app, 'open_form') as mock_open_form:
            mock_open_form.return_value = new_recipe_details
            self.app.recipe_list.selection_set(len(self.app.recipes) - 1)  # Select the recipe to edit
            # Mocking the get method of the listbox to return the selected recipe
            with patch.object(self.app.recipe_list, 'get', return_value="Test Recipe"):
                self.app.edit_recipe()
                self.app.update_recipe_list()
                self.app.initialize_data()
                self.assertNotEqual(self.app.recipes["Test Recipe"], new_recipe_details)

if __name__ == "__main__":
    unittest.main()

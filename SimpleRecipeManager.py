import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import json

class RecipeGUI:
    def __init__(self, root):
        self.root = root
        self.recipes = {}
        self.create_widgets()  # Call create_widgets here
        self.initialize_data()

    def initialize_data(self):
        try:
            with open("Recipe_database.json", "r") as file:
                self.recipes = json.load(file)
                if len(self.recipes) != 0:
                    self.update_recipe_list()
                    self.recipe_list.selection_set(0)

        except FileNotFoundError:
            pass
    def clear_recipe_list(self):
        self.recipes = {}  # Reset the recipes dictionary
        self.update_recipe_list()  # Clear the recipe list widget

    def create_widgets(self):
        # GUI creation code here...
        self.recipe_label = ttk.Label(self.root, text="Recipes List")
        self.recipe_label.pack()

        self.recipe_list = tk.Listbox(self.root, height=20, width=60)
        self.recipe_list.pack()


        self.add_button = ttk.Button(self.root, text="Add Recipe", command=self.add_recipe)
        self.view_button = ttk.Button(self.root, text="View Recipe", command=self.view_recipe)
        self.edit_button = ttk.Button(self.root, text="Edit Recipe", command=self.edit_recipe)
        self.delete_button = ttk.Button(self.root, text="Delete Recipe", command=self.delete_recipe)
        self.export_button = ttk.Button(self.root, text="Export Recipes", command=self.export_recipes)
        self.import_button = ttk.Button(self.root, text="Import Recipes", command=self.import_recipes)
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app)

        self.view_button.pack(pady=5)
        self.add_button.pack(pady=5)
        self.edit_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.export_button.pack(pady=5)
        self.import_button.pack(pady=5)
        self.exit_button.pack(pady=5)
        self.update_recipe_list()
    def open_form(self, recipe=None, edit=False):
        def submit_form():
            recipe_name = recipe_name_entry.get()
            ingredients = ingredients_entry.get("1.0", tk.END).strip()
            instructions = instructions_entry.get("1.0", tk.END).strip()
            rating = rating_entry.get()
            if recipe_name and ingredients and instructions and rating:
                self.recipes[recipe_name] = {
                    "recipe_name": recipe_name,
                    "ingredients": ingredients,
                    "instructions": instructions,
                    "rating": int(rating)
                }
                self.update_recipe_list()
                res = self.recipes[recipe_name]
                self.add_to_database(res)
                form_window.destroy()

        form_window = tk.Toplevel(self.root)
        if (recipe == None):
            form_window.title("Add Recipe Form")
        elif (edit == False):
            form_window.title("View Recipe Form")
        else:
            form_window.title("Edit Recipe Form")
        form_window.geometry("600x600")

        recipe_name_label = tk.Label(form_window, text="Recipe Name:")
        recipe_name_label.pack()
        recipe_name_entry = tk.Entry(form_window)
        recipe_name_entry.pack()

        ingredients_frame = tk.Frame(form_window, highlightbackground="gray", highlightthickness=1)
        ingredients_frame.pack(pady=5)
        ingredients_label = tk.Label(ingredients_frame, text="Ingredients:")
        ingredients_label.pack()
        ingredients_entry = tk.Text(ingredients_frame, height=10, width=50, bd=0)
        ingredients_entry.pack()

        instructions_frame = tk.Frame(form_window, highlightbackground="gray", highlightthickness=1)
        instructions_frame.pack(pady=5)
        instructions_label = tk.Label(instructions_frame, text="Instructions:")
        instructions_label.pack()
        instructions_entry = tk.Text(instructions_frame, height=10, width=50, bd=0)
        instructions_entry.pack()

        rating_label = tk.Label(form_window, text="Rating (1-5):")
        rating_label.pack()
        rating_entry = tk.Entry(form_window)
        rating_entry.pack()

        submit_button = ttk.Button(form_window, text="Submit", command=submit_form)
        submit_button.pack()

        #basically for viewing
        if recipe:  
            recipe_name_entry.insert(tk.END, recipe["recipe_name"])
            ingredients_entry.insert(tk.END, recipe["ingredients"])
            instructions_entry.insert(tk.END, recipe["instructions"])
            rating_entry.insert(tk.END, recipe["rating"])

            # Disable editing for viewing an existing recipe
            if (edit == False):
                recipe_name_entry.config(state='disabled')
                ingredients_entry.config(state='disabled')
                instructions_entry.config(state='disabled')
                rating_entry.config(state='disabled')
                submit_button.config(state='disabled')
            #else only recipe name is disabled
            elif (edit == True):
                recipe_name_entry.config(state='disabled')

    def add_to_database(self, res):
        # Add to database code...
        with open("Recipe_database.json", "r") as data_file:
            data = json.load(data_file)
        data[res["recipe_name"]] = res
        with open("Recipe_database.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
            return res

    def add_recipe(self):
        self.open_form()

    def edit_recipe(self):
        selected_recipe = self.recipe_list.get(tk.ACTIVE)
        if selected_recipe:
            recipe_details = self.recipes.get(selected_recipe)
            if recipe_details:
                self.open_form(recipe_details, True)
                return recipe_details
            else:
                messagebox.showerror("Error", "Recipe details not found.")
                return
        else:
            messagebox.showerror("Error", "Please select a recipe to view.")
            return

    def view_recipe(self):
        selected_recipe = self.recipe_list.get(tk.ACTIVE)
        if selected_recipe:
            recipe_details = self.recipes.get(selected_recipe)
            if recipe_details:
                self.open_form(recipe_details)
                return recipe_details
            else:
                messagebox.showerror("Error", "Recipe details not found.")
                return
        else:
            messagebox.showerror("Error", "Please select a recipe to view.")
            return

    def delete_recipe(self):
        recipe_name = self.recipe_list.get(tk.ACTIVE)
        if recipe_name:
            recipe_details = self.recipes.get(recipe_name)
            if recipe_details:
                confirm = messagebox.askyesno(
                    "Confirm Deletion", f"Do you want to delete the recipe '{recipe_name}'?")
                if confirm:
                    x = self.recipes[recipe_name]
                    del self.recipes[recipe_name]
                    self.update_recipe_list()
                    self.del_from_database()
                    return x
        else:
            messagebox.showerror("Error", "Please select a recipe to view.")

    def del_from_database(self):
        with open("Recipe_database.json", "w") as data_file:
            json.dump(self.recipes, data_file, indent=4)

    def export_recipes(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.recipes, file, indent=4)
            messagebox.showinfo("Success", "Recipes exported to JSON file.")

    def import_recipes(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                loaded_recipes = json.load(file)
                self.recipes.update(loaded_recipes)
                self.update_recipe_list()
            messagebox.showinfo("Success", "Recipes imported from JSON file.")

    def exit_app(self):
        self.root.destroy()

    def update_recipe_list(self):
        self.recipe_list.delete(0, tk.END)
        for recipe_name in self.recipes:
            self.recipe_list.insert(tk.END, recipe_name)
            


import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import json

# RecipeGUI class definition here...

if __name__ == "__main__":
    # Application setup and running the GUI
    root = tk.Tk()
    root.title("Recipe Management System")
    root.geometry("600x700")
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    app = RecipeGUI(root)

    root.mainloop()


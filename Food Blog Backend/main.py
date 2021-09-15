from os import name
import sqlite3
import argparse
import sys


class Blog:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('food_blog.db')
        self.cursor_name = self.conn.cursor()
        self.first_connection()
        self.get_order()
        self.multiple_args()

    def first_connection(self):
        self.cursor_name.execute('PRAGMA foreign_keys = ON;')
        self.cursor_name.execute('''
        CREATE Table IF NOT EXISTS meals (
            meal_id INT PRIMARY KEY,
            meal_name UNIQUE NOT NULL
        );''')
        self.conn.commit()
        self.cursor_name.execute('''
        CREATE TABLE IF NOT EXISTS ingredients(
            ingredient_id INT PRIMARY KEY,
            ingredient_name VARCHAR(200) UNIQUE NOT NULL
        );''')
        self.conn.commit()
        self.cursor_name.execute('''
        CREATE TABLE IF NOT EXISTS measures(
            measure_id INT PRIMARY KEY,
            measure_name VARCHAR(200) UNIQUE
        );''')
        self.conn.commit()
        self.cursor_name.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INT PRIMARY KEY,
            recipe_name VARCHAR(200) NOT NULL,
            recipe_description VARCHAR(200)
        );
        ''')
        self.conn.commit()
        self.cursor_name.execute('''
        CREATE TABLE IF NOT EXISTS serve (
            serve_id INT PRIMARY KEY,
            meal_id INT NOT NULL,
            recipe_id INT NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(meal_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        );
        ''')
        self.conn.commit()
        self.cursor_name.execute('''
        CREATE TABLE IF NOT EXISTS quantity(
            quantity_id INT PRIMARY KEY,
            quantity INT NOT NULL,
            recipe_id INT NOT NULL,
            measure_id INT NOT NULL,
            ingredient_id INT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
            FOREIGN KEY (measure_id) REFERENCES measures(measure_id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
        );
        ''')
        self.conn.commit()
        cou = self.cursor_name.execute('SELECT * FROM meals WHERE meal_id = (SELECT MAX(meal_id) FROM meals)')
        index_cou = cou.fetchone()
        b = False
        if index_cou is None:
            b = True
        
        if len(sys.argv) <= 2 and b:
            self.cursor_name.execute('''
            INSERT INTO meals (meal_id, meal_name) VALUES (1, 'breakfast'), (2, 'brunch'), (3, 'lunch'), (4, 'supper');''')
            self.conn.commit()
            self.cursor_name.execute('''
            INSERT INTO ingredients (ingredient_id, ingredient_name) VALUES (1, 'milk'), (2, 'cacao'), (3, 'strawberry'), (4, 'blueberry'), (5, 'blackberry'), (6, 'sugar');
            ''')
            self.conn.commit()
            measures = ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")
            i = 1
            for measure in measures:
                self.cursor_name.execute(f'INSERT INTO measures (measure_id, measure_name) VALUES ({i}, "{measure}");')
                self.conn.commit()
                i += 1

    def get_order(self):
        if len(sys.argv) <= 2:
            while True:
                print('Pass the empty recipe name to exit.')
                recipe_name = input('Recipe name: ')
                if recipe_name == '':
                    break
                recipe_desc = input('Recipe_description: ')

                recipe_time = ['breakfast', 'brunch', 'lunch', 'supper']
                for index, elem in enumerate(recipe_time):
                    print(str(index + 1) + ') ' + elem, end=' ')
                print()
                numbers = [int(x) for x in input('Enter proposed meals separated by a space: ').split()]

                count_recipe = self.cursor_name.execute('SELECT * FROM recipes WHERE recipe_id = (SELECT MAX(recipe_id) FROM recipes)')
                index_recipe = count_recipe.fetchone()
                if index_recipe is None:
                    index_recipe = 1
                else:
                    index_recipe = int(index_recipe[0]) + 1
                self.conn.commit()

                self.cursor_name.execute(
                    f'INSERT INTO recipes (recipe_id, recipe_name, recipe_description) VALUES ({index_recipe}, "{recipe_name}", "{recipe_desc}");')
                self.conn.commit()

                count_recipe = self.cursor_name.execute('SELECT * FROM recipes WHERE recipe_id = (SELECT MAX(recipe_id) FROM recipes)')
                index_recipe = count_recipe.fetchone()
                if index_recipe is None:
                    index_recipe = 1
                else:
                    index_recipe = int(index_recipe[0])
                self.conn.commit()

                count = self.cursor_name.execute('Select * FROM serve Where serve_id = (SELECT MAX(serve_id) FROM serve)')
                index_serve = count.fetchone()
                if index_serve is None:
                    index_serve = 1
                else:
                    index_serve = int(index_serve[0]) + 1
                for i in numbers:
                    self.cursor_name.execute(f'INSERT INTO serve (serve_id, meal_id, recipe_id) VALUES ({index_serve}, {i}, {index_recipe});')
                    self.conn.commit()
                    index_serve += 1

                measures = ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")
                ingredients = ('milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar')
                while True:
                    count_quantity = self.cursor_name.execute('Select * from quantity where quantity_id = (select max(quantity_id) from quantity)')
                    index_quantity = count_quantity.fetchone()
                    if index_quantity is None:
                        index_quantity = 1
                    else:
                        index_quantity = int(index_quantity[0]) + 1

                    i_quantity = input('Input quantity of ingredient <press enter to stop>: ').split()
                    if len(i_quantity) == 0:
                        break
                    
                    if len(i_quantity) == 3:
                
                        quantity = int(i_quantity[0])
                        recipe_id = index_recipe
                        total_n = len([x for x in measures if i_quantity[1] in x])
                        total_ing = len([x for x in ingredients if i_quantity[2] in x])
                        if total_n == 1:
                            if total_ing == 1:
                                measure = [x for x in measures if i_quantity[1] in x][0]
                                ing = [x for x in ingredients if i_quantity[2] in x][0]
                                self.cursor_name.execute(f'INSERT INTO quantity (quantity_id, quantity, recipe_id, measure_id, ingredient_id) VALUES({index_quantity}, {quantity}, {recipe_id}, {measures.index(measure) + 1}, {ingredients.index(ing) + 1})')
                                self.conn.commit()
                            else:
                                print('The ingredient is not conclusive!')
                        else:
                            print('The measure is not conclusive!')

                    elif len(i_quantity) == 2:
                        quantity = int(i_quantity[0])
                        recipe_id = index_recipe
                        measure = measures.index("") + 1
                        total_ing = len([x for x in ingredients if i_quantity[1] in x])
                        if total_ing == 1:
                            ing = [x for x in ingredients if i_quantity[1] in x][0]
                            self.cursor_name.execute(f'INSERT INTO quantity (quantity_id, quantity, recipe_id, measure_id, ingredient_id) VALUES ({index_quantity}, {quantity}, {recipe_id}, {measure}, {ingredients.index(ing) + 1})')
                            self.conn.commit()
                        else:
                            print('The ingredient is not conclusive!')
                        

    def multiple_args(self):
        if len(sys.argv) <= 2:
            return 0

        parser = argparse.ArgumentParser()
        parser.add_argument('database_name')
        parser.add_argument('--ingredients')
        parser.add_argument('--meals')
        args = parser.parse_args()
        list_ingredients = args.ingredients.split(',')
        list_meals = args.meals.split(',')

        index = self.cursor_name.execute('select * from quantity where quantity_id = (select max(quantity_id) from quantity)')
        index = index.fetchall()
        if index is None:
            index = 1
        else:
            index = [x for x in index[0]][2]

        ingredients = ['milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar']
        recipe_time = ['breakfast', 'brunch', 'lunch', 'supper']
        name_list = []
        i = 1
        while i < index + 1:
            recipe_list = self.cursor_name.execute(f'select recipe_id, measure_id, ingredient_id from quantity where recipe_id={i}')
            self.conn.commit()
            i_list = recipe_list.fetchall()

            meal_list = self.cursor_name.execute(f'select meal_id recipe_id from serve where recipe_id=({i})')
            self.conn.commit()
            m_list = meal_list.fetchall()
            m_list = [x[0] for x in m_list]  # meal list
            i_list = [x[2] for x in i_list]  # ingredient list
            i_list = [ingredients[x - 1] for x in i_list]
            m_list = [recipe_time[x - 1] for x in m_list]
            i_result = all(x in i_list for x in list_ingredients)
            m_result = any(x in m_list for x in list_meals)

            if i_result is True and m_result is True:
                recipe_name = self.cursor_name.execute(f'select recipe_name from recipes where recipe_id={i}')
                self.conn.commit()
                r_name = recipe_name.fetchone()
                name_list.insert(0, r_name[0])

            
            i += 1 


        if len(name_list) > 0: 
            name_list = ', '.join(name_list)
            print('Recipes selected for you:', name_list)
        else:
            print('There are no such recipes in the database.')
        
        self.conn.close()



blog = Blog()
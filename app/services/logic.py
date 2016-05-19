import collections

from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, oid
import app.models as models
from config import POSTS_PER_PAGE
import json


def get_user_by_username(user_name):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.username == user_name).one()
    return user_schema.dump(user).data


def get_user_by_email(email):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.email == email).one()
    return user_schema.dump(user).data


def get_user_by_id(_id):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.id == _id).one()
    return user_schema.dump(user).data


def get_users():
    users_schema = models.UserSchema(many=True)
    users = models.User.query.all()
    return users_schema.dump(users).data


def get_recipe(recipe_id):
    recipe_schema = models.RecipeSchema()
    recipe = models.Recipe.query.filter(models.Recipe.id == recipe_id).one()
    print(recipe)
    return recipe_schema.dump(recipe).data


def get_recipes():
    recipes_schema = models.RecipeSchema(many=True)
    recipes = models.Recipe.query.all()
    return recipes_schema.dump(recipes).data


def get_ingredient(_id):
    ingredient_schema = models.IngredientSchema()
    ingredient = models.Ingredient.query.filter(models.Ingredient.id == _id).one()
    return ingredient_schema.dump(ingredient).data


def get_ingredients():
    ingredients_schema = models.IngredientSchema(many=True)
    ingredients = models.Ingredient.query.all()
    return ingredients_schema.dump(ingredients).data


def get_step(recipe_id, step_id):
    step_schema = models.StepSchema()
    step = models.Step.query.filter(models.Step.recipe_id == recipe_id, models.Step.id == step_id).one()
    return step_schema.dump(step).data


def get_steps(recipe_id):
    steps_schema = models.StepSchema(many=True)
    steps = models.Step.query.all()
    return steps_schema.dump(steps).data


def get_menu(menu_id):
    menu_schema = models.MenuSchema()
    menu = models.Menu.query.filter(models.Menu.id == menu_id).one()
    return menu_schema.dump(menu).data


def get_menus():
    menu_schema = models.MenuSchema(many=True)
    menus = models.Menu.query.all()
    return menu_schema.dump(menus).data


def get_client(client_id):
    client_schema = models.ClientSchema()
    client = models.Client.query.filter(models.Client.id == client_id).one()
    return client_schema.dump(client).data


def get_clients():
    client_schema = models.ClientSchema(many=True)
    clients = models.Client.query.all()
    print(clients)
    return client_schema.dump(clients).data


def get_client_recipe(client_id, recipe_id):
    recipe_schema = models.RecipeSchema()
    # recipe = models.Recipe.query.filter(models.Client.id == client_id, models.Recipe.id == recipe_id).one()
    recipe = db.session.query(models.Recipe) \
        .join(models.client_recipes) \
        .join(models.Client) \
        .filter(models.Client.id == client_id, models.Client.id == models.client_recipes.c.client_id,
                models.client_recipes.c.recipe_id == recipe_id).one()
    return recipe_schema.dump(recipe).data


def get_client_recipes(client_id):
    client_recipes_schema = models.RecipeSchema(many=True)
    recipes = db.session.query(models.Recipe) \
        .join(models.client_recipes) \
        .join(models.Client) \
        .filter(models.Client.id == client_id, models.Client.id == models.client_recipes.c.client_id).all()
    return client_recipes_schema.dump(recipes).data


def get_menu_recipe(menu_id, recipe_id):
    recipe_schema = models.RecipeSchema()
    recipe = db.session.query(models.Recipe) \
        .join(models.MenuRecipe) \
        .filter(models.MenuRecipe.menu_id == menu_id, models.MenuRecipe.recipe_id == models.Recipe.id).one()
    return recipe_schema.dump(recipe).data


def get_menu_recipes(menu_id):
    client_recipes_schema = models.RecipeSchema(many=True)
    recipes = db.session.query(models.Recipe) \
        .join(models.MenuRecipe) \
        .filter(models.MenuRecipe.menu_id == menu_id).all()
    return client_recipes_schema.dump(recipes).data


def create_client(name, nickname, email, home, mobile=None, work=None):
    client = models.Client()
    client.name = name
    client.nickname = nickname
    client.email = email
    client.home_phone = home
    client.work_phone = work
    client.mobile_phone = mobile

    db.session.add(client)
    db.session.commit()

    client_schema = models.ClientSchema()
    client_tuple = collections.namedtuple('ClientData', ['id', 'data'])
    result = client_tuple(id=client.id, data=client_schema.dump(client).data)

    return result


def create_client_recipe(client_id, recipe_name, description=None, style=None, type=None):
    client = models.Client.query.filter(models.Client.id == client_id).one()
    recipe = models.Recipe()
    recipe.name = recipe_name
    recipe.description = description
    recipe.style = style
    recipe.type = type
    client.add_recipe(recipe)

    db.session.commit()

    recipe_schema = models.RecipeSchema()
    recipe_tuple = collections.namedtuple('RecipeData', ['id', 'data'])
    result = recipe_tuple(id=recipe.id, data=recipe_schema.dump(recipe).data)
    return result


def edit_recipe(recipe_id, recipe_name, description=None, style=None, type=None):
    recipe = models.Recipe.query.filter(models.Recipe.id == recipe_id).one()
    recipe.name = recipe_name or recipe.name
    recipe.description = description or recipe.description
    recipe.style = style or recipe.style
    recipe.type = type or recipe.type

    db.session.commit()

    recipe_schema = models.RecipeSchema()
    recipe_tuple = collections.namedtuple('RecipeData', ['id', 'data'])
    result = recipe_tuple(id=recipe.id, data=recipe_schema.dump(recipe).data)
    return result


def edit_ingredient(id, name=None, description=None, nutrition=None, is_allergen=None, type=None):
    ingredient = models.Ingredient.query.filter(models.Ingredient.id == id).one()
    ingredient.name = name or ingredient.name
    ingredient.description = description or ingredient.description
    ingredient.nutrition = description or ingredient.nutrition
    ingredient.is_allergen = is_allergen or ingredient.is_allergen
    ingredient.type = type or ingredient.type

    db.session.commit()

    ingredient_schema = models.IngredientSchema()
    ingredient_tuple = collections.namedtuple('IngredientData', ['id', 'data'])
    result = ingredient_tuple(id=ingredient.id, data=ingredient_schema.dump(ingredient).data)
    return result


def create_step(recipe_id, order_no, instructions):
    recipe = models.Recipe.query.filter(models.Recipe.id == recipe_id).one()
    step = models.Step()
    step.recipe_id = recipe_id
    step.order_no = order_no
    step.instructions = instructions
    recipe.add_step(step)

    db.session.commit()

    step_schema = models.StepSchema()
    step_tuple = collections.namedtuple('StepData', ['id', 'data'])
    result = step_tuple(id=step.id, data=step_schema.dump(step).data)
    return result


def create_recipe(name, description=None, style=None, type=None):
    recipe = models.Recipe()
    recipe.name = name or None
    recipe.description = description or None
    recipe.style = style or None
    recipe.type = type or None
    db.session.add(recipe)
    db.session.commit()

    recipe_schema = models.RecipeSchema()
    recipe_tuple = collections.namedtuple('RecipeData', ['id', 'data'])
    result = recipe_tuple(id=recipe.id, data=recipe_schema.dump(recipe).data)
    return result


def edit_step(step_id, recipe_id, order_no, instructions):
    step = models.Step.query.filter(models.Step.id == step_id, models.Step.recipe_id == recipe_id).one()
    step.recipe_id = recipe_id
    step.order_no = order_no
    step.instructions = instructions

    db.session.commit()

    step_schema = models.StepSchema()
    step_tuple = collections.namedtuple('StepData', ['id', 'data'])

    result = step_tuple(id=step.id, data=step_schema.dump(step).data)
    return result


def delete_recipe(recipe_id):
    recipe = models.Recipe.query.filter(models.Recipe.id == recipe_id).one()
    db.session.delete(recipe)
    db.session.commit()


def delete_step(step_id):
    step = models.Step.query.filter(models.Step.id == step_id).one()
    db.session.delete(step)
    db.session.commit()


def create_ingredient(name, description=None, nutrition=None, is_allergen=None, type=None):
    ingredient = models.Ingredient()
    ingredient.name = name or ingredient.name
    ingredient.description = description or ingredient.description
    ingredient.nutrition = nutrition or ingredient.nutrition
    ingredient.is_allergen = is_allergen or ingredient.is_allergen
    ingredient.type = type or ingredient.type

    db.session.add(ingredient)
    db.session.commit()

    ingredient_schema = models.IngredientSchema()
    ingredient_tuple = collections.namedtuple('IngredientData', ['id', 'data'])
    result = ingredient_tuple(id=ingredient.id, data=ingredient_schema.dump(ingredient).data)
    return result


def edit_menu(id, start_date, description, end_date):
    menu = models.Menu.query.filter(models.Menu.id == id).one()
    menu.description = description or None
    menu.start_date = datetime.strptime(start_date, '%d/%m/%Y') or None
    menu.end_date = datetime.strptime(end_date, '%d/%m/%Y') or None

    db.session.commit()

    menu_schema = models.MenuSchema()
    menu_tuple = collections.namedtuple('MenuData', ['id', 'data'])
    result = menu_tuple(id=menu.id, data=menu_schema.dump(menu).data)
    return result


def create_menu(start_date, description, end_date):
    menu = models.Menu()
    menu.description = description or None
    menu.start_date = datetime.strptime(start_date, '%d/%m/%Y')
    menu.end_date = datetime.strptime(end_date, '%d/%m/%Y')
    db.session.add(menu)
    db.session.commit()

    menu_schema = models.MenuSchema()
    menu_tuple = collections.namedtuple('MenuData', ['id', 'data'])
    result = menu_tuple(id=menu.id, data=menu_schema.dump(menu).data)
    return result


def delete_menu(menu_id):
    menu = models.Menu.query.filter(models.Menu.id == menu_id).one()
    db.session.delete(menu)
    db.session.commit()


def delete_ingredient(ingredient_id):
    ingredient = models.Ingredient.query.filter(models.Ingredient.id == ingredient_id).one()
    db.session.delete(ingredient)
    db.session.commit()


def delete_client(client_id):
    client = models.Client.query.filter(models.Client.id == client_id).one()
    db.session.delete(client)
    db.session.commit()

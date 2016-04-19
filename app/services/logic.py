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


def get_recipe(_id):
    recipe_schema = models.RecipeSchema()
    recipe = models.Recipe.query.filter(models.Recipe.id == _id).one()
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

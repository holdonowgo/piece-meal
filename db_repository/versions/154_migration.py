from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
allergen_alternative = Table('allergen_alternative', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('notes', String(length=50)),
    Column('alt_ingredient_id', Integer),
)

client = Table('client', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('home_phone', String(length=10)),
    Column('mobile_phone', String(length=10)),
    Column('work_phone', String(length=10)),
)

client_allergens = Table('client_allergens', post_meta,
    Column('client_id', Integer),
    Column('ingredient_id', Integer),
)

client_menu = Table('client_menu', post_meta,
    Column('client_id', Integer),
    Column('menu_id', Integer),
)

client_recipes = Table('client_recipes', post_meta,
    Column('client_id', Integer),
    Column('recipe_id', Integer),
)

ingredient = Table('ingredient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('nutrition', String(length=128)),
    Column('description', String(length=256)),
    Column('is_allergen', Boolean, default=ColumnDefault(True)),
    Column('timestamp', DateTime),
    Column('type', Enum('seafood', 'dairy', 'tree_nut', name='allergen_groups')),
)

menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('start_date', DateTime),
    Column('end_date', DateTime),
)

menu_recipe = Table('menu_recipe', post_meta,
    Column('menu_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

order_item = Table('order_item', post_meta,
    Column('order_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('each_serving', Integer, nullable=False),
    Column('each_cost', DECIMAL),
)

recipe = Table('recipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128), nullable=False),
    Column('description', String(length=128)),
    Column('style', Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style')),
    Column('type', Enum('breakfast', 'lunch', 'dinner', 'snack', 'sauce', 'bread', 'dessert', name='recipe_type')),
)

recipe_ingredients = Table('recipe_ingredients', post_meta,
    Column('recipe_id', Integer),
    Column('ingredient_id', Integer),
)

step = Table('step', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('order_no', Integer),
    Column('recipe_id', Integer),
    Column('instructions', String(length=256)),
)

step_ingredient = Table('step_ingredient', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('measurement', String(length=50)),
)

step_sub_recipe = Table('step_sub_recipe', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('measurement', String(length=50)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['allergen_alternative'].create()
    post_meta.tables['client'].create()
    post_meta.tables['client_allergens'].create()
    post_meta.tables['client_menu'].create()
    post_meta.tables['client_recipes'].create()
    post_meta.tables['ingredient'].create()
    post_meta.tables['menu'].create()
    post_meta.tables['menu_recipe'].create()
    post_meta.tables['order'].create()
    post_meta.tables['order_item'].create()
    post_meta.tables['recipe'].create()
    post_meta.tables['recipe_ingredients'].create()
    post_meta.tables['step'].create()
    post_meta.tables['step_ingredient'].create()
    post_meta.tables['step_sub_recipe'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['allergen_alternative'].drop()
    post_meta.tables['client'].drop()
    post_meta.tables['client_allergens'].drop()
    post_meta.tables['client_menu'].drop()
    post_meta.tables['client_recipes'].drop()
    post_meta.tables['ingredient'].drop()
    post_meta.tables['menu'].drop()
    post_meta.tables['menu_recipe'].drop()
    post_meta.tables['order'].drop()
    post_meta.tables['order_item'].drop()
    post_meta.tables['recipe'].drop()
    post_meta.tables['recipe_ingredients'].drop()
    post_meta.tables['step'].drop()
    post_meta.tables['step_ingredient'].drop()
    post_meta.tables['step_sub_recipe'].drop()
    post_meta.tables['user'].drop()

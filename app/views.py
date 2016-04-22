from os import abort

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify, abort, \
    make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, oid
from .forms import LoginForm, IngredientEditForm, EditClientForm, EditStepForm, SignUpForm
# from .models import User, Recipe, Ingredient, Step, Client
import models
from config import POSTS_PER_PAGE
import json
from sqlalchemy.orm.exc import NoResultFound
from services import logic
from flask_swagger import swagger


@login_required
@app.route('/')
@app.route('/index')
def index():
    # client = {'name': 'Randall'}  # fake user
    client = models.Client.query.filter_by(id=1).first()
    # allergens = [  # fake array of allergens
    #     {
    #         'client': {'name': 'Randall'},
    #         'name': 'Black Pepper'
    #     },
    #     {
    #         'client': {'name': 'Susan'},
    #         'name': 'Corn'
    #     }
    # ]
    allergens = client._allergens.all()
    return render_template("index.html",
                           title='Home',
                           client=client,
                           allergens=allergens)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated:
    # return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            session['remember_me'] = form.remember_me.data
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data,
                           username=form.username.data,
                           password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}!  Please Login'.format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    user = models.User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you
        # require that.
        user = models.User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route('/recipe/book')
def recipe_book(page=1):
    recipes = models.Recipe.get_catalogue().paginate(page, POSTS_PER_PAGE, False)
    return render_template('recipe_book.html',
                           recipes=recipes)


# @app.route('/recipe/<name>')
@app.route('/recipe/<int:_id>')
@login_required
def recipe(_id, page=1):
    r = models.Recipe.query.filter_by(id=_id).first()
    if r is None:
        # flash('Recipe %s not found.' % r.name)
        flash('Recipe not found.')
        return redirect(url_for('index'))
    ingredients = r.ingredients.paginate(page, POSTS_PER_PAGE, False)
    steps = r.steps.paginate(page, POSTS_PER_PAGE, False)
    return render_template('recipe.html',
                           recipe=r,
                           ingredients=ingredients,
                           steps=steps)


@app.route('/recipe/<int:recipe_id>/step/<int:step_id>')
def step(recipe_id, step_id):
    s = models.Step.query.filter_by(recipe_id=recipe_id, id=step_id).first()
    return render_template('step.html', step=s)


@app.route('/recipe/<int:recipe_id>/step/<int:step_id>/edit')
@login_required
def edit_step(recipe_id, step_id):
    s = models.Step.query.filter_by(recipe_id=recipe_id, id=step_id).first()
    form = EditStepForm()
    if s is None:
        # flash('Recipe %s not found.' % r.name)
        flash('Recipe Step not found.')
        return redirect(url_for('recipe'))
    elif form.validate_on_submit():
        s.order_no = form.order_no.data
        s.instructions = form.instructions.data
        # s.ingredients = form.ingredients.data
        db.session.add(s)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('step'))
    # elif request.method != "POST":
    form.order_no.data = s.order_no
    form.instructions.data = s.instructions
    # form.ingredients.data = s.ingredientsV2.all()
    ingredients = s.ingredientsV2.all()
    ingredients_all = models.Ingredient.all()
    return render_template('edit_step.html', step=s, form=form, ingredients=ingredients,
                           ingredients_all=ingredients_all)


@app.route('/ingredient/<int:_id>')
def ingredient(_id):
    i = models.Ingredient.query.get(_id)
    return render_template('ingredient.html', ingredient=i)


@app.route('/ingredient/<int:_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_ingredient(_id):
    i = models.Ingredient.query.get(_id)
    form = IngredientEditForm()
    if i is None:
        # flash('Recipe %s not found.' % r.name)
        flash('Ingredient not found.')
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        i.name = form.name.data
        i.description = form.description.data
        db.session.add(i)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('ingredient'))
    elif request.method != "POST":
        form.name.data = i.name
        form.nutrition.data = i.nutrition
        form.description.data = i.description
        form.is_allergen.data = i.is_allergen
    return render_template('edit_ingredient.html', form=form)


@app.route('/client/<int:_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_client(_id):
    c = models.Client.query.get(_id)
    form = EditClientForm()
    if form.validate_on_submit():
        c.name = form.name.data
        c.nickname = form.nickname.data
        c.email = form.email.data
        c.mobile_phone = form.mobile_phone.data
        # g.user.about_me = form.about_me.data
        db.session.add(c)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('client'))
    else:
        form.name.data = c.name
        form.nickname.data = c.nickname
        form.email.data = c.email
        form.mobile_phone.data = c.mobile_phone
        # form.about_me.data = g.user.about_me
    return render_template('edit_client.html', form=form)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    NAMES = ["betty", "jane", "lance", "brock"]
    search = request.args.get('autocomplete')

    for arg in request.args:
        app.logger.debug(arg)

    app.logger.debug(search)
    app.logger.debug('THIS HAPPENED')
    return Response(json.dumps(NAMES), mimetype='application/json')


@app.context_processor
def inject_ingredients():
    return dict(all_ingredients=models.Ingredient.all)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Piece Meal API"
    swag['info']['paths'] = ('/piece-meal/api/v1.0/users', '/piece-meal/api/v1.0/recipes')
    return jsonify(swag)


@app.route('/piece-meal/api/v1.0/users', methods=['GET'])
def _get_users():
    try:
        users = logic.get_users()
    except NoResultFound:
        abort(404)
    return jsonify({'users': users})


@app.route('/piece-meal/api/v1.0/users/<int:id>', methods=['GET'])
def _get_user_by_id(id):
    try:
        users = logic.get_user_by_id(_id=id)
    except NoResultFound:
        abort(404)
    return jsonify({'users': users})


@app.route('/piece-meal/api/v1.0/users/<email>', methods=['GET'])
def _get_user_by_email(email):
    try:
        users = logic.get_user_by_email(email=email)
    except NoResultFound:
        abort(404)
    return jsonify({'users': users})


@app.route('/piece-meal/api/v1.0/users/<username>', methods=['GET'])
def _get_user_by_username(user_name):
    try:
        users = logic.get_user_by_username(user_name=user_name)
    except NoResultFound:
        abort(404)
    return jsonify({'users': users})


@app.route('/piece-meal/api/v1.0/ingredients/<int:id>', methods=['GET', 'PUT'])
def _get_ingredient(id):
    if request.method == 'GET':
        try:
            ingredient = logic.get_ingredient(_id=id)
        except NoResultFound:
            abort(404)
        return jsonify({'ingredient': ingredient})

    elif request.method == 'PUT':
        name = request.form['name']
        description = request.form['description']
        nutrition = request.form['nutrition']
        is_allergen = request.form['is_allergen']
        type = request.form['type']
        result = logic.edit_ingredient(id=id,
                                       name=name,
                                       description=description,
                                       nutrition=nutrition,
                                       is_allergen=is_allergen,
                                       type=type)

        resp = jsonify({'ingredient': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        # Get the parsed contents of the form data
        json = request.json
        print(json)
        # # Render template
        # return jsonify(json)

        return resp


@app.route('/piece-meal/api/v1.0/ingredients', methods=['GET'])
def _get_ingredients():
    try:
        ingredients = logic.get_ingredients()
    except NoResultFound:
        abort(404)
    return jsonify({'ingredients': ingredients})


@app.route('/piece-meal/api/v1.0/menus/<int:menu_id>', methods=['GET'])
def _get_menu(menu_id):
    try:
        menu = logic.get_menu(menu_id=menu_id)
    except NoResultFound:
        abort(404)
    return jsonify({'menu': menu})


@app.route('/piece-meal/api/v1.0/menus', methods=['GET'])
def _get_menus():
    try:
        menus = logic.get_menus()
    except NoResultFound:
        abort(404)
    return jsonify({'menus': menus})


@app.route('/piece-meal/api/v1.0/clients', methods=['GET', 'POST'])
def _create_client():
    if request.method == 'GET':
        try:
            clients = logic.get_clients()
        except NoResultFound:
            abort(404)

        resp = jsonify({'clients': clients})
        resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients'
        resp.status_code = 200

    elif request.method == 'POST':
        client = models.Client()
        name = request.form['name']
        nickname = request.form['nickname']
        email = request.form['email']
        home = request.form['home']
        mobile = request.form['mobile']
        work = request.form['work']

        result = logic.create_client(name=name,
                                     nickname=nickname,
                                     email=email,
                                     home=home,
                                     mobile=mobile,
                                     work=work)

        resp = jsonify({'client': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/clients/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/clients/<int:client_id>', methods=['GET', 'PUT'])
def _get_client(client_id):
    if request.method == 'GET':
        try:
            client = logic.get_client(client_id=client_id)
        except NoResultFound:
            abort(404)

        resp = jsonify({'client': client})
        resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients'
        resp.status_code = 200

        return resp

        # js = json.dumps(client)
        #
        # resp = Response(response=js, status=200, mimetype='application/json')
        # resp.headers['Location'] = 'localhost:5000/piece-mea/index'
        #
        # return resp

    elif request.method == 'PUT':
        name = request.form['name']
        nickname = request.form['nickname']
        email = request.form['email']
        home = request.form['home']
        mobile = request.form['mobile']
        work = request.form['work']
        result = logic.edit_client(name=name,
                                   nickname=nickname,
                                   email=email,
                                   home=home,
                                   mobile=mobile,
                                   work=work)

        resp = jsonify({'client': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/client/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/clients/<int:client_id>/recipes', methods=['GET', 'POST'])
def _client_recipes(client_id):
    if request.method == 'GET':
        try:
            recipes = logic.get_client_recipes(client_id)
        except NoResultFound:
            abort(404)

        resp = jsonify({'recipes': recipes})
        resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients/{0}/recipes'.format(client_id)
        resp.status_code = 200

    elif request.method == 'POST':
        client_id = request.form['client_id']
        recipe_name = request.form['recipe_name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        result = logic.create_client_recipe(client_id=client_id,
                                            recipe_name=recipe_name,
                                            description=description,
                                            style=style,
                                            type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 201
        resp.headers['Location'] = '/cah/api/v1.0/clients/{0}/recipes/{1}'.format(client_id, result.id)
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/clients/<int:client_id>/recipes/<int:recipe_id>', methods=['GET'])
def _get_client_recipe(client_id, recipe_id):
    if request.method == 'GET':
        try:
            recipe = logic.get_client_recipe(client_id=client_id, recipe_id=recipe_id)
        except NoResultFound:
            abort(404)
        return jsonify({'recipe': recipe})

    elif request.method == 'PUT':
        recipe_name = request.form['recipe_name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        result = logic.edit_recipe(recipe_id=recipe_id,
                                   recipe_name=recipe_name,
                                   description=description,
                                   style=style,
                                   type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/recipes', methods=['GET', 'POST'])
def _get_recipes():
    if request.method == 'GET':
        try:
            recipe = logic.get_recipes()
        except NoResultFound:
            abort(404)
        return jsonify({'recipe': recipe})

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        result = logic.create_recipe(name=name,
                                     description=description,
                                     style=style,
                                     type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def _get_recipe(recipe_id):
    if request.method == 'GET':
        try:
            recipe = logic.get_recipe(recipe_id=recipe_id)
        except NoResultFound:
            abort(404)

        resp = jsonify({'recipe': recipe.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(recipe.id)
        resp.autocorrect_location_header = False

        return resp

    elif request.method == 'PUT':
        recipe_name = request.form['recipe_name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        result = logic.edit_recipe(recipe_id=recipe_id,
                                   recipe_name=recipe_name,
                                   description=description,
                                   style=style,
                                   type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 201
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        # Get the parsed contents of the form data
        json = request.json
        print(json)
        # Render template

        return resp

    elif request.method == 'POST':
        recipe_id = request.form['recipe_id']
        logic.delete_recipe(recipe_id)

        resp = Response()
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes'
        resp.autocorrect_location_header = False

        return resp


@app.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>/steps', methods=['GET', 'POST'])
def _get_step(recipe_id, step_id):
    if request.method == 'GET':
        try:
            step = logic.get_step(recipe_id=recipe_id, step_id=step_id)
        except NoResultFound:
            abort(404)
        return jsonify({'step': step})

    elif request.method == 'PUT':
        name = request.form['name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        id = request.form['id']

        result = logic.edit_recipe(recipe_id=recipe_id,
                                   recipe_name=name,
                                   description=description,
                                   style=style,
                                   type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        # Get the parsed contents of the form data
        json = request.json
        print(json)
        # Render template

        return resp

    elif request.method == 'PUT':
        logic.delete_recipe(recipe_id)


@app.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>/steps/<int:step_id>', methods=['GET', 'PUT', 'DELETE'])
def recipe_step(recipe_id, step_id):
    if request.method == 'GET':
        try:
            steps = logic.get_steps(recipe_id=recipe_id)
        except NoResultFound:
            abort(404)
        return jsonify({'steps': steps})

    elif request.method == 'PUT':
        recipe_id = request.form['recipe_id']
        order_no = request.form['order_no']
        instructions = request.form['instructions']
        result = logic.edit_step(step_id=step_id,
                                 recipe_id=recipe_id,
                                 order_no=order_no,
                                 instructions=instructions)

        resp = jsonify({'step': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}/steps/{1}'.format(recipe_id, result.id)
        resp.autocorrect_location_header = False

        return resp

    elif request.method == 'DELETE':
        logic.delete_step(step_id)

        resp = Response()
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}/steps'
        resp.autocorrect_location_header = False

        return  resp


@app.route('/piece-meal/api/v1.0/menus/<int:menu_id>/recipes/<int:recipe_id>', methods=['GET'])
def _get_menu_recipe(menu_id, recipe_id):
    try:
        recipe = logic.get_menu_recipe(menu_id=menu_id, recipe_id=recipe_id)
    except NoResultFound:
        abort(404)
    return jsonify({'recipe': recipe})


@app.route('/piece-meal/api/v1.0/menus/<int:menu_id>/recipes', methods=['GET', 'POST'])
def _get_menu_recipes(menu_id):
    if request.method == 'GET':
        try:
            recipes = logic.get_menu_recipes(menu_id)
        except NoResultFound:
            abort(404)
        return jsonify({'recipes': recipes})

    elif request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']
        style = request.form['style']
        type = request.form['type']
        result = logic.create_recipe(description=description,
                                     style=style,
                                     type=type)

        resp = jsonify({'recipe': result.data})
        resp.status_code = 200
        resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
        resp.autocorrect_location_header = False

        # Get the parsed contents of the form data
        json = request.json
        print(json)
        # Render template

        return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

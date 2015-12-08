from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, IngredientEditForm
from .models import User, Recipe, Ingredient, Step, Client
from config import POSTS_PER_PAGE


@app.route('/')
@app.route('/index')
def index():
    # client = {'name': 'Randall'}  # fake user
    client = Client.query.filter_by(id=1).first()
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
    allergens = client.allergens.all()
    return render_template("index.html",
                           title='Home',
                           client=client,
                           allergens=allergens)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    user = User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you
        # require that.
        user = User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route('/recipe/book')
def recipe_book(page=1):
    recipes = Recipe.get_catalogue().paginate(page, POSTS_PER_PAGE, False)
    return render_template('recipe_book.html',
                           recipes=recipes)


# @app.route('/recipe/<name>')
@app.route('/recipe/<int:_id>')
# @login_required
def recipe(_id, page=1):
    r = Recipe.query.filter_by(id=_id).first()
    if r is None:
        flash('Recipe %s not found.' % r.name)
        return redirect(url_for('index'))
    ingredients = r.ingredients.paginate(page, POSTS_PER_PAGE, False)
    steps = recipe.steps.paginate(page, POSTS_PER_PAGE, False)
    return render_template('recipe.html',
                           recipe=r,
                           ingredients=ingredients,
                           steps=steps)


@app.route('/recipe/<int:recipe_id>/step/<int:step_id>')
def step(recipe_id, step_id):
    s = Step.query.filter_by(recipe_id=recipe_id, id=step_id).first()
    return render_template('step.html', step=s)


@app.route('/ingredient/<int:_id>')
def ingredient(_id):
    i = Ingredient.query.get(_id)
    return render_template('ingredient.html', ingredient=i)


@app.route('/ingredient/<int:_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit(_id):
    i = Ingredient.query.get(_id)
    form = IngredientEditForm(int(_id))
    if form.validate_on_submit():
        i.name = form.name.data
        i.description = form.description.data
        db.session.add(i)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('ingredient'))
    elif request.method != "POST":
        form.name.data = i.name
        form.description.data = i.description
    return render_template('edit_ingredient.html', form=form)

# END OAuth

# from app import models
# from flask import request, Response, jsonify, abort
# from flask_swagger import swagger
# from os import abort
# import services
# from sqlalchemy.orm.exc import NoResultFound
# from . import api
#
# from .. import app
# app.register_blueprint(api, url_prefix='/piece-meal/api/v1.0')
#
# @api.route('/search')
# def search():
#     pass
#
# @api.route("/spec")
# def spec():
#     swag = swagger(api)
#     swag['info']['version'] = "1.0"
#     swag['info']['title'] = "Piece Meal API"
#     swag['info']['paths'] = ('/piece-meal/api/v1.0/users', '/piece-meal/api/v1.0/recipes')
#     return jsonify(swag)
#
#
# @api.route('/users', methods=['GET'])
# def _get_users():
#     try:
#         users = services.get_users()
#     except NoResultFound:
#         abort(404)
#     return jsonify({'users': users})
#
#
# @api.route('/piece-meal/api/v1.0/users/<int:id>', methods=['GET'])
# def _get_user_by_id(id):
#     try:
#         users = services.get_user_by_id(_id=id)
#     except NoResultFound:
#         abort(404)
#     return jsonify({'users': users})
#
#
# @api.route('/piece-meal/api/v1.0/users/<email>', methods=['GET'])
# def _get_user_by_email(email):
#     try:
#         users = services.get_user_by_email(email=email)
#     except NoResultFound:
#         abort(404)
#     return jsonify({'users': users})
#
#
# @api.route('/piece-meal/api/v1.0/users/<username>', methods=['GET'])
# def _get_user_by_username(user_name):
#     try:
#         users = services.get_user_by_username(user_name=user_name)
#     except NoResultFound:
#         abort(404)
#     return jsonify({'users': users})
#
#
# @api.route('/piece-meal/api/v1.0/ingredients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def _get_ingredient(id):
#     if request.method == 'GET':
#         try:
#             ingredient = services.get_ingredient(_id=id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'ingredient': ingredient})
#
#     elif request.method == 'PUT':
#         name = request.form['name']
#         description = request.form['description']
#         nutrition = request.form['nutrition']
#         is_allergen = request.form['is_allergen']
#         type = request.form['type']
#         result = services.edit_ingredient(id=id,
#                                        name=name,
#                                        description=description,
#                                        nutrition=nutrition,
#                                        is_allergen=is_allergen,
#                                        type=type)
#
#         resp = jsonify({'ingredient': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # # Render template
#         # return jsonify(json)
#
#         return resp
#
#     elif request.method == 'DELETE':
#         services.delete_ingredient(ingredient_id=id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/ingredients/<int:id>/alternatives', methods=['GET', 'PUT', 'DELETE'])
# def _get_alt_ingredients(id):
#     if request.method == 'GET':
#         try:
#             alternatives = services.get_alt_ingredients(_id=id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'alternatives': alternatives})
#
#     elif request.method == 'PUT':
#         name = request.form['name']
#         description = request.form['description']
#         nutrition = request.form['nutrition']
#         is_allergen = request.form['is_allergen']
#         type = request.form['type']
#         result = services.edit_ingredient(id=id,
#                                        name=name,
#                                        description=description,
#                                        nutrition=nutrition,
#                                        is_allergen=is_allergen,
#                                        type=type)
#
#         resp = jsonify({'ingredient': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # # Render template
#         # return jsonify(json)
#
#         return resp
#
#     elif request.method == 'DELETE':
#         services.delete_ingredient(ingredient_id=id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/ingredients', methods=['GET', 'POST'])
# def _get_ingredients():
#     if request.method == 'GET':
#         try:
#             ingredients = services.get_ingredients()
#         except NoResultFound:
#             abort(404)
#         return jsonify({'ingredients': ingredients})
#
#     elif request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         nutrition = request.form['nutrition']
#         is_allergen = request.form['is_allergen']
#         type = request.form['type']
#         result = services.create_ingredient(name=name,
#                                          description=description,
#                                          nutrition=nutrition,
#                                          is_allergen=is_allergen,
#                                          type=type)
#
#         resp = jsonify({'ingredient': result.data})
#         resp.status_code = 201
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # # Render template
#         # return jsonify(json)
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/menus/<int:menu_id>', methods=['GET', 'PUT', 'DELETE'])
# def _get_menu(menu_id):
#     if request.method == 'GET':
#         try:
#             menu = services.get_menu(menu_id=menu_id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'menu': menu})
#
#     elif request.method == 'PUT':
#         id = request.form['menu_id']
#         description = request.form['description']
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']
#         result = services.edit_menu(id=id,
#                                  start_date=start_date,
#                                  description=description,
#                                  end_date=end_date)
#
#         resp = jsonify({'ingredient': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # # Render template
#         # return jsonify(json)
#
#         return resp
#
#     elif request.method == 'DELETE':
#         services.delete_menu(menu_id=menu_id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/menus'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/menus', methods=['GET', 'POST'])
# def _get_menus():
#     if request.method == 'GET':
#         try:
#             menus = services.get_menus()
#         except NoResultFound:
#             abort(404)
#         return jsonify({'menus': menus})
#
#     elif request.method == 'POST':
#         description = request.form['description']
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']
#         result = services.create_menu(id=id,
#                                    start_date=start_date,
#                                    description=description,
#                                    end_date=end_date)
#
#         resp = jsonify({'ingredient': result.data})
#         resp.status_code = 201
#         resp.headers['Location'] = '/cah/api/v1.0/ingredients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # # Render template
#         # return jsonify(json)
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/clients/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
# def _get_client(client_id):
#     if request.method == 'GET':
#         try:
#             client = services.get_client(client_id=client_id)
#         except NoResultFound:
#             abort(404)
#
#         resp = jsonify({'client': client})
#         resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients'
#         resp.status_code = 200
#
#         return resp
#
#         # js = json.dumps(client)
#         #
#         # resp = Response(response=js, status=200, mimetype='application/json')
#         # resp.headers['Location'] = 'localhost:5000/piece-mea/index'
#         #
#         # return resp
#
#     elif request.method == 'PUT':
#         name = request.form['name']
#         nickname = request.form['nickname']
#         email = request.form['email']
#         home = request.form['home']
#         mobile = request.form['mobile']
#         work = request.form['work']
#         result = services.edit_client(name=name,
#                                    nickname=nickname,
#                                    email=email,
#                                    home=home,
#                                    mobile=mobile,
#                                    work=work)
#
#         resp = jsonify({'client': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/client/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#     elif request.method == 'DELETE':
#         services.delete_client(client_id=client_id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/clients'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/clients', methods=['GET', 'POST'])
# def _create_client():
#     if request.method == 'GET':
#         try:
#             clients = services.get_clients()
#         except NoResultFound:
#             abort(404)
#
#         resp = jsonify({'clients': clients})
#         resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients'
#         resp.status_code = 200
#
#     elif request.method == 'POST':
#         client = models.Client()
#         name = request.form['name']
#         nickname = request.form['nickname']
#         email = request.form['email']
#         home = request.form['home']
#         mobile = request.form['mobile']
#         work = request.form['work']
#
#         result = services.create_client(name=name,
#                                      nickname=nickname,
#                                      email=email,
#                                      home=home,
#                                      mobile=mobile,
#                                      work=work)
#
#         resp = jsonify({'client': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/clients/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/clients/<int:client_id>/recipes', methods=['GET', 'POST'])
# def _client_recipes(client_id):
#     if request.method == 'GET':
#         try:
#             recipes = services.get_client_recipes(client_id)
#         except NoResultFound:
#             abort(404)
#
#         resp = jsonify({'recipes': recipes})
#         resp.headers['Location'] = 'localhost:5000/piece-meal/api/v1.0/clients/{0}/recipes'.format(client_id)
#         resp.status_code = 200
#
#     elif request.method == 'POST':
#         client_id = request.form['client_id']
#         recipe_name = request.form['recipe_name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         result = services.create_client_recipe(client_id=client_id,
#                                             recipe_name=recipe_name,
#                                             description=description,
#                                             style=style,
#                                             type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 201
#         resp.headers['Location'] = '/cah/api/v1.0/clients/{0}/recipes/{1}'.format(client_id, result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/clients/<int:client_id>/recipes/<int:recipe_id>', methods=['GET'])
# def _get_client_recipe(client_id, recipe_id):
#     if request.method == 'GET':
#         try:
#             recipe = services.get_client_recipe(client_id=client_id, recipe_id=recipe_id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'recipe': recipe})
#
#     elif request.method == 'PUT':
#         recipe_name = request.form['recipe_name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         result = services.edit_recipe(recipe_id=recipe_id,
#                                    recipe_name=recipe_name,
#                                    description=description,
#                                    style=style,
#                                    type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/recipes', methods=['GET', 'POST'])
# def _get_recipes():
#     if request.method == 'GET':
#         try:
#             recipe = services.get_recipes()
#         except NoResultFound:
#             abort(404)
#         return jsonify({'recipe': recipe})
#
#     elif request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         result = services.create_recipe(name=name,
#                                      description=description,
#                                      style=style,
#                                      type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>', methods=['GET', 'PUT', 'DELETE'])
# def _get_recipe(recipe_id):
#     if request.method == 'GET':
#         try:
#             recipe = services.get_recipe(recipe_id=recipe_id)
#         except NoResultFound:
#             abort(404)
#
#         resp = jsonify({'recipe': recipe.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(recipe.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#     elif request.method == 'PUT':
#         recipe_name = request.form['recipe_name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         result = services.edit_recipe(recipe_id=recipe_id,
#                                    recipe_name=recipe_name,
#                                    description=description,
#                                    style=style,
#                                    type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 201
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # Render template
#
#         return resp
#
#     elif request.method == 'POST':
#         recipe_id = request.form['recipe_id']
#         services.delete_recipe(recipe_id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>/steps', methods=['GET', 'POST'])
# def _get_step(recipe_id, step_id):
#     if request.method == 'GET':
#         try:
#             step = services.get_step(recipe_id=recipe_id, step_id=step_id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'step': step})
#
#     elif request.method == 'PUT':
#         name = request.form['name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         id = request.form['id']
#
#         result = services.edit_recipe(recipe_id=recipe_id,
#                                    recipe_name=name,
#                                    description=description,
#                                    style=style,
#                                    type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # Render template
#
#         return resp
#
#     elif request.method == 'PUT':
#         services.delete_recipe(recipe_id)
#
#
# @api.route('/piece-meal/api/v1.0/recipes/<int:recipe_id>/steps/<int:step_id>', methods=['GET', 'PUT', 'DELETE'])
# def recipe_step(recipe_id, step_id):
#     if request.method == 'GET':
#         try:
#             steps = services.get_steps(recipe_id=recipe_id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'steps': steps})
#
#     elif request.method == 'PUT':
#         recipe_id = request.form['recipe_id']
#         order_no = request.form['order_no']
#         instructions = request.form['instructions']
#         result = services.edit_step(step_id=step_id,
#                                  recipe_id=recipe_id,
#                                  order_no=order_no,
#                                  instructions=instructions)
#
#         resp = jsonify({'step': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}/steps/{1}'.format(recipe_id, result.id)
#         resp.autocorrect_location_header = False
#
#         return resp
#
#     elif request.method == 'DELETE':
#         services.delete_step(step_id)
#
#         resp = Response()
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}/steps'
#         resp.autocorrect_location_header = False
#
#         return resp
#
#
# @api.route('/piece-meal/api/v1.0/menus/<int:menu_id>/recipes/<int:recipe_id>', methods=['GET'])
# def _get_menu_recipe(menu_id, recipe_id):
#     try:
#         recipe = services.get_menu_recipe(menu_id=menu_id, recipe_id=recipe_id)
#     except NoResultFound:
#         abort(404)
#     return jsonify({'recipe': recipe})
#
#
# @api.route('/piece-meal/api/v1.0/menus/<int:menu_id>/recipes', methods=['GET', 'POST'])
# def _get_menu_recipes(menu_id):
#     if request.method == 'GET':
#         try:
#             recipes = services.get_menu_recipes(menu_id)
#         except NoResultFound:
#             abort(404)
#         return jsonify({'recipes': recipes})
#
#     elif request.method == 'POST':
#         id = request.form['id']
#         name = request.form['name']
#         description = request.form['description']
#         style = request.form['style']
#         type = request.form['type']
#         result = services.create_recipe(description=description,
#                                      style=style,
#                                      type=type)
#
#         resp = jsonify({'recipe': result.data})
#         resp.status_code = 200
#         resp.headers['Location'] = '/cah/api/v1.0/recipes/{0}'.format(result.id)
#         resp.autocorrect_location_header = False
#
#         # Get the parsed contents of the form data
#         json = request.json
#         print(json)
#         # Render template
#
#         return resp
#
#
# @api.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 404
#
#     return resp
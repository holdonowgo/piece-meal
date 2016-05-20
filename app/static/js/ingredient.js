$(document).ready(function () {
    function IngredientsViewModel() {
        var self = this;
        self.ingredientsURI = 'http://localhost:5000/piece-meal/api/v1.0/ingredients';
        self.username = "monty";
        self.password = "python";
        self.ingredients = ko.observableArray();

        self.ajax = function (uri, method, data) {
            var request = {
                url: uri,
                type: method,
                contentType: "application/json",
                accepts: "application/json",
                cache: false,
                dataType: 'json',
                data: JSON.stringify(data),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("Authorization",
                        "Basic " + btoa(self.username + ":" + self.password));
                },
                error: function (jqXHR) {
                    console.log("ajax error " + jqXHR.status);
                }
            };
            return $.ajax(request);
        }

        self.beginAdd = function () {
            $('#add').modal('show');
        }
        self.beginEdit = function (ingredient) {
            editIngredientViewModel.setIngredient(ingredient);
            $('#edit').modal('show');
        }

        self.edit = function (ingredient, data) {
            self.ajax(ingredient.uri(), 'PUT', data).done(function (res) {
                self.updateIngredient(ingredient, res.ingredient);
            });
            // alert(JSON.stringify(data));
        }

        self.updateIngredient = function (ingredient, newIngredient) {
            var i = self.ingredients.indexOf(ingredient);
            self.ingredients()[i].uri(newIngredient.uri);
            self.ingredients()[i].name(newIngredient.name);
            self.ingredients()[i].description(newIngredient.description);
            self.ingredients()[i].nutrition(newIngredient.nutrition);
            self.ingredients()[i].is_allergen(newIngredient.is_allergen);
            self.ingredients()[i].type(newIngredient.type);
        }

        self.remove = function (ingredient) {
            self.ajax(ingredient.uri(), 'DELETE').done(function () {
                self.ingredients.remove(ingredient);
                alert(ingredient);
            });
        }

        self.markNotAllergen = function (ingredient) {
            self.ajax(ingredient.uri(), 'PUT', {is_allergen: false}).done(function (res) {
                self.updateIngredient(ingredient, res.ingredient);
            });
        }

        self.markAllergen = function (ingredient) {
            self.ajax(ingredient.uri(), 'PUT', {is_allergen: true}).done(function (res) {
                self.updateIngredient(ingredient, res.ingredient);
            });
        }

        self.ajax(self.ingredientsURI, 'GET').done(function (data) {
            for (var i = 0; i < data.ingredients.length; i++) {
                self.ingredients.push({
                    uri: ko.observable(data.ingredients[i].uri),
                    type: ko.observable(data.ingredients[i].type),
                    name: ko.observable(data.ingredients[i].name),
                    description: ko.observable(data.ingredients[i].description),
                    nutrition: ko.observable(data.ingredients[i].nutrition),
                    is_allergen: ko.observable(data.ingredients[i].is_allergen)
                });
            }
        });

        self.add = function (ingredient) {
            self.ajax(self.ingredientsURI, 'POST', ingredient).done(function (data) {
                self.ingredients.push({
                    uri: ko.observable(data.ingredient.uri),
                    name: ko.observable(data.ingredient.name),
                    description: ko.observable(data.ingredient.description),
                    nutrition: ko.observable(data.ingredient.nutrition),
                    is_allergen: ko.observable(data.ingredient.is_allergen),
                type: ko.observable(data.ingredient.type)
                });
            });
        }
    }

    function AddIngredientViewModel() {
        var self = this;
        self.name = ko.observable();
        self.description = ko.observable();
        self.nutrition = ko.observable();
        self.is_allergen = ko.observable();
        self.type = ko.observable();

        self.addIngredient = function () {
            $('#add').modal('hide');
            var data = {
                name: self.name(),
                nutrition: self.nutrition(),
                description: self.description(),
                is_allergen: self.is_allergen(),
                type: self.type()
            };
            ingredientsViewModel.add(data);
            self.name("");
            self.description("");
            self.nutrition("");
            self.is_allergen(false);
            self.type();
        }
    }

    function EditIngredientViewModel() {
        var self = this;
        self.name = ko.observable();
        self.description = ko.observable();
        self.nutrition = ko.observable();
        self.is_allergen = ko.observable();
        self.type = ko.observable();

        self.setIngredient = function (ingredient) {
            self.ingredient = ingredient;
            self.name(ingredient.name());
            self.description(ingredient.description());
            self.nutrition(ingredient.nutrition());
            self.is_allergen(ingredient.is_allergen());
            self.type(ingredient.type());
            $('edit').modal('show');
        }

        self.editIngredient = function () {
            $('#edit').modal('hide');
            ingredientsViewModel.edit(self.ingredient, {
                name: self.name(),
                description: self.description(),
                nutrition: self.nutrition(),
                is_allergen: self.is_allergen(),
                type: self.type()
            });
        }
    }

    var ingredientsViewModel = new IngredientsViewModel();
    var addIngredientViewModel = new AddIngredientViewModel();
    var editIngredientViewModel = new EditIngredientViewModel();

    ko.applyBindings(ingredientsViewModel, $('#main')[0]);
    ko.applyBindings(addIngredientViewModel, $('#add')[0]);
    ko.applyBindings(editIngredientViewModel, $('#edit')[0]);

});

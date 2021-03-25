from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_appbuilder.api import (expose, rison, safe, schemas, BaseApi,
                                  BaseModelApi)
# from flask_appbuilder.security.api import SecurityApi
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.widgets import ListThumbnail

from . import appbuilder, db, models


# class UserApiSchema(schemas.BaseModelSchema):
#     pass

# class UserApi(ModelRestApi):
#     resource_name = 'users'
#     datamodel = SQLAInterface(User)
#     add_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                            'changed_on']
#     edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                             'changed_on']
#     show_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                              'password', 'first_name', 'last_name',
#                              'login_count']
#     list_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                              'password', 'first_name', 'last_name',
#                              'login_count', 'fail_login_count']
#     list_columns = ['active', 'username', 'first_name', 'last_name']


class PublicMenuApi(ModelRestApi):
    resource_name = 'menu_cards'
    base_permissions = ['can_get', 'can_get_list']
    allow_browser_login = True
    datamodel = SQLAInterface(models.MenuCard)

    @safe
    @expose("/")
    def get_list(self, **kwargs):
        """Get item from Model
        ---
        get:
          description: >-
            Get an item model
          responses:
            200:
              description: Item from Model
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      id:
                        description: The item id
                        type: string
                      result:
                        $ref: '#/components/schemas/{
                        {self.__class__.__name__}}.get_list'
        """
        return self.get_list()

    # list_model_schema =
    # @expose('/')
    # def list_all(self):
    #     """List all available Menu Cards
    #     ---
    #     get:
    #       responses:
    #         200:
    #           description: Menu Cards
    #           content:
    #             application/json:
    #               schema:
    #                 properties:
    #                   dishes: $ref: #/components/schemas/MenuCardApi.get_list
    #                   type: array
    #               type: object
    #     """
    #     return self.response(200)

    """
        raise ScannerError(None, None,
        yaml.scanner.ScannerError: mapping values are not allowed here
    """
    # openapi_spec_methods = {
    #     "menu_cards": {
    #         "get": {
    #             "description": "List all",
    #             "content": {
    #                 "application/json": {
    #                     "schema": {
    #                         "$ref":
    #                             "#/components/schemas/MenuCardApi.get_list"
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     }
    label_columns = {'created_by.username': 'Created by',
                     'changed_by.username': 'Changed by'}
    list_columns = ['name', 'description', 'dishes',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']
    show_columns = ['name', 'description', 'dishes',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']


class MenuCardApi(ModelRestApi):
    resource_name = 'menus'
    datamodel = SQLAInterface(models.MenuCard)
    allow_browser_login = True
    label_columns = {'created_by.username': 'Created by',
                     'changed_by.username': 'Changed by'}
    # show_exclude_columns = ['created_by.password',
    #                         'changed_by.password'] doesn't work
    add_exclude_columns = ['created_by', 'created_on', 'changed_by',
                           'changed_on']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
                            'changed_on']
    list_columns = ['name', 'description',  'dishes',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']


class DishesApi(ModelRestApi):
    resource_name = 'dishes'
    datamodel = SQLAInterface(models.Dish)
    allow_browser_login = True
    # base_order = ('changed_on', 'desc')
    label_columns = {'created_by.username': 'Created by',
                     'changed_by.username': 'Changed by',
                     'menu_card.name': 'Menu'}
    show_exclude_columns = ['created_by.password',
                            'changed_by.password',
                            'changed_on']
    add_exclude_columns = ['created_by', 'created_on', 'changed_by',
                           'changed_on']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
                            'changed_on']
    list_columns = ['name', 'preparation_time', 'price',
                    'vegetarian', 'description', 'menu_card.name',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']


appbuilder.add_api(MenuCardApi)
appbuilder.add_api(DishesApi)
appbuilder.add_api(PublicMenuApi)
# appbuilder.security_cleanup()


db.create_all()

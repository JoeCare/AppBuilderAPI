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


class PublicMenuApi(BaseModelApi):
    resource_name = 'menu_cards'
    base_permissions = ['can_get', 'can_get_list']
    datamodel = SQLAInterface(models.MenuCard)

    list_columns = ['name', 'description', 'dishes',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']
    show_columns = ['name', 'description', 'dishes',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']
    # openapi_spec_methods = {
    #     "menu_cards": {
    #         "get": {
    #             "description": "Override description",
    #             }
    #         }
    #     }


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
# appbuilder.security_cleanup()


db.create_all()

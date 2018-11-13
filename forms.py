"""
file to store classes for every form in the application

@author Preston Mackert
"""

# ---------------------------------------------------------------------------------------------------- #
# imports
# ---------------------------------------------------------------------------------------------------- #

from wtforms import Form, StringField, SelectField


# ---------------------------------------------------------------------------------------------------- #
# form classes
# ---------------------------------------------------------------------------------------------------- #

class stringSearchForm(Form):
    select = SelectField('Search Files...')
    search = StringField("")


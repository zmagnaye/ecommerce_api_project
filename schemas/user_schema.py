from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from models.user import User

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):

    name = fields.String(required = True, validate = validate.Length(min = 1))
    address = fields.String(required = True, validate = validate.Length(min = 1))
    email = fields.Email(required = True)

    class Meta:
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many = True)
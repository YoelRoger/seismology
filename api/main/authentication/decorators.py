from .. import jwt
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def admin_required(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if claims['admin']:
            return method(*args, **kwargs)
        else:
            return 'ONLY ADMINS ALLOWED ACCESS ', 403
    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        "id": user.id,
        "email": user.email,
        "admin": user.admin,
    }

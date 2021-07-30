from flask import url_for
from flask_restx import Namespace, Resource, \
    reqparse, inputs, fields
from flask_jwt_extended import jwt_required, get_jwt

from app.data.user_controller import create_user, \
    get_user_by_username, get_user_by_email
from app.utils.access_JWT import blacklist_token

auth_ns = Namespace('auth', 
    description='User Authentication related operations')

user_schema = auth_ns.model('User', { 
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
})

login_schema = auth_ns.model('Login', { 
    'username': fields.String,
    'password': fields.String
})


user_parser = reqparse.RequestParser()
user_parser.add_argument("name", required=True, help="name cannot be blank")
user_parser.add_argument("username", required=True, help="username cannot be blank")
user_parser.add_argument("email", type=inputs.email(), required=True, help="email cannot be blank")
user_parser.add_argument("password", required=True, help="password cannot be blank")


@auth_ns.route('/signup')
class SignupResource(Resource):
    """Handles the User sign up operation
    """

    @auth_ns.doc("signup")
    @auth_ns.expect(user_schema)
    @auth_ns.response(201, "Account created Succesfully")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(409, "Username or Email already exists")
    def post(self):
        """Create an Account
        """

        new_user_args = user_parser.parse_args()

        name = new_user_args['name']
        username = new_user_args['username']
        email = new_user_args['email']
        password = new_user_args['password']

        
        if get_user_by_email(email):
            return {
                'msg': f'Email already exists: {email}',
                'action': 'Use another email',
            }, 409
        elif get_user_by_username(username):
            return {
                'msg': f'Username has already been taken: {username}',
                'action': 'Choose another username'
            }, 409
        else:
            create_user(name, username, email, password)

            return {
                "msg": f"Welcome {name}, account was created successfully",
                "action": "Continue to login",
                "link": url_for('api_bp.auth_login_resource')
            }, 201


@auth_ns.route('/login')
class LoginResource(Resource):
    """Handles creating a User session
    """
    login_parser = user_parser.copy()
    login_parser.remove_argument('name')
    login_parser.remove_argument('email')

    @jwt_required(optional=True)
    @auth_ns.doc("login")
    @auth_ns.expect(login_schema)
    @auth_ns.response(200, "Access Token was successfully issued")
    @auth_ns.response(401, "User login details are wrong")
    def post(self):
        """Get a valid Access Token 
        """
        if get_jwt(): # blacklist existing token if available
            jti = get_jwt()['jti']
            blacklist_token(jti)
        
        login_args = self.login_parser.parse_args()
        username = login_args['username']
        password = login_args['password']

        user = get_user_by_username(username)

        if user and user.verify_password(password):
            return {
                'msg': f'Welcome back {user.name}',
                'access_token':f'Bearer {user.generate_access_token()}',
                'action': 'Update Authorization header with-access_token'
            }, 200
        
        return {
            'msg': 'Your Username or Password is wrong',
            'action': 'Head over to registration',
            'link': url_for('api_bp.auth_signup_resource')
        }, 401



@auth_ns.route('/logout')
class LogoutResource(Resource):
    """Handle Token Revocation
    """
    @jwt_required()
    @auth_ns.doc('logout', security='Bearer')
    @auth_ns.response(200, "Access Token was Revoked")
    @auth_ns.response(401, 'Something Wrong with Authorization token')
    def delete(self):
        """Revoke Access Token
        """
        if get_jwt():
            jti = get_jwt()['jti']
            blacklist_token(jti)

            return{
                'msg': 'Access Token has been revoked',
                'action': 'Login to get a Valid token',
                'link': url_for('api_bp.auth_login_resource')
            }, 200
        else:
            return{
                'msg': 'Access Token Revocation is forbidden',
                'action': 'Login to acquire Valid token',
                'link': url_for('api_bp.auth_login_resource')
            }, 401






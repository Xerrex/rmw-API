from http import HTTPStatus

from flask import url_for
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt

from app.data.controller_user import create_user, \
    get_user_by_username, get_user_by_email
from app.utils.access_JWT import blacklist_token

from .dto_auth import user_signup_parser, user_login_parser

auth_ns = Namespace('auth', 
    description='User Authentication related operations')


@auth_ns.route('/signup')
class SignupResource(Resource):
    """Handles the User sign up operation
    """

    @auth_ns.doc("signup")
    @auth_ns.expect(user_signup_parser)
    @auth_ns.response(int(HTTPStatus.CREATED), "Account created Succesfully")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "Username or Email already exists")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server error")
    def post(self):
        """Create an Account
        """

        new_user_args = user_signup_parser.parse_args()

        name = new_user_args['name']
        username = new_user_args['username']
        email = new_user_args['email']
        password = new_user_args['password']

        
        if get_user_by_email(email):
            return {
                'msg': f'Email already exists: {email}',
                'action': 'Use another email',
            }, HTTPStatus.CONFLICT #409
        elif get_user_by_username(username):
            return {
                'msg': f'Username has already been taken: {username}',
                'action': 'Choose another username'
            }, HTTPStatus.CONFLICT #409
        else:
            create_user(name, username, email, password)

            return {
                "msg": f"Welcome {name}, account was created successfully",
                "action": "Continue to login",
                "link": url_for('api_bp.auth_login_resource')
            }, HTTPStatus.CREATED #201


@auth_ns.route('/login')
class LoginResource(Resource):
    """Handles creating a User session
    """

    @jwt_required(optional=True)
    @auth_ns.doc("login")
    @auth_ns.expect(user_login_parser)
    @auth_ns.response(int(HTTPStatus.OK), "Access Token was successfully issued")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Username or password is wrong")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation Error")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def post(self):
        """Get a valid Access Token 
        """
        if get_jwt(): # blacklist existing token if available
            jti = get_jwt()['jti']
            blacklist_token(jti)
        
        login_args = user_login_parser.parse_args()
        username = login_args['username']
        password = login_args['password']

        user = get_user_by_username(username)

        if user and user.verify_password(password):
            return {
                'msg': f'Welcome back {user.name}',
                'access_token':f'Bearer {user.generate_access_token()}',
                'action': 'Update Authorization header with-access_token'
            }, HTTPStatus.OK #200
        
        return {
            'msg': 'Your Username or Password is wrong',
            'action': 'Head over to registration',
            'link': url_for('api_bp.auth_signup_resource')
        }, HTTPStatus.UNAUTHORIZED #401



@auth_ns.route('/logout')
class LogoutResource(Resource):
    """Handle Token Revocation
    """
    @jwt_required()
    @auth_ns.doc('logout', security='Bearer')
    @auth_ns.response(int(HTTPStatus.OK), "Access Token was Revoked")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Authorization token is Invalid or expired')
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
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
            }, HTTPStatus.OK
        else:
            return{
                'msg': 'Access Token Revocation is forbidden',
                'action': 'Login to acquire Valid token',
                'link': url_for('api_bp.auth_login_resource')
            }, HTTPStatus.UNAUTHORIZED






from flask_restx import Namespace, Resource

auth_ns = Namespace('Authentication', 
    description='User Authentication related operations')


@auth_ns.route('/signup')
class SignupResource(Resource):
    pass


@auth_ns.route('/login')
class LoginResource(Resource):
    pass


@auth_ns.route('logout')
class LogoutResource(Resource):
    pass



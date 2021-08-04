"""Data Transfer Objects for Authentication"""
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import email

user_login_parser = RequestParser(bundle_errors=True)
user_login_parser.add_argument("username", required=True, help="username cannot be blank", location='json', nullable=False) # TODO: Remove fieldS
user_login_parser.add_argument("password", required=True, help="password cannot be blank", location='json', nullable=False)

user_signup_parser = user_login_parser.copy()
user_signup_parser.add_argument("name", required=True, help="name cannot be blank", location='json', nullable=False)
user_signup_parser.add_argument("email", type=email(), required=True, help="email cannot be blank", location='json', nullable=False)


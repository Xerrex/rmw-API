from datetime import datetime

from app.data.controller_user import get_user_by_username
from app.utils.exts import db, jwt

@jwt.user_lookup_loader
def user_loader(_jwt_header, jwt_data):
    username = jwt_data["sub"]
    return get_user_by_username(username)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = Tokenblacklist.query.filter_by(jti=jti).first()
    return token is not None

def blacklist_token(jti):
    """ Blacklist a Token by saving
    """
    token_bl = Tokenblacklist(jti)
    token_bl.save()


class Tokenblacklist(db.Model):
    """Handles Expired or cancelled tokens
    """

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, jti):
        self.jti = jti

    def save(self):
        """Save the model to db
        """
        db.session.add(self)
        db.session.commit()




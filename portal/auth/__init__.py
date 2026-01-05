from .routes import auth_bp

from portal.extensions import login_manager
from portal.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from app.core.config import firebaseConfig




class UserFirebase:
    certeficate = credentials.Certificate(firebaseConfig)
    app_firebase = firebase_admin.initialize_app(certeficate)
    client = auth._get_client(app_firebase)
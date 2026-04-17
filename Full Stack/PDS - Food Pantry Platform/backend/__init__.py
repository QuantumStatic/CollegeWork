from flask import Flask
from dotenv import load_dotenv
import os
from app.registerUser import RegisterUser
from app.login import login
from app.getItem import getItem
from app.getOrder import getOrder
from app.addDonations import addDonation
from app.orderHistory import getOrderHistory
from app.categoryFilter import CategoryFilter
from app.tasksPerformed import tasksPerformed
from app.getUser import user
from app.phone import phone
from app.createOrder import createOrder
from app.rank import rank
from app.statusUpdate import status
from app.checkUser import checkUser

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config.update(
    SESSION_COOKIE_SECURE=True,  
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_PATH = "/"
    )
    
    app.register_blueprint(RegisterUser)
    app.register_blueprint(login)
    app.register_blueprint(getItem)
    app.register_blueprint(getOrder)
    app.register_blueprint(addDonation)
    app.register_blueprint(getOrderHistory)
    app.register_blueprint(CategoryFilter)
    app.register_blueprint(tasksPerformed)
    app.register_blueprint(user)
    app.register_blueprint(phone)
    app.register_blueprint(createOrder)
    app.register_blueprint(rank)
    app.register_blueprint(status)
    app.register_blueprint(checkUser)

    return app
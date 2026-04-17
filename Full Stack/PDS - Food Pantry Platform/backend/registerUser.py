from flask import Blueprint, jsonify, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
import bcrypt

RegisterUser = Blueprint('register', __name__)

@RegisterUser.route('/api/register', methods = ['POST'])
def registerUser():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        role = request.form.get('role').split(",")
        phone = request.form.get('phone').split(",")
      
        # not null checked in frontend

        salt = bcrypt .gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500 
        
        with connection.cursor() as cursor:
            check_query = '''
            select *
            from personphone
            where phone = %s
            '''
            for i in phone:
                cursor.execute(check_query, (i))
                result = cursor.fetchone()
                if result:
                    connection.close()
                    return jsonify({"error" : "Phone Number already exists"}), 409
            
            query = '''
            insert into person (userName, password, fname, lname, email) values
            (%s, %s, %s, %s, %s)
            '''
            query2 = '''
            insert into act (username, roleID) values
            (%s, %s)
            '''

            query3 = '''
            insert into personphone (username, phone) values
            (%s, %s)
            '''
            cursor.execute(query, (username, hash_password, fname, lname, email))

            for i in role:
                cursor.execute(query2, (username, i))

            for i in phone:
                cursor.execute(query3, (username, i))

            connection.commit()
            connection.close()

        response = {
            "message" : "User Registered Successfully" 
        }
        return jsonify(response), 201
    
    except datababaseError as e:
        print(e)
        response = {
            "error": str(e)
        }
        return jsonify(response), 500
    except Exception as e:
        print(e)
        response = {
            "error": "Cannot Connect to Server"
        }
        return jsonify(response), 500
    
from flask import Blueprint, jsonify, request, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
import bcrypt

login = Blueprint('login', __name__)

'''
API to login to the system and generate session

Input:
username
password

Output:
1. Seesion Infromation with Success Message- 200

2. Failure Message -404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Session Error - 404
'''
@login.route('/api/login', methods = ['POST'])
def loginAuth():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        # not null verified in front-end

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            query = '''
            select username, password 
            from person
            where person.username = %s
            '''
            cursor.execute(query, (username))
            result = cursor.fetchone()
   
        connection.close()

        if not result:
            response = {
                "error": "Invalid username or password"
            }
            return jsonify(response), 404
        
        elif result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
            session['username'] = username
            response = {
                "message": "Login successful"
            }
            return jsonify(response), 200
        
        else:
            response = {
                "error": "Invalid username or password"
            }
            return jsonify(response), 404

    except datababaseError as e:
        response = {
            "error": str(e)
        }
        return jsonify(response), 500

    except Exception as e:
        print(e)
        response = {
            "error": "Cannot Login"
        }
        return jsonify(response), 500

"""
Logout API
Input:
None
Ouptut:
1. OK Message with deletion of Session. 200
2. Server Error - 500
3. Session Error - 404
"""
@login.route('/api/logout', methods = ['GET'])
def logoutUser():
    try:
        if 'username' not in session:
            response = {
                "error" : "User Not LogedIn"
            }
            return jsonify(response), 404
        
        session.pop('username')
        response = {
            "message": "Logout Succeful"
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        response = {
            "error" : "Server Not Found"
        }
        return jsonify(response), 500
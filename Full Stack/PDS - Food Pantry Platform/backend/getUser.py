from flask import Blueprint, jsonify, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError

user = Blueprint('user', __name__)

'''
API to get Information for a perticular Item
Called on Landing Page

Input:
None

Output:
1. User Infromation - 200
    User Detiails - except password :)
    
2. Not Found Error -404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Session Error - 404
'''
@user.route('/api/profile', methods = ['GET'])
def get_profile():
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        username = session['username']
        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
            
        with connection.cursor() as cursor:
            query = '''
            select *
            from person natural join personphone
            where person.userName = %s
            '''
            cursor.execute(query, (username))
            result = cursor.fetchall()

        connection.close()
        response = {
            "username" : result[0]["userName"],
            "fname" : result[0]['fname'],
            "lname" : result[0]['lname'],
            "email" : result[0]['email'],
            "phone" : []
        }
        for idx, i in enumerate(result):
            response['phone'].append(i['phone'])
            
        return jsonify(response), 200
    
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

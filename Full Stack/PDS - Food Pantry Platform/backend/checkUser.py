"""
API to check is user is staff or volunteer
"""

from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError

checkUser = Blueprint('checkUser', __name__)

@checkUser.route('/api/check/user', methods = ['GET'])
def checkUser_function():
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404
        username = session['username']

        connection = get_db_connection()
        if not connection:
            response = {
                "database error": "Cannot Connect to Database"
            }
            return jsonify(response), 500

        with connection.cursor() as cursor:
            # QUery to Check of Delivery partner is a Volunteer or Staff
            query_check = '''
                select *
                from act
                where username = %s
                and (roleID = 'Volunteer' or roleID = 'Staff')
            '''
            cursor.execute(query_check, (username))
            result = cursor.fetchall()
            if not result:
                return jsonify({'error': 'Delivery Partner not found'}), 404
            else:
                return jsonify({'message' : 'OK'}), 200
            
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

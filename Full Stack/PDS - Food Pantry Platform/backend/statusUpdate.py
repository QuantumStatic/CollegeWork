from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError

status = Blueprint('statusUpdate', __name__)

@status.route('/api/status-update', methods = ['POST'])
def statusUpdate_function():
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        username = session['username']
        new_satus = request.form.get('stauts')
        orderID = int(request.form.get('orderID'))
        print(orderID, username, new_satus)
        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        with connection.cursor() as cursor:
            query = "call UpdateOrderStatus(%s, %s, %s)"
            cursor.execute(query, (orderID, username, new_satus))

            connection.commit()
            connection.close()
            
        return jsonify({'message': 'Status Updated'}), 200
    
    except datababaseError as e:
        return jsonify({'error' : str(e).split(",")[1][2:-2]}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
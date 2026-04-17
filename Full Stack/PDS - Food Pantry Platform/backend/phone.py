from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
phone = Blueprint('phone', __name__)

@phone.route('/api/phone/add', methods = ['POST'])
def add_phone():
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        username = session['username']
        phone = request.form.get('phone')
        
        if len(phone) < 10 or len(phone) > 12:
            return jsonify({"error" : "Incorrect Phone Number"}), 404
        
        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            # check of numeric and length in frontend
            check_query = '''
            select *
            from personphone
            where phone = %s
            '''
            cursor.execute(check_query, (phone))
            result = cursor.fetchone()

            if result:
                connection.close()
                return jsonify({"error" : "Phone Number already exists"}), 409
            
            query = '''
            insert into personphone(userName, phone) values
            (%s, %s)
            '''
            cursor.execute(query, (username, phone))
            
            connection.commit()
        connection.close()
        response = {
                "message" : "Phone Registered Successfully" 
        }
        return jsonify(response), 201
    
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
@phone.route('/api/phone/remove', methods = ['POST'])
def remove_phone():
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        username = session['username']
        phone = request.form.get('phone')
        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:            
            query = '''
            delete from personphone
            where userName = %s
            and phone = %s
            '''
            cursor.execute(query, (username, phone))
            
            connection.commit()
        connection.close()
        response = {
                "message" : "Phone Deleted Successfully" 
        }
        return jsonify(response), 201
    
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    


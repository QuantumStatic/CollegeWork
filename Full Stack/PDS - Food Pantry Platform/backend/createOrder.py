from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
from datetime import datetime

createOrder = Blueprint('createorder', __name__)

'''
API to check if a given username has a role of client

Input:
1. Username as URL parameter

Output:
1. Ok Message - 200
2. Session Error - 404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
'''
@createOrder.route('/api/check/client/<username>', methods = ['GET'])
def ClientAuth(username):
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404
        
        if session['username'] == username:
            return jsonify({'error': 'Staff cannot be a client Client '}), 403
        connection = get_db_connection()

        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            query = '''
            select *
            from act
            where userName = %s
            and roleID = 'Client'
            '''
            cursor.execute(query, (username))

            result = cursor.fetchone()
        connection.close()
        if result:
            return jsonify({'message' : 'OK'}), 200
        else:
            return jsonify({'error': 'Client not found'}), 404
        
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except KeyError as e:
        return jsonify({'error': 'Login not found'}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


'''
API to create new order

Input:
1. Username - text
2. orderNotes - text
3. order Date - text - YYYY-MM-DD
4. itemID's - As Array
5. Deliverd By username - Text
6. Deliveriyu Date - text - YYYY-MM-DD
7. Delivery Status - text

Output:
1. Ok Message - 200
2. Session Error - 404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Item Not Found / Already Bought - 404
7. Delivery Partner not found - 404
'''
@createOrder.route('/api/createorder', methods = ['POST'])
def createOrder_function():
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404
        
        supervisor = session['username']
        username = request.form.get('username')
        orderNotes = request.form.get('orderNotes')
        orderDate = datetime.strptime(request.form.get('orderDate'), '%Y-%m-%d').date()
        itemID = request.form.get('itemID').split(',')
        deliveredBy = request.form.get('deliveredBy')
        deliveredDate = datetime.strptime(request.form.get('deliveredDate'), '%Y-%m-%d').date()
        deliveredStatus = request.form.get('deliveredStatus')

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
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
            cursor.execute(query_check, (deliveredBy))
            result = cursor.fetchall()
            if not result:
                return jsonify({'error': 'Delivery Partner not found'}), 404

            # Query To Check if Item exists and not bough already -> found in itemIn Table
            # Cannot apply trigger as we first create order which does not take itemID, hence can't check.
            # * Redundant now
            query_check = '''
            select * 
            from item
            where ItemID = %s
            and ItemID not in (select ItemID 
            from itemin)
            '''
            for item in itemID:
                cursor.execute(query_check, int(item))
                result = cursor.fetchone()

                if not result:
                    return jsonify({'error' : f'Item {item} Not Found or already bought'},404)
                
            # Crate New Order in DB
            
            query = '''
            insert into ordered (orderDate, orderNotes, supervisor, client) values
            (%s, %s, %s, %s)
            '''
            cursor.execute(query, (orderDate, orderNotes, supervisor, username))
            connection.commit()
            
            last_order_id = cursor.lastrowid # get Order ID

            #* insert item into itemIn with OrderID
            query = '''
            insert into itemin (ItemID, orderID, found) values
            (%s, %s, %s)
            '''
            for item in itemID:
                cursor.execute(query, (int(item), last_order_id, True))
                connection.commit()

            # * Insert Delivery Partiner Information
            query = '''
            insert into delivered (userName, orderID, status, date) values
            (%s, %s, %s, %s)
            '''
            cursor.execute(query, (deliveredBy, last_order_id, deliveredStatus, deliveredDate))
            connection.commit()

        connection.close()
        return jsonify({'message' : f'Order Created {last_order_id}'}) ,200  

    except datababaseError as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        print(e)
        return jsonify({'error' : str(e)}), 500
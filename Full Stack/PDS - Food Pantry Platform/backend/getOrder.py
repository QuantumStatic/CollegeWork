from flask import Blueprint, jsonify, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
from itertools import groupby
getOrder = Blueprint('getorder', __name__)

'''
API to get Information for a perticular Order

Input:
Order ID as URL parameter

Output:
1. Order Infromation - 200
    Order Detiails
    Order Item Details
    Item-Piece Location
    
2. Not Found Error -404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Session Error - 404
'''
@getOrder.route('/api/order/<int:order_id>', methods = ['GET'])
def getOrder_function(order_id):
    try:
        if 'username' not in session:
            response = {
            'error' : 'User Not Found'
            }
            return jsonify(response), 404
        
        connection = get_db_connection()
        if not connection:
            response = {
                "database error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            query = '''
            select *
            from (`ordered` natural join delivered) natural join
            (itemin natural join item) natural join
            piece
            where orderID = %s
            '''
            cursor.execute(query, (order_id))
            result = cursor.fetchall()
        
        connection.close()
        if not result:
            response = {
                'error': 'Order Not Found'
            }
            return jsonify(response), 404
        else: 
            # Formating the Response
            """
            Remove Dupicate Order Details
            Aggreate Item Information
            """
            order_data = {
                'client' : result[0]['client'],
                'orderDate' : result[0]['orderDate'],
                'delivery_partner' : result[0]['userName'],
                'supervisor' : result[0]['supervisor'],
                'delivery_date' : result[0]['date'],
                'status' : result[0]['status'],
                'item' : []
            }
            for key, group in groupby(result, key = lambda x:(x['ItemID'], x['iDescription'])):
                item_data = {
                    'ItemID' : key[0],
                    'iDescription' : key[1],
                    'piece' : []
                }

                for piece in group:
                    item_data['piece'].append({
                        'pieceNum' : piece['pieceNum'],
                        'pDescription' : piece['pDescription'],
                        'roomNum' : piece['roomNum'],
                        'shelfNum' : piece['shelfNum']
                    })
                
                order_data['item'].append(item_data)
                
            return jsonify(order_data), 200
        
    except datababaseError as e:
        response = {
            'error' : str(e)
        }
        return jsonify(response), 500
        
    except Exception as e:
        response = {
            'error' : str(e)
        }
        return jsonify(response), 500

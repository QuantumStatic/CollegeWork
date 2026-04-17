from flask import Blueprint, jsonify, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
import base64

getItem = Blueprint('getitem', __name__)

'''
API to get Information for a perticular Item

Input:
Item ID as URL parameter

Output:
1. Item Infromation - 200
    Item Detiails
    Pieces Details
    Piece Location Details

2. Not Found Error -404
3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Session Error - 404
'''
@getItem.route('/api/getitem/<int:item_id>', methods = ['GET'])
def getItem_function(item_id):
    try:
        if 'username' not in session:
            response = {
                'error' : 'User not logined'
            }
            return jsonify(response), 404

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        with connection.cursor() as cursor:
            query = '''
            select * 
            from item natural join piece
            where itemID = %s
            '''
            cursor.execute(query, (item_id))
            result = cursor.fetchall()
        connection.close()

        if not result:
            response = {
                'error' : 'Item not Found'
            }
            return jsonify(response), 404
        
        else:
            # Formating the Response
            """
            Remove Dupicate Item Details
            Aggreate Piece Information
            """
            item_data = {
                'itemID' : result[0]['ItemID'],
                'iDescription' : result[0]['iDescription'],
                'photo' : base64.b64encode(result[0]['photo']).decode('utf-8'),
                'Category' : result[0]['mainCategory'],
                'subCategory' : result[0]['subCategory'],
                'color' : result[0]['color'],
                'isNew' : result[0]['isNew'],
                'hasPieces' : result[0]['hasPieces'],
                'material' : result[0]['material'],
                'pieces' : []
            }
            for i in result:
                item_data['pieces'].append({
                    'pieceNum' : i['pieceNum'],
                    'pDescription' : i['pDescription'],
                    'roomNum' : i['roomNum'],
                    'shelfNum' : i['shelfNum']

                })
            return jsonify(item_data), 200
        
    except datababaseError as e:
        print(e)
        response = {
            'error' : str(e)
        }
        return jsonify(response), 500
        
    except Exception as e:
            response = {
                'error' : str(e)
            }
            return jsonify(response), 500


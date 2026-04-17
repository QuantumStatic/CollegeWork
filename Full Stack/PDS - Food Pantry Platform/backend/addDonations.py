from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
from datetime import datetime
import json

addDonation = Blueprint('add_donation', __name__)

'''
API to verfiy if the seesion user has a role of Staff
Called before creating a donation as only staff as the right to insert donation

Input: 
No input

Output:
1. Ok Message - 200
2. Session user not a Staff - 404
3. Database Connetion - 500
4. Seesion not found - 404
5. Server Error - 500
6. Database Error - 500
'''
@addDonation.route('/api/check/staff', methods = ['GET'])
def SupervisorAuth():
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404
        
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
            from act
            where username = %s
            and roleID = 'Staff'
            '''
            cursor.execute(query, (username))
            result = cursor.fetchone()

        connection.close()

        if result:
            return jsonify({'message' : 'OK'}), 200
        else:
            return jsonify({'error': 'Not A Staff'}), 401
        
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

'''
API to verfiy if the given username has a role of Donor
Called before creating a donation

Input: 
donor username as URL parameter

Output:
1. Ok Message - 200
2. Not found error - 404
3. Database Connetion - 500
4. Seesion not found - 404
5. Server Error - 500
6. Database Error - 500
'''
@addDonation.route('/api/check/donator/<username>', methods = ['GET'])
def donatorAuth(username):
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404

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
            where username = %s
            and roleID = 'Donator'
            '''
            cursor.execute(query, (username))
            result = cursor.fetchone()
        connection.close()
        if result:
            return jsonify({'message' : 'OK'}), 200
        else:
            return jsonify({'error': 'Donator not found'}), 404
        
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

'''
API to donate items

input :
all item details:
1. Item Description - Text
2. Color - Text
3. IsNew - 1/0
4. hasPieces - 1/0
5 Material - text
6 Main Category - Text
7 Sub Categoory - Text
8 Photo - img
9 Pieces Info - JSON with piece Information and Location information
10. Donate Date - YYYY-MM-DD

Output:
1. throw error is no database connection - 500
2. throw error is no session found - 404
3. throw database errors - 500
4. Send Message : Item Donated - 500
'''
@addDonation.route('/api/donate/', methods = ['POST'])
def addDonation_function():
    try:
        if 'username' not in session:
            return jsonify({'error': 'Cannot Access This Page'}), 404

        donor = request.form.get('donor')

        item = request.form.get('iDescription')
        color = request.form.get('color')
        isNew = bool(int(request.form.get('isNew')))
        hasPieces = bool(int(request.form.get('hasPieces')))
        material = request.form.get('material')
        mainCategory = request.form.get('mainCategory')
        subCatrgory = request.form.get('subCategory')
        
        photo = request.files.get('photo')
        photo_binary = photo.read()

        pieces = request.form.get('pieces')
        pieces = json.loads(pieces)

        donateDate = datetime.strptime(request.form.get('donateDate'), '%Y-%m-%d').date()

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            # Qurry to Create Item
            query = '''
            insert into Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory) values
            (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (item, photo_binary, color, isNew, hasPieces, material, mainCategory, subCatrgory))
            connection.commit()
            
            # get greated item ID
            last_item_id = cursor.lastrowid

            # create Donation with username and itemID
            query2 = '''
            insert into DonatedBy (ItemID, userName, donateDate) values
            (%s, %s, %s)
            '''
            cursor.execute(query2, (last_item_id, donor, donateDate))
            connection.commit()
            
            # Store the Pieces Information 
            query3 = '''
            insert into Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes) values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            for piece in pieces:
                cursor.execute(query3, (last_item_id, int(piece['pieceNum']), piece['pDescription'], int(piece['Length']), int(piece['width']), int(piece['height']), int(piece['roomNum']), int(piece['shelfNum']), piece['pNotes']))
                connection.commit()

        connection.close() 

        return jsonify({'message' : f'Item Donated {last_item_id}'}) ,200
    
    except datababaseError as e:
        return jsonify({'error' : str(e)}), 500
 
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
from flask import Blueprint, jsonify, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
from itertools import groupby
getOrderHistory = Blueprint('orderHistory', __name__)

'''
API to get Information for user Order History

Input:
None

Output:
1. Orders Infromation / No History Message- 200
    All Order Detials
    Item In Order Details

3. Database Connection -500
4. Server Error - 500
5. Database Error - 500
6. Session Error - 404
'''
@getOrderHistory.route('/api/orderhistory', methods = ['GET'])
def getOrderHistory_function():
    try:
        if 'username' not in session:
            response = {
                'error' : 'User not logined'
            }
            return jsonify(response), 404
        
        username = session['username']
        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        """
        (select distinct orderID
        from `ordered` natural join itemin natural join delivered
        where client = 'meetoswal' or supervisor = 'meetoswal' or userName = 'meetoswal')

        select orderID, ItemID, iDescription
        from orderIDs natural join (itemin natural join item)
        """
        with connection.cursor() as cursor:
            query = '''
            with orderIDs as(select *
            from ordered natural join itemin natural join delivered
            where delivered.userName = %s or ordered.client = %s or ordered.supervisor = %s)

            select orderID, orderDate, ItemID, iDescription, client, supervisor, userName
            from (orderIDs natural join itemin) natural join item
            order by orderDate desc
            '''
            cursor.execute(query, (username, username, username))
            result = cursor.fetchall()
        
        connection.close()
        if not result:
            return jsonify({'error' : 'No Order History Found'}), 404
        else:
            order_data = {
                'client' : username,
                'orders' : []
            }
            for key, group in groupby(result, key = lambda x: (x['orderID'], x['orderDate'], x['client'], x['supervisor'], x['userName'])):
                order_details = {
                    'orderId' : key[0],
                    'orderDate' : key[1],
                    'items' : [],
                    'as' : ["" , "" , ""]
                }
                if key[2] == username:
                    order_details['as'][0] = 'Client'
                if key[3] == username:
                    order_details['as'][1] = 'Supervisor'
                if key[4] == username:
                    order_details['as'][2] = 'Delivery-Partner'
                for item in group:
                    
                    order_details['items'].append({
                        'ItemID' : item['ItemID'],
                        'iDescription' : item['iDescription']
                    })
                    
                order_data['orders'].append(order_details)
            
            return jsonify(order_data), 200
        
    except datababaseError as e:
        return jsonify({'error' : str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


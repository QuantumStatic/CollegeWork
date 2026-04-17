from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
rank = Blueprint('rank', __name__)

@rank.route('/api/rank/', methods = ['POST'])
def rank_function():
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        start_date = request.form.get('start')
        end_date = request.form.get('end')

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        with connection.cursor() as cursor:
            query = """
            select userName, count(orderID) as 'count'
            from (select * from act where roleID = 'Volunteer') as volunteers natural left join (delivered natural join ordered)
            where orderDate >= %s and date <= %s
            group by userName 
            order by count(orderID) desc
            limit 10
            """
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
        if len(result) == 0:
            result = []
        connection.close()
        if len(result) < 10:
            extras = [
                {
                'count' : 0,
                'userName' : ''
                }
            ] * (10 - len(result))
            result.extend(extras)
    
        return jsonify(result), 200
        
    except datababaseError as e:
        return jsonify({'error' : str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
        
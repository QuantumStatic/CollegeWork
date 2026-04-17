from flask import Blueprint, jsonify, session
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
tasksPerformed = Blueprint('tasksPerformed', __name__)

@tasksPerformed.route('/api/tasks/volunteer/<volunteer>', methods = ['GET'])
def get_tasks_volunteer(volunteer):
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            query = '''
            select *
            from delivered natural join act
            where roleID = 'Volunteer'
            and userName = %s
            order by username, date
            '''
            cursor.execute(query, volunteer)
            result = cursor.fetchall()
        
        connection.close()

        if not result:
            return jsonify({"error" : "No Data Found"}), 404
        else:
            for i in result:
                del i['userName']
                del i['roleID']
            return jsonify(result), 200
            
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : "Somenthing Went Wrong"}), 500


@tasksPerformed.route('/api/tasks/supervision/<staff>', methods = ['GET'])
def get_tasks_staff(staff):
    try:
        if 'username' not in session:
            return jsonify({'error': 'User not found'}), 404
        
        connection = get_db_connection()

        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            query = '''
            select *
            from `ordered`
            where supervisor = %s
            order by `ordered`.orderDate
            '''
            cursor.execute(query, staff)
            result = cursor.fetchall()

        connection.close()

        if not result:
            return jsonify({"error" : "Data Not Found"}), 404
        else:
            for data in result:
                del data['supervisor']
                
            return jsonify(result), 200
            
    except datababaseError as e:
        return jsonify({'error': str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : "Somenthing Went Wrong"}), 500
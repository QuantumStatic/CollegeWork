from flask import Blueprint, jsonify, session, request
from app.utils import get_db_connection
from pymysql import MySQLError as datababaseError
from itertools import groupby
import base64
import json

CategoryFilter = Blueprint('categoryFilter', __name__)

'''
API to get the Category and SubCategory Catalog

Input:
None

Ouput:
1. Data Catalog - 200
2. Seesion Not Found - 404
3. Database Connection - 500
4. Server Error - 500
5. Database Error - 500

'''
@CategoryFilter.route('/api/getcategory', methods = ['GET'])
def getCategory():
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
            select mainCategory, subCategory
            from Category
            order by mainCategory, subCategory
            '''
            cursor.execute(query)
            result = cursor.fetchall()

        connection.close()

        category_data = {
            'categories' : []
        }
        for key, group in groupby(result, key = lambda x: x['mainCategory']):
            category_data['categories'].append({
                'category' : key,
                'sub_category': [i['subCategory'] for i in group]
            })

        return jsonify(category_data), 200

    except datababaseError as e:
        return jsonify({'error' : str(e)}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

'''
API to get Filtered Items Base on Category and SubCategory

Input:
Filter Parameters - JSON Object
    Category Name as key and Array as Values, where array will contain selected sub-categories

Output:
1. Items based on filter / no filter 200
2. Seesion error - 404
3. Server Error - 500
5. Database Connection - 500
6. Database Error - 500
'''    
    

@CategoryFilter.route('/api/category/<int:page>', methods = ['POST'])
def categoryFilter(page):
    try:
        if 'username' not in session:
            response = {
                'error' : 'User Not Logined'
            }
            return jsonify(response), 404
        
        data = request.form.get('data')
        # Convert Json to Dict.
        data = json.loads(data)

        connection = get_db_connection()
        if not connection:
            response = {
                "error": "Cannot Connect to Database"
            }
            return jsonify(response), 500
        
        with connection.cursor() as cursor:
            # filter parameters for parametrized query
            queryParameters = []

            # Parameterized Query 
            '''
            Sample:

            select *
            from item natural left join itemin
            where orderID is null and 
            (( mainCategory = 'Books' and subCategory in ( 'Comedy' )) or 
            ( mainCategory = 'Clothing' and subCategory in ('Men')))
            order by ItemID desc
            limit 11 offset 10 

            '''
            query = '''
            select * 
            from item natural left join itemin
            where orderID is null
            '''
            if data: # in case not filter applied
                query += 'and ('

                for category,sub_category in data.items():
                    query += "( mainCategory = %s"

                    queryParameters.append(category)
                    """
                    Every %s corresponds to a input parmater and it is in accepted in sequence, hence we append the category 
                    to variable to pass it when query is executed
                    """

                    if len(sub_category) > 0: # in case no subCategory choosen
                        query += " and subCategory in ( %s "
                        queryParameters.append(sub_category[0])

                        for idx in range(1, len(sub_category)):
                            query += ", %s"
                            queryParameters.append(sub_category[idx]) 
                        query += ")" 
                    # SubCategor Part Completed for 1 main Category

                    query += ") or " 
                    # 1 Main Category Part Completed
                
                query = query[:-4]  # remove the last OR from the query
                query += ")"
            query += """
            order by ItemID desc 
            limit %s offset %s
            """
            queryParameters.append(11)
            queryParameters.append((page - 1) * 10)
            
            cursor.execute(query, tuple(queryParameters)) # Execute the query with prameterized query and its parmameters
            result = cursor.fetchall()
        
        connection.close()

        if not result:
            return jsonify({"error" : "No Item Found"}), 404
        
        response = {
            'next' : 0,
            'prev' : 0,
            'result' : []
        }

        if len(result) == 11:
            result.pop()
            response['next'] = 1
        if page != 1:
            response['prev'] = 1

        for item in result: # enocede photo to a base 64 as we cannot send binary image string as json.
            item['photo'] = base64.b64encode(item['photo']).decode('utf-8') 
        
        response['result'] = result    
        return jsonify(response), 200
    
    except datababaseError as e:
        return jsonify({'error' : query}), 500
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


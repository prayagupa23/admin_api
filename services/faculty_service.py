import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_db_connection
from psycopg2.extras import RealDictCursor

def create_faculty(faculty_data):
    """
    Create a new faculty record in the database
    
    Args:
        faculty_data (dict): Dictionary containing faculty information
            - faculty_id (str): Required
            - password (str): Required (plain text as requested)
            - name (str): Required
            - email (str): Required
            - phone (str): Optional
            - department (str): Optional
            - designation (str): Optional
    
    Returns:
        dict: Result of the operation with success status and message
    """
    try:
        # Validate required fields
        required_fields = ['faculty_id', 'password', 'name', 'email']
        for field in required_fields:
            if field not in faculty_data or not faculty_data[field]:
                return {
                    'success': False,
                    'message': f'Missing required field: {field}'
                }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if faculty_id already exists
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s", 
                      (faculty_data['faculty_id'],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Faculty ID already exists'
            }
        
        # Check if email already exists
        cursor.execute("SELECT email FROM faculty WHERE email = %s", 
                      (faculty_data['email'],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Email already exists'
            }
        
        # Insert new faculty
        insert_query = """
        INSERT INTO faculty (faculty_id, password_hash, name, email, phone, department, designation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            faculty_data['faculty_id'],
            faculty_data['password'],  # Plain text password as requested
            faculty_data['name'],
            faculty_data['email'],
            faculty_data.get('phone'),
            faculty_data.get('department'),
            faculty_data.get('designation')
        )
        
        cursor.execute(insert_query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Faculty created successfully',
            'faculty_id': faculty_data['faculty_id']
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }

def get_all_faculty():
    """Get all faculty members from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT faculty_id, name, email, phone, department, designation
            FROM faculty 
            ORDER BY faculty_id
        """)
        
        faculty_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": faculty_list,
            "count": len(faculty_list)
        }
        
    except Exception as e:
        if 'conn' in locals():
            cursor.close()
            conn.close()
        
        return {
            "success": False,
            "message": f"Error retrieving faculty: {str(e)}"
        }

def get_faculty_by_id(faculty_id):
    """Get a specific faculty member by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT faculty_id, name, email, phone, department, designation
            FROM faculty 
            WHERE faculty_id = %s
        """, (faculty_id,))
        
        faculty = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not faculty:
            return {
                "success": False,
                "message": "Faculty not found"
            }
        
        return {
            "success": True,
            "data": faculty
        }
        
    except Exception as e:
        if 'conn' in locals():
            cursor.close()
            conn.close()
        
        return {
            "success": False,
            "message": f"Error retrieving faculty: {str(e)}"
        }

def delete_faculty(faculty_id):
    """Delete a faculty member by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if faculty exists
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s", (faculty_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                "success": False,
                "message": "Faculty not found"
            }
        
        # Delete faculty
        cursor.execute("DELETE FROM faculty WHERE faculty_id = %s", (faculty_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Faculty deleted successfully"
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        
        return {
            "success": False,
            "message": f"Error deleting faculty: {str(e)}"
        }

from db import get_db_connection

class CourseService:
    
    @staticmethod
    def create_course(course_data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO courses (course_code, course_name, department, batch, credits)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                course_data['course_code'],
                course_data['course_name'],
                course_data['department'],
                course_data['batch'],
                course_data['credits']
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {'message': 'Course created successfully'}, 201
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def get_all_courses():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM courses ORDER BY course_code")
            courses = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {'courses': courses}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def get_course_by_code(course_code):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
            course = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not course:
                return {'error': 'Course not found'}, 404
            
            return {'course': course}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def delete_course(course_code):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {'message': 'Course deleted successfully'}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

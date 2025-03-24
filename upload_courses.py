from app import db, create_app
from app.models import Course, Professor, CourseProfessor
import json

app = create_app()

def clean_credits(credits_str):
    """Convert credit strings to numeric values"""
    if not credits_str:
        return None
    try:
        # Handle ranges like "1 to 3" by taking the first value
        if 'to' in credits_str:
            return float(credits_str.split('to')[0].strip())
        return float(credits_str)
    except ValueError:
        return None

with open("courses.json", "r") as file:
    courses = json.load(file)

with app.app_context():
    for course_data in courses:
        # Clean and prepare data
        professor_name = course_data.pop("professor", "").strip()
        semester = course_data.get("semester")
        credits = clean_credits(course_data.get("credits"))
        course_data["credits"] = credits if credits is not None else 0.0
        
        # Skip if missing critical data
        if not semester or not course_data.get("course_code"):
            continue

        # Find or create course
        existing_course = Course.query.filter_by(
            course_code=course_data["course_code"],
            semester=semester
        ).first()

        if not existing_course:
            try:
                new_course = Course(**course_data)
                db.session.add(new_course)
                db.session.flush()  # Flush to get the ID without committing
                existing_course = new_course
            except Exception as e:
                print(f"Error creating course {course_data['course_code']}: {str(e)}")
                db.session.rollback()
                continue

        # Handle professor association if valid name exists
        if professor_name and professor_name not in (",", ""):
            professor = Professor.query.filter_by(name=professor_name).first()
            if not professor:
                professor = Professor(name=professor_name)
                db.session.add(professor)
                db.session.flush()
            
            # Check if relationship already exists
            existing_relationship = CourseProfessor.query.filter_by(
                course_id=existing_course.id,
                professor_id=professor.id,
                semester=semester
            ).first()
            
            if not existing_relationship:
                try:
                    course_professor = CourseProfessor(
                        course_id=existing_course.id,
                        professor_id=professor.id,
                        semester=semester,
                        specific_class_rating=None
                    )
                    db.session.add(course_professor)
                except Exception as e:
                    print(f"Error creating relationship for {professor_name}: {str(e)}")
                    db.session.rollback()

    try:
        db.session.commit()
        print("Courses and professors uploaded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Final commit failed: {str(e)}")
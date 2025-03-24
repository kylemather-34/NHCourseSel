import requests
import xml.etree.ElementTree as ET
import json

# URL of the XML file
XML_URL = "https://newhaven-web-01.newhaven.edu/CourseXML/data/courseXML_undergradfall.xml"

def save_to_json(data, filename="courses.json"):
    """Save the extracted course data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

def format_professor_name(professor_name):
    """Reformat professor names from 'lastname,firstname middleinitial' to 'Firstname Lastname'."""
    if not professor_name or not professor_name.strip():
        return "Not Available"  # Return a default value if the name is empty

    if "," in professor_name:
        lastname, firstname = professor_name.split(",", 1)
        firstname_parts = firstname.strip().split()
        if firstname_parts:  # Check if firstname_parts is not empty
            firstname = firstname_parts[0]
            formatted_name = f"{firstname} {lastname.strip()}"
            return formatted_name
    return professor_name.strip()

def fetch_xml_data(url):
    """Fetch the XML data from the given URL."""
    response = requests.get(url, stream=True)
    response.raw.decode_content = True  # Handle compressed responses
    return response.raw

def parse_course_element(course_element):
    """Parse a <course> element and extract relevant data."""
    instructor_element = course_element.find('instructor')
    professor_name = instructor_element.text.strip() if instructor_element is not None and instructor_element.text else "Not Available"

    course_dict = {
        "course_name": course_element.find('title').text.strip(),
        "course_code": course_element.find('offering').text.strip(),
        "section": course_element.find('sec').text.strip(),
        "semester": "Fall 2025",  # Hardcoded based on the page title
        "description": course_element.find('description').text.strip(),
        "examinations_assignments": "Unavailable",  # Default value
        "credits": course_element.find('credits').text.strip(),
        "prerequisites": "None",  # Default value
        "professor": format_professor_name(professor_name),
        "time": f"{course_element.find('start_time').text.strip()} - {course_element.find('end_time').text.strip()}",
        "location": course_element.find('location').text.strip(),
        "days": course_element.find('days').text.strip(),
        "term_dates": course_element.find('pterm_dates').text.strip()
    }
    return course_dict

def parse_xml(xml_file):
    """Parse the XML file and extract course data."""
    all_courses = []
    context = ET.iterparse(xml_file, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)  # Get the root element

    for event, elem in context:
        if event == 'end' and elem.tag == 'course':
            course_dict = parse_course_element(elem)
            all_courses.append(course_dict)
            elem.clear()  # Free memory
            root.clear()  # Free memory

    return all_courses

def main():
    """Main function to fetch XML data, parse it, and save to JSON."""
    print("Fetching XML data...")
    xml_file = fetch_xml_data(XML_URL)

    print("Parsing XML data...")
    all_courses = parse_xml(xml_file)

    print(f"Total courses extracted: {len(all_courses)}")
    save_to_json(all_courses)

if __name__ == "__main__":
    main()
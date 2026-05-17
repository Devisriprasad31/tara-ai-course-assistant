def normalize_courses(course_data):

    normalized_documents = []

    for course in course_data:

        content = f"""
        Title: {course.get("title", "")}

        Category: {course.get("category", "")}

        Level: {course.get("level", "")}

        Description: {course.get("description", "")}

        Skills: {", ".join(course.get("skills", []))}

        Prerequisites: {", ".join(course.get("prerequisites", []))}

        Career Outcomes: {", ".join(course.get("career_outcomes", []))}
        """

        document = {
            "content": content,
            "metadata": {
                "id": course.get("id"),
                "title": course.get("title"),
                "category": course.get("category"),
                "level": course.get("level"),
                "rating": course.get("rating")
            }
        }

        normalized_documents.append(document)

    return normalized_documents

def normalize_pdf_text(raw_text, source="PDF Document"):
    document = {
        "content": raw_text.strip(),
        "metadata": {
            "source": source,
            "type": "documentation"
        }
    }
    return [document]
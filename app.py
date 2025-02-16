from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["FILE_UPLOAD_FOLDER"] = "/home/derrick/Desktop/edms/uploads/"

user = {"email": "derrickmbarani@gmail.com", "password": "12345678"}

authenticated_user = {"id": "1", "name": "John Doe", "role": "Admin"}

registry = [
    {
        "id": 1,
        "created_by": {"id": "1", "name": "John Doe", "role": "Admin"},
        "description": "For the case between Jomo and Kasongo",
        "file_size": 4542,
        "file_type": "application/octet-stream",
        "file_url": "/home/derrick/Desktop/edms/uploads/shofco_logo-1.webp",
        "tag": "case_file",
    }
]

id_counter = 0

@app.post("/login")
def login():
    """Authenticate User"""
    payload = request.get_json()
    if payload.get("email") is None or payload.get("password") is None:
        return {"message": "invalid username or password"}, 400
    if payload.get("email") != user.get("email") or payload.get("password") != user.get(
        "password"
    ):
        return {"message": "invalid username or password"}, 400

    return {"message": "login successful"}, 200

# curl -X POST \
#   http://127.0.0.1:5000/document/upload \
#   -H 'Content-Type: multipart/form-data' \
#   -F "file=@/home/derrick/Downloads/images.webp" \
#   -F "tag=case_file"
#   -F "description=For the case between Jomo and Kasongo"
@app.post("/documents/upload")
def upload_file():
    """Upload Document"""
    payload = request.files

    form = dict(request.form)

    if "file" not in payload or payload["file"].filename == "":
        return {"message": "File not in request"}, 400

    file = payload["file"]
    filename = secure_filename(file.filename)

    file_url = os.path.join(app.config["FILE_UPLOAD_FOLDER"], filename)
    file.save(file_url)

    file_size = os.path.getsize(file_url)
    file_type = payload["file"].content_type

    global id_counter
    id_counter += 1
    file_uploaded = {
        "id": id_counter,
        "file_url": file_url,
        "file_size": file_size,
        "file_type": file_type,
        "created_by": authenticated_user,
        "tag": form.get("tag"),
        "description": form.get("description"),
    }
    registry.append(file_uploaded)

    return file_uploaded, 200

# curl -X GET http://localhost:6000/documents
@app.get('/documents')
def get_documents():
    '''''return all documets'''
    return registry, 200


# curl -X GET http://localhost:6000/documents/1
@app.get('/documents/<int:document_id>')
def get_document(document_id):
    """""retrieve a single document"""
    found_document= None
    for document in registry:       
        if document['id'] == document_id:
            found_document= document

    if found_document is None:
        return{"message": "document not found"}, 404
    
    return found_document, 200

if __name__ == "__main__":
    app.run(port=6000, debug=True)



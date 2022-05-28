from pydoc import doc
from flask import jsonify, request, make_response
from app import app
from app import db
from app import models

document_list = []


@app.route('/api/v1/index', methods=['POST'])
def add_document():
    document = models.Document(
        title=request.json.get('title', ""),
        body=request.json.get('body', ""),
    )
    db.session.add(document)
    db.session.commit()

    doc_tags = request.json.get('tags', "")
    for tag in doc_tags:
        tag_model = models.Tag(tag_text=tag)
        db.session.add(tag_model)
        document.tags.append(tag_model)
    db.session.commit()
    # print(request.json.get('tags', ""), 'requestststst')

    return make_response(f"{document} successfully created!")


@app.route('/api/v1/search/<search_word>', methods=['GET'])
def search_document(search_word):
    matched_documents = []
    related_documents = []
    print(search_word)

    results = db.session.query(models.Document)\
    .select_from(models.Document)\
    .join(models.document_tag)\
    .join(models.Tag)\
    .filter(models.Tag.tag_text == search_word)\
    .all()
    documents_schema = models.DocumentSchema(many=True)
    return jsonify(documents_schema.dump(results))


@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    documents = models.Document.query.all()
    documents_schema = models.DocumentSchema(many=True)
    return jsonify(documents_schema.dump(documents))

from pydoc import doc
from flask import jsonify, request, make_response
from sqlalchemy import and_, or_
from app import app
from app import db
from app import models, helper_function

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
    search_words = request.args
    removed_stop_word = helper_function.remove_stop_words(search_word).strip(" ")
    update_search_word = removed_stop_word if removed_stop_word else " "
    print(update_search_word, "hhhh", search_words)

    related_results = db.session.query(models.Document)\
    .select_from(models.Document)\
    .join(models.document_tag)\
    .join(models.Tag)\
    .filter(and_(models.Tag.tag_text == update_search_word, \
              (and_(models.Document.body.notlike("%{0}%".format(update_search_word)), \
                  models.Document.title.notlike("%{0}%".format(update_search_word))))))\
                .all()
    documents_schema = models.DocumentSchema(many=True)
    refined_related_results = documents_schema.dump(related_results)
    helper_function.format_tags(refined_related_results)

#     session.query(tbl_member) \
#   .filter(and_(models.Tag.tag_text == search_word, \
#               (or_(models.Document.body.notlike("%{0}%".format(search_word)),models.Document.title.like("%{0}%".format(search_word))))))

    results = db.session.query(models.Document)\
    .select_from(models.Document)\
    .join(models.document_tag)\
    .join(models.Tag)\
    .filter(or_(models.Document.body.like("%{0}%".format(update_search_word)), models.Document.title.like("%{0}%".format(update_search_word))))\
    .all()
    documents_schema = models.DocumentSchema(many=True)
    refined_results = documents_schema.dump(results)
    helper_function.format_tags(refined_results)

    return jsonify({"matched_documents": refined_results, "related_documents": refined_related_results})

@app.route('/api/v1/documents/<documents_slug>', methods=['GET'])
def get_document_slug(documents_slug):
    doc_slug = helper_function.make_document_slug(documents_slug)
    return jsonify({"document-slug": doc_slug})

@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    documents = models.Document.query.all()
    documents_schema = models.DocumentSchema(many=True)
    return jsonify(documents_schema.dump(documents))

names = ["Elena", "Eve", "Ulises", "Caio", "David"]


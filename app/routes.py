from pydoc import doc
from flask import jsonify, request, make_response
from sqlalchemy import and_, or_
from app import app
from app import db
from app import models, helper_function
# from slugify import slugify

# This endpoint creates a new document


@app.route('/api/v1/documents/index', methods=['POST'])
def add_document():
    if invalid_document(request.json):
        return jsonify({'error': 'Invalid input or missing value'}), 404
    elif ('title' not in request.json) or ('body' not in request.json) or ('tags' not in request.json):
        bad_request = {
            "error": "Invalid document object",
            "help_string":
                "Request format should be {'title': 'string',"
                "'body': 'string','tags': ['string'] }"
        }
        return jsonify({'bad_request': bad_request}), 400
    else:
        # The document is created and saved to the database
        document = models.Document(
            title=request.json.get('title', ""),
            slug_title=helper_function.make_document_slug(request.json.get('title', "")).lower(),
            body=request.json.get('body', ""),
        )
        db.session.add(document)
        db.session.commit()

        # For each slug created we add it to a particular document
        doc_tags = request.json.get('tags', "")
        for tag in doc_tags:
            tag_model = models.Tag(tag_text=tag)
            db.session.add(tag_model)
            document.tags.append(tag_model)
        db.session.commit()

        return make_response(jsonify({'message': 'successfully created!'}), 201)

# This function checks whether document submitted is valid

def check_slug(slug_doc):
    slug_doc = slug_doc.strip()
    return slug_doc.replace(' ','-')


def invalid_document(document_request):
    if not document_request:
        return True
    if('title' in document_request and (type(document_request['title']) != str
                                        or not document_request['title'].strip())):
        return True
    if('body' in document_request and (type(document_request['body']) != str or document_request['body'].strip() == "")):
        return True
    if('tags' in document_request and (type(request.json['tags']) != list or len(document_request['tags']) < 0)):
        return True


# This endpoint searches for keywords in the document body/title or tags
@app.route('/api/v1/documents/search/', methods=['GET'])
def search_document():
    searchTerm = request.args.get('search_term')
    if not searchTerm:
        return jsonify({'error': 'You need to enter a valid query with "search?"'})

    removed_stop_word = helper_function.remove_stop_words(searchTerm).strip(" ")

    if removed_stop_word:
        '''
        This query searches for documents which do have search words in their tags
        and not the body/title
        '''
        related_results = db.session.query(models.Document)\
        .select_from(models.Document)\
        .join(models.document_tag)\
        .join(models.Tag)\
        .filter(and_(models.Tag.tag_text == removed_stop_word, \
                (and_(models.Document.body.notlike("%{0}%".format(removed_stop_word)), \
                    models.Document.title.notlike("%{0}%".format(removed_stop_word))))))\
                    .all()
        documents_schema = models.DocumentSchema(many=True)
        refined_related_results = documents_schema.dump(related_results)
        helper_function.format_tags(refined_related_results)

        '''
        This query searches for documents which do have search words in the
        body/title
        '''
        results = db.session.query(models.Document)\
        .select_from(models.Document)\
        .join(models.document_tag)\
        .join(models.Tag)\
        .filter(or_(models.Document.body.like("%{0}%".format(removed_stop_word)), models.Document.title.like("%{0}%".format(removed_stop_word))))\
        .all()
        documents_schema = models.DocumentSchema(many=True)
        refined_results = documents_schema.dump(results)
        helper_function.format_tags(refined_results)

        return jsonify({"matched_documents": refined_results, "related_documents": refined_related_results})
    else:
        return jsonify({"matched_documents": [], "related_documents": []})

@app.route('/api/v1/documents/<document_slug>', methods=['GET'])
def get_document_slug(document_slug):

    if (check_slug(document_slug) != document_slug):
        return jsonify({'error': 'You need to enter a slug title'}), 400

    slug_doc = document_slug.replace('-',' ')
    doc_slug = helper_function.make_document_slug(slug_doc).strip(" ").lower()

    if doc_slug:
        '''
        This query searches for documents based on a slug provided
        '''
        results = db.session.query(models.Document)\
            .select_from(models.Document)\
            .join(models.document_tag)\
            .join(models.Tag)\
            .filter(models.Document.slug_title == doc_slug)\
            .all()
        documents_schema = models.DocumentSchema(many=True)
        refined_results = documents_schema.dump(results)
        helper_function.format_tags(refined_results)

        return jsonify({"matched_documents": refined_results})
    else:
        return jsonify({"matched_documents": [], "related_documents": []})

# This endpoint returns all the documents
@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    documents = models.Document.query.all()
    documents_schema = models.DocumentSchema(many=True)
    all_documents = documents_schema.dump(documents)
    helper_function.format_tags(all_documents)
    return jsonify(all_documents)



# mini_wiki
## Getting Started

This git repoisitory aims to achieve the following.

A /search -> A GET request that allows the user to search documents by the contents of the
title or the body. 

1. The search needs to strip the “stop words”
2. The search algorithm will always return 2 lists of results:
  1. Matched documents (by title or body)
  2. Related documents (other documents with the same tag)
 
As an example, a document can be indexed with a POST request into the /index endpoint containing the
following body: .
```
{
“title”: “I Robot”,
“body”: “this is the body of the document”,
“tags”: [“robots”, “sci-fi”]
}
```
Then, a user can search the document by words in the body (bearing in mind that stop words will be
ignored), title or tags. Then the return will be something like:

```
{
“matchedDocuments”: [
…
],
“relatedDocuments”: [
…
]
}
```
The following instructions will get you a copy of the project up and running on your local machine for development and testing purposes. These are specific to windows machines.

### Prerequisites

The following are things you need to have on your machine
* Python 3.9.4 and above
* Postman
* Browser(preferably chrome)
* IDE(sublime/visual studio code)
* GIT
* DOCKER


### Installing
This is a step by step process of how to get a development environment running.
1. Open your terminal and change to a directory where you want the project to live.
2. Clone the project using git clone `** git@github.com:Evie-ey/mini_wiki.git **`.
3. Create virtual environment.
4. Install all project dependencies using pip install -r requirements.txt
## Set environement variables
1. Create .flaskenv file and add this.
  *FLASK_APP=mini_wiki.py*
  *FLASK_ENV=development*
 Run the application using pyhton mini_wiki.py

5. Test the output using postman with the following endpoints

| Verb | Endpoint               | Functionality |Public Access |
|------|------------------------|---------------|--------------|
|POST   |/api/v1/documents/index | add new document|  True        |  
|GET   |/api/v1/documents|Fetch all documents|True |
|GET  |/api/v1/documents/search/?search_term=<search_term>| Return searched items and keywords|  True 
|GET  |/api/v1/documents//api/v1/documents/<slug-term> | Returns document based on slug title
  
  

from prov.model import ProvDocument

# create a new provenance document
d1 = ProvDocument()

# declaring namespaces for various prefixes used in the example
d1.add_namespace('now', 'http://www.provbook.org/nownews/')
d1.add_namespace('nowpeople', 'http://provbook.org/nownews/people/')
d1.add_namespace('bk', 'http://www.provbook.org/ns/#')

# Entity: now:employment-article-v1.html
el = d1.entity('now:employment-article-v1.html')
# Agent: nowpeople:Bob
d1.agent('nowpeople:bob')

# attributing the article to the agent
d1.wasAttributedTo(el, 'nowpeople:bob')

print(d1.get_provn())


# add more namespace declarations
d1.add_namespace('govftp', 'ftp://ftp.bls/gov/pub/special.requests/oes')
d1.add_namespace('void', 'http://vocab.deri.ie/void#')

# 'now:employment-article-v1' was derived from a dataset at govftp
d1.entity('govftp:oesm11st.zip', { 'prov:label': 'employment-stats-2011', 'prov:type': 'void:Dataset'})
d1.wasDerivedFrom('now:employment-article-v1.html', 'govftp:oesm11st.zip')

print(d1.get_provn())


# adding an activity
d1.add_namespace('is', 'http://www.provbook.org/nownews/is/#')
d1.activity('is:writeArticle')

# uage and generation
d1.used('is:writeArticle', 'govftp:oesm11st.zip')
d1.wasGeneratedBy('now:employment-article-v1', 'is:writeArticle')

# visualize the graph
from prov.dot import prov_to_dot
dot = prov_to_dot(d1)
dot.write_png('article-prov.png')

# or save it as a .pdf
dot.write_pdf('article-prov.pdf')

# display the image (only if running in a Jupyter Notebook)
# from Ipython.display import Image
# Image('article-prov.png')

# creating a prov-json serialization
print('********************')
print(d1.serialize(indent=2))
d1.serialize('article-prov.json')


# creating a prov-o RDF turtle serialization
print('********************')
d1.serialize('article-prov.ttl', format='rdf', rdf_format='ttl')


# connecting to ProvStore Api for storing Prov documents
from provstore.api import Api
api = Api(username='tomtom92', api_key='502deeb0d574ada76fb54dc89f019449a1f819d8')

# submit the document to ProvStore
provstore_document = api.document.create(d1, name='article-prov', public=False)

# generate a nice link to the document on ProvStore, as not to search manually for
# (only when working in Jupyter Notebook)
# from Ipython.display import HTML
# document_uri = provstore_document.url
# HTML('<a href="%s" target="_blank">Open your new provenance document on ProvStore</a>' % document_uri)


# retrieva back the document
retrieved_document = api.document.get(provstore_document.id)
d2 = retrieved_document.prov
d1 == d2 # are the submitted and retrieved documents the same?

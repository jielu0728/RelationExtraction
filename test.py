from gensim.models import word2vec


sentences = word2vec.Text8Corpus('./textdone')
model = word2vec.Word2Vec(sentences)
model.save('./model')
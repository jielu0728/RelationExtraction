import gensim

model = gensim.models.Word2Vec.load('./model')
print model['Eddard']
#print model.most_similar(positive=['Eddard','Robert'], negative=['Brandon'], topn=10)
#print model.similarity('Ned_Stark','Ned')
#print model.doesnt_match("Your Jaime Arya Edmure".split())


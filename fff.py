import nltk
import string
import jsonrpclib
import json
from nltk.corpus import wordnet as wn
from simplejson import loads
import re
from string import punctuation
server = jsonrpclib.Server("http://localhost:8080")
r = re.compile(r'[{}]'.format(punctuation))


text = '  The night was warm, but the thought of Riverrun was enough to make her shiver. Where are they? she wondered. Could her uncle have been wrong? So much rested on the truth of what he had told them. Robb had given the Blackfish three hundred picked men, and sent them ahead to screen his march. "Jaime does not know," Ser Brynden said when he rode back. "I\'ll stake my life on that. No bird has reached him, my archers have seen to that. We\'ve seen a few of his outriders, but those that saw us did not live to tell of it. He ought to have sent out more. He does not know."'

with open('./temp.gg', 'w') as fp:
    result = loads(server.parse(text))
    json.dump(result,fp)

fp.close()
import re

sentences = [{'body': '',
              'contextual_rate': -2,
              'uncontextual_rate': -2,
              'article_id': 0,
              'position_in_article': 0}]

with open('phrases_extended.txt', 'r') as reader:
    pos_iterator = 1
    for line in reader.readlines():
        splitted = re.split(r'\t+', line)
        
        if splitted[3] == sentences[-1]['article_id']:
            pos_iterator += 1
        else:
            pos_iterator = 1
            
        sent_dict = dict({'body': splitted[0],
                          'contextual_rate': splitted[1],
                          'uncontextual_rate': splitted[2],
                          'article_id': splitted[3],
                          'position_in_article': pos_iterator})
        sentences.append(sent_dict)
    sentences = sentences[1:]
    
pickle.dump(sentences, open('sentences_dict.dump', 'wb'))
import xml.etree.ElementTree as ET
import pickle
import os


class plWordNet():
    def __init__(self, path_to_wn):
        tree = pickle.load(open(path_to_wn, 'rb'))
        self.root = tree.getroot()

        exists = os.path.isfile('synunitmap.dump')
        if exists:
            self.synunitmap = pickle.load(open('synunitmap.dump', 'rb'))
        else:
            synsets = dict()
            for child in self.root.iter():
                if child.tag == "synset":
                    synset_id = child.attrib['id']
                    unit_list = list(child.findall("unit-id"))
                    synsets[synset_id] = [uid.text for uid in unit_list]
                    
            self.synunitmap = synsets

        self.units = self.root.findall('lexical-unit')
        self.relations = self.root.findall('synsetrelations')
        self.hyperonymy = []
        
        for child in self.relations:
            if child.attrib['relation'] in ['11', '211']:
            	self.hyperonymy.append(child)


    def printNFirstMappings(self, n=100):
        from heapq import nlargest

        for key in nlargest(10, self.synunitmap, key=self.synunitmap.get):
            print(key, self.synunitmap[key])
    
    def wordFromId(self, word_id):
        for child in self.units:
            if child.attrib['id'] == word_id:
                return child.attrib['name']
        raise ValueError("No such lexical unit ID in plWordNet")
        
        
    def idFromWord(self, word):
        for child in self.units:
            if child.attrib['name'] == word:
                return child.attrib['id']
        raise ValueError("No such lexical unit in plWordNet")
        

    def synsetsForWord(self, word='', word_id='', tagtype='name'):
        ''' 
        Find synset for a word (given by id or name).
        The loop iterates through synset - lex. unit mapping.
        '''
        if tagtype == 'name':
            word_id = idFromWord(word)
        
        synsets = []
        for s in self.synunitmap.keys():
            if word_id in self.synunitmap[s]:
                synsets.append(s)
        
        return synsets


    def getHyponymsFromWord(self, word):
        synsets_for_word = synsetsForWord(word=word)
        hypo_synsets = []
        
        for child in self.hyperonymy:
            if child.attrib['parent'] in synsets_for_word:
                hypo_synsets.append(child.attrib['child'])
        
        hyponyms = []
        for s in hypo_synsets:
            hyponyms = list(set().union(hyponyms, self.synunitmap[s]))
        
        return [wordFromId(word_id) for word_id in hyponyms]

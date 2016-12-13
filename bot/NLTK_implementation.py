
# nltk implementation
import json
import logging
import nltk
import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

class NLTK(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
    def recieve_text(self,text):
        text = text
        words = text.flatMap(word_tokenize)
        test1 = words.take(10)
        pos_word = words.map(pos_tag)
        test2 = pos_word.take(5)
        return test1, test2
    def word_feats(words):
        return dict([(word, True) for word in words])
    def word_tokenize(x):
        return nltk.word_tokenize(x)
    def pos_tag(x):
        return nltk.pos_tag([x])




dat=str(nltk.data.load('corpora/final_dataset/'+str(address),format='raw')).lower()#dat contains data of the current text files
        tokenizer=list(sent_tokenize(dat))#all the data being tokenized into sentences and made alist of that
        features=[]  #for all sent tokenizer it will have data as list of list containing noun phrases
        for i in range(len(tokenizer)):
            words=nltk.word_tokenize(tokenizer[i])#for each sentence all words have been tokenized
            tagged=nltk.pos_tag(words)#pos tags given
            chunkgram=r"""Chunk: {<JJ.?>*<NN.?>*<NNPS>*<NN.?>}"""#now extracting only noun phrases i.e,extracting medical terms
            chunkparser=nltk.RegexpParser(chunkgram)
            chunked=chunkparser.parse(tagged)
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                features.append(list(subtree))
        featuresetnounphrase=[] #it contains noun phrases features in appropriate format
        for featureset in features:#here featureset is an individual list
            stri=''
            for members in featureset:
                if '.\\n' in members[0]:
                    stri=stri+str(members[0].replace('.\\n',''))#to remove .\\n characters from features that was automatically coming with chunking
                elif '.' in members[0]:
                    stri=stri+str(members[0].replace('.',''))#to remove . character from the feature that was automatically coming with chunking
                else:
                     stri=stri+str(members[0])
            featuresetnounphrase.append(stri)
        featuresetnounphrase=list(set(featuresetnounphrase))
        #print(len(featuresetnounphrase))
        #now stemming all the words and having them as features
        tokenizer1=RegexpTokenizer(r'\w+')
        tokenized_data=tokenizer1.tokenize(dat)
        #print(tokenized_data)
        single_letter_data=list(string.ascii_lowercase)
        stop_words = set(stopwords.words('english'))
        filtered_words = [w for w in tokenized_data if not w in stop_words]
        filtered_words = [w for w in filtered_words if not w in single_letter_data]
        filtered_words=nltk.pos_tag(filtered_words)
        #print(filtered_words)

        ps=PorterStemmer()
        refiltered_words=[]#stemming performed
        for word_count in range(len(filtered_words)):
            if filtered_words[word_count][1]!='CD':   #not taking numbers as 'CD' represents numbers,NOTE: word_count[1]represents pos tag
                refiltered_words.append(ps.stem(filtered_words[word_count][0]))
        refiltered_words=list(set(refiltered_words))


        for nounphrases in featuresetnounphrase:
            refiltered_words.append(nounphrases)
        refiltered_words=list(set(refiltered_words))#refilteres_words contains all the features for a particular file.
        c_number=category_folders[cat_no]
        filewrite = open(str(path1)+str(c_number)+"\\"+str(file),'w')
        for all_items in refiltered_words:
            filewrite.write("%s," % all_items)
        filewrite.close()
    print("done for another category:")
    '''

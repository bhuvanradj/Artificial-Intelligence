"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import time
import numpy as np


def baseline(train, test):
        '''
        TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
        input:  training data (list of sentences, with tags on the words)
                   E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
                  test data (list of sentences, no tags on the words)
                  E.g  [[word1,word2,...][word1,word2,...]]
        output: list of sentences, each sentence is a list of (word,tag) pairs.
               E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
         '''

        predicts = []
        ttags = {}
        wtcount = {}

        for sentence in train:
                for wordtag in sentence:
                        word, tag = wordtag
                        if tag not in ttags:
                                ttags[tag] = 1
                        else:
                                ttags[tag] += 1

                        if word not in wtcount:
                                wtcount[word] = {}
                        if tag in wtcount[word]:
                                wtcount[word][tag] += 1
                        else:
                                wtcount[word][tag] = 1

        maxtag = max(ttags.keys(), key=(lambda key: ttags[key]))

        for sentence in test:
                spred = []
                for word in sentence:
                        if word in wtcount:
                                t = wtcount[word]
                                best = max(t.keys(), key=(lambda key: t[key]))
                                spred.append((word, best))
                        else:
                                spred.append((word, maxtag))
                predicts.append(spred)

        return predicts


def viterbi_p1(train, test):
    '''
        TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
                input:  training data (list of sentences, with tags on the words)
                        E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
                        test data (list of sentences, no tags on the words)
                        E.g [[word1,word2...]]
                output: list of sentences with tags on the words
                        E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    
    predicts = [] 
    ptag = {} 
    ntrans = {} 
    ttrans = {} 
    nems = {} 
    tems = {} 
    uinit = {} 
    utrans = {} 
    uem = {} 
    pinit = {} 
    ptrans = {} 
    pem = {} 
    smol = 0.000001

    for sentence in train:
        ftag = sentence[0][1]
        if ftag not in pinit:
            pinit[ftag] = 1
        else:
            pinit[ftag] += 1

    for sentence in train:
        for wordtag in sentence:
            tag = wordtag[1]
            if tag not in ptag:
                ptag[tag] = 1
            else: 
                ptag[tag] += 1
        
    for x in ptag:
        if x in pinit:
            pinit[x] = np.log((pinit[x]+smol)/(len(train)+len(ptag)))
        else:
            uinit[x] = np.log((smol)/(len(train)+len(ptag)))

    for sentence in train:
        for x in range(len(sentence)-1):
            p = (sentence[x][1],sentence[x+1][1])
            if p not in ptrans:
                ptrans[p] = 1
                if sentence[x][1] not in ntrans:
                    ntrans[sentence[x][1]] = 1
                    ttrans[sentence[x][1]] = 1
                else:
                    ntrans[sentence[x][1]] += 1
                    ttrans[sentence[x][1]] += 1
            else:
                ptrans[p] += 1
                ntrans[sentence[x][1]] += 1
    
    for p in ptrans:
        fp = np.log((ptrans.get(p)+smol)/(ptag.get(p[0])+smol*len(ptag)))
        ptrans[p] = fp

    for n in ntrans:
        fp = np.log(smol/(ptag.get(n) + smol*len(ptag)))
        utrans[n] = fp
    
    for sentence in train:
        for wordtag in sentence:
            tag = wordtag[1]
            if wordtag not in pem:
                pem[wordtag] = 1
                if tag not in nems:
                    nems[tag] = 1
                    tems[tag] = 1
                else:
                    nems[tag] += 1
                    tems[tag] += 1
            else:
                pem[wordtag] +=1
                nems[tag] += 1
    
    for p in pem:
        fp = np.log((pem.get(p)+smol)/(ptag.get(p[1])+smol*len(ptag)))
        pem[p] = fp
    
    for n in nems:
        fp = np.log(smol/(ptag.get(n) + smol*len(ptag)))
        uem[n] = fp

    for sentence in test:
        ll = []
        dl = []
        for x in range(len(sentence)):
            dw = {}
            if x==0:
                for p in ptag:
                    if p in pinit:
                        dw[(sentence[x],p)] = [pinit.get(p), 'None']
                    else: 
                        dw[(sentence[x],p)] = [uinit.get(p), 'None']
                    if (sentence[x],p) in pem:
                        dw.get((sentence[x],p))[0] += pem.get((sentence[x],p))
                    else:
                        dw[(sentence[x],p)][0] += uem.get(p)
                dl.append(dw)
            else:
                for t in ptag:
                    tl = []
                    for itm in dl[x-1]:
                        if(itm[1],t) in ptrans:
                            trans = ptrans.get((itm[1],t))
                            pr = dl[x-1].get(itm)[0]+trans
                            if(sentence[x],t) in pem:
                                pr += pem.get((sentence[x],t))
                            else:
                                pr += uem.get(t)
                            tl.append((itm[1],pr))
                        else:
                            trans = utrans.get(itm[1])
                            pr = dl[x-1].get(itm)[0]+trans
                            if(sentence[x],t) in pem:
                                pr += pem.get((sentence[x],t))
                            else:
                                pr += uem.get(t)
                            tl.append((itm[1],pr))
                    tl.sort(key=lambda y:y[1])
                    dw[sentence[x],t] = [tl[len(tl)-1][1],tl[len(tl)-1][0]]
                dl.append(dw)
    
        lpr = float("-inf")
        lkey = ('None','None')   
        for k in dl[len(dl)-1]:
            if dl[len(dl)-1].get(k)[0] > lpr:
                lpr = dl[len(dl)-1].get(k)[0]
                lkey = k
        last = lkey
        start = len(dl)-1
        for x in range(start, -1, -1):
            ll.append(last)
            if x >= 1:
                tmp = dl[x].get(last)
                last = (sentence[x-1], tmp[1])         
        ll.reverse()
        predicts.append(ll)
    return predicts
    

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    predicts = []
    raise Exception("You must implement me")
    return predicts

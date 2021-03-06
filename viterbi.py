"""source: http://en.wikipedia.org/wiki/Viterbi_algorithm
The code has been modified to match our Bigram models:
- models are dictionaries with tuples as keys
- starting probabilities are not separate and end probabilities are also
taken into consideration
- transProbs should be a Bigram instance
- tagProbsByPos should be a list containing, for each position, 
  the probability distribution over tags as returned by the maxent model
- all probabilities are expected to be in log space"""

def viterbi(transProbs, tagProbsByPos, languageModelWeight, boundarySymbol='S'):
    V = [{}]
    path = {}
    states = transProbs.tags
    # Initialize base cases (t == 0)
    for y in states:
        trProb = transProbs.logProb(boundarySymbol,y)
        tagProb = tagProbsByPos[0][y]
        unigrProb = transProbs.unigramLogProb[y]
        V[0][y] = trProb+tagProb-unigrProb
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1,len(tagProbsByPos)):
        V.append({})
        newpath = {}
 
        for y in states:
            if t == len(tagProbsByPos):
                (prob, state) = max([languageModelWeight*transProbs.logProb(y, boundarySymbol) + \
                                (V[t-1][y0] + \
                                languageModelWeight*transProbs.logProb(y0,y) + \
                                tagProbsByPos[t][y] - \
                                transProbs.unigramLogProb[y], #dividing by a priori probability so as not to count it twice
                                y0) for y0 in states])
            else:
                (prob, state) = max([(V[t-1][y0] + \
                                languageModelWeight*transProbs.logProb(y0,y) + \
                                tagProbsByPos[t][y] - \
                                languageModelWeight*transProbs.unigramLogProb[y], #dividing by a priori probability so as not to count it twice
                                y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
 
    (prob, state) = max([(V[len(tagProbsByPos) - 1][y], y) for y in states])
    return (prob, path[state])

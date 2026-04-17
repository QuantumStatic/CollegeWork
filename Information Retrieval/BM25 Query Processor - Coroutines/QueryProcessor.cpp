//
//  QueryProcessor.cpp
//  HW 3
//
//  Created by Utkarsh Jain on 01/11/23.
//

#include <algorithm>
#include <boost/algorithm/string.hpp>
#include <cmath>
#include <map>
#include <numeric>
#include <queue>
#include <sstream>
#include <string>
#include <unordered_set>

#include "QueryProcessor.hpp"

using std::map;
using std::pair;
using std::priority_queue;
using std::string;
using std::unordered_set;
using std::vector;

QueryProcessor::QueryProcessor(){
    this->_docManager = SearchDocManager();
}

// Calculates K constant for the a docId
float QueryProcessor::_calcDocConstantForBM25(int docId, float k1, float b=0.75){
    float K;
    
    K = k1 * ((1 - b) + b*this->_docManager.getLengthOfDoc(docId)/QueryProcessor::_avgDocLength);
    
    return K;
}

// Given a docId and queries this can accumulate all scores
float QueryProcessor::_BM25ForDocId(int docId, const vector<string>* words, float k1){
    float docKValue = this->_calcDocConstantForBM25(docId, k1);
    float temp=0.0;
    
    /*  This implementation uses reduce so that when apple fully implements reduce, this can be sped up
     using std::execution::parallel which will sum these in parallel*/
//    return std::reduce(words->begin(), words->end(), temp,
//               [&](double acum, const string& word) {
//                   int wordFreq = this->_docManager.getWordOccurenceFrequency(word);
//                   int wordInDocFreq = this->_docManager.wordInDocFreq(word, docId);
//                   return acum + log10((QueryProcessor::_totalDocuments - wordFreq + 0.5)/(wordFreq + 0.5)) * ((k1 + 1.0)*((double)wordInDocFreq)/((double)(docKValue + wordInDocFreq)));
//               });
    
    // TODO: Generator for frequencies
    // TODO: Word Occurence Frequency store
    for (const string &word: *words){
        int wordFreq = this->_docManager.getWordOccurenceFrequency(word);
        int wordInDocFreq = this->_docManager.wordInDocFreq(word, docId);
        temp += log10((QueryProcessor::_totalDocuments - wordFreq + 0.5)/(wordFreq + 0.5)) * ((k1 + 1.0)*((double)wordInDocFreq)/((double)(docKValue + wordInDocFreq)));
    }
    
    return temp;

}

float QueryProcessor::_bareBonesBM25(int docId, int wordFreq, int wordInDocFreq, float k1){
    float docKValue = this->_calcDocConstantForBM25(docId, k1);

    return log10((QueryProcessor::_totalDocuments - wordFreq + 0.5)/(wordFreq + 0.5)) * ((k1 + 1.0)*((double)wordInDocFreq)/((double)(docKValue + wordInDocFreq)));
}

// Definition of comparision operator for the custom priority queue
struct ComparePair {
    bool operator()(const pair<float, int>& a, const pair<float, int>& b) {
        return a.first > b.first; // This will create a min-heap based on the first element of the pair
    }
};

// BM25 for multiple docids and words
vector<pair<float, int>> QueryProcessor::_BM25(vector<int> docIds, const vector<string>* words, short K=10){
    
    priority_queue<pair<float, int>, vector<pair<float, int>>, ComparePair> pq;
    
    // Maintinaing a priority queue with top K documents using a minheap
    for (const int &docId : docIds) {
        float val = this->_BM25ForDocId(docId, words);
        pq.emplace(val, docId);
        
        if (pq.size() > K)
            pq.pop();
    }
    
    vector<pair<float, int>> orderedDocs;
    
    while (not pq.empty()){
        orderedDocs.push_back(pq.top());
        pq.pop();
    }
    
    // reversing them so the highest score goes first
    std::reverse(orderedDocs.begin(), orderedDocs.end());
    return orderedDocs;
    
}

vector<pair<float,int>> QueryProcessor::_runConjunctiveQuery(const vector<string>* words){
    
    // Older conjunctive query, see _runConjunctiveQuery2 for proper documentation
    
    vector<const vector<int>*> allDocIds;
    
    for (const string &word: *words){
        const vector<int>* docIds = this->_docManager.getDocIdsForWord(word);
    
        if (not docIds->empty())
            allDocIds.push_back(docIds);
    }
    
    vector<int> result;
    
    if (allDocIds.empty()){
        return vector<pair<float, int>>();
    } else if (allDocIds.size() == 1) {
        result = *allDocIds[0];
    } else {
        bool found = true;
        for (const int& docId: *allDocIds[0]) {
            found = true;
            for (int i=1; i < allDocIds.size(); i++)
                if (not this->_docManager.wordInDoc(words->at(i), docId)){
                    found = false;
                    break;
                }
            
            if (found)
                result.push_back(docId);
        }
        allDocIds.clear();
    }
    
    // Tried to use reduce in parallel but Apple Clang doesn't support it right now.
    /*
    vector<int> result = std::reduce(std::execution::par, std::next(allDocIds.begin()), allDocIds.end(), allDocIds[0],
         [&](const vector<int> a, const vector<int> b){
            vector<int> tempVec;
            std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::back_inserter(tempVec));
            return tempVec;
        });
     */
    
    // TODO: Further filter BM25 values using something else?
    
    vector<pair<float, int>> results = this->_BM25(result, words);
    
    vector<string> a;
    a.push_back("hi");
    
    return results;
    
}

vector<pair<float,int>> QueryProcessor::_runConjunctiveQuery2(const vector<string>* words, short K){
    
    vector<int> wordLengths;
    
    // Get length of inverted indexes
    for (const string &word: *words){
        int freq = this->_docManager.getWordOccurenceFrequency(word);
        if (freq > 0)
            wordLengths.push_back(freq);
    }
    
    // Sorting based on length of inverted indexes of the words
    std::vector<size_t> indices(wordLengths.size());
    std::iota(indices.begin(), indices.end(), 0);
    
    std::sort(indices.begin(), indices.end(),
        [&wordLengths](size_t a, size_t b) {
            return wordLengths[a] < wordLengths[b];
        });
    
    vector<string>* modifiableWords = new vector<string>;
    modifiableWords->reserve(words->size());
    
    // Sort complete
    for (const auto &indice: indices)
        modifiableWords->push_back(words->at(indice));
    
//    vector<int> result;
    priority_queue<pair<float, int>, vector<pair<float, int>>, ComparePair> pq;
    
    if (wordLengths.empty()){
        return vector<pair<float, int>>();
    } else {
        int docId = 0;
        vector<generator<int>> docIdGenerators;
        vector<bool> produceNextHold(modifiableWords->size(), false);
        
        // Creating coroutines for each word
        for (const string &word: *modifiableWords)
            docIdGenerators.push_back(this->_docManager.getIterativeDocIdByWordAndPos(word));
        
        while (true) {
            // Using the coroutine to compute the next value
            docIdGenerators[0].move_next();
            docId = docIdGenerators[0].current_value();
            
            if (docId == -1)
                break;
            
            bool found = true, goToNextId=false;
    
            for (int i=1; i < words->size(); i++){
                while (true) {
                    
                    // Sometimes we don't want to shift to the next value in the list
                    if (not produceNextHold[i])
                        docIdGenerators[i].move_next();
                    
                    // Gets the current value from current state of the coroutine
                    int innerDocId = docIdGenerators[i].current_value();
                    
                    // List has ended or other lists don't have the docId so we put a hold on fetching the next ID
                    if (innerDocId == -1 or innerDocId > docId){
                        found = false;
                        goToNextId = true;
                        produceNextHold[i] = true;
                        break;
                    // Doc ID match !
                    } else if (innerDocId == docId){
                        produceNextHold[i] = false;
                        break;
                    }
                    produceNextHold[i] = false;

                }
                // Loop management with multiple flags
                if (goToNextId)
                    break;
            }
            if (found){
//                result.push_back(docId);
                float val = this->_BM25ForDocId(docId, words);
                pq.emplace(val, docId);
                
                if (pq.size() > K)
                    pq.pop();
            }
        }
        docIdGenerators.clear();
    }
    
    vector<pair<float, int>> results; // = this->_BM25(result, words);
    
    while (not pq.empty()){
        results.push_back(pq.top());
        pq.pop();
    }
    
    std::reverse(results.begin(), results.end());
    
    return results;
    
}

vector<pair<float, int>> QueryProcessor::_maxxScore(vector<vector<int>> sortedDocIds, const vector<string>* words, vector<float> maxBM25scores, short K=10){
    
    // Older MaxxScore, see _maxxScore2 for proper documentation
    
    size_t nePos = sortedDocIds.size();
    float maxScore=maxBM25scores[nePos], threshold=0.0;
    priority_queue<pair<float, int>, vector<pair<float, int>>, ComparePair> pq;
    unordered_set<int> evaluatedDocIds;
    
    for (size_t i=0; i < sortedDocIds.size(); i++){
        if (i == nePos)
            break;
        
        while (not sortedDocIds[i].empty() and i != nePos){
            int docId = sortedDocIds[i].back();
            sortedDocIds[i].pop_back();
            
            if (evaluatedDocIds.contains(docId))
                continue;
            
            evaluatedDocIds.insert(docId);
            
            float docIdScore=this->_BM25ForDocId(docId, words);
            
            if (docIdScore > threshold){
                pq.emplace(docIdScore, docId);
                
                if (pq.size() > K){
                    pq.pop();
                    threshold = pq.top().first;
                }
                
                for (size_t i = nePos-1; i >= 0; i--) {
                    if (maxScore + maxBM25scores[i] <= threshold){
                        maxScore += maxBM25scores[i];
                        nePos--;
                    } else break;
                }
            }
        }
    }
    
    vector<pair<float, int>> orderedDocs;
    
    while (not pq.empty()){
        orderedDocs.push_back(pq.top());
        pq.pop();
    }
    
    std::reverse(orderedDocs.begin(), orderedDocs.end());
    
    return orderedDocs;
    
}


int QueryProcessor::getFrequencyByIDAtleast(int Id, generator<int>* docIdGen, generator<int>* FreqGenerator){
    int id=0;
    while (true) {
        id = docIdGen->current_value();
        if (id == Id)
            return FreqGenerator->current_value();
        else if (id > Id or id == -1)
            return 0;
        docIdGen->move_next();
        FreqGenerator->move_next();
    }
}


std::vector<std::pair<float, int>> QueryProcessor::_maxxScore2(const std::vector<std::string>* words, std::vector<float> maxBM25scores, short K) {
    size_t nePos = words->size();
    float maxScore=0.0, threshold=0.0;
    priority_queue<pair<float, int>, vector<pair<float, int>>, ComparePair> pq;
    unordered_set<int> evaluatedDocIds;
    
    vector<string> wordsCopy;
    std::copy(words->begin()+1, words->end(), std::back_inserter(wordsCopy));
    
    // storing how many times a term occurs in a document to reduce computation in BM25.
    vector<int> wordFreqs;
    for (const string &word: *words)
        wordFreqs.push_back(this->_docManager.getWordOccurenceFrequency(word));
    
    // Iterate over all lists
    for (size_t i=0; i < words->size(); i++){
        if (i == nePos)
            break;
        
        // Get generator for current docId
        std::cout << "starting " << i << std::endl;
        generator<int> docIdGenerator = this->_docManager.getIterativeDocIdByWordAndPos(words->at(i));
        generator<int> freqGenerator = this->_docManager.getIterativeFreqByWord(words->at(i));
        
        vector<generator<int>> otherDocIds, otherFreqs;
        
        // Generators for sequential access later on
        for (size_t j=i+1; j < words->size(); j++){
            otherDocIds.push_back(this->_docManager.getIterativeDocIdByWordAndPos(words->at(j)));
            otherFreqs.push_back(this->_docManager.getIterativeFreqByWord(words->at(j)));
        }
        
        int docId=-1;
        while (true){
            bool check = docIdGenerator.move_next();
            docId = docIdGenerator.current_value();
            
            // If the list ends or has been declared non essential time to break
            if (docId == -1 or i == nePos)
                break;
            
            freqGenerator.move_next();
            int freq = freqGenerator.current_value();
            
            // have we checked this doc Id before?
            if (evaluatedDocIds.contains(docId))
                continue;
            
            evaluatedDocIds.insert(docId);
            
            float docIdScore = this->_bareBonesBM25(docId, wordFreqs[i], freq);
            
            // Find docIds in other terms to get accurate scores
            for (size_t j = 0; j < otherDocIds.size(); j++){
                int freq = this->getFrequencyByIDAtleast(docId, &otherDocIds[j], &otherFreqs[j]);
                if (freq > 0)
                    docIdScore += this->_bareBonesBM25(docId, wordFreqs[j], freq);
            }

            
            // Is it really worth it to add the docId to our store?
            if (docIdScore > threshold or pq.size() < K){
                pq.emplace(docIdScore, docId);
                
                // If we have top K then we need to keep the best ones so far
                if (pq.size() > K){
                    pq.pop();
                    threshold = pq.top().first;
                }
                
                // Re-evaluating the NE threshold
                for (size_t j = nePos-1; j >= 0; j--) {
                    if (maxScore + maxBM25scores[j] <= threshold){
                        maxScore += maxBM25scores[j];
                        nePos--;
                    } else break;
                }
            }
        }
    }
    
    vector<pair<float, int>> orderedDocs;
    
    while (not pq.empty()){
        orderedDocs.push_back(pq.top());
        pq.pop();
    }
    
    std::reverse(orderedDocs.begin(), orderedDocs.end());
    
    return orderedDocs;
    
}

vector<pair<float, int>> QueryProcessor::_runDisjunctiveQuery(const vector<string>* words){
    
    // This is the older version, see _runDisjunctiveQuery2 for proper documentaion
    
    vector<const vector<int>*> allDocIds;
    vector<float> maxBM25scores;
    
    for (const string &word: *words){
        const vector<int>* docIds = this->_docManager.getDocIdsForWord(word);
    
        if (not docIds->empty()){
            allDocIds.push_back(docIds);
            maxBM25scores.push_back(this->_docManager.getMaxBM25score(word));
        }
    }
    
    // Sorting based on BM25 scores of the words
    std::vector<size_t> indices(allDocIds.size());
    std::iota(indices.begin(), indices.end(), 0);
    
    std::sort(indices.begin(), indices.end(),
        [&maxBM25scores](size_t a, size_t b) {
            return maxBM25scores[a] > maxBM25scores[b];
        });
    
    std::vector<std::vector<int>> sortedDocIds(allDocIds.size());
    
    
    for (size_t i = 0; i < indices.size(); ++i)
        sortedDocIds[i] = *allDocIds[indices[i]];
    
    allDocIds.clear();
    // Sorting ends
    
    std::sort(maxBM25scores.begin(), maxBM25scores.end(), std::greater<int>());
    vector<pair<float, int>> results = this->_maxxScore(sortedDocIds, words, maxBM25scores);
    
    return results;
}

vector<pair<float, int>> QueryProcessor::_runDisjunctiveQuery2(const vector<string>* words, short K){

    vector<float> maxBM25scores;
    
    // Fetches the max BM25 scores to sort the docIds
    for (const string &word: *words){
        float BM25Scores = this->_docManager.getMaxBM25score(word);
        if (BM25Scores > 0)
            maxBM25scores.push_back(BM25Scores);
    }
    
    // Sorting based on BM25 scores of the words
    std::vector<size_t> indices(maxBM25scores.size());
    std::iota(indices.begin(), indices.end(), 0);
    
    std::sort(indices.begin(), indices.end(),
        [&maxBM25scores](size_t a, size_t b) {
            return maxBM25scores[a] > maxBM25scores[b];
        });
    
    vector<string>* modifiableWords = new vector<string>;
    modifiableWords->reserve(words->size());
    
    // Sorting ends
    for (const auto &indice: indices)
        modifiableWords->push_back(words->at(indice));
    
    if (maxBM25scores.empty())
        return vector<pair<float, int>>();
    
    std::sort(maxBM25scores.begin(), maxBM25scores.end(), std::greater<int>());
    vector<pair<float, int>> results = this->_maxxScore2(modifiableWords, maxBM25scores, K);
    
    return results;
}

vector<string> QueryProcessor::runQuery(string query, int queryType, short K){
    
    vector<pair<float, int>> results;
    vector<string> words;
    
    // convert query words to lower case
    boost::to_lower(query);
    
    std::stringstream ss(query);
    string word;
    
    while(ss >> word)
        words.push_back(word);
    
    // Running the appropriate query
    if (queryType == QueryProcessor::CONJUNCTIVE)
        results = this->_runConjunctiveQuery2(&words, K);
    else if (queryType == QueryProcessor::DISJUNCTIVE)
        results = this->_runDisjunctiveQuery2(&words, K);
    else return vector<string>();
    
    vector<string> snippets;
    
    // Generating snippets
    for (const pair<float, int> &result: results){
        string url = this->_docManager.getDocUrl(result.second);
        float BM25Score = result.first;
        string snippet = this->_generateSnippet(result.second, &words);
        snippets.push_back(url + " " + std::to_string(BM25Score) +"\n"+snippet);
    }
    
    return snippets;
}

string QueryProcessor::_generateSnippet(int docId, const vector<string>* words, short snippetLimit){
    string docText = this->_docManager.getDocumentText(docId);
    map<size_t, size_t> sentencePositions;
    
    if (not docText.empty())
        docText = docText.substr(docText.find(" ") + 1);
    
    for (const string &word: *words){

        size_t pos = docText.find(word);
        
        /* If the word is in the document or if we have reached the snippet limit is the new sentence
        closer to the beginning */
        if (pos != string::npos and (!(sentencePositions.size() >= snippetLimit) or pos < sentencePositions.rbegin()->second)) {
            
            bool dontFindSentence = false;
            
            // Is the word in one of the words previously found
            for (const auto &startStop: sentencePositions) {
                if (startStop.first <= pos and pos <= startStop.second) {
                    dontFindSentence = true;
                    break;
                }
            }
            
            // No it's new word
            if (not dontFindSentence){
                short spaceCount=0;
                size_t iter = pos, start = 0, stop = 0;
                
                short letterPadCount = 0;
                
                // Determining start of the sentence
                while(spaceCount < 16 and iter > 0 and letterPadCount < 10 and iter < docText.size()){
                    switch (docText.at(iter)) {
                        case ' ':
                            spaceCount++;
                            iter--;
                            break;
                        case '.':
                            start = iter+1;
                            iter--;
                            break;
                        default:
                            iter--;
                            if (start != 0){
                                letterPadCount++;
                                start--;
                            }
                    }
                }
                if (start == 0)
                    start = iter;
                
                // Determining end of sentence
                iter = pos + 1; spaceCount = 0;
                letterPadCount = 0; stop = -1;
                while(spaceCount < 15 and iter < docText.size() - 1 and letterPadCount < 10 and iter < docText.size()){
                    const char ch = docText.at(iter);
                    switch (ch) {
                        case ' ':
                            spaceCount++;
                            iter++;
                            break;
                        case '.':
                            stop = iter;
                            iter++;
                            break;
                        default:
                            iter++;
                            if (stop != -1){
                                letterPadCount++;
                                stop++;
                            }
                    }
                }
                if (stop == -1)
                    stop = iter;
                
                sentencePositions.emplace(start, stop);
                
                // Keeping a small pool of snippetLimit number of sentences
                // checking if we have to add beyond the set limit
                if (sentencePositions.size() >= snippetLimit)
                    sentencePositions.erase(--sentencePositions.end());

            }
        }
    }
    
    string result;
    result.reserve(109*5);
    
    // Combinging everything into a single sentence
    for (const auto &startStop: sentencePositions){
        if (not result.empty())
            result.push_back(' ');
        result += docText.substr(startStop.first, startStop.second - startStop.first) + ".";
    }
    
    result.shrink_to_fit();
    return result;
}

void QueryProcessor::clearSearchDocs(){
    this->_docManager.clearFileStuff();
}

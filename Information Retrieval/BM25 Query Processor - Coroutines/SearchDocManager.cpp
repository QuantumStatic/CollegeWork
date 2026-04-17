//
//  SearchDocManager.cpp
//  HW 3
//
//  Created by Utkarsh Jain on 31/10/23.
//

#include <array>
#include <algorithm>
#include <boost/algorithm/string.hpp>
#include <memory>
#include "SearchDocManager.hpp"

using std::getline;
using std::pair;
using std::string;
using std::vector;


SearchDocManager::SearchDocManager(){
    _initPathAndFiles();
}

void SearchDocManager::_initPathAndFiles(){
    this->_currDirectory = "/Users/utkarsh/Desktop/Utkarsh/NYU/Year 1/Semester 1/Web Search Engines/Assignments/HW 2/HW2/output3";
    
    this->_invertedFile = std::ifstream(this->_currDirectory + "/fin.bin", std::ios::binary);
    this->_createLexiAndDocTable();
}

void SearchDocManager::_createLexiAndDocTable(){
    std::ifstream lexiconFile(this->_currDirectory + "/lexi.txt");
    std::ifstream docTable(this->_currDirectory + "/docToUrlTable.txt");
    
    string line;
    while (getline(lexiconFile, line)) {
        size_t pos = line.find(":");
        string word = line.substr(0, pos);
        string lexiString = line.substr(pos + 1);
        this->_lexiTableWords.push_back(word);
        this->_lexiTableStrings.push_back(lexiString);
    }
    
    lexiconFile.close();
    line.clear();
    
    while (getline(docTable, line)) {
        size_t pos = line.find(":");
        string word = line.substr(0, pos);
        string docString = line.substr(pos + 1);
//        this->_docTableIds.push_back(std::stoi(word));
        this->_docTableStrings.push_back(docString);
    }
    
    docTable.close();
    line.clear();
}

string SearchDocManager::_searchDocTableById(int docId) const{
    
    if (docId >= this->_docTableStrings.size())
        return "";
    
    return this->_docTableStrings[docId];

}

string SearchDocManager::_searchlexiTableByWord(string word) const {
    auto it = std::lower_bound(this->_lexiTableWords.begin(), this->_lexiTableWords.end(), word);
    
    if (it != this->_lexiTableWords.end() && *it == word)
        return this->_lexiTableStrings[std::distance(this->_lexiTableWords.begin(), it)];
    else return "";
    
}

std::pair<std::streampos, std::streampos> SearchDocManager::_getInvertedListStartStop(string word) const {
    string lexiString = this->_searchlexiTableByWord(word);
    
    if (not lexiString.empty()){
        size_t pos1 = lexiString.find(" ");
        size_t pos2 = lexiString.rfind(" ");
        return std::pair<std::streampos, std::streampos>(
                                         (std::streampos) std::stod(lexiString.substr(0, pos1)),
                                         (std::streampos) std::stod(lexiString.substr(pos1+1, pos2)));
    } else
        return std::pair<std::streampos, std::streampos>(-1, -1);
    
}

const vector<int>* SearchDocManager::_getDecodedInvertedList(size_t start, size_t stop) {
    vector<int>* invertedListNums = new vector<int>();
    
    this->_invertedFile.seekg(start, std::ios::beg);
    
    int val = 0, shift = 0;
    for (size_t i = start; i < stop; i++) {
        const short b = this->_invertedFile.get();
        if (b < 128) {
            val = val + (b << shift);
            shift = shift + 7;
        } else {
            val = val + ((b-128) << shift);
            invertedListNums->push_back(val);
            val=0; shift=0;
        }
    }
    
    return invertedListNums;
}

// metaData format -> {totalBlocks, blockSize, lastBlockSize}
const vector<int>* SearchDocManager::_getDecodedDocIds(const vector<int>* invertedList) const {
    
    std::array<int, 3> metaData = {0, 0, 0};
    for (short i=0; i<3; i++)
        metaData[i] = invertedList->at(i);
    
    short foundCount=0, blockCount=0;
    size_t i = 3;

    std::vector<int>* docIds = new std::vector<int>();
    
    while (true) {
        const int b = invertedList->at(i);
        docIds->push_back(b);
        foundCount++;
        
        if (blockCount == (metaData[0] - 1) and foundCount == metaData[2]) {
            break;
        } else if (foundCount == metaData[1]) {
            i += metaData[1] + 1;
            blockCount++;
            foundCount=0;
        } else i++;
    }
    
    return docIds;
}

// metaData format -> {totalBlocks, blockSize, lastBlockSize}
short SearchDocManager::_docInInvertedList(int docId, const vector<int>* invertedList) const {
/*
    returns frequency of the doc if it's found otherwise returns 0
*/
    
    int totalBlocks = invertedList->at(0);
    int blockJump = invertedList->at(1);
    for (int i=0; i < totalBlocks; i++){
        if (docId < invertedList->at(i*blockJump*2 + 3)){
            if (i == 0)
                return 0;
            
            for (int j=0; j < blockJump; j++)
                if (invertedList->at((i-1)*blockJump*2 + j + 3) == docId)
                    return invertedList->at((i-1)*blockJump*2 + j + 3 + blockJump);
        }
    }
    
    int lastBlockSize = invertedList->at(2);
    for (int i=0; i < lastBlockSize; i++)
        if (docId == invertedList->at((totalBlocks - 1)*blockJump*2 + i + 3))
            return invertedList->at((totalBlocks - 1)*blockJump*2 + i + 3 + lastBlockSize);
    
    return 0;
}

bool SearchDocManager::wordInDoc(string word, int docId){
//    const vector<int>* decodedList = this->getInvertedListForWord(word);
    return this->WordInDocFreqOneByOne(docId, word) > 0;
}

int SearchDocManager::wordInDocFreq(string word, int docId){
    
    return this->WordInDocFreqOneByOne(docId, word);
}

const std::vector<int>* SearchDocManager::getDocIdsForWord(string word) {
    const vector<int>* invertedList = this->getInvertedListForWord(word) ;
    return this->_getDecodedDocIds(invertedList);
}

const vector<int>* SearchDocManager::getInvertedListForWord(string word){
    
    // Older method to fetch an entire inverted list by word
    
    string lexiString = this->_searchlexiTableByWord(word);
    if (lexiString.empty())
        return new vector<int>();
    
    const auto cacheHit = this->_cache.find(word);
    if (cacheHit != this->_cache.end())
        return cacheHit->second;
    
    std::pair<size_t, size_t> startStopPair = this->_getInvertedListStartStop(word);
    const vector<int>* decodedInvertedList = this->_getDecodedInvertedList(startStopPair.first, startStopPair.second);
    this->_cache.emplace(word, decodedInvertedList);
    
    return decodedInvertedList;
}

int SearchDocManager::getLengthOfDoc(int docId) const {
    string docString = this->_searchDocTableById(docId);
    
    int docLength = -1;
    if (not docString.empty()){
        size_t pos = docString.find(" ");
        docLength = std::stoi(docString.substr(0, pos));
    }
    
    return docLength;
}

int SearchDocManager::getWordOccurenceFrequency(string word) const {
    
    // How many documents does a term occur in?
    
    string lexiString = this->_searchlexiTableByWord(word);
    
    int occurenceFrequency = 0;
    
    if (not lexiString.empty()){
        size_t pos1 = lexiString.rfind(" ");
        size_t pos2 = lexiString.find("|");
        occurenceFrequency = std::stoi(lexiString.substr(pos1 + 1, pos2));
        lexiString.clear();
    }
    
    return occurenceFrequency;
}

bool SearchDocManager::docIdInDocList(int docId, const vector<int>* docList) const {
    return std::binary_search(docList->begin(), docList->end(), docId);
}

float SearchDocManager::getMaxBM25score(string word) const {
    // Get maximum BM25 scores for terms from the lexicon table
    
    string lexiString = this->_searchlexiTableByWord(word);
    
    float maxxScore = 0.0;
    
    if (not lexiString.empty()){
        size_t pos1 = lexiString.rfind("|");
        maxxScore = std::stof(lexiString.substr(pos1 + 1));
        lexiString.clear();
    }
    
    return maxxScore;
}

std::string SearchDocManager::getDocumentText(int docId) {
    
    // This function caches the document as and when extraxted
    auto docTextCacheHit = this->_docTextCache.find(docId);
    
    // If the text is found in the cache return it
    if (docTextCacheHit != this->_docTextCache.end())
        return docTextCacheHit->second;
    
    // Get Document info from the document table
    string docString = this->_searchDocTableById(docId);
    
    // Document text start and end position in the big document.
    size_t docStartLoc = -1;
    if (not docString.empty()){
        size_t posBeg = docString.find(" ");
        size_t posEnd = docString.find("|");
        docStartLoc = (size_t) std::stod(docString.substr(posBeg+1, posEnd));
    }
    
    if (docStartLoc == -1)
        return "";
    
    string path = "/Users/utkarsh/Desktop/Utkarsh/NYU/Year 1/Semester 1/Web Search Engines/Assignments/HW 2/Data/msmarco-docs.trec";
    std::ifstream file = std::ifstream(path);
    
    file.clear();
    file.seekg(docStartLoc);
    
    
    // Only return the document text not any other meta information about it.
    string line, docText;
    while (std::getline(file, line)) {
        if (line.empty() or line == " ")
            continue;
        else if (line.starts_with("</TEXT>"))
            break;
        docText += line;
        
        const char ch = docText.at(docText.length()-1);
        if (ch == '.'){
            docText += " ";
        } else if (ch == ' '){
            docText.pop_back();
            docText += ". ";
        } else if (std::isalpha(ch)) {
            docText += ". ";
        }
    }
    file.close();
    
    docText.shrink_to_fit();
    // Return lower cased text so it's easier to match.
    boost::to_lower(docText);
    this->_docTextCache.emplace(docId, docText);
    
    return docText;

}

std::string SearchDocManager::getDocUrl(int docId) const {
    string docString = this->_searchDocTableById(docId);
    
    string url;
    if (not docString.empty()){
        size_t pos = docString.find("|");
        url = docString.substr(pos+1);
    }
        
    return url;
}

std::pair<int, size_t> SearchDocManager::_decodeOnebyOne(size_t start, size_t stop){
    // decode the first number starting at start position and return it
    // Runs varbyte decompression
    this->_invertedFile.seekg(start, std::ios::beg);
    
    int val = 0, shift = 0;
    for (; start < stop; start++) {
        const short b = this->_invertedFile.get();
        if (b < 128) {
            val = val + (b << shift);
            shift = shift + 7;
        } else {
            val = val + ((b-128) << shift);
            shift=0;
            break;
        }
    }
    
    return std::make_pair(val, ++start);
    
}

pair<vector<int>, size_t> SearchDocManager::_getBlock(int blockSize, size_t start, size_t stop){
    
    /* Function to fetch a block of elements between start and stop.
     A block may or may not exhuast the entire term list*/
    
    vector<int> blockNums;
    
    if (start >= stop)
        return std::make_pair(blockNums, start);
    
    for (int i=0; i < blockSize*2; i++){
        pair<int, size_t> decodedNum = this->_decodeOnebyOne(start, stop);
        blockNums.push_back(decodedNum.first);
        start = decodedNum.second;
    }
    
    return std::make_pair(blockNums, start);
}

// metaData format -> {totalBlocks, blockSize, lastBlockSize}
int SearchDocManager::WordInDocFreqOneByOne(int docId, string word){
    
    /* Older method of searching in an inverted list if a doc ID exists
    if it does return the frequency of the docid */
     
    auto it = this->_blockByBlockCache.find(word);
    size_t start = 0, stop = 0;
    vector<int> invertedList;
    int blocksDone=0;
    
    if (it != this->_blockByBlockCache.end()){
        invertedList = std::get<0>(it->second);
        blocksDone = std::get<1>(it->second);
        start = std::get<2>(it->second);
        stop = std::get<3>(it->second);
    } else {
        pair<size_t, size_t> startStopPair = this->_getInvertedListStartStop(word);
        start = startStopPair.first; stop = startStopPair.second;
        for (short j=0; j<3; j++){
            std::pair<int, size_t> decodedNum = this->_decodeOnebyOne(start, stop);
            invertedList.push_back(decodedNum.first);
            start = decodedNum.second;
        }
        std::tuple<std::vector<int>, int, size_t, size_t> myTuple(invertedList, 0, start, stop);
        this->_blockByBlockCache[word] = myTuple;
        it = this->_blockByBlockCache.find(word);
    }
    
    int totalBlocks = invertedList[0];
    int blockSize = invertedList[1];
    int lastBlockSize = invertedList[2];
    
    if (totalBlocks > 1){
        for (int i=0; i < totalBlocks - 1; i++){
            if (i >= blocksDone){
                pair<vector<int>, size_t> blockInfo = this->_getBlock(blockSize, start, stop);
                invertedList.insert(invertedList.end(), blockInfo.first.begin(), blockInfo.first.end());
                start = blockInfo.second;
                blocksDone++;
                std::get<0>(it->second) = invertedList;
                std::get<1>(it->second) = blocksDone;
                std::get<2>(it->second) = start;
            }

            if (docId < invertedList.at(i*blockSize*2 + 3)){
                if (i == 0)
                    return 0;
                
                auto end = invertedList.begin() + (i-1)*blockSize*2 + blockSize + 3;
                auto it = std::lower_bound(invertedList.begin() + (i-1)*blockSize*2 + 3, end, docId);
                
                if (it != end && *it == docId)
                    return invertedList[std::distance(invertedList.begin(), it) + blockSize];
                
            }
        }
        
        if (blocksDone != totalBlocks){
            pair<vector<int>, size_t> blockInfo = this->_getBlock(lastBlockSize, start, stop);
            invertedList.insert(invertedList.end(), blockInfo.first.begin(), blockInfo.first.end());
            blocksDone++;
            std::get<0>(it->second) = invertedList;
            std::get<1>(it->second) = blocksDone;
            std::get<2>(it->second) = blockInfo.second;
        }
        
        if (docId < invertedList.at((totalBlocks - 1)*blockSize*2 + 3)){
            auto end = invertedList.begin() + (totalBlocks - 2)*blockSize*2 + blockSize + 3;
            auto it = std::lower_bound(invertedList.begin() + (totalBlocks - 2)*blockSize*2 + 3, end, docId);
            
            if (it != end && *it == docId)
                return invertedList[std::distance(invertedList.begin(), it) + blockSize];

        } else {
            
            auto end = invertedList.begin() + (totalBlocks - 1)*blockSize*2 + lastBlockSize + 3;
            auto it = std::lower_bound(invertedList.begin() + (totalBlocks - 1)*blockSize*2 + 3, end, docId);
            
            if (it != end && *it == docId)
                return invertedList[std::distance(invertedList.begin(), it) + lastBlockSize];
            
        }
    } else {
        
        if (blocksDone < 1){
            pair<vector<int>, size_t> blockInfo = this->_getBlock(lastBlockSize, start, stop);
            invertedList.insert(invertedList.end(), blockInfo.first.begin(), blockInfo.first.end());
            std::get<0>(it->second) = invertedList;
            std::get<1>(it->second)++;
            std::get<2>(it->second) = blockInfo.second;
        }
        
        auto end = invertedList.begin() + blockSize*2 + lastBlockSize + 3;
        auto it = std::lower_bound(invertedList.begin() + 3, invertedList.end(), docId);
       
       if (it != end && *it == docId)
           return invertedList[std::distance(invertedList.begin(), it) + lastBlockSize];
        
        for (int i=0; i < lastBlockSize; i++)
            if (docId == invertedList.at(i + 3))
                return invertedList.at(i + 3 + lastBlockSize);
    }
    
    return 0;
}

std::pair<int, size_t> SearchDocManager::getIterativeDocIdByWordAndPos(std::string word, size_t readIdx){
    
    /* Manual fetching of docids with explicit state management, see getIterativeDocIdByWordAndPos(std::string word) for proper
     documentation */
    
    auto it = this->_blockByBlockCache.find(word);
    
    vector<int> invertedList;
    size_t readPos=0, stop=0;
    int blocksDone=0;
    
    if (it != this->_blockByBlockCache.end()){
        invertedList = std::get<0>(it->second);
        blocksDone = std::get<1>(it->second);
        readPos = std::get<2>(it->second);
        stop = std::get<3>(it->second);
        
        if (blocksDone == invertedList[0] and (readIdx % invertedList[1]) == invertedList[2])
            return std::make_pair(-1, readIdx);
        else if (readIdx % invertedList[1] == 0 and readIdx > 0) {
            int blockToFetch = blocksDone == invertedList[0] - 1 ? invertedList[2] : invertedList[1];
            pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
            std::get<0>(it->second).insert(std::get<0>(it->second).end(), newPostings.first.begin(), newPostings.first.end());
            std::get<1>(it->second)++;
            std::get<2>(it->second) = newPostings.second;
            readIdx+=invertedList[1];
            return std::make_pair(std::get<0>(it->second).at(readIdx + 3), readIdx+1);
        } else {
            readIdx++;
            return std::make_pair(std::get<0>(it->second).at(readIdx + 2), readIdx);
        }
    }
    
    std::pair<size_t, size_t> startStopPair = this->_getInvertedListStartStop(word);
    readPos = startStopPair.first; stop = startStopPair.second;
    
    for (short i=0; i<3; i++){
        auto decodedNum = this->_decodeOnebyOne(readPos, stop);
        invertedList.push_back(decodedNum.first);
        readPos = decodedNum.second;
    }
    
    int totalBlocks = invertedList[0];
    int blockSize = invertedList[1];
    int lastBlockSize = invertedList[2];
    
    int blockToFetch = blocksDone == totalBlocks - 1 ? lastBlockSize: blockSize;
    pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
    invertedList.insert(invertedList.end(), newPostings.first.begin(), newPostings.first.end());
    
    std::tuple<std::vector<int>, int, size_t, size_t> myTuple(invertedList, 1, newPostings.second, stop);
    this->_blockByBlockCache[word] = myTuple;
    
    return std::make_pair(newPostings.first.at(0), 1);
    
    
}

generator<int> SearchDocManager::getIterativeDocIdByWordAndPos(std::string word){
    auto it = this->_blockByBlockCache.find(word);
    
    size_t readPos=0, stop=0;
    vector<int> invertedList;
    int blocksDone=0;
    
    // Is it not there in cache? create its entry
    if (it == this->_blockByBlockCache.end()){
        std::pair<size_t, size_t> startStopPair = this->_getInvertedListStartStop(word);
        readPos = startStopPair.first; stop = startStopPair.second;
        
        // Get Metadata of list
        for (short i=0; i<3; i++){
            auto decodedNum = this->_decodeOnebyOne(readPos, stop);
            invertedList.push_back(decodedNum.first);
            readPos = decodedNum.second;
        }
        
        int totalBlocks = invertedList[0];
        int blockSize = invertedList[1];
        int lastBlockSize = invertedList[2];
        
        // Block size to fetch
        int blockToFetch = blocksDone == totalBlocks - 1 ? lastBlockSize: blockSize;
        pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
        invertedList.insert(invertedList.end(), newPostings.first.begin(), newPostings.first.end());
        
        blocksDone = 1;
        readPos = newPostings.second;
        
        // Creating cache entry tuple
        std::tuple<std::vector<int>, int, size_t, size_t> myTuple(invertedList, blocksDone, newPostings.second, stop);
        
        // Entry finally added to cache
        this->_blockByBlockCache[word] = myTuple;
        
        // Getting the new iterator
        it = this->_blockByBlockCache.find(word);
        
    } else {
        // Term exists in map so fetches its data
        invertedList = std::get<0>(it->second);
        blocksDone = std::get<1>(it->second);
        readPos = std::get<2>(it->second);
        stop = std::get<3>(it->second);
    }
    
    size_t readIdx=0;
    int endPoint = (invertedList[0]-1)*invertedList[1]*2 + invertedList[2];
    
    while (true) {
        // has the list ended? ((totalblock - (bool)invertedList[2])*2 - 1) + invertedList[2]
        if (blocksDone >= invertedList[0] and (endPoint == readIdx)) //(readIdx % invertedList[1]) == invertedList[2])
            break;
        // Is it time to fetch a new block?
        else if (readIdx % invertedList[1] == 0 and readIdx > 0) {
            
            if (blocksDone != invertedList[0]){
                // Decide block size
                int blockToFetch = blocksDone == invertedList[0] - 1 ? invertedList[2] : invertedList[1];
                // Fetch the block
                pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
                // Add to the list
                invertedList.insert(invertedList.end(), newPostings.first.begin(), newPostings.first.end());
                blocksDone++;
                readPos = newPostings.second;
                
                // Update the cache
                std::get<0>(it->second) = invertedList;
                std::get<1>(it->second) = blocksDone;
                std::get<2>(it->second) = readPos;
            }
            
            readIdx+=invertedList[1];
            co_yield invertedList.at(readIdx + 3);
            readIdx++;
        
        } else {
            // We have the ID in the cache, just return it
            co_yield invertedList.at(readIdx + 3);
            readIdx++;
        }
        it = this->_blockByBlockCache.find(word);
    }
    
    co_return -1;
}

generator<int> SearchDocManager::getIterativeFreqByWord(string word){
    auto it = this->_blockByBlockCache.find(word);
    
    size_t readPos=0, stop=0;
    vector<int> invertedList;
    int blocksDone=0;
    size_t readIdx=0;
    
    // Is it not there in cache? create its entry
    if (it == this->_blockByBlockCache.end()){
        std::pair<size_t, size_t> startStopPair = this->_getInvertedListStartStop(word);
        readPos = startStopPair.first; stop = startStopPair.second;
        
        // Get Metadata of list
        for (short i=0; i<3; i++){
            auto decodedNum = this->_decodeOnebyOne(readPos, stop);
            invertedList.push_back(decodedNum.first);
            readPos = decodedNum.second;
        }
        
        int totalBlocks = invertedList[0];
        int blockSize = invertedList[1];
        int lastBlockSize = invertedList[2];
        
        // Block size to fetch
        int blockToFetch = blocksDone == totalBlocks - 1 ? lastBlockSize: blockSize;
        pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
        invertedList.insert(invertedList.end(), newPostings.first.begin(), newPostings.first.end());
        readIdx = blockToFetch;
        
        blocksDone = 1;
        readPos = newPostings.second;
        
        // Creating cache entry tuple
        std::tuple<std::vector<int>, int, size_t, size_t> myTuple(invertedList, blocksDone, newPostings.second, stop);
        
        // Entry finally added to cache
        this->_blockByBlockCache[word] = myTuple;
        
        // Getting the new iterator
        it = this->_blockByBlockCache.find(word);
        
    } else {
        // Term exists in map so fetches its data
        invertedList = std::get<0>(it->second);
        blocksDone = std::get<1>(it->second);
        readPos = std::get<2>(it->second);
        stop = std::get<3>(it->second);
        readIdx = invertedList[1];
    }
    
    
    int endPoint = (invertedList[0]-1)*invertedList[1]*2 + 2*invertedList[2];
    
    while (true) {
        // has the list ended?
        if (blocksDone >= invertedList[0] and (endPoint == readIdx)) //(readIdx % invertedList[1]) == invertedList[2])
            break;
        // Is it time to fetch a new block?
        else if (blocksDone != invertedList[0] and readIdx % invertedList[1] == 0 and readIdx > invertedList[1]) {
            
            // Decide block size
            int blockToFetch = blocksDone == invertedList[0] - 1 ? invertedList[2] : invertedList[1];
            
            if (blocksDone != invertedList[0]){
                
                // Fetch the block
                pair<vector<int>, size_t> newPostings = this->_getBlock(blockToFetch, readPos, stop);
                // Add to the list
                invertedList.insert(invertedList.end(), newPostings.first.begin(), newPostings.first.end());
                blocksDone++;
                readPos = newPostings.second;
                
                // Update the cache
                std::get<0>(it->second) = invertedList;
                std::get<1>(it->second) = blocksDone;
                std::get<2>(it->second) = readPos;
            }
            
            readIdx+=blockToFetch;
            co_yield invertedList.at(readIdx + 3);
            readIdx++;
        
        } else {
            // We have the ID in the cache, just return it
            co_yield invertedList.at(readIdx + 3);
            readIdx++;
        }
        it = this->_blockByBlockCache.find(word);
    }
    co_return 0;
}

void SearchDocManager::clearFileStuff(){
    this->_invertedFile.clear();
    this->_invertedFile.seekg(0, std::ios::beg);
}
// docText    std::string    "https://www.nytimes.com/2016/07/13/technology/personaltech/voice-searches-with-cortana-or-chrome.html. Voice Searches With Cortana or Chrome. Personal Tech. Voice Searches With Cortana or Chrome. Tech Tip. By J. D. BIERSDORFER JULY 12, 2016Microsoft’s Cortana assistant may use the Edge browser, but you can select a preferred program as your default app in the Windows 10 settings. The New York Times. Q. When I do voice searches with Cortana in Windows 10, it always uses the Edge browser and the Bing search engine. Can I set it to use Google Chrome and search?A. While workarounds like the Google Chrome Chrometana extension for redirecting Cortana-prompted Bing searches were once an easy option for using alternate software, Microsoft recently made changes to its software that broke Chrometana and restricted Cortana to using only Edge and Bing. (Programmers with a dislike of Bing and Edge immediately began to look for new solutions and you may find tools online to help get around Microsoft’s block, but downlo"...



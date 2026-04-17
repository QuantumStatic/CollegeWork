//
//  SearchDocManager.hpp
//  HW 3
//
//  Created by Utkarsh Jain on 31/10/23.
//


#ifndef SearchDocManager_hpp
#define SearchDocManager_hpp

#include <fstream>
#include <memory>
#include <stdio.h>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
#include "Generator.cpp"

class SearchDocManager {
private:
    std::string _currDirectory;
    std::ifstream _invertedFile;
    std::vector<std::string> _lexiTableWords, _lexiTableStrings;
//    std::vector<int> _docTableIds;
    std::vector<std::string> _docTableStrings;
//    std::vector<unsigned char> _indexBinarybuffer;
    
    // Initialise files function
    void _initPathAndFiles();
    void _createLexiAndDocTable();
    
    
    std::pair<std::streampos, std::streampos> _getInvertedListStartStop(std::string) const;
    const std::vector<int>* _getDecodedInvertedList(size_t start, size_t stop);
    const std::vector<int>* _getDecodedDocIds(const std::vector<int>*) const;
    std::pair<int, size_t> _decodeOnebyOne(size_t start, size_t stop);
    
    short _docInInvertedList(int docId, const std::vector<int>* invertedList) const;
    
    std::string _searchDocTableById(int docId) const;
    std::string _searchlexiTableByWord(std::string word) const;
    
    std::unordered_map<std::string, const std::vector<int>*> _cache;
    std::unordered_map<std::string, std::tuple<std::vector<int>, int, size_t, size_t>> _blockByBlockCache;
    std::unordered_map<int, std::string> _docTextCache;
    
    std::pair<std::vector<int>, size_t> _getBlock(int blockSize, size_t start, size_t end);
    
    
public:
    SearchDocManager();
    const std::vector<int>* getInvertedListForWord(std::string word);
    const std::vector<int>* getDocIdsForWord(std::string word);
    bool wordInDoc(std::string word, int docId);
    bool docIdInDocList(int docId, const std::vector<int>* docList) const;
    int wordInDocFreq(std::string word, int docId);
    int getLengthOfDoc(int docId) const;
    int getWordOccurenceFrequency(std::string word) const;
    float getMaxBM25score(std::string word) const;
    std::string getDocumentText(int docId);
    std::string getDocUrl(int docId) const;
    
    int WordInDocFreqOneByOne(int docId, std::string word);
    std::pair<int, size_t> getIterativeDocIdByWordAndPos(std::string, size_t idx);
    generator<int> getIterativeDocIdByWordAndPos(std::string);
    generator<int> getIterativeFreqByWord(std::string);
    
    void clearFileStuff();
};


#endif /* SearchDocManager_hpp */

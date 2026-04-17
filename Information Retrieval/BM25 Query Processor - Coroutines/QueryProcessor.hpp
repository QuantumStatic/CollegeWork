//
//  QueryProcessor.hpp
//  HW 3
//
//  Created by Utkarsh Jain on 01/11/23.
//

#ifndef QueryProcessor_hpp
#define QueryProcessor_hpp

#include <stdio.h>
#include <vector>

#include "SearchDocManager.hpp"


class QueryProcessor{
private:
    SearchDocManager _docManager;

    std::vector<std::pair<float, int>> _runConjunctiveQuery(const std::vector<std::string>* words);
    std::vector<std::pair<float,int>> _runConjunctiveQuery2(const std::vector<std::string>* words, short K);
    std::vector<std::pair<float, int>> _runDisjunctiveQuery(const std::vector<std::string>* words);
    std::vector<std::pair<float, int>> _runDisjunctiveQuery2(const std::vector<std::string>* words, short K);
    
    // Tells the compiler to evaluate these as compile time constants.
    static constexpr const float _totalDocuments=3213835.0, _avgDocLength=84.788;
    
    float _calcDocConstantForBM25(int docId, float k1, float b);
    float _BM25ForDocId(int docId, const std::vector<std::string>* words, float k1=1.2);
    float _bareBonesBM25(int docId, int wordOccurenceFrequency, int wordInDocFreq, float k1=1.2);
    std::string _generateSnippet(int docId, const std::vector<std::string>* words, short limit=5);
    std::vector<std::pair<float, int>> _BM25(std::vector<int> docIds, const std::vector<std::string>* words, short K);
    std::vector<std::pair<float, int>> _maxxScore(std::vector<std::vector<int>> docIds, const std::vector<std::string>* words, std::vector<float> maxBM25scores, short K);
    std::vector<std::pair<float, int>> _maxxScore2(const std::vector<std::string>* words, std::vector<float> maxBM25scores, short K=10);
    int getFrequencyByIDAtleast(int Id, generator<int>* docIdGen, generator<int>* FreqGenerator);
    
public:
    static constexpr const short CONJUNCTIVE=0, DISJUNCTIVE=1;
    
    QueryProcessor();
    std::vector<std::string> runQuery(std::string query, int queryType=QueryProcessor::CONJUNCTIVE, short K=10);
    void clearSearchDocs();
};

#endif /* QueryProcessor_hpp */

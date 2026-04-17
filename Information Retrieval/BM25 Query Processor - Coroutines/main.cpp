//
//  main.cpp
//  HW3-4
//
//  Created by Utkarsh Jain on 18/11/23.
//

#include <iostream>
#include "QueryProcessor.hpp"
//#include "SearchDocManager.hpp"

int main(int argc, const char * argv[]) {
    QueryProcessor queryProcessor = QueryProcessor();
    
    std::cout<<"Files Loaded!"<<std::endl;
    std::string query;
    
    while (true) {
        std::cout << "Enter Input ('q' to exit):";
        
        std::getline(std::cin, query);
        
        if (query.size() == 1 and query == "q")
            break;
        
        std::cout << "C for Conjunctive, D for Disjunctive:";
        
        char command;
        std::cin >> command;
        std::cout << std::endl;
        command = tolower(command);
        
        int mode = -1;
        
        switch (command) {
            case 'c':
                mode = QueryProcessor::CONJUNCTIVE;
                break;
            case 'd':
                mode = QueryProcessor::DISJUNCTIVE;
                break;
            default:
                std::cerr << "Command Not recognised" << std::endl;
        }
        
        std::vector<std::string> outputText;
        
        if (mode != -1)
            outputText = queryProcessor.runQuery(query, mode);
        
        for (const std::string &result: outputText)
            std::cout << result <<'\n'<< std::endl;

        query.clear();
        std::cin.ignore();
        queryProcessor.clearSearchDocs();
    }

    return 0;
}

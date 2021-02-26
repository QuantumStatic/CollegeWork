//  747
//  Created by Utkarsh on 09/11/20.

#include <iostream>
#include <queue>
using namespace std;

pair<int, int> max(queue<pair<int,int>> Q){
    pair<int, int> maximum = Q.front(); Q.pop();
    while (not Q.empty()) {
        if (Q.front().first > maximum.first){
            maximum.first = Q.front().first;
            maximum.second = Q.front().second;
        }
        Q.pop();
    }
    return maximum;
}

int main() {
    int test_cases; cin >> test_cases;
    while (test_cases){
        int queueSize, extractionSize; cin >> queueSize >> extractionSize;
        queue<pair<int,int>> sequence;
        
        for (int i=0; i < queueSize; i++) {
            int temp; cin >> temp;
            sequence.push(make_pair(temp, i));
        }
    
        while (not sequence.empty()) {
            queue<pair<int,int>> subSequence;
            for (int i=0; (i < extractionSize) and (not sequence.empty()); i++) {
                subSequence.push(sequence.front());
                sequence.pop();
            }
            
            pair<int, int> maxEle = max(subSequence);
            cout << maxEle.second + 1;
            
            if (subSequence.size() == 1 and sequence.empty())
                cout << endl;
            else
                cout << ' ';

            while (not subSequence.empty()){
                if (subSequence.front().second != maxEle.second){
                    subSequence.front().first--;
                    sequence.push(subSequence.front());
                }
                subSequence.pop();
            }
        }
        test_cases--;
    }
    
}

//  737
//  Created by Utkarsh on 27/09/20.

#include <iostream>
#include <map>

using namespace std;

int main() {
    map <string, int, less<>> Words;
    string word;
    
    while (cin >> word)
        Words[word]++;
        
    for (auto &item : Words)
        cout << item.first << ' ' << item.second << endl;
}

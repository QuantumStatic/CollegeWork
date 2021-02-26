//  740
//  Created by Utkarsh on 30/09/20.

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(void) {
    vector<int> circle{0};
    int initial_tags =0;
    
    cin >> initial_tags;
    while (initial_tags) {
        int input =0;
        cin >> input;
        circle.push_back(input);
        initial_tags--;
    }
    circle.erase(circle.begin());
    
    int operations =0;
    cin >> operations;
    
    while (operations) {
        int command;
        cin >> command;
        switch (command) {
            case 1:
                int in_pos; cin >> in_pos;
                int tag; cin >> tag;
                circle.insert(circle.begin()+in_pos, tag);
                break;
            case 2:
                int del_pos; cin >> del_pos;
                circle.erase(circle.begin()+del_pos-1);
                break;
            case 3:
                int lowerBound; cin >> lowerBound;
                int upperBound; cin >> upperBound;
                reverse(circle.begin()+lowerBound-1, circle.begin()+upperBound);
                break;
            case 4:
                int pos; cin >> pos;
                cout << circle.at(pos-1) << endl;
                break;
            default:
                break;
        }
        operations--;
    }
}

//  767
//  Created by Utkarsh on 21/10/20.

#include <iostream>
#include <list>
using namespace std;

int main(void) {
    list<int> pile;
    int test_cases;
    cin >> test_cases;
    while (test_cases) {
        int instructions; cin >> instructions;
        while (instructions) {
            char command; cin >> command;
            if (command == 'I'){
                char location; cin >> location;
                int value; cin >> value;
                if (location == 'H')
                    pile.push_front(value);
                else
                    pile.push_back(value);
            }
            else if (command == 'R'){
                char location; cin >> location;
                if (location == 'H')
                    pile.pop_front();
                else
                    pile.pop_back();
            }
            else {
                int pos; cin >> pos;
                for (auto i:pile)
                    if (pos == 1){
                        cout << i << endl;
                        break;
                    }
                    else
                        pos--;
            }
            instructions--;
        }
        pile.clear();
        test_cases--;
    }
        return 0;
}

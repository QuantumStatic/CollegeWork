//  744
//  Created by Utkarsh on 05/11/20.

#include <iostream>
#include <unordered_set>
#include <stack>
#include <queue>
using namespace std;

int main() {
    int test_cases;
    cin >> test_cases;
    while (test_cases) {
        int stackSize; cin >> stackSize;
        queue<int> OG_combo;
        
        for (int i=0; i < stackSize; i++) {
            int temp;
            cin>>temp;
            OG_combo.push(temp);
        }
        
        int combos_to_check; cin >> combos_to_check;
        while (combos_to_check) {
            stack<int> combo, middlestein;
            queue<int> cpy_OG = OG_combo;
            unordered_set<int> comboRegister;
            for (int i=0; i < stackSize; i++) {
                int temp;
                cin>>temp;
                combo.push(temp);
                comboRegister.insert(temp);
            }
            
            while (not cpy_OG.empty()) {
                if (comboRegister.find(cpy_OG.front()) != comboRegister.end()){
                    while (cpy_OG.front() != combo.top()) {
                        middlestein.push(combo.top());
                        comboRegister.erase(combo.top());
                        combo.pop();
                    }
                    cpy_OG.pop();
                    comboRegister.erase(combo.top());
                    combo.pop();
                }
                else if (!middlestein.empty() && middlestein.top() == cpy_OG.front()){
                    middlestein.pop();
                    cpy_OG.pop();
                }
                else break;
            }
            
            if (cpy_OG.empty())
                cout << "Aye" << endl;
            else
                cout << "Impossible" << endl;
            combos_to_check--;
        }
        test_cases--;
    }
}

//  753
//  Created by Utkarsh.

#include <iostream>
#include <stack>
using namespace std;

int main() {
    string str;
    stack<int> weights;
    while (getline(cin, str)) {
        int minSum = 0, len = (int)str.length();
        for (int i = 0; i < len; i++) {
            if (str[i] == '(')
                weights.push(i);
            else {
                minSum ^= (i + 1 - weights.top()) / 2;
                weights.pop();
            }
        }
        cout << minSum << endl;
    }
}

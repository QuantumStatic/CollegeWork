//  751
//  Created by Utkarsh.

#include <iostream>
#include <string>
#include <stack>
#include <sstream>
using namespace std;

int main() {
    string str;
    while (getline(cin, str)) {
        stack<int> Stack;
        stringstream SS(str);
        string currChar;
        while (SS >> currChar) {
            bool add = currChar.compare("+") == 0, substraction = currChar.compare("-") == 0, multiply = currChar.compare("*")  ==0;
            if (not add and not substraction and not multiply)
                Stack.push(stoi(currChar));
            else {
                int b = Stack.top();
                Stack.pop();
                int a = Stack.top();
                Stack.pop();
                if (add)
                    Stack.push(a + b);
                else if (substraction)
                    Stack.push(a - b);
                else if (multiply)
                    Stack.push(a * b);
            }
        }
        cout << Stack.top() << endl;
    }
}
// 5 1 2 + 4 * + 3 -

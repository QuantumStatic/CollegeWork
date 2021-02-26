//  743
//  Created by Utkarsh on 04/11/20.

#include <iostream>
#include <stack>
#include <string>
using namespace std;

class bracket{
public:
    char bracket_type;
    int pos;
    inline bracket(char a, int b){
        bracket_type = a;
        pos = b;
    }
};

int main() {
    string in;
    while(getline(cin, in)){
        stack<bracket> brackets;
        bracket unmatched_openBracket('a',-1);
        
        for (int i=0; i < in.length(); i++){
            if (in[i] =='(' or in[i] =='{' or in[i] =='[')
                brackets.push(bracket(in[i],i));
            
            else if (in[i] ==')' or in[i] =='}' or in[i] ==']'){
                if (brackets.empty()){
                    cout << ++i;
                    goto l1;
                }
                else if (in[i] == ')'){
                    if (brackets.top().bracket_type == '(')
                        brackets.pop();
                    else {
                        cout << ++i;
                        goto l1;
                    }
                }
                else if ((char)((int)in[i]-2) == brackets.top().bracket_type)
                    brackets.pop();
                else{
                    cout << ++i;
                    goto l1;
                }
            }
        }
        
        while (not brackets.empty()){
            unmatched_openBracket = brackets.top();
            brackets.pop();
        }
        
        if (unmatched_openBracket.pos != -1)
            cout << ++unmatched_openBracket.pos;
        else
            cout << "Success";
        l1:
        cout << endl; ///< "ended"<<endl;
    }
}

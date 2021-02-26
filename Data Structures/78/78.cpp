//  78
//  Created by Utkarsh on 23/10/20.

#include <iostream>
#include <cstring>
using namespace std;

int main() {
    int test_cases, pos, len, inLen;
    cin>>test_cases;
    char str[52], biggestSub[52];
    while (test_cases) {
        cin >> str;
        pos=-1; len=0; inLen = (int) strlen(str);
        while (pos != inLen-1){
            for (int i=++pos; i < inLen; i++)
                if (str[i] > str[pos])
                    pos = i;
            biggestSub[len++] = str[pos];
        }
        biggestSub[len++] = '\0';
        cout << biggestSub << endl;
        test_cases--;
    }
    return 0;
}

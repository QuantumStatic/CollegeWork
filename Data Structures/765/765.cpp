//  765
//  Created by Utkarsh on 21/10/20.

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct planet {
    int pos;
    int strategic_value;
    int ordered_pos=1;
};

planet toConquer;

void selection(vector<int> vec, int pos){
    sort(vec.begin(),vec.end());
    toConquer.strategic_value = vec[pos];
    for (int i=0; i < pos; i++)
        if (vec[i] == toConquer.strategic_value)
            toConquer.ordered_pos++;
}

int main(void){
    int test_cases; cin >> test_cases;
    while (test_cases) {
        int elements, choice;
        vector<int> arr{0};
        cin >> elements;
        cin>>choice;
        while (elements){
            int element;
            cin>>element;
            arr.push_back(element);
            elements--;
        }
        arr.erase(arr.begin());
        selection(arr, --choice);
        int i=0;
        for (int count=0; count < toConquer.ordered_pos; i++)
            if (arr[i] == toConquer.strategic_value)
                count++;
        toConquer.pos = i;
        cout << toConquer.pos << ' ' << toConquer.strategic_value << endl;
        test_cases--;
    }
    return 0;
}

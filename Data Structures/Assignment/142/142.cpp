//  142
//  Created by Utkarsh.

#include <iostream>
#include <climits>
using namespace std;

int arr[30000];
int getRoot(int num) {
    return arr[num] < 0 ? arr[num]: arr[num] = getRoot(arr[num]);
}

int main() {
    int test_cases; cin >> test_cases;
    while (test_cases) {
        fill(arr, arr+30000, -1);
        int townPeople, pairs;
        cin >> townPeople >> pairs;
        while (pairs) {
            int firstPerson, secondPerson;
            cin >> firstPerson >> secondPerson;
            int root1 = getRoot(firstPerson-1);
            int root2 = getRoot(secondPerson-1);
            if (root1 != root2){
                arr[root1] += arr[root2];
                arr[root2] = root1;
            }
            pairs--;
        }
        int Max = INT_MAX;
        for (int i = 0; i < townPeople; i++)
            if (arr[i] < Max)
                Max = arr[i];
        cout << Max - 2 * Max << endl;
        test_cases--;
    }
}

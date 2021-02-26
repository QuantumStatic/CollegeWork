//  750
//  Created by Utkarsh.

#include <iostream>
using namespace std;

int main() {
    int arr[100], test_cases;
    cin >> test_cases;
    
    while(test_cases) {
        int root; cin >> root;
        int familyMembers; cin >> familyMembers;
        arr[root] = -1;
        while (familyMembers > 1) {
            int memberNumber; cin >> memberNumber;
            int parent; cin >> parent;
            arr[memberNumber] = parent;
            familyMembers--;
        }
        int descendant1; cin >> descendant1;
        int descendant2; cin >> descendant2;
        while(arr[descendant1] != -1) {
            int temp = descendant1;
            descendant1 = arr[descendant1];
            arr[temp] = -1;
        }
        while(arr[descendant2] != -1)
            descendant2 = arr[descendant2];
        cout << descendant2 << endl;
        test_cases--;
    }
}

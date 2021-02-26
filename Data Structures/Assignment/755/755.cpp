//  755
//  Created by Utkarsh.

#include <cmath>
#include <stack>
#include <iostream>
using namespace std;
int arr[1000000];

auto findMaxArea(int days) {
    long long int height, maxArea = 0, length;
    stack<int> index;
    for (int i = 0; i <= days; i++) {
        while (i == days || (!index.empty() && arr[i] < arr[index.top()]) ) {
            if (i == days && index.empty()) {
                i++;
                height = 0;
            }
            else {
                height = arr[index.top()];
                index.pop();
            }
            length = !index.empty() ? index.top() : -1;
            maxArea = maxArea > height * (i - length - 1) ? maxArea : height * (i - ++length);
        }
        index.push(i);
    }
    return maxArea;
}

int main() {
    int test_cases;
    cin >> test_cases;
    while (test_cases) {
        int days; cin >> days;
        for (int i = 0; i < days; i++){
            int temp;  cin >> temp;
            arr[i] = temp;
        }
        cout << (long long int) findMaxArea(days) << endl;
        test_cases--;
    }
}

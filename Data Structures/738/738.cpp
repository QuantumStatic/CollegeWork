    //  Created by Utkarsh on 28/09/20.

#include <iostream>
#include <vector>
using namespace std;

vector<int> matrixMultiply(vector<int>,vector<int>);
int fibonacciRemainder(int);

int main(void) {
    int n=0;
    while (cin >> n)
        cout << fibonacciRemainder(n) << endl;
}

vector<int> matrixMultiply(vector<int> a, vector<int> b){
    vector<int> helper{0,0,0,0};
    helper[0] = (a[0]*b[0] + a[1]*b[2]) % 10;
    helper[1] = (a[0]*b[1] + a[1]*b[3]) % 10;
    helper[2] = (a[2]*b[0] + a[3]*b[2]) % 10;
    helper[3] = (a[2]*b[1] + a[3]*b[3]) % 10;
    return helper;
}

int fibonacciRemainder(int num) {
    if (num == 0 || num == 1)
        return num;
    num--;
    vector<int> result{1,0,0,1};
    vector<int> OG{1,1,1,0};
    while (num) {
        if (num & 1) result = matrixMultiply(OG, result);
        OG = matrixMultiply(OG, OG);
        num = (int)(num/2);
    }
    vector<int>base{1,0,0,1};
    base = matrixMultiply(result, base);
    return base[0];
}

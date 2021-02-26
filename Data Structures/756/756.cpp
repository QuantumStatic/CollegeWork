//  756
//  Created by Utkarsh.

#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
//
int Heap[10000], currIndex = 0;
long long int sum;

void insert(int toInsert){
    sum += (Heap[currIndex] = toInsert);
    int parent = currIndex / 2, child = currIndex++;
    while (Heap[parent] < Heap[child] && parent > 0){
        int temp = Heap[child];
        Heap[child] = Heap[parent];
        Heap[parent] = temp;
        child = parent;
        parent /= 2;
    }
}

void pop() {
    sum -= Heap[1];
    Heap[1] = Heap[--currIndex];
    Heap[currIndex + 1] = -1;
    int parent = 1, kid1 = 2, kid2 = 3;
    while (Heap[parent] < (Heap[kid1] > Heap[kid2] ? Heap[kid1] : Heap[kid2])) {
        int temp = Heap[parent], newChild;
        if (Heap[kid1] >= Heap[kid2])
            newChild = kid1;
        else
            newChild = kid2;
        Heap[parent] = Heap[newChild];
        Heap[newChild] = temp;
        parent = newChild;
        kid1 = parent * 2;
        kid2 = kid1 + 1;
    }
}

int main()
{
    int test_cases;
    while (cin >> test_cases){
        fill(Heap,Heap + 10000, -1);
        sum = 0; currIndex = 1;
        while (test_cases--) {
            char choice; cin >> choice;
            if (choice == 'a'){
                int toInsert; cin >> toInsert;
                insert(toInsert);
            }
            else if (choice == 'p')
                pop();
            else if (choice == 'r')
                cout << sum << endl;
        }
    }
}

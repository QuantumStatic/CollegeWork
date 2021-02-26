#include <iostream>
#include <unordered_map>
using namespace std;

unordered_map<int, int> inOrderIndexes;
int preOrder[100], inOrder[100], nodeIndex=0, treeSize;

void getPostOrder(int begin, int end){
    if (begin <= end){
        int currRoot = inOrderIndexes[preOrder[nodeIndex++]] - 1;
        if (currRoot >= 0) {
            getPostOrder(begin, currRoot-1);
            getPostOrder(currRoot+1, end);
            if (nodeIndex == treeSize)
                cout << inOrder[currRoot] << endl;
            else cout << inOrder[currRoot] << ' ';
        }
    }
}

int main() {
    int test_cases; cin >> test_cases;
    while (test_cases){
        cin >> treeSize;
        fill(preOrder,preOrder+100,0);
        fill(preOrder,preOrder+100,0);
        
        for (int i=0; i < treeSize; i++){
            int temp; cin >> temp;
            preOrder[i] = temp;
        }
        for (int i=0; i < treeSize; i++){
            int temp; cin >> temp;
            inOrder[i] = temp;
            inOrderIndexes[temp] = i+1;
        }
        nodeIndex=0;
        getPostOrder(0, --treeSize);
        inOrderIndexes.clear();
        test_cases--;
    }
    return 0;
}  

/*
 2
 8
 1 2 4 7 3 5 6 8
 4 7 2 1 5 3 8 6
 5
 1 2 4 5 3
 4 2 5 1 3
 */

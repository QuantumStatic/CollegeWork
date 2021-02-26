// 748
// Created by Utkarsh.

#include <iostream>
using namespace std;

int totalNodes = 0;

class Quadtree{
 public:
    bool isWhite;
    bool needsNewBranch;
    Quadtree **child;
    Quadtree *parent;

    Quadtree() {needsNewBranch = false;}

    void addNewBranch(Quadtree *b1, Quadtree *b2, Quadtree *b3, Quadtree *b4);
    Quadtree* createQuadtree(Quadtree *root, bool **arr, int, int, int);
    void modify(Quadtree *root, int row, int col, int size);
};

void Quadtree::addNewBranch(Quadtree *b1, Quadtree *b2, Quadtree *b3, Quadtree *b4) {
    child = new Quadtree *[4];
    child[0] = b1;
    child[1] = b2;
    child[2] = b3;
    child[3] = b4;
}

Quadtree* Quadtree::createQuadtree(Quadtree *root, bool **arr, int row, int coloumn, int len) {
    Quadtree *t = new Quadtree();
    t->parent = root;

    bool needsMoreChildren = false;
    bool flag = false;
    
    for (int r = row; r < row + len; r++){
        for (int c = coloumn; c < coloumn + len; c++)
            if (arr[row][coloumn] != arr[r][c]) {
                needsMoreChildren = true;
                flag = true;
                break;
            }
        if (flag)
            break;
    }
    if (!needsMoreChildren)
        t->isWhite = arr[row][coloumn];
    else {
        len /= 2;
        t->needsNewBranch = true;
        t->addNewBranch(createQuadtree(t, arr, row, coloumn, len), createQuadtree(t, arr, row, coloumn + len, len), createQuadtree(t, arr, row + len, coloumn, len),createQuadtree(t, arr, row + len, coloumn + len, len));
    }
    totalNodes++;
    return t;
}

void Quadtree::modify(Quadtree *root, int row, int coloumn, int size) {
    if (size > 1) {
        if (!root->needsNewBranch) {
            root->addNewBranch(new Quadtree(), new Quadtree(), new Quadtree(), new Quadtree());
            totalNodes += 4;
            root->child[0]->isWhite = root->child[1]->isWhite = root->child[2]->isWhite = root->child[3]->isWhite = root->isWhite;
            root->needsNewBranch = true;
            root->child[0]->parent = root->child[1]->parent = root->child[2]->parent = root->child[3]->parent = root;
        }
        int halfSize = size / 2;
        if (row < halfSize) {
            if (coloumn < halfSize)
                modify(root->child[0], row, coloumn, halfSize);
            else
                modify(root->child[1], row, coloumn - halfSize, halfSize);
        }
        else {
            if (coloumn < halfSize)
                modify(root->child[2], row - halfSize, coloumn, halfSize);
            else
                modify(root->child[3], row - halfSize, coloumn - halfSize, halfSize);
        }
    }
    else {
        root->isWhite = !root->isWhite;
        while (root->parent != nullptr) {
            Quadtree *parentCpy = root->parent;
            if (!parentCpy->child[0]->needsNewBranch && !parentCpy->child[1]->needsNewBranch && !parentCpy->child[2]->needsNewBranch && !parentCpy->child[3]->needsNewBranch && parentCpy->child[0]->isWhite == parentCpy->child[1]->isWhite && parentCpy->child[0]->isWhite == parentCpy->child[2]->isWhite && parentCpy->child[0]->isWhite == parentCpy->child[3]->isWhite ) {
                root->parent->needsNewBranch = false;
                root->parent->isWhite = root->isWhite;
                root = root->parent;
                totalNodes -= 4;
            } else break;
        }
    }
}

int main() {
    int test_cases, edgeLength;
    bool **arr = new bool *[1024];
    
    for (int i = 0; i < 1024; i++) //10124
        arr[i] = new bool[1024];
    cin >> test_cases;
    
    while (test_cases) {
        totalNodes = 0;
        
        cin >> edgeLength;
        edgeLength = pow(2, edgeLength);

        getchar();
        for (int i = 0; i < edgeLength; i++) {
            for (int j = 0; j < edgeLength; j++)
                arr[i][j] = (getchar() == '0');
            getchar();
        }

        Quadtree *tree = new Quadtree();
        tree = tree -> createQuadtree(nullptr, arr, 0, 0, edgeLength);
        int K, row, coloumn;
        cin >> K;
        while(K) {
            cin >> row >> coloumn;
            row--; coloumn--;
            tree -> modify(tree, row, coloumn, edgeLength);
            cout << totalNodes << endl;
            K--;
        }
        test_cases--;
    }
}

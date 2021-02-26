//  742
//  Created by Utkarsh on 23/10/20.

#include <iostream>
#include <cmath>
#include <vector>
#include <string>
using namespace std;

bool pixels[1024][1024];
int countNodes(int x, int y, int limit);

int main() {
    int compressedSize;
    while (cin >> compressedSize) {
        int photoEdge = pow(2, compressedSize);
        int currRow=0;
        while (currRow != photoEdge){
            string str;
            cin >> str;
            for (int currCol=0; currCol<photoEdge; currCol++)
                pixels[currRow][currCol] = ((bool)((int)str.at(currCol) - (int)'0'));
            currRow++;
        }
        cout << countNodes(0,0, photoEdge) << endl;
    }
    return 0;
}

int countNodes(int x, int y, int limit){
    if (limit == 1)
        return 1;
    int sum=0;
    for(int height=y; height < y+limit; height++)
        for (int width=x; width<x+limit; width++)
            sum += pixels[height][width];
    if (sum ==0 || sum == limit*limit)
        return 1;
    
    return (countNodes(x+limit/2, y, limit/2) + countNodes(x,y,limit/2) + countNodes(x,y+limit/2, limit/2) + countNodes(x+limit/2,y+limit/2,limit/2) + 1);
}

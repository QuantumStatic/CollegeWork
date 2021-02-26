//  372
//  Created by Utkarsh.
#include <cstdio>

int main(){
    int test_cases; scanf("%d", &test_cases);
    for (int i=0; i < test_cases; i++){
        int Walls, high=0, low=0;
        short currWall, prevWall;
        scanf("%d", &Walls);
        scanf("%hd", &prevWall);
        while (--Walls){
            scanf("%hd", &currWall);
            if (currWall > prevWall)
                high++;
            else if (currWall < prevWall)
                low++;
            prevWall = currWall;
        }
        printf("Case %d: %d %d\n",i+1,high,low);
    }
}

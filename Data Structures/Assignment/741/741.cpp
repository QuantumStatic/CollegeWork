//  741
//  Created by Utkarsh.
#include <iostream>
using namespace std;

int rows, coloumns;

int heads(bool board[100][10], int currCol) {
    if (coloumns == currCol) {
        int totalHeads = 0, rowHeads = 0;
        for (int i = 0; i < rows; i++){
            rowHeads = 0;
            for (int j = 0; j < coloumns; j++)
            rowHeads += board[i][j];
            if (rowHeads <= coloumns / 2)
                rowHeads = coloumns - rowHeads;
            totalHeads += rowHeads;
        }
        return totalHeads;
    }
    else {
        int unflippedCoins = heads(board, currCol + 1);
        for (int i = 0; i < rows; i++)
            board[i][currCol] = not board[i][currCol];
        int flippedCoins = heads(board, currCol + 1);
        return flippedCoins > unflippedCoins ? flippedCoins: unflippedCoins;
    }
}

int main(){
    rows=0; coloumns=0;
    bool gameBoard[100][10];
    while (cin >> rows  >> coloumns){
        for (int i = 0; i< rows; i++){
            string str; cin >>  str;
            for (int j = 0; j < coloumns; j++)
                gameBoard[i][j] = (bool)(str.at(j) - '0');
        }
        cout << heads(gameBoard,0) << endl;
    }
}


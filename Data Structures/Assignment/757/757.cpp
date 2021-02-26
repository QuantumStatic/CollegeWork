//  757
//  Created by Utkarsh.

#include <iostream>
#include <queue>
using namespace std;

struct node {
    int index;
    int frequency;
    node(int x, int y){
        index = x;
        frequency = y;
    }
};

int arr[200000][3];

int HuffmanLength(int position, int dist){
    if (arr[position][1] == -1)
        return dist * arr[position][0];
    else
        return HuffmanLength(arr[position][1], dist + 1) + HuffmanLength(arr[position][2], dist + 1);
}

bool operator < (const node& node1, const node& node2){
    return node1.frequency > node2.frequency;
}

int main(){
    int stringLen;
    while (cin >> stringLen){
        priority_queue<node> PQ;
        int position = stringLen;
        for (int i = 0; i < stringLen; i++) {
            int temp; cin >> temp;
            PQ.push(node(i, temp));
            arr[i][0] = temp;
            arr[i][1] = -1;
            arr[i][2] = -1;
        }
        while (true) {
            node node1 = PQ.top();
            PQ.pop();
            if (PQ.empty())
                break;
            node node2 = PQ.top();
            PQ.pop();
            PQ.push(node(position, node1.frequency + node2.frequency));
            arr[position][0] = node1.frequency + node2.frequency;
            arr[position][1] = node1.index;
            arr[position][2] = node2.index;
            position++;
        }
        cout << HuffmanLength(position-1, 0) << endl;
    }
}

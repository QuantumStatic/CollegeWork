//  745
//  Created by Utkarsh on 05/11/20.

#include <iostream>
#include <set>
#include <stack>
using namespace std;

int main() {
    int test_cases; cin >> test_cases;
    while (test_cases) {
        stack<int> cardPile; set<int> maxCards;
        int init_pileSize; cin >> init_pileSize;
        while (init_pileSize) {
            int temp; cin >> temp;
            cardPile.push(temp);
            maxCards.insert(temp);
            init_pileSize--;
        }
        int operations; cin >> operations;
        while (operations) {
            char operation; cin>>operation;
            if (operation == 'm')
                cout << *(maxCards.rbegin()) << endl;
            else if (operation == 'r'){
                maxCards.erase(cardPile.top());
                cardPile.pop();
            }
            else{
                int cardValue; cin >> cardValue;
                cardPile.push(cardValue);
                maxCards.insert(cardValue);
            }
            operations--;
        }
        test_cases--;
    }
    return 0;
}

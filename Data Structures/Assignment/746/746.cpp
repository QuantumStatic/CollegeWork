//  746
//  Created by Utkarsh on 05/11/20.

#include <iostream>
#include <queue>
using namespace std;

class customer{
public:
    int arrivalTime;
    int leaveTime;
    int patienceLimit;
    int index;
    inline customer(int index, int arrivalTime, int orderTime, int patienceLimit){
        this->arrivalTime = arrivalTime;
        this->leaveTime = orderTime;
        this->patienceLimit = patienceLimit;
        this->index=index;
    }
    inline void addToLeaveTime(int toAdd){
        leaveTime += toAdd;
    }
};

int main() {
    int customers;
    while(cin >> customers){
        queue<customer> customerSet;
        
        for (int i=0; i< customers; i++) {
            int a, o, l; cin >> a >> o >> l;
            customerSet.push(customer(1+i,a,o,l));
        }
        
        queue<customer> finalQueue; int customers_to_service = 0;
        
        for(int time=0; not customerSet.empty(); time++){
            
            while (not customerSet.empty() and time == customerSet.front().arrivalTime){
                
                while (not finalQueue.empty() and finalQueue.front().leaveTime <= time){
                    finalQueue.pop();
                    customers_to_service--;
                }
                
                if (customers_to_service <= customerSet.front().patienceLimit){
                    if (customers_to_service >= 1){
                        customerSet.front().addToLeaveTime(max(customerSet.front().arrivalTime, finalQueue.back().leaveTime));
                        finalQueue.push(customerSet.front());
                    }
                    else{
                        customerSet.front().addToLeaveTime(customerSet.front().arrivalTime);
                        finalQueue.push(customerSet.front());
                    }
                    customers_to_service++;
                }
                customerSet.pop();
            }
        }
        
        if (finalQueue.back().index == customers){
            while (customers_to_service > 2) {
                finalQueue.pop();
                customers_to_service--;
            }
            int ans = customers_to_service == 2 ? max(finalQueue.front().leaveTime, finalQueue.back().arrivalTime):finalQueue.front().arrivalTime;
            cout << ans << endl;
        }
        else
            cout << -1 << endl;
    }
}

/*
 9
 2 12 26
 4 21 18
 5 29 15
 8 23 5
 13 28 1
 14 9 1
 14 23 6
 15 13 15
 17 5 15
 */
// -> 123

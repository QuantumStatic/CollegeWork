//  754
//  Created by Utkarsh

#include <iostream>
#include <algorithm>
using namespace std;

int totalRooms, badCustomers;
bool possible(int[], int);

int largestMinGap(int hotel[]) {
    int result = -1, choice = 1, lastRoom = hotel[totalRooms - 1];
    while (choice < lastRoom) {
        int suggestedRoom = (lastRoom + choice) >> 1;
        if (possible(hotel, suggestedRoom)) {
            choice = suggestedRoom + 1;
            result = result > suggestedRoom ? result : suggestedRoom;
        } else
            lastRoom = suggestedRoom;
    }
    return result;
}

bool possible(int hotel[], int suggestedRoom) {
    int accomodatedCustomers = 1, curRoom = hotel[0];
    for (int i = 1; i < totalRooms; i++)
        if (hotel[i] - curRoom >= suggestedRoom) {
            curRoom = hotel[i];
            if (++accomodatedCustomers == badCustomers)
                return true;
        }
    return false;
}

int main() {
    int test_cases; cin >> test_cases;
    while(test_cases){
        cin >> totalRooms >> badCustomers;
        int hotel[totalRooms];
        for (int room = 0; room < totalRooms; room++){
            int temp; cin >> temp;
            hotel[room] = temp;
        }
        sort(hotel, hotel + totalRooms);
        cout << largestMinGap(hotel) << endl;
        test_cases--;
    }
}

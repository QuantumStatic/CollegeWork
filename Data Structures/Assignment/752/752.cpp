//  752
//  Created by Utkarsh.

#include <iostream>
#include <vector>
#include <map>
using namespace std;

int numOfTasks;

class Task {
public:
    int index, arrivalTime, processingTime, servicingTime;
    inline Task (int index, int arrival, int time) {
        this->index = index;
        this->arrivalTime = arrival;
        this->processingTime = time;
    }
};

void allTasks(vector<Task> &priorityTasks, vector<Task> &normalTasks) {
    bool normFirst = normalTasks.front().arrivalTime < priorityTasks.front().arrivalTime;
    int currTime = normFirst ? normalTasks.front().arrivalTime : priorityTasks.front().arrivalTime;
    auto priorityIter = priorityTasks.begin();
    auto normalIter = normalTasks.begin();
    int i = 0;
    if (normFirst){
        currTime += normalIter->processingTime;
        normalIter->servicingTime = currTime;
        normalIter++; i++;
    }
    for (; i < numOfTasks; i++){
        if ((normalIter->arrivalTime < priorityIter->arrivalTime && currTime < priorityIter->arrivalTime && normalIter != normalTasks.end()) || priorityIter == priorityTasks.end()) {
            if (currTime < normalIter->arrivalTime)
                currTime = normalIter->arrivalTime;
            currTime += normalIter->processingTime;
            normalIter->servicingTime = currTime;
            normalIter++;
        }
        else {
            if (currTime < priorityIter->arrivalTime)
                currTime = priorityIter->arrivalTime;
            currTime += priorityIter->processingTime;
            priorityIter->servicingTime = currTime;
            priorityIter++;
        }
    }
    map<int, int> orderedTasks;
    
    for (int i = 0; i < priorityTasks.size(); i++)
        orderedTasks[priorityTasks.at(i).index] = priorityTasks.at(i).servicingTime;
    
    for (int i = 0; i < normalTasks.size(); i++)
        orderedTasks[normalTasks.at(i).index] = normalTasks.at(i).servicingTime;
    
    auto it = orderedTasks.begin();
    for (int i = 0; i < numOfTasks - 1; i++, it++)
        cout << it->second << " ";
    cout << it->second << endl;
}

void genTasks(vector<Task> &generalTasks) {
    int currTime = 0;
    for (auto iter = generalTasks.begin(); iter != generalTasks.end(); iter++) {
        if (currTime < iter->arrivalTime)
            currTime = iter->arrivalTime;
        currTime += iter->processingTime;
        iter->servicingTime = currTime;
    }
    map<int, int> orderedTasks;
    
    for (auto gentask : generalTasks)
        orderedTasks[gentask.index] = gentask.servicingTime;
    auto iter = orderedTasks.begin();
    for (int i = 0; i < numOfTasks - 1; i++, iter++)
        cout << iter->second << " ";
    cout << iter->second << endl;
}

int main() {
    while (cin >> numOfTasks) {
        vector<Task> priorityTasks, normalTasks;
        for (int i = 0; i < numOfTasks; i++) {
            int Arrival, processingTime, priority;
            cin >> Arrival >> processingTime >> priority;
            priority == 0 ? priorityTasks.push_back(Task(i, Arrival, processingTime)) : normalTasks.push_back(Task(i, Arrival, processingTime));
        }
        if (!priorityTasks.empty() && !normalTasks.empty())
            allTasks(priorityTasks, normalTasks);
        else if (priorityTasks.empty())
            genTasks(normalTasks);
        else
            genTasks(priorityTasks);
    }
}

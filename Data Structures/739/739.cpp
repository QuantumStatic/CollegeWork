//  739
//  Created by Utkarsh on 30/09/20.

#include <iostream>
using namespace std;

class element {
    public:
    int value;
    element(int val =0, element* previous=nullptr, element* next=nullptr) {this->value=val; this->next=next; prev=previous;}
    element* next;
    element* prev;
    element& operator = (const element& rhs);
    element& operator = (const int rhs);
    void showPointer();
    friend ostream& operator<< (ostream &output, const element &ele);
    friend istream& operator>> (istream &input, element &ele);
};

element& element::operator=(const element &rhs){
    if (this != &rhs)
        this->value = rhs.value;
    return *this;
}

element& element::operator=(const int rhs){
    this->value=rhs;
    return *this;
}

void element::showPointer() {
    cout<<this<<endl;
}

ostream& operator<< (ostream &output, const element &ele){
    output << ele.value;
    return output;
}

istream& operator>>(istream &input, element &ele){
    input >> ele.value;
    return input;
}

class LinkedList{
    private:
    element *head, *tail;
    int length;
    element *manIterator;
    
    public:
    LinkedList();
    int len();
    element* find(int index, bool haltPermission=false);
    element& operator[] (int index);
    void operator* (int);
    void append(int val);
    int pop();
    void display();
    void showPointer(int pos);
    void insert(int index, int value);
    void insertwithPointer(element* location, int value);
    int del(int index);
    void delwithPointer (element*);
    void getwithPointer (element*);
    friend ostream &operator<< (ostream &output, const LinkedList &List);
    void setoHead();
    element* manualIteration(int);
};

LinkedList::LinkedList() {
    this->head = nullptr;
    this->tail = nullptr;
    this->length =0;
}

int LinkedList::len(){
    return this->length;
}

element* LinkedList::find(int index, bool haltPermission){
    if (index >= this->length) {
        cerr << "index out of range!" << endl;
        if (haltPermission)
            exit(69);
        return this->tail;
    } else if (index ==0)
        return this->head;
    else if (index == length-1)
        return this->tail;
    
    int halflen = this->length/2;
    element* iterator = nullptr;
    
    if (index < --halflen){
        iterator = this->head;
        while (index) {
            iterator = iterator->next;
            index--;
        }
        return iterator;
    } else {
        iterator = this->tail;
        index = this->length - index - 1;
        while (index) {
            iterator = iterator->prev;
            index--;
        }
        return iterator;
    }
}

element& LinkedList::operator[](int index){
    return *find(index, true);
}

void LinkedList::operator*(int num){
    for (int i=0; i<num; i++)
        this->append(0);
}

void LinkedList::append(int val) {
    element* new_element = new element(val,this->tail,this->head);
    this->length++;
    if (head == nullptr){
        head = new_element;
        tail = new_element;
        new_element->prev = this->tail;
        new_element->next = this->head;
    } else {
        tail->next = new_element;
        tail = new_element;
        head->prev = tail;
    }
    manIterator = new_element;
}

int LinkedList::pop(){
    element* toDelete = tail;
    int value = toDelete->value;
    toDelete->prev->next=head;
    tail = toDelete->prev;
    head->prev = tail;
    delete toDelete;
    length--;
    manIterator = head;
    return value;
}

ostream& operator<< (ostream &output, const LinkedList &List) {
    element* iterator = List.head;
    while (iterator != List.tail) {
        output << iterator->value << ',';
        iterator = iterator->next;
    }
    output << iterator->value << endl;
    return output;
}

void LinkedList::display() {
    element* iterator = head;
    while (iterator != tail){
        cout << iterator->value <<',';
        iterator = iterator->next;
    }
    cout << iterator->value << endl;
}

void LinkedList::showPointer(int pos){
    element* iterator = this->head;
    while(pos){
        iterator = iterator->next;
        pos--;
    }
    cout << iterator << endl;
}

void LinkedList::insert(int index, int value){
    if (index >= this->length){
        this->append(value);
        return;
    }
    else if (index == 0){
        element* new_element = new element(value, tail, head);
        this->length++;
        head->prev = new_element;
        tail->next = new_element;
        head = new_element;
        manIterator = new_element;
        return;
    }
    element* add_point = find(index, true);
    add_point = add_point->prev;
    element* new_element = new element(value,add_point,add_point->next);
    this->length++;
    add_point->next->prev = new_element;
    add_point->next = new_element;
    manIterator = new_element;
}

int LinkedList::del(int index){
    if (index == this->length-1)
        return this->pop();
    else if (index ==0){
        element *toDelete = this->head;
        int val = toDelete->value;
        tail->next = head->next;
        head->next->prev = tail;
        head = toDelete->next;
        delete toDelete;
        this->length--;
        return val;
    }
    element* toDelete = this->find(index, true);
    int value = toDelete->value;
    toDelete->prev->next = toDelete->next;
    toDelete->next->prev = toDelete->prev;
    delete toDelete;
    this->length--;
    return value;
}

void LinkedList::setoHead(){
    manIterator = this->head;
}

element* LinkedList::manualIteration(int pos){
    pos--;
    while (pos){
        manIterator = manIterator->next;
        pos--;
    }
    return manIterator;
}

void LinkedList::insertwithPointer(element *location, int value){
    if (this->length ==0)
        this->append(value);
    element* new_element = new element(value, location, location->next);
    this->length++;
    manIterator = new_element;
    location->next->prev = new_element;
    location->next=new_element;
    if (this->tail->next != this->head)
        tail = new_element;
}

void LinkedList::delwithPointer(element * location){
    if (location == this->tail){
        this->pop();
        return;
    }
    if (location == this->head)
        head = head->next;
    location->next->prev = location->prev;
    location->prev->next= location->next;
    manIterator = location->next;
    delete location;
    this->length--;
}

void LinkedList::getwithPointer(element * location){
    cout << location->value << endl;
}

int main(void) {
    LinkedList list;
//    cout << "init:";
    int initial_tags; cin >> initial_tags;
    
    list*initial_tags;
//    cout << "Enter vals:";
    for (int i=0; i<initial_tags; i++)
        cin >> list[i];

    int operations; cin >> operations;
    list.setoHead();
    
    while(operations){
        int command;
//        cout <<"Enter command:";
        cin >> command;
//        if (command>=5)
//            break;
        switch (command) {
            case 1:
                int in_pos; cin >> in_pos;
                int tag; cin >> tag;
                list.insertwithPointer(list.manualIteration(in_pos), tag);
//                cout << list;
                break;
            case 2:
                int del_pos; cin >> del_pos;
                list.delwithPointer(list.manualIteration(del_pos));
//                cout << list;
                break;
            case 3:
                int pos; cin >> pos;
                list.getwithPointer(list.manualIteration(pos));
//                cout << list;
                break;
            default:
                break;
        }
        operations--;
    }
    return 0;
}















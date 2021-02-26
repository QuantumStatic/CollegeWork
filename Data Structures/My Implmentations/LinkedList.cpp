#include <iostream>
using std::cout;
using std::endl;
using std::cerr;
using std::ostream;
using std::istream;

// !head is equivalent to head == nullptr while head is equivalent to head != nullptr

class number {
public:
    int value;
    inline number(int val =0, number* previous=nullptr, number* next=nullptr) {
        this->value=val;
        this->next=next;
        previous=previous;
        
    }
    number* next;
    number* previous;
    number& operator = (const number& rhs);
    number& operator = (const int rhs);
    void showPointer();
    friend ostream& operator<< (ostream &output, const number &ele);
    friend istream& operator>> (istream &input, number &ele);
};

number& number::operator=(const number &rhs){
    if (this != &rhs)
        this->value = rhs.value;
    return *this;
}

number& number::operator=(const int rhs){
    this->value=rhs;
    return *this;
}

void number::showPointer() {
    cout<<this<<endl;
}

ostream& operator<< (ostream &output, const number &ele){
    output << ele.value;
    return output;
}

istream& operator>>(istream &input, number &ele){
    input >> ele.value;
    return input;
}


class LinkedList {
    private:
        number* head; number* tail; int length;
    public:
        LinkedList();
        void append(int);
        void display(int start= 0, int end= 0, int direction= 1);
        int get_val_at_pos(int);
        void modify_at_pos(int,int);
        int len();
        void append_multiple(int,int);
        void insert_at_pos(int value,int position);
        void increment_at_pos(int,int increment = 1);
        void sort();
        void reverse();
        void sort_internal(int);
        void delete_number(int);
        LinkedList slicer(int, int, int direction =1);
        void reset();
        number* find(int index, bool haltPermission=false);
        number& operator[] (int index);
        void operator* (int);
        friend ostream &operator<< (ostream &output, const LinkedList &List);
};


LinkedList::LinkedList(){
    head = nullptr;
    tail = nullptr;
}


void LinkedList::append(int num){
    number* new_number = new number(num);
    if (!head){
        head = new_number;
        tail = new_number;
    }
    else{
        new_number->previous = tail;
        tail->next = new_number;
        tail = new_number;
        head->previous = tail;
    }
    this->length++;
}

void LinkedList::operator*(int num){
    this->append_multiple(0, num);
}

number* LinkedList::find(int index, bool haltPermission){
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
    number* iterator = nullptr;

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
            iterator = iterator->previous;
            index--;
        }
        return iterator;
    }
}

number& LinkedList::operator[](int index){
    return *find(index, true);
}


void LinkedList::display(int start,int end, int direction){
    if (!head) {cerr << "Empty List" << endl; return;} else if(abs(start) >= this->length || abs(end) >= this->length){cerr << "Start or end out of range!"<<endl;return;} else if(start !=0 && start == end) {cerr << "No number fits the criteria" << endl; return;} else if (abs(direction)>1 || direction == 0) {cerr <<"Invalid direction";}
    LinkedList temp;
    temp = this->slicer(start, end, direction);
    cout << temp;
}


int LinkedList::get_val_at_pos(int position){
    if (position >= this->length || abs(position) > this->length) { cerr<<"That position doesn't exist! Returning NULL"<<endl; return NULL;}
    number* iterator = nullptr;
    if (position >= 0){
        iterator = head;
        for(int i=0; i< position; i++) iterator = iterator-> next;
        return(iterator->value);
    }
    else{
        iterator = tail;
        for (int i=1; i < abs(position); i++) iterator = iterator-> previous;
        return (iterator->value);
    }
}


void LinkedList::modify_at_pos(int num, int position){
   if (position >= this->length || abs(position) > this->length) { cerr<<"That position doesn't exist!"<<endl; return;}
    if (position ==0 && !head) append(num);
    number* iterator = nullptr;
    if (position >= 0){
        iterator = head;
        for(int i=0; i< position; i++) iterator = iterator-> next;
        iterator->value = num;
    }
    else{
        iterator = tail;
        for(int i=1; i< abs(position); i++) iterator = iterator-> previous;
        iterator->value = num;
    }
}


int LinkedList::len(){
    return (this->length);
}


void LinkedList::append_multiple(int value,int number){
  for(int x=0; x<number; x++) append(value);
}


void LinkedList::insert_at_pos(int num, int pos) {
    if ((pos ==0 && !head) || pos == this->length){ append(num); return; }
    if (pos > this->length){ cerr<<"LinkedList is not that big, position for insertion out of range!"<<endl;return; }
    number* new_number = new number(num);
    if (pos==0 && head){
        new_number-> next = head;
        new_number-> previous = tail;
        head-> previous = new_number;
        head = new_number;
    }
    else {
        number* current = head; number* prev = nullptr;
        for (int i=0; i<pos; i++){
            prev = current;
            current = current-> next;
        }
        new_number-> next = current;
        prev-> next = new_number;
    }
}


void LinkedList::increment_at_pos(int pos, int increment){
    if (pos >= this->length){ cerr << "Positon doesn't exist!"; return;}
    modify_at_pos(increment + get_val_at_pos(pos), pos);
}

ostream& operator<< (ostream &output, const LinkedList &List) {
    number* iterator = List.head;
    while (iterator != List.tail) {
        output << iterator->value << ',';
        iterator = iterator->next;
    }
    output << iterator->value << endl;
    return output;
}

void LinkedList::sort() {
    int end_point = this->length;
    for(int i=0; i < end_point; i++) {
        number* iterator = head; number* prev = head;
        while (true) {
            if (iterator->value > (iterator->next)->value){
                if (iterator == head){
                    head = iterator-> next;
                    iterator->next = (iterator->next)->next;
                    head->next = prev;
                    prev = head;
                }
                else{
                    number* temp = (iterator->next)-> next;
                    prev-> next =  iterator-> next;
                    prev = iterator-> next;
                    prev-> next = iterator;
                    iterator-> next = temp;
                }
                if (iterator->next == nullptr) {tail = iterator;break;}
            }
            else{
                if (iterator->next == nullptr) {tail = iterator;break;}
                break;
            }
        }
    }
    number* temp2 = head;
    for (int i=1; i<this->length;i++){
        (temp2->next)->previous = temp2;
        temp2 = temp2->next;
    }
    tail = temp2;
    head->previous = tail;
}



void LinkedList::reverse(){
    number* iterator = head;
    head = tail;
    tail = iterator;
    while (iterator){
        number* temp = iterator-> next;
        iterator-> next = iterator-> previous;
        iterator-> previous = temp;
        iterator = iterator-> previous;
    }
    tail-> next = iterator;
    head-> previous = tail;
}



void LinkedList::sort_internal(int) {
    for (int i=0; i < this->length; i++){
        number* iterator =head;
        while (iterator-> next){
            if(iterator->value > (iterator->next)-> value){
                int temp = iterator->value;
                iterator->value = (iterator->next)->value;
                (iterator->next)->value = temp;
                iterator = iterator-> next;
            }
            else {iterator = iterator-> next; break;}
        }
        iterator = iterator-> next;
    }
}



LinkedList LinkedList::slicer(int start, int end, int direction){
    LinkedList return_LinkedList;
    if (!head) {cerr << "Empty List" << endl; return return_LinkedList;} else if(abs(start) >= this->length || abs(end) >= this->length){cerr << "Start or end out of range!"<<endl;return return_LinkedList;} else if(start !=0 && start == end) {cerr << "No number fits the criteria" << endl; return return_LinkedList;} else if (abs(direction)>1 || direction == 0) {cerr <<"Invalid direction";}
    if (direction == 1){
       if(end == 0 && start >= 0) end = this->length - start; else if (start < 0 && end == 0) end = abs(start)-1;else if(end < 0 && start > 0) end = 2*this->length + end - start; else if(start < 0 && end < 0 && abs(start) > abs(end)) end -= start; else if(start < 0 && end < 0 && abs(start) < abs(end)) end = this->length - start + end; else if(end < start) end = this->length - start + end; else end -= start;
        number* iterator = head;
       if(start >= 0) for (int x = 1; x < start; x++) iterator = iterator-> next; else for (int x=0; x < abs(start); x++) iterator = iterator-> previous;
       for (int x = 0; true ; x++){
           if (x+1 > end) {return_LinkedList.append(iterator->value); break;}
            return_LinkedList.append(iterator->value);
           if (iterator == tail) iterator = head; else iterator = iterator-> next;
       }
    }
    else{
       if(end == 0 && start >= 0) end = start; else if (start < 0 && end == 0) end = this->length + start; else if(end < 0 && start > 0) end = start - end; else if(start < 0 && end < 0 && abs(start) > abs(end)) end = this->length + start - end; else if(start < 0 && end < 0 && abs(start) < abs(end)) end = start - end; else if(end < start) end = start - end; else end = start + this->length - end;
        number* iterator = head;
      if(start >= 0) for (int x = 0; x < start; x++) iterator = iterator-> next; else for (int x=0; x < abs(start); x++) iterator = iterator-> previous;
      for (int x = 0; true ; x++){
          if (x+1 > end) { return_LinkedList.append(iterator->value); break;}
           return_LinkedList.append(iterator->value);
          iterator = iterator->previous;
      } cout<<endl;
    }
    return (return_LinkedList);
}


void LinkedList::delete_number(int pos) {
    if(!head){cerr << "Empty List!";return;} else if(pos >= this->length || (pos < 0 && abs(pos) > this->length)) cerr<< "position out of range!";
    number* temp = nullptr;
    if (pos == 0 || (pos < 0 && abs(pos) == this->length)){
        temp = head;
        (head->next)->previous = tail;
        head = head->next;
    }
    else if(pos == this->length-1 || pos == -1) {
        temp = tail;
        tail = tail->previous;
        head->previous = tail;
    }
    else if(pos > 0){
        number* iterator = head;
        for(int x=1; x<pos; x++) iterator = iterator-> next;
        temp = iterator -> next;
        ((iterator->next)->next)->previous = iterator;
        iterator -> next =(iterator->next)-> next;
    }
    else{
        number* iterator = tail;
        for (int x =2 ; x < abs(pos); x++) iterator = iterator->previous;
        temp = iterator-> previous;
        ((iterator->previous)->previous)-> next = iterator;
        iterator-> previous = (iterator->previous)-> previous;
    }
    this->length--;
    delete temp;
}


void LinkedList::reset(){
    number* iterator = head;
    int end_point = this->length;
    for (int i=0; i < end_point; i++){
        number* temp = iterator;
        iterator = iterator-> next;
        delete temp;
    }
    head = nullptr;
    tail = nullptr;
    this->length=0;
}

int main() {
    LinkedList LinkedList1;
}

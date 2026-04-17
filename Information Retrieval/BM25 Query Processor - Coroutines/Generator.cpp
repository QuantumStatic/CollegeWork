//
//  Generator.cpp
//  HW3-3
//
//  Created by Utkarsh Jain on 13/11/23.
//

#include <coroutine>
#include <iostream>

// This struct represents a generator object that produces a sequence of integers
template<typename T>
struct generator {
    struct promise_type;
    using handle_type = std::coroutine_handle<promise_type>;
    
    struct promise_type { // A member variable that stores the current value of the generator
        T value;
        // A method that returns the generator object when the coroutine is created
        auto get_return_object() { return generator{handle_type::from_promise(*this)}; }
        // A method that suspends the coroutine before the first value is produced
        auto initial_suspend() { return std::suspend_always{}; }
        // A method that suspends the coroutine before the first value is produced
        auto final_suspend() noexcept { return std::suspend_always{}; }
        // A method that handles any uncaught exception in the coroutine
        void unhandled_exception() { std::terminate(); }
        // A method that indicates the end of the generator sequence
        void return_value(T value) { this->value = value; }
        // A method that suspends the coroutine and yields a value to the generator
        auto yield_value(T value) {
            this->value = value;
            return std::suspend_always{};
        }
    };
    
    // A method that resumes the coroutine and returns true if there is more value to generate
    bool move_next() {
//        bool check = (bool) coro;
//        coro.resume();
        return coro ? (coro.resume(), !coro.done()) : false;
//        return coro ? (bool)(coro.resume()) : false;
//        return true;
    }
    // A method that returns the current value of the generator
    T current_value() { return coro.promise().value; }
    
    // Delete the copy constructor of the generator
    generator(generator const&) = delete;
    // Define the move constructor of the generator
    generator(generator && rhs) : coro(rhs.coro) { rhs.coro = nullptr; }
    // Define the destructor of the generator
    ~generator() { if (coro) coro.destroy(); }

private:
    // A private constructor of the generator that takes a coroutine
    generator(handle_type h) : coro(h) {}
    // A member variable that stores the coroutine handle
    handle_type coro;
};

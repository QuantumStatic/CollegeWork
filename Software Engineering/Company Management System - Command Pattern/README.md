# Company Management System — Command Pattern in Java

> A company simulator — hire people, form teams, assign projects. Built in three iterative phases, each adding new capabilities on top of the last.

**Course:** Problem Solving and Programming (CS2310)  
**Institution:** CityU  
**Type:** Individual Assignment  

## Skills
`Java`, `OOP`, `Design Patterns`, `IntelliJ IDEA`

## About
- Every user action is its own Command class — hire, setup-team, take-project, suggest-best-team — keeping the core domain objects clean and each new phase purely additive
- 15+ custom exception classes make every invalid state explicit; Phase 3 adds team ranking by available capacity to suggest the best fit for a given project

## Files
```
Phase 1/src/       — Core: hire, setup-team, list commands + base exception classes
Phase 2/src/       — Adds: take-project, join-team, change-team, suggest-best-team
Phase 3/src/       — Adds: show-employee-details, show-project-worker-details, team ranking
Phase 1/Test Cases/ — Input/output test cases A–C
Phase 2/Test Cases/ — Input/output test cases D–F
Phase 3/Test Cases/ — Input/output test cases G–I
Assignment_Question.pdf — Full assignment specification
```

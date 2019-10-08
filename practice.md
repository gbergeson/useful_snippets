1. Remove target string

Warmup:

Given a list of strings, remove the first instance of a target string.

Input: `["apple", "orange", "grape", "orange", "apple"], "orange"`
Output: `["apple", "grape", "orange", "apple"]`

More difficult version:

Instead of a flat list of strings, you can have nested lists inside the list. Make a copy, without the first instance.

Input: `["apple", ["orange", "grape"], "orange", ["pickle", ["dragonfruit"]]], "orange"` (also test with with target string `dragonfruit` to make sure it can removce from 3rd level deep)

Output: `["apple", ["grape"], "orange", ["pickle", ["dragonfruit"]]]`

bool removed = false
list, removed = recursive(list_so_far, removed)



2. Stock prices

Given a list of stock prices over several days, find the indices best day to buy and sell.
Input: `[100, 200, 300, 50, 150, 310]`
Output: `3, 5`

More difficult test case: (have to buy and sell on different days)
Input: `[500, 100, 200, 300, 50, 150, 310, 20]`
Output: `4, 6`

https://www.hackerrank.com/challenges/stockmax/problem

Best solution is O(n)


3. directed graph
(Cracking the coding interview)

A) Parse the graph
Input: `A->B,B->C,C->E,C->D`
Output an adjacency list:
```
A: B
B: C
C: D,E
D: 
E: 
```

B) Output the leaf nodes (extra credit: in alphabetical order)
Input: `A->B,B->C,C->E,C->D`
Output: `D,E`

C) Check if it's cyclical and output "true" or "false"
`A->B,B->A true`
`A->B,B->C,C->E,C->D` false
`A->B,B->C,C->E,C->D,E->B` true

hairier:
`A->B,X->Y,Y->A`
(extra credit: O(n) solution)



4. Island problem
given a 2d array (map), find the size of the biggest island.
```
x..xx.
xx..x.
..x.x.
x.xxx.
```
output: 8



5. Baby names
Given counts of baby names like so:
```
John 10
Kristine 15
Jon 5
Christina 20
Johnny 8
Eve 5
Chris 12
```
Some of the names are variations so the counts should be combined.
```
John-Jon
Johnny-John
Kristine-Christina
```
Output:
```
John 23
Christina 35
Eve 5
Chris 12
```
Hairier test case: try to confuse your algorithm with a chain of references.

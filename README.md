# Homework on "Cache Management Algorithms"

Welcome! 🌞
Ready to apply **cache management algorithms**? Let’s get to work!

In the first task, you'll learn to use **LRU cache** to optimize data processing in a program. This task will allow you to compare performance with and without caching, demonstrating how caching can significantly reduce query execution time in systems handling large datasets.

In the second task, you'll implement two optimization methods for computing Fibonacci numbers:

1. Using the `@lru_cache` decorator
2. Using a `Splay Tree` data structure

By completing this task, you'll compare two different caching strategies, analyze their efficiency, and visually compare the results.

This assignment will help you understand the advantages and limitations of different caching approaches and their impact on program performance, especially with large input data.

Good luck! 😎


## Task 1: Optimizing Data Access with LRU Cache

### Objective:

Implement a program that optimizes query processing on an array of numbers using LRU caching.

### Technical Requirements

1. You are given an array of size N containing positive integers (1 ≤ N ≤ 100,000). You need to process Q queries (1 ≤ Q ≤ 50,000) of the following types:

- `Range(L, R)`: Find the sum of elements between indices L and R (inclusive).
- `Update(index, value)`: Update the element at `index` index with a new value `value`.

2. Implement four functions to work with the array:

- `range_sum_no_cache(array, L, R)`: Computes the sum without caching (recomputes each time).
- `update_no_cache(array, index, value)`: Updates an element without caching.
- `range_sum_with_cache(array, L, R)`: Uses LRU cache to store and retrieve previously computed sums.
- `update_with_cache(array, index, value)`: Updates an element and invalidates affected cache entries.

3. Test your program by generating:

- A 100,000-element array filled with random numbers.
- 50,000 random queries (mix of `Range` and `Update`).
- Example query list:` [('Range', 46943, 91428), ('Range', 5528, 29889), ('Update', 77043, 78), ...]`

4. Use an LRU cache of size K = 1000 for `Range` queries. The cache should automatically evict least recently used items when full.

5. Measure execution time for:

- Query processing without caching
- Query processing with LRU caching
- Compare the results and display execution times.

### Acceptance Criteria

📌 Your solution must meet these criteria for review. If any are missing, the mentor will return it for revision without grading. If you're stuck, ask your mentor in Slack.

1. All four functions are implemented and work correctly.
2. The program measures and displays execution time for both approaches.
3. Test results are presented in a clear format to evaluate LRU cache efficiency.
4. The code runs without errors and meets technical requirements.

**Example Terminal Output**

```python
Execution time without caching: 3.11 seconds  
Execution time with LRU cache: 0.02 seconds  
```

***

## Task 2: Performance Comparison of Fibonacci Computation Using LRU Cache and Splay Tree

### Objective:
Implement a program to compute Fibonacci numbers using:

1. LRU Cache (`@lru_cache`)
2. Splay Tree (to store previously computed values)

Then, compare their performance by measuring execution time for each method.

### Technical Requirements

1. Implement two functions for Fibonacci computation:

  - `fibonacci_lru(n)`: Uses @lru_cache to store and reuse computed Fibonacci numbers.
  - `fibonacci_splay(n, tree)`: Uses a Splay Tree for caching computed values.

2. Measure execution time for each method:

- Compute Fibonacci numbers for n = 0 to 950 (step = 50).
- Use `timeit` to measure execution time.
- For each `n`, compute the average execution time using both LRU Cache and Splay Tree.

3. Plot a performance comparison graph:

- Use `matplotlib` to visualize execution times.
- X-axis: Fibonacci index `n`.
- Y-axis: Average execution time (seconds).
- Include legend distinguishing LRU Cache vs. Splay Tree.

4. Analyze the results based on the graph.

5. Print a formatted table showing:

  - `n` values
  - Average execution time for LRU Cache
  - Average execution time for Splay Tree

### Acceptance Criteria

1. Both functions (`fibonacci_lru` and `fibonacci_splay`) are implemented correctly.
2. Execution time is measured for each method at every `n` value.
3. A graph is generated with proper axis labels, title, and legend.
4. A formatted table is printed in the terminal.
5. Results are analyzed to determine which method is more efficient for large n.
6. Code runs correctly and meets technical requirements.

### Example Table Output

```python
n         LRU Cache Time (s)  Splay Tree Time (s)  
--------------------------------------------------  
0         0.00000028          0.00000020  
50        0.00000217          0.00000572  
100       0.00000164          0.00000532  
150       0.00000174          0.00000526  
```

Example of a graph

![example](./assets/task.png)

This homework will give you practical experience with cache optimization and its impact on performance. 🚀
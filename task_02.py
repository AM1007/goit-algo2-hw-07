from functools import lru_cache
import timeit
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

# Реалізація LRU-кешованого обчислення чисел Фібоначчі
@lru_cache(maxsize=None)  # Необмежений розмір кешу
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

# Реалізація Splay Tree
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None
    
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y
    
    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y
    
    def _splay(self, root, key):
        if root is None or root.key == key:
            return root
        
        if root.key > key:  # Ключ знаходиться в лівому піддереві
            if root.left is None:
                return root
            
            if root.left.key > key:  # Zig-Zig (Left Left)
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
                if root.left is None:
                    return root
                return self._right_rotate(root)
            elif root.left.key < key:  # Zig-Zag (Left Right)
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)
                if root.left is None:
                    return root
                return self._right_rotate(root)
            else:
                return self._right_rotate(root)
        else:  # Ключ знаходиться в правому піддереві
            if root.right is None:
                return root
            
            if root.right.key > key:  # Zag-Zig (Right Left)
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)
                if root.right is None:
                    return root
                return self._left_rotate(root)
            elif root.right.key < key:  # Zag-Zag (Right Right)
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
                if root.right is None:
                    return root
                return self._left_rotate(root)
            else:
                return self._left_rotate(root)
    
    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root is not None and self.root.key == key:
            return self.root.value
        return None
    
    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        
        self.root = self._splay(self.root, key)
        
        if self.root.key == key:
            # Оновлення значення, якщо ключ вже існує
            self.root.value = value
            return
        
        new_node = Node(key, value)
        
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

# Функція для обчислення чисел Фібоначчі з використанням Splay Tree
def fibonacci_splay(n, tree):
    # Спробуємо знайти значення в дереві
    result = tree.search(n)
    if result is not None:
        return result
    
    # Якщо значення не знайдено, обчислюємо його і зберігаємо в дереві
    if n <= 1:
        tree.insert(n, n)
        return n
    
    # Рекурсивно обчислюємо два попередні числа
    result = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    
    # Зберігаємо результат у дереві
    tree.insert(n, result)
    return result

# Функція для вимірювання часу виконання
def measure_performance(max_n=950, step=50):
    n_values = list(range(0, max_n+1, step))
    lru_times = []
    splay_times = []
    
    # Створюємо таблицю результатів
    results = []
    
    # Отримаємо дані для кожного значення n
    for n in n_values:
        print(f"Вимірювання для n={n}...")
        
        # Вимірювання часу для LRU Cache
        # Скидаємо кеш перед кожним вимірюванням
        fibonacci_lru.cache_clear()
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
        
        # Вимірювання часу для Splay Tree
        tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=3) / 3
        
        lru_times.append(lru_time)
        splay_times.append(splay_time)
        
        # Додаємо результати до таблиці
        results.append([n, lru_time, splay_time])
        
        print(f"LRU Cache: {lru_time:.8f} сек, Splay Tree: {splay_time:.8f} сек")
    
    return n_values, lru_times, splay_times, results

# Функція для побудови графіка
def plot_results(n_values, lru_times, splay_times):
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, 'o-', label='LRU Cache')
    plt.plot(n_values, splay_times, 'x-', label='Splay Tree')
    plt.xlabel('Число Фібоначчі (n)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
    plt.legend()
    plt.grid(True)
    plt.savefig('fibonacci_comparison.png')
    plt.show()

# Функція для виведення таблиці результатів
def print_table(results):
    headers = ["n", "LRU Cache Time (s)", "Splay Tree Time (s)"]
    print(tabulate(results, headers=headers, tablefmt="grid", floatfmt=".8f"))

# Головна функція
def main():
    print("Порівняння продуктивності обчислення чисел Фібоначчі")
    print("=====================================================")
    
    # Вимірюємо продуктивність
    n_values, lru_times, splay_times, results = measure_performance()
    
    # Виводимо таблицю результатів
    print("\nРезультати вимірювань:")
    print_table(results)
    
    # Будуємо графік
    plot_results(n_values, lru_times, splay_times)
    
    # Аналіз результатів
    if np.mean(lru_times) < np.mean(splay_times):
        print("\nВисновок: LRU Cache в середньому працює швидше, ніж Splay Tree для обчислення чисел Фібоначчі.")
    else:
        print("\nВисновок: Splay Tree в середньому працює швидше, ніж LRU Cache для обчислення чисел Фібоначчі.")
    
    fastest_lru = n_values[lru_times.index(min(lru_times))]
    fastest_splay = n_values[splay_times.index(min(splay_times))]
    
    print(f"Найшвидше значення для LRU Cache: n={fastest_lru}")
    print(f"Найшвидше значення для Splay Tree: n={fastest_splay}")

if __name__ == "__main__":
    main()
from collections import OrderedDict
import random
import time

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return None
        # Move the accessed item to the end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        # If key exists, update its value and move it to the end
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return
        
        # If cache is full, remove the least recently used item (first item)
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        
        # Add the new key-value pair
        self.cache[key] = value
    
    def remove_by_prefix(self, prefix):
        # Remove all cache entries whose key starts with the given prefix
        keys_to_remove = [k for k in self.cache.keys() if k.startswith(prefix)]
        for k in keys_to_remove:
            del self.cache[k]

# Initialize a global LRU cache with capacity 1000
CACHE = LRUCache(1000)

def range_sum_no_cache(array, L, R):
    """Calculate sum of elements from index L to R without caching"""
    # Використання вбудованої функції sum з обмеженням діапазону для більшої швидкості
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    """Update array at index with value without caching"""
    array[index] = value
    return array

def range_sum_with_cache(array, L, R):
    """Calculate sum of elements from index L to R using LRU cache"""
    # Create a unique key for this range query
    cache_key = f"range_{L}_{R}"
    
    # Check if the result is in the cache
    cached_result = CACHE.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # If not in cache, compute the result and store it
    result = sum(array[L:R+1])
    CACHE.put(cache_key, result)
    return result

def update_with_cache(array, index, value):
    """Update array at index with value and invalidate affected cache entries"""
    old_value = array[index]
    array[index] = value
    
    # Оптимізована інвалідація кешу - тільки для ключів, що містять оновлений індекс
    keys_to_check = list(CACHE.cache.keys())
    for key in keys_to_check:
        if key.startswith("range_"):
            parts = key.split("_")
            if len(parts) == 3:
                try:
                    start_idx = int(parts[1])
                    end_idx = int(parts[2])
                    if start_idx <= index <= end_idx:
                        del CACHE.cache[key]
                except ValueError:
                    continue
    
    return array

def generate_random_array(size):
    """Generate a random array of given size"""
    return [random.randint(1, 1000) for _ in range(size)]

def generate_random_queries(num_queries, array_size, reduced_size=False):
    """Generate random queries of type Range and Update"""
    queries = []
    for _ in range(num_queries):
        if random.random() < 0.8:  # 80% probability for Range queries
            # Generate random range indices with limited range size
            if reduced_size:
                # Обмежуємо розмір діапазону для швидшого тестування
                L = random.randint(0, array_size - 2)
                max_range = min(L + 1000, array_size - 1)  # Обмежуємо діапазон до 1000 елементів
                R = random.randint(L, max_range)
            else:
                L = random.randint(0, array_size - 2)
                R = random.randint(L, array_size - 1)
            queries.append(('Range', L, R))
        else:  # 20% probability for Update queries
            index = random.randint(0, array_size - 1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))
    return queries

def test_performance(small_test=True):
    # Для тестування використовуємо менший масив і менше запитів
    if small_test:
        array_size = 10000  # Зменшуємо розмір масиву для швидшого тестування
        num_queries = 5000  # Зменшуємо кількість запитів для швидшого тестування
    else:
        array_size = 100000
        num_queries = 50000
    
    print(f"Тестування з масивом розміром {array_size} та {num_queries} запитами")
    
    # Create a random array
    array = generate_random_array(array_size)
    
    # Generate random queries
    queries = generate_random_queries(num_queries, array_size, reduced_size=True)
    
    # Make copies of the array for both approaches
    array_no_cache = array.copy()
    array_with_cache = array.copy()
    
    # Test without cache
    print("Виконання запитів без кешування...")
    start_time = time.time()
    for query_type, param1, param2 in queries:
        if query_type == 'Range':
            range_sum_no_cache(array_no_cache, param1, param2)
        else:  # Update
            update_no_cache(array_no_cache, param1, param2)
    no_cache_time = time.time() - start_time
    
    # Reset the LRU cache
    global CACHE
    CACHE = LRUCache(1000)
    
    # Test with LRU cache
    print("Виконання запитів з LRU-кешем...")
    start_time = time.time()
    for query_type, param1, param2 in queries:
        if query_type == 'Range':
            range_sum_with_cache(array_with_cache, param1, param2)
        else:  # Update
            update_with_cache(array_with_cache, param1, param2)
    with_cache_time = time.time() - start_time
    
    # Print results
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {with_cache_time:.2f} секунд")
    print(f"Прискорення: {no_cache_time / with_cache_time:.2f}x")
    
    # Перевірка правильності результатів
    print("\nПеревірка правильності реалізації...")
    test_array = [1, 2, 3, 4, 5]
    assert range_sum_no_cache(test_array, 1, 3) == 9  # 2 + 3 + 4 = 9
    assert range_sum_with_cache(test_array, 1, 3) == 9
    update_no_cache(test_array, 2, 10)
    assert test_array[2] == 10
    assert range_sum_no_cache(test_array, 1, 3) == 16  # 2 + 10 + 4 = 16
    
    # Відновлюємо початковий масив
    test_array = [1, 2, 3, 4, 5]
    CACHE = LRUCache(10)
    # Кешуємо результат
    assert range_sum_with_cache(test_array, 1, 3) == 9
    # Оновлюємо значення
    update_with_cache(test_array, 2, 10)
    # Перевіряємо, що кеш інвалідовано і повертається нове значення
    assert range_sum_with_cache(test_array, 1, 3) == 16
    
    print("Всі тести пройдено успішно!")

if __name__ == "__main__":
    # За замовчуванням запускаємо зменшений тест для швидкого виконання
    test_performance(small_test=True)
    
    # Можна розкоментувати наступний рядок для повного тесту
    # test_performance(small_test=False)
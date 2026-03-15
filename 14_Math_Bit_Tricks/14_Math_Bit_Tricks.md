# Math & Bit Tricks — Complete Guide

## 1. Bit Manipulation

### Essential Operations
```python
# Check if bit i is set
(n >> i) & 1

# Set bit i
n | (1 << i)

# Clear bit i
n & ~(1 << i)

# Toggle bit i
n ^ (1 << i)

# Clear lowest set bit
n & (n - 1)

# Isolate lowest set bit
n & (-n)

# Check power of 2
n > 0 and (n & (n - 1)) == 0

# Count set bits (popcount)
bin(n).count('1')  # Python
# Or Brian Kernighan's:
count = 0
while n:
    n &= n - 1
    count += 1
```

### XOR Properties
```python
a ^ a = 0       # self-cancel
a ^ 0 = a       # identity
a ^ b = b ^ a   # commutative
(a ^ b) ^ c = a ^ (b ^ c)  # associative
```
**Key application:** XOR all elements. Duplicates cancel. Single unique element remains.

### Template: Single Number
```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

### Template: Find Two Missing/Unique Numbers
```python
def two_unique(nums):
    xor_all = 0
    for num in nums:
        xor_all ^= num
    
    # Find rightmost set bit (differentiator)
    diff_bit = xor_all & (-xor_all)
    
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num
    return a, b
```

### Template: Subset Enumeration via Bitmask
```python
# Enumerate all subsets of n elements
n = len(arr)
for mask in range(1 << n):
    subset = []
    for i in range(n):
        if mask & (1 << i):
            subset.append(arr[i])

# Enumerate all submasks of a given mask
submask = mask
while submask > 0:
    # process submask
    submask = (submask - 1) & mask
```

---

## 2. Number Theory

### GCD / LCM
```python
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

# Extended GCD: finds x, y such that ax + by = gcd(a, b)
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y
```

### Fast Exponentiation
```python
def power(base, exp, mod=None):
    result = 1
    base = base % mod if mod else base
    while exp > 0:
        if exp & 1:
            result = result * base % mod if mod else result * base
        exp >>= 1
        base = base * base % mod if mod else base * base
    return result

# Python built-in: pow(base, exp, mod)
```

### Sieve of Eratosthenes
```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]
```
O(n log log n) time, O(n) space.

### Modular Arithmetic
```python
MOD = 10**9 + 7

# (a + b) % MOD
# (a * b) % MOD
# (a - b + MOD) % MOD  (avoid negative)

# Modular inverse (when MOD is prime): a^(-1) = a^(MOD-2) mod MOD
def mod_inverse(a, mod):
    return pow(a, mod - 2, mod)

# nCr mod p
def ncr(n, r, mod):
    if r > n:
        return 0
    num = den = 1
    for i in range(r):
        num = num * (n - i) % mod
        den = den * (i + 1) % mod
    return num * mod_inverse(den, mod) % mod
```

### Prime Factorization
```python
def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors
```

---

## 3. Common Math Patterns

### Counting Digits
```python
# Number of digits of n in base 10
import math
digits = math.floor(math.log10(n)) + 1 if n > 0 else 1
# Or: len(str(n))
```

### Integer Overflow Handling (Other Languages)
Python handles big ints natively. In Java/C++:
- Use `long` or check before multiplication.
- For `a + b` overflow: check `a > MAX - b`.
- For `a * b`: use `(long)a * b`.

### Pigeonhole Principle
If n items go into m boxes and n > m, at least one box has > 1 item. Used in duplicate detection (LC 287).

### Reservoir Sampling
Pick k items uniformly at random from a stream of unknown length.
```python
import random
def reservoir_sample(stream, k):
    result = []
    for i, item in enumerate(stream):
        if i < k:
            result.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                result[j] = item
    return result
```

---

## 4. Edge Cases

- **n = 0** — log(0) undefined, 0^0 varies by convention.
- **Negative numbers + bit ops** — Python ints have infinite precision. `-1 & mask` may surprise you.
- **Overflow in modular arithmetic** — multiply before mod: `(a % mod * b % mod) % mod`.
- **GCD(0, x) = x** — handle 0 input.
- **Power of 2 check** — must check `n > 0` first. `0 & (0-1) == 0` but 0 is not a power of 2.

---

## 5. LeetCode Problems

### Bit Manipulation
| # | Problem | Key Concept |
|---|---------|-------------|
| 136 | Single Number | XOR all |
| 260 | Single Number III | XOR + partition by diff bit |
| 191 | Number of 1 Bits | Popcount / Kernighan |
| 231 | Power of Two | n & (n-1) == 0 |
| 338 | Counting Bits | DP: dp[i] = dp[i >> 1] + (i & 1) |
| 371 | Sum of Two Integers | Bit manipulation add (no + operator) |
| 78 | Subsets | Bitmask enumeration |
| 268 | Missing Number | XOR with indices |
| 461 | Hamming Distance | XOR + popcount |

### Math
| # | Problem | Key Concept |
|---|---------|-------------|
| 204 | Count Primes | Sieve of Eratosthenes |
| 50 | Pow(x, n) | Fast exponentiation |
| 7 | Reverse Integer | Digit manipulation + overflow |
| 9 | Palindrome Number | Reverse half |
| 172 | Factorial Trailing Zeroes | Count factors of 5 |
| 202 | Happy Number | Cycle detection (Floyd's) |
| 287 | Find the Duplicate Number | Pigeonhole + Floyd's cycle |
| 1523 | Count Odd Numbers in Range | Math formula |
| 279 | Perfect Squares | BFS or DP |

### Study Order
**Phase 1 (2-3 days):** 136, 191, 231, 338, 268
**Phase 2 (2-3 days):** 260, 371, 461, 78
**Phase 3 (2-3 days):** 204, 50, 172, 287, 202

## 📘 **Homework 6 - Summary of Learnings**

### 🎯 **Main Concepts Learnt**

- **Sliding Window** - Computed subarray sums in O(N) time using window updates instead of recalculating full sums, significantly improving efficiency.
- **Anti-Diagonals** - Extracted anti-diagonals with simple index movement while maintaining optimal O(N²) complexity for an N×N matrix.
- **GCD and Modulo** - Used `math.gcd()` to evenly divide groups and applied mod 10⁹+7 to handle large outputs and prevent overflow. Have recently learnt this on my Applied Math course and happy to have used it here.
- **Recurrence Relations (Friend Pairing)** - Implemented the recurrence relation:
```
  f(n) = f(n-1) + (n-1) * f(n-2)
```
  Recognized as involution numbers in combinatorics and implemented with O(N) time and O(1) space.
- **Pair Sum Optimization** - Avoided nested loops by keeping a running sum, achieving O(N) time instead of O(N²).

---

### 🛠 **Key Techniques Applied**

- Efficient algorithm design to reduce time complexity.
- Mathematical reasoning using combinatorics and recurrence relations.
- Optimization strategies to avoid redundant computations.
- Clear justification of correctness and complexity analysis.

---

### 🧠 **Conclusion**

This homework improved my ability to design efficient algorithms, apply combinatorics and mathematical reasoning, and justify correctness and complexity in a concise and professional way.

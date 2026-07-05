# LeetCode Local Tester
A lightweight and universal Python tool to run and test **all LeetCode problems** directly on your computer.

### Features
- **Supports All Problems:** Works for both regular algorithms and System Design problems.
- **Auto Data Parsing:** Automatically converts raw LeetCode inputs into real Python objects, including `TreeNode` (Binary Trees) and `ListNode` (Linked Lists).
- **Easy Debugging:** Color outputs (`PASSED` / `WRONG ANSWER`) and automatically prints clean, flattened arrays when a test fails.

### How to Use

It is very simple to use. You only need to copy your code from LeetCode and paste it into `solution.py`.

1. Open `solution.py`.
2. Replace the existing class with your LeetCode solution class.
3. Put your test cases into the input files (e.g., `input.txt` or `expected.txt`).
4. Run `main.py` to start the tester.

#### Example:
Just paste your class into `solution.py`:

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Your LeetCode code here
        pass
from __future__ import annotations
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self,
                 val: int = 0,
                 left: Optional[TreeNode] = None,
                 right: Optional[TreeNode] = None):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, value: object) -> bool:
        if self is value:
            return True

        if value is None or not isinstance(value, TreeNode):
            return False

        def dfs(root1: Optional[TreeNode], root2: Optional[TreeNode]):
            if root1 is None and root2 is None:
                return True
            if root1 is None or root2 is None:
                return False

            return (root1.val == root2.val and
                    dfs(root1.left, root2.left) and
                    dfs(root1.right, root2.right))

        return dfs(self, value)

    def __repr__(self) -> str:
        return str(TreeNode.serialize(self))

    @staticmethod
    def serialize(root: Optional[TreeNode]) -> List[Optional[int]]:
        if not root:
            return []

        data = []
        q: deque[Optional[TreeNode]] = deque([root])

        while q:
            cur_node = q.popleft()
            if cur_node:
                data.append(cur_node.val)
                q.append(cur_node.left)
                q.append(cur_node.right)
            else:
                data.append(None)

        while data and data[-1] is None:
            data.pop()

        return data

    @staticmethod
    def deserialize(data: List[Optional[int]]) -> Optional[TreeNode]:
        if not data or data[0] is None:
            return None

        root = TreeNode(data[0])
        q: deque[TreeNode] = deque([root])

        i = 1
        while q and i < len(data):
            cur = q.popleft()

            if i < len(data):
                x = data[i]
                if x is not None:
                    cur.left = TreeNode(x)
                    q.append(cur.left)
            i += 1

            if i < len(data):
                x = data[i]
                if x is not None:
                    cur.right = TreeNode(x)
                    q.append(cur.right)
            i += 1

        return root

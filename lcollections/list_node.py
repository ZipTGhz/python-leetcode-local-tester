from __future__ import annotations
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        self.val = val
        self.next = next

    def __eq__(self, value: object) -> bool:
        if self is value:
            return True

        if value is None or not isinstance(value, ListNode):
            return False

        cur: Optional[ListNode] = self
        other: Optional[ListNode] = value
        while cur and other:
            if cur.val != other.val:
                return False
            cur = cur.next
            other = other.next

        return cur is other

    def __repr__(self) -> str:
        return str(ListNode.serialize(self))

    @staticmethod
    def serialize(head: Optional[ListNode]) -> List[int]:
        res: List[int] = []
        while head:
            res.append(head.val)
            head = head.next
        return res

    @staticmethod
    def deserialize(data: List[int]) -> Optional[ListNode]:
        head = ListNode(-1)
        tail = head
        for x in data:
            tmp = ListNode(x)
            tail.next = tmp
            tail = tmp
        return head.next

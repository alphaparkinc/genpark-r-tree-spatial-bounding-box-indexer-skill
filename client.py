"""
Autonomous Agent KD-Tree Spatial Indexer Skill
Pure Python Standard Library implementation.
"""
import math
from typing import List, Tuple, Dict, Any, Optional

class KDTree2D:
    """
    2D KD-Tree spatial index for O(log n) nearest neighbor search.
    """
    class Node:
        def __init__(self, point: Tuple[float, float], data: Any, axis: int, left=None, right=None):
            self.point = point
            self.data = data
            self.axis = axis
            self.left = left
            self.right = right

    def __init__(self, points_with_data: List[Tuple[Tuple[float, float], Any]]):
        self.root = self._build(points_with_data, depth=0)

    def _build(self, points, depth):
        if not points:
            return None
        axis = depth % 2
        points.sort(key=lambda item: item[0][axis])
        mid = len(points) // 2
        return KDTree2D.Node(
            point=points[mid][0],
            data=points[mid][1],
            axis=axis,
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1:], depth + 1)
        )

    def nearest_neighbor(self, target: Tuple[float, float]) -> Tuple[Tuple[float, float], Any, float]:
        best = [None, None, float("inf")]

        def search(node):
            if node is None:
                return
            d_sq = (node.point[0] - target[0])**2 + (node.point[1] - target[1])**2
            if d_sq < best[2]:
                best[0] = node.point
                best[1] = node.data
                best[2] = d_sq

            axis = node.axis
            diff = target[axis] - node.point[axis]
            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left

            search(first)
            if diff**2 < best[2]:
                search(second)

        search(self.root)
        return best[0], best[1], round(math.sqrt(best[2]), 4)

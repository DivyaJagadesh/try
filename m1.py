import math
import itertools
import sys
import os
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def centroid_average(corners):
    n = len(corners)
    if n == 0:
        return [0.0, 0.0]
    sx = sum(p[0] for p in corners)
    sy = sum(p[1] for p in corners)
    

    return [sx / n, sy / n]

def dist(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def solve_tsp(centroids, start, velocity):
    if not centroids:
        return 0.0, 0.0, [start]
    best_len = float('inf')
    best_path = None
    for perm in itertools.permutations(centroids):
        path = [start] + list(perm)
        total = 0.0
        for i in range(len(path) - 1):
            total += dist(path[i], path[i+1])
        if total < best_len:
            best_len = total
            best_path = path
    total_time = best_len / velocity if velocity != 0 else float('inf')
    return best_len, total_time, best_path

def main():
    default = r"C:/hack/Software_Workshop_Day1/Day1/TestCases/Milestone1/Input_Milestone1_Testcase4.json"
    path = sys.argv[1] if len(sys.argv) > 1 else default
    if not os.path.exists(path):
        print(f"Input file not found: {path}")
        return
    data = load_json(path)

    start = data.get("InitialPosition") or data.get("Initial") or [0.0, 0.0]
    velocity = float(data.get("StageVelocity") or data.get("StageSpeed") or data.get("Velocity") or 1.0)

    dies = data.get("Dies", [])
    centroids = []
    for d in dies:
        corners = d.get("Corners") or d.get("corners") or []
        centroids.append(centroid_average(corners))

    total_dist, total_time, path = solve_tsp(centroids, start, velocity)

    out = {
        "TotalTime": round(total_time, 3),
        "Path": [[round(p[0], 3), round(p[1], 3)] for p in path]
    }

    print(json.dumps(out, indent=4))

    out_path = r"C:/hack/Software_Workshop_Day1/Day1/TestCases/Milestone1/TestCase_1_4.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

if __name__ == "__main__":
    main()

# src/optimizer.py

import pandas as pd

def greedy_assign(courses_df, rooms_df, timeslots):
    """
    Very simple greedy scheduler:
    - Assign largest courses first
    - Find first room with enough capacity
    - Pick first available timeslot
    """

    assignments = []

    # Sort courses by predicted size descending to place big ones first
    sorted_courses = courses_df.sort_values("predicted_students", ascending=False)

    # Track when each room is free
    room_free = {room: set(timeslots) for room in rooms_df["room_id"]}

    for _, course in sorted_courses.iterrows():
        needed = int(course["predicted_students"])
        duration = int(course["duration"])  # not used yet but reserved

        # Candidate rooms with enough capacity
        candidates = rooms_df[rooms_df["capacity"] >= needed].sort_values("capacity")

        assigned = False

        for _, room in candidates.iterrows():
            r = room["room_id"]

            if len(room_free[r]) > 0:
                ts = sorted(list(room_free[r]))[0]  # pick earliest available timeslot

                assignments.append({
                    "course_id": course["course_id"],
                    "course_name": course["course_name"],
                    "room_id": r,
                    "timeslot": ts,
                    "predicted_students": needed
                })

                room_free[r].remove(ts)
                assigned = True
                break

        if not assigned:
            assignments.append({
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "room_id": None,
                "timeslot": None,
                "predicted_students": needed
            })

    return pd.DataFrame(assignments)

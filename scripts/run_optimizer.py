import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.optimizer import greedy_assign

def main():
    
    courses = pd.read_csv("data/synthetic/courses_with_predictions.csv")
    rooms = pd.read_csv("data/synthetic/rooms.csv")
    hist = pd.read_csv("data/synthetic/historical_instances.csv")

    timeslots = sorted(hist["timeslot"].unique())

    print("Loaded data:")
    print(" - Courses:", len(courses))
    print(" - Rooms:", len(rooms))
    print(" - Timeslots:", len(timeslots))

    assignments = greedy_assign(courses, rooms, timeslots)

    out_path = "data/synthetic/assignments.csv"
    assignments.to_csv(out_path, index=False)
    print("Assignments saved to:", out_path)

    print("\nSample assignments:")
    print(assignments.head(10))

if __name__ == "__main__":
    main()

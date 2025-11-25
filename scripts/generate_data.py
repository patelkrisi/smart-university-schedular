import os, json, random
import pandas as pd, numpy as np

def generate_synthetic(num_courses=200, num_rooms=40, seed=123):
    random.seed(seed)
    np.random.seed(seed)

    days = ("Mon", "Tue", "Wed", "Thu", "Fri")
    start_hour = 8
    times_per_day = 8
    timeslots = [f"{start_hour + i:02d}:00-{start_hour + i + 1:02d}:00" for i in range(times_per_day)]

    instructors = [f"Dr. {n} {chr(65+i)}" for i, n in enumerate(np.random.choice(
        ["Singh","Kumar","Mehta","Schultz","Müller","Jansen","Garcia","Smith","Lee","Ng"], size=50, replace=True))]

    equip_pool = ["projector", "computers", "lab_kits", "whiteboard", "smartboard"]
    room_types = ["lecture", "lab"]

    courses = []
    historical_instances = []

    for i in range(num_courses):
        cid = f"C{i:04d}"
        course_level = np.random.choice(["UG", "PG"], p=[0.8, 0.2])
        course_name = f"{np.random.choice(['Calc','Data','Algo','Econ','Mgmt','Stat','AI','Networks','Sys','Opt'])} {np.random.randint(100,499)}"
        instr = np.random.choice(instructors)
        duration = np.random.choice([1, 2], p=[0.85, 0.15])
        room_type = np.random.choice(room_types, p=[0.8, 0.2])

        base = int(np.clip(np.random.normal(60 if course_level == 'UG' else 25, 15), 5, 200))
        hist = [int(max(1, np.random.poisson(base))) for _ in range(3)]

        if np.random.rand() < 0.6:
            prefs = []
            for _ in range(np.random.choice([1, 2])):
                d = random.choice(days)
                t = random.choice(timeslots)
                prefs.append(f"{d} {t}")
            pref_str = ";".join(prefs)
        else:
            pref_str = ""

        equipment = ",".join(np.random.choice(equip_pool, size=np.random.choice([0, 1, 2]), replace=False).tolist())
        expected = int(max(1, np.random.normal(base, base * 0.15)))

        courses.append({
            "course_id": cid,
            "course_name": course_name,
            "instructor": instr,
            "course_level": course_level,
            "duration": duration,
            "room_type": room_type,
            "historical_enrollment": json.dumps(hist),
            "expected_students": expected,
            "preferred_timeslots": pref_str,
            "equipment": equipment
        })

        for term_idx in range(3):
            term_name = f"T{2022 + term_idx}"
            d = np.random.choice(days)
            t = np.random.choice(timeslots)
            enrolled = max(1, int(np.random.normal(base, 10)))
            historical_instances.append({
                "course_id": cid,
                "term": term_name,
                "day_of_week": d,
                "timeslot": t,
                "enrolled": enrolled
            })

    courses_df = pd.DataFrame(courses)
    hist_df = pd.DataFrame(historical_instances)

    rooms = []
    buildings = ["A", "B", "C", "D"]

    for j in range(num_rooms):
        rid = f"R{j:03d}"
        cap = int(np.random.choice([20, 30, 40, 60, 80, 100], p=[0.2, 0.25, 0.25, 0.15, 0.1, 0.05]))
        rtype = np.random.choice(room_types, p=[0.85, 0.15])
        eq = ",".join(np.random.choice(equip_pool, size=np.random.choice([0, 1, 2]), replace=False).tolist())
        building = np.random.choice(buildings)
        floor = np.random.choice([1, 2, 3])

        rooms.append({
            "room_id": rid,
            "capacity": cap,
            "room_type": rtype,
            "equipment_list": eq,
            "building": building,
            "floor": floor
        })

    rooms_df = pd.DataFrame(rooms)

    return courses_df, rooms_df, hist_df


if __name__ == "__main__":
    out_dir = "data/synthetic"
    os.makedirs(out_dir, exist_ok=True)

    courses_df, rooms_df, hist_df = generate_synthetic()

    courses_df.to_csv(os.path.join(out_dir, "courses.csv"), index=False)
    rooms_df.to_csv(os.path.join(out_dir, "rooms.csv"), index=False)
    hist_df.to_csv(os.path.join(out_dir, "historical_instances.csv"), index=False)

    print("Dataset generated in:", out_dir)

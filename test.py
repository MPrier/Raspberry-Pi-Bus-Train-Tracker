# import requests
# import time
# from datetime import datetime, timedelta
# import pytz

# # === CONFIG ===
# STOP_ID = "590900"  # North & Worthen
# BASE_PTA_URL = f"https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/pta/{STOP_ID}"
# BASE_HORAIRE_URL = "https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/horaire"

# def format_time(seconds):
#     """Convert seconds since midnight to 12-hour AM/PM format."""
#     base_time = datetime(2000, 1, 1) + timedelta(seconds=seconds)
#     return base_time.strftime("%I:%M %p").lstrip("0")

# def fetch_json(url):
#     """Fetch JSON from URL with dynamic timestamp."""
#     params = {"_tmp": int(time.time() * 1000)}
#     response = requests.get(url, params=params, timeout=10)
#     response.raise_for_status()
#     return response.json()

# def fetch_initial_schedule():
#     """Fetch the initial schedule for the stop."""
#     data = fetch_json(BASE_PTA_URL)
#     horaires_data = []

#     liste_horaires = data.get("listeHoraires", [])
#     if not liste_horaires:
#         return []

#     ligne = liste_horaires[0]
#     destination = ligne["destination"][0]
#     line_id = ligne["idLigne"]
#     dest_name = destination["libelle"]
#     horaires_list = destination["horaires"]

#     for h in horaires_list:
#         horaires_data.append({
#             "line_id": line_id,
#             "destination": dest_name,
#             "idHoraire": h["idHoraire"],
#             "time": format_time(h["horaire"])
#         })
#     return horaires_data

# def fetch_next_schedule(stop_id, id_horaire):
#     """Fetch the next schedule for a given idHoraire."""
#     url = f"{BASE_HORAIRE_URL}/{stop_id}/{id_horaire}/SUIVANT"
#     data = fetch_json(url)
#     dest = data["destination"][0]
#     horaires_next = dest["horaires"][1:]  # skip first repeated time

#     result = []
#     for h in horaires_next:
#         result.append({
#             "idHoraire": h["idHoraire"],
#             "destination": dest["libelle"],
#             "time": format_time(h["horaire"])
#         })
#     existe_suivant = dest.get("existeSuivant", False)
#     return result, existe_suivant

# def lowell_bus():
#     all_times = []

#     # Step 1: Fetch initial schedule
#     initial_schedule = fetch_initial_schedule()
#     if not initial_schedule:
#         print("⚠️ No initial schedule found.")
#         return

#     # print("\n🚌 Initial schedule:")
#     # for entry in initial_schedule:
#     #     print(f"  Arrival at {entry['time']}")
#     all_times.extend(initial_schedule)

#     # Step 2: Start fetching /SUIVANT using second idHoraire
#     if len(initial_schedule) > 1:
#         next_id = initial_schedule[1]["idHoraire"]
#         while True:
#             next_schedule, existe_suivant = fetch_next_schedule(STOP_ID, next_id)
#             if not next_schedule:
#                 break

#             # print("\n✅ Next schedule block:")
#             # for entry in next_schedule:
#             #     print(f"  Next arrival at {entry['time']}")
#             all_times.extend(next_schedule)

#             if not existe_suivant:
#                 # print("\n🟢 Reached end of schedule for the day.")
#                 break

#             next_id = next_schedule[-1]["idHoraire"]
#     else:
#         print("⚠️ Only one time found — no second idHoraire to fetch next schedule.")

#     # Step 3: Print full day schedule
#     print("\n🕐 Full day schedule:")
#     for entry in all_times:
#         print("  ", entry['time'])

# def get_commuter_rail_schedule():
#     """Fetches and prints MBTA commuter rail predictions for all stops at Lowell Station."""
#     # Optional: You can add your MBTA API key for higher limits
#     headers = {
#         # "x-api-key": "YOUR_MBTA_API_KEY"
#     }

#     # Known Lowell Station stop IDs for MBTA commuter rail
#     stops = ["place-NHRML-0254"]  # (usually inbound/outbound platforms)
#     stops_param = ",".join(stops)

#     Wrongurl = f"https://api-v3.mbta.com/predictions?filter[stop]={stops_param}&include=stop,route"
#     url = f"https://api-v3.mbta.com/schedules?filter[stop]=place-NHRML-0254&filter[route]=CR-Lowell&filter[direction_id]=1&sort=departure_time"

#     response = requests.get(url, headers=headers)
#     data = response.json()

#     if "data" not in data or not data["data"]:
#         print("No upcoming trains found.")
#         return

#     # Convert times to Eastern Time
#     eastern = pytz.timezone("America/New_York")
#     now = datetime.now(eastern)

#     print("🚉 Upcoming Trains at Lowell Station:\n")

#     for pred in data["data"]:
#         attrs = pred["attributes"]

#         arrival_time = attrs["arrival_time"]
#         departure_time = attrs["departure_time"]
#         direction = "Inbound" if attrs["direction_id"] == 1 else "Outbound"

#         # Skip past trains
#         dep_time = datetime.fromisoformat(departure_time.replace("Z", "+00:00")).astimezone(eastern)

#         if dep_time < now:
#             continue

#         def format_time(t):
#             if not t:
#                 return "—"
#             dt = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(eastern)
#             return dt.strftime("%I:%M %p")

#         route_id = pred["relationships"]["route"]["data"]["id"] if pred["relationships"]["route"]["data"] else "Unknown Route"
#         stop_id = pred["relationships"]["stop"]["data"]["id"]

#         print(f"🛤  Route: {route_id}")
#         print(f"🕑  Direction: {direction}")
#         print(f"🚌  Stop ID: {stop_id}")
#         print(f"⏰  Arrival: {format_time(arrival_time)}")
#         print(f"⏰  Departure: {format_time(departure_time)}")
#         print("-" * 40)

# def main():
#     get_commuter_rail_schedule()
#     lowell_bus()
    

# if __name__ == "__main__":
#     main()


import requests
import time
from datetime import datetime, timedelta
import pytz

# === CONFIG ===
STOP_ID = "590900"  # North & Worthen
BASE_PTA_URL = f"https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/pta/{STOP_ID}"
BASE_HORAIRE_URL = "https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/horaire"
MBTA_URL = (
    "https://api-v3.mbta.com/schedules"
    "?filter[stop]=place-NHRML-0254"
    "&filter[route]=CR-Lowell"
    "&filter[direction_id]=1"
    "&sort=departure_time"
)

# === COLORS ===
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# === HELPERS ===
def format_time(seconds):
    """Convert seconds since midnight to 12-hour AM/PM format."""
    base_time = datetime(2000, 1, 1) + timedelta(seconds=seconds)
    return base_time.strftime("%I:%M %p").lstrip("0")

def parse_time_str(t):
    """Convert 'HH:MM AM/PM' string to datetime today."""
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)
    parsed = datetime.strptime(t, "%I:%M %p").replace(
        year=now.year, month=now.month, day=now.day
    )
    return eastern.localize(parsed)

def fetch_json(url):
    params = {"_tmp": int(time.time() * 1000)}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

# === BUS FUNCTIONS ===
def fetch_initial_schedule():
    data = fetch_json(BASE_PTA_URL)
    horaires_data = []
    liste_horaires = data.get("listeHoraires", [])
    if not liste_horaires:
        return []
    ligne = liste_horaires[0]
    destination = ligne["destination"][0]
    line_id = ligne["idLigne"]
    dest_name = destination["libelle"]
    horaires_list = destination["horaires"]
    for h in horaires_list:
        horaires_data.append({
            "line_id": line_id,
            "destination": dest_name,
            "idHoraire": h["idHoraire"],
            "seconds": h["horaire"],
            "time": format_time(h["horaire"])
        })
    return horaires_data

def fetch_next_schedule(stop_id, id_horaire):
    url = f"{BASE_HORAIRE_URL}/{stop_id}/{id_horaire}/SUIVANT"
    data = fetch_json(url)
    dest = data["destination"][0]
    horaires_next = dest["horaires"][1:]  # skip duplicate
    result = []
    for h in horaires_next:
        result.append({
            "idHoraire": h["idHoraire"],
            "destination": dest["libelle"],
            "seconds": h["horaire"],
            "time": format_time(h["horaire"])
        })
    existe_suivant = dest.get("existeSuivant", False)
    return result, existe_suivant

def get_all_bus_times():
    all_times = []
    initial_schedule = fetch_initial_schedule()
    if not initial_schedule:
        return []

    all_times.extend(initial_schedule)
    if len(initial_schedule) > 1:
        next_id = initial_schedule[1]["idHoraire"]
        while True:
            next_schedule, existe_suivant = fetch_next_schedule(STOP_ID, next_id)
            if not next_schedule:
                break
            all_times.extend(next_schedule)
            if not existe_suivant:
                break
            next_id = next_schedule[-1]["idHoraire"]
    return all_times

# === TRAIN FUNCTIONS ===
def get_commuter_rail_schedule():
    r = requests.get(MBTA_URL)
    data = r.json()
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)
    schedule = []
    for item in data.get("data", []):
        attrs = item["attributes"]
        dep = attrs.get("departure_time")
        if not dep:
            continue
        dep_dt = datetime.fromisoformat(dep.replace("Z", "+00:00")).astimezone(eastern)
        if dep_dt >= now:
            schedule.append(dep_dt)
    return schedule

# === COMPARISON ===
def compare_bus_and_train(bus_times, train_times):
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)

    # Convert bus times to datetime
    bus_datetimes = []
    for b in bus_times:
        dt = parse_time_str(b["time"])
        # Skip buses already departed
        if dt > now:
            bus_datetimes.append(dt)

    print("\n🚍 Bus → 🚆 Train Connections:\n")
    for bus_time in bus_datetimes:
        # Find the next train after this bus
        next_train = next((t for t in train_times if t > bus_time), None)
        if not next_train:
            continue
        diff = (next_train - bus_time).total_seconds() / 60
        color = RESET
        if diff <= 40 and diff > 20:
            color = GREEN
        elif diff <= 60 and diff > 40:
            color = YELLOW
        print(f"{color}🚌 {bus_time.strftime('%I:%M %p')}  →  🚆 {next_train.strftime('%I:%M %p')}  ({int(diff)} min apart){RESET}")
    return bus_datetimes

# === MAIN ===
def main():
    print("Fetching schedules...\n")
    bus_times = get_all_bus_times()
    train_times = get_commuter_rail_schedule()

    if not bus_times:
        print("⚠️ No bus schedule found.")
        return
    if not train_times:
        print("⚠️ No train schedule found.")
        return

    future_buses = compare_bus_and_train(bus_times, train_times)

    # === Print full remaining schedules ===
    eastern = pytz.timezone("America/New_York")
    now = datetime.now(eastern)

    print("\n🕐 Remaining Bus Departures Today:")
    for b in future_buses:
        print(f"   🚌 {b.strftime('%I:%M %p')}")

    print("\n🚆 Remaining Train Departures Today:")
    for t in train_times:
        if t > now:
            print(f"   🚆 {t.strftime('%I:%M %p')}")
    

if __name__ == "__main__":
    while True:
        print("\n==============================")
        print(f"⏰ Running update at {datetime.now().strftime('%I:%M %p')}")
        print("==============================\n")
        main()

        # Countdown timer (10 minutes)
        wait_time = 600  # seconds
        for remaining in range(wait_time, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r💤 Next update in {mins:02d}:{secs:02d}", end="", flush=True)
            time.sleep(1)
        print("\n")


    

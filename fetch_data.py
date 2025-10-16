# fetch_data.py
import requests
from datetime import datetime, timedelta
import pytz
import time

# --- CONFIG ---
STOP_ID = "590900"
BASE_PTA_URL = f"https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/pta/{STOP_ID}"
BASE_HORAIRE_URL = "https://swiv.lrta.cadavl.com/SWIV/LRTA/proxy/restWS/horaires/horaire"
MBTA_URL = (
    "https://api-v3.mbta.com/schedules"
    "?filter[stop]=place-NHRML-0254"
    "&filter[route]=CR-Lowell"
    "&filter[direction_id]=1"
    "&sort=departure_time"
)

# --- HELPERS ---
def format_time(seconds):
    base_time = datetime(2000, 1, 1) + timedelta(seconds=seconds)
    return base_time.strftime("%I:%M %p").lstrip("0")

def parse_time_str(t):
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

# --- BUS FUNCTIONS ---
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
            "idHoraire": h["idHoraire"],
            "destination": dest_name,
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

# --- TRAIN FUNCTIONS ---
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

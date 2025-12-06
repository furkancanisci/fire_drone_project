import folium
import json
from pathlib import Path

def generate_map():
    data_path = Path(__file__).resolve().parent / "drones.json"

    # JSON dosyasını oku
    if not data_path.exists():
        print("drones.json bulunamadı.")
        return

    with open(data_path, 'r') as f:
        drone_positions = json.load(f)

    # Haritayı başlat (İstanbul odaklı)
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=13, control_scale=True)

    # Drone'ları ekle
    for drone_id, pos in drone_positions.items():
        folium.CircleMarker(
            location=[pos['latitude'], pos['longitude']],
            radius=10,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            popup=f"Drone {drone_id}"
        ).add_to(m)


    target_latitude = 41.1902
    target_longitude = 28.9982

    # Yangın bölgesi dairesi
    folium.Circle(
        location=[target_latitude, target_longitude],
        radius=700,  # metre cinsinden
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.3,
        popup="Yangın Bölgesi"
    ).add_to(m)

    # Haritayı kaydet
    map_path = Path(__file__).resolve().parent / "drone_map.html"
    m.save(str(map_path))
    print("Harita güncellendi.")

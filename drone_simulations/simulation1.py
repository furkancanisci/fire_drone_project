import socketio
import asyncio
import random
import json
from pathlib import Path

sio = socketio.AsyncClient()

# Yangın bölgesi koordinatları
FIRE_LAT = 41.1902
FIRE_LON = 28.9982

# Başlangıç pozisyonları (farklı konumlardan başlasınlar)
DRONE_START_POSITIONS = [
    (41.01, 28.97),
    (41.02, 28.96),
    (41.00, 28.98),
    (41.03, 28.95),
    (40.99, 28.99)
]

def move_towards_fire(current_lat, current_lon, step_size=0.002):
    """Drone'u yangın bölgesine doğru hareket ettir"""
    lat_diff = FIRE_LAT - current_lat
    lon_diff = FIRE_LON - current_lon
    
    # Adım boyutunu sınırla
    if abs(lat_diff) > step_size:
        lat_diff = step_size if lat_diff > 0 else -step_size
    if abs(lon_diff) > step_size:
        lon_diff = step_size if lon_diff > 0 else -step_size
    
    return current_lat + lat_diff, current_lon + lon_diff

async def main():
    await sio.connect('http://localhost:8000')
    
    # Birden fazla drone için konumları başlat
    drone_positions = {}
    for i, (start_lat, start_lon) in enumerate(DRONE_START_POSITIONS):
        drone_positions[f"drone_{i+1}"] = {
            "latitude": start_lat + random.uniform(-0.01, 0.01),
            "longitude": start_lon + random.uniform(-0.01, 0.01)
        }
    
    while True:
        # Her drone'un konumunu güncelle
        for drone_id, pos in drone_positions.items():
            # Yangın bölgesine doğru hareket et
            new_lat, new_lon = move_towards_fire(pos['latitude'], pos['longitude'])
            pos['latitude'] = new_lat
            pos['longitude'] = new_lon
            
            # WebSocket üzerinden konumu gönder
            await sio.emit('drone_position', {
                'drone_id': drone_id,
                'latitude': new_lat,
                'longitude': new_lon
            })
            
            print(f"{drone_id} Konum Gönderildi: ({new_lat:.6f}, {new_lon:.6f})")
        
        # JSON dosyasına da yaz (map generator için)
        data_path = Path(__file__).resolve().parent.parent / "control_center" / "maps" / "drones.json"
        with open(data_path, 'w') as f:
            json.dump(drone_positions, f, indent=2)
        
        await asyncio.sleep(2)  # 2 saniyede bir güncelle

asyncio.run(main())

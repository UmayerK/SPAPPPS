import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const Map = () => {
    useEffect(() => {
        // Initialize the map
        const map = L.map('map').setView([0, 0], 3); // Centered on the Moon

        // Add a tile layer (Moon Map)
        L.tileLayer('https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-moon-basemap-v0-1/all/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenPlanetary'
        }).addTo(map);

        // Optional: Add a marker on the map
        const marker = L.marker([0, 0]).addTo(map)
            .bindPopup('Center of the Moon')
            .openPopup();

        // Cleanup on unmount
        return () => {
            map.remove();
        };
    }, []);

    return <div id="map" style={{ height: '100vh', width: '100%' }} />;
};

export default Map;

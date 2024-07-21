function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: { lat: 34.823278, lng: 135.383083 }
    });

    let currentInfoWindow = null;

    function getAddress(lat, lng, callback) {
        const geocoder = new google.maps.Geocoder();
        const latlng = { lat: parseFloat(lat), lng: parseFloat(lng) };
        geocoder.geocode({ location: latlng }, (results, status) => {
            if (status === 'OK') {
                if (results[0]) {
                    callback(results[0].formatted_address);
                } else {
                    callback('住所が見つかりませんでした');
                }
            } else {
                callback('Geocoder failed due to: ' + status);
            }
        });
    }

    function loadMarkers() {
        fetch('/get_markers/')
            .then(response => response.json())
            .then(data => {
                data.forEach(marker => {
                    const mapMarker = new google.maps.Marker({
                        position: { lat: marker.lat, lng: marker.lng },
                        map: map,
                        draggable: true
                    });

                    getAddress(marker.lat, marker.lng, (address) => {
                        const infoWindowContent = `
                            <div>
                                <p>マーカーID: ${marker.id}</p>
                                <p>住所: ${address}</p>
                                <button onclick="window.location.href='/marker_detail/${marker.id}/'">詳細</button>
                            </div>
                        `;
                        const infoWindow = new google.maps.InfoWindow({
                            content: infoWindowContent
                        });

                        // マウスオーバーとタッチイベントでInfoWindowを表示するリスナーを追加
                        mapMarker.addListener('mouseover', function() {
                            if (currentInfoWindow) {
                                currentInfoWindow.close();
                            }
                            infoWindow.open(map, mapMarker);
                            currentInfoWindow = infoWindow;
                        });

                        mapMarker.addListener('click', function() {
                            if (currentInfoWindow) {
                                currentInfoWindow.close();
                            }
                            infoWindow.open(map, mapMarker);
                            currentInfoWindow = infoWindow;
                        });

                        mapMarker.addListener('rightclick', function() {
                            if (confirm('このマーカーを削除しますか？')) {
                                fetch('/delete_marker/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken')
                                    },
                                    body: JSON.stringify({ id: marker.id })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.success) {
                                        mapMarker.setMap(null);
                                        if (currentInfoWindow === infoWindow) {
                                            currentInfoWindow.close();
                                            currentInfoWindow = null;
                                        }
                                    } else {
                                        alert('マーカーの削除に失敗しました: ' + data.error);
                                    }
                                });
                            }
                        });

                        mapMarker.addListener('dragend', function(event) {
                            const newLat = event.latLng.lat();
                            const newLng = event.latLng.lng();

                            fetch('/update_marker/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken')
                                },
                                body: JSON.stringify({ id: marker.id, lat: newLat, lng: newLng })
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (!data.success) {
                                    alert('マーカーの位置更新に失敗しました: ' + data.error);
                                } else {
                                    getAddress(newLat, newLng, (newAddress) => {
                                        infoWindow.setContent(`
                                            <div>
                                                <p>マーカーID: ${marker.id}</p>
                                                <p>住所: ${newAddress}</p>
                                                <button onclick="window.location.href='/marker_detail/${marker.id}/'">詳細</button>
                                            </div>
                                        `);
                                    });
                                }
                            });
                        });
                    });
                });
            });
    }

    loadMarkers();

    map.addListener('click', function(event) {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();

        fetch('/add_marker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ lat: lat, lng: lng })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadMarkers();
            } else {
                alert('マーカーの追加に失敗しました: ' + data.error);
            }
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
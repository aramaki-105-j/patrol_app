function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: { lat: 34.823278, lng: 135.383083 }
    });

    let currentInfoWindow = null;

    // Geocoding APIを使用して住所を取得する関数
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

    // マーカーを読み込む関数
    function loadMarkers() {
        fetch('/get_markers/')
            .then(response => response.json())
            .then(data => {
                data.forEach(marker => {
                    const mapMarker = new google.maps.Marker({
                        position: { lat: marker.lat, lng: marker.lng },
                        map: map,
                        draggable: true // ドラッグを有効にする
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

                        // マウスオーバーでInfoWindowを表示するリスナーを追加
                        mapMarker.addListener('mouseover', function() {
                            if (currentInfoWindow) {
                                currentInfoWindow.close();
                            }
                            infoWindow.open(map, mapMarker);
                            currentInfoWindow = infoWindow;
                        });

                        // 右クリックでマーカーを削除するリスナーを追加
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

                        // ドラッグ終了時にマーカーの位置を更新するリスナーを追加
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

    // 初期にマーカーを読み込む
    loadMarkers();

    // マップクリック時にマーカーを追加
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
                // 新しいマーカーを追加した後にマーカーを再読み込み
                loadMarkers();
            } else {
                alert('マーカーの追加に失敗しました: ' + data.error);
            }
        });
    });
}

// クッキーからCSRFトークンを取得する関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
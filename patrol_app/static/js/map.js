function initMap() {
  var location = {lat: 34.823278, lng: 135.383083};  // 長尾小学校の緯度と経度
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 16,
      center: location
  });

  // サーバーから既存のマーカーを取得します
  fetch('/get_markers/')
      .then(response => response.json())
      .then(data => {
          data.forEach(markerData => {
              var marker = new google.maps.Marker({
                  position: {lat: markerData.lat, lng: markerData.lng},
                  map: map,
                  draggable: true  // ドラッグを有効にする
              });

              // マーカーにクリックイベントを追加する
              marker.addListener('click', function() {
                  window.location.href = '/review/' + markerData.lat + ',' + markerData.lng;
              });

              // マーカーの位置を更新するためにドラッグイベントを追加します
              marker.addListener('dragend', function(event) {
                  updateMarkerPosition(event.latLng, markerData.id);
              });
          });
      });

  // クリックイベントをマップに追加する
  map.addListener('click', function(event) {
      placeMarker(event.latLng, map);
      saveMarker(event.latLng);  // マーカーをデータベースに保存します
  });
}

function placeMarker(location, map) {
  var marker = new google.maps.Marker({
      position: location,
      map: map,
      draggable: true  // ドラッグを有効にする
  });

  // マーカーにクリックイベントを追加する
  marker.addListener('click', function() {
      window.location.href = '/review/' + location.lat() + ',' + location.lng();
  });

  // マーカーの位置を更新するためにドラッグイベントを追加します
  marker.addListener('dragend', function(event) {
      updateMarkerPosition(event.latLng, marker.id);
  });
}

function saveMarker(location) {
   // メタタグからCSRFトークンを取得する
  var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch('/add_marker/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken  // ヘッダーにCSRFトークンを含めます
      },
      body: JSON.stringify({lat: location.lat(), lng: location.lng()})
  }).then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Failed to save marker');
        }
    });
}

function updateMarkerPosition(location, markerId) {
  // メタタグからCSRFトークンを取得する
  var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch('/update_marker/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken  // ヘッダーにCSRFトークンを含めます
      },
      body: JSON.stringify({id: markerId, lat: location.lat(), lng: location.lng()})
  }).then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Failed to update marker position');
        }
    });
}
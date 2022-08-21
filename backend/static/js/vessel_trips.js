// Initialize and add the map
function initMap() {
  const center_map = { lat: 0, lng: 0 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 2,
    center: center_map,
  });

  $.ajax({
        url: "http://127.0.0.1:5000/vessel_positions",
        contentType: "application/json",
        dataType: 'json',
        success: function(result){
            for (var element of result) {
                var position = { lat: element.latitude, lng: element.longitude };
                var marker = new google.maps.Marker({
                    position: position,
                    map: map,
                    description: "test",
                    id: element.vessel_id
              });
            }
        }
    })
}

function searchVessel() {
    var vessel_id = document.getElementById("vessel_identifiant").value;


}

function postData() {
    var vessel_id = document.getElementById("vessel_id").value;
    var received_time_utc = document.getElementById("received_time_utc").value;
    var latitude = document.getElementById("latitude").value;
    var longitude = document.getElementById("longitude").value;


}

function uploadDataCsv() {
    var upload_csv = document.getElementById("upload_csv").value;


}

window.initMap = initMap;
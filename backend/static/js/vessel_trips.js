// Initialize and add the map
function initMap(vessel_id) {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 2,
    center: { lat: 0, lng: 0 },
  });

  if (vessel_id === undefined) {
    url = "http://127.0.0.1:5000/vessel_positions"
  }
  else {
    url = "http://127.0.0.1:5000/vessel_positions/" + vessel_id
  }

  $.ajax({
        url: url,
        contentType: "application/json",
        dataType: 'json',
        success: function(result){
            var vessel_positions = {};
            for (var element of result) {
                if (!vessel_positions[element.vessel_id]) {
                    vessel_positions[element.vessel_id] = [];
                }
                vessel_positions[element.vessel_id].push(element);
            }

            var infowindow = new google.maps.InfoWindow();

            for (vessel_position in vessel_positions) {
                for (vessel_position_entry in vessel_positions[vessel_position]) {
                    var position = { lat: parseFloat(vessel_positions[vessel_position][vessel_position_entry].latitude),
                                    lng: parseFloat(vessel_positions[vessel_position][vessel_position_entry].longitude) };

                    var marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        draggable: false,
                        data: "Vessel ID: " + String(vessel_positions[vessel_position][vessel_position_entry].vessel_id) +
                        "\n Received time UTC: " + String(vessel_positions[vessel_position][vessel_position_entry].received_time_utc),
                    });

                    google.maps.event.addListener(marker, 'click', (function (marker) {
                        return function () {
                            infowindow.setContent(marker.data);
                            infowindow.open(map, marker);
                        }
                    })(marker));

                }
            }
        }
    })
}

function searchVessel() {
    var vessel_id = document.getElementById("vessel_identifiant").value;
    if (vessel_id != "") {
        initMap(vessel_id);
    }
    else {
        initMap();
    }
}

function postData() {
    var vessel_id = document.getElementById("vessel_id").value;
    var received_time_utc = document.getElementById("received_time_utc").value;
    var latitude = document.getElementById("latitude").value;
    var longitude = document.getElementById("longitude").value;

    $.ajax({
        url: "http://127.0.0.1:5000/vessel_positions/add_vessel_position",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"vessel_id": vessel_id, "received_time_utc": received_time_utc,
                "latitude": latitude, "longitude": longitude}),

        success: function(result, textStatus, xhr){
            if (xhr.status == 201) {
                alert('data added');
            }
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}

function uploadDataCsv() {
    var url = "http://127.0.0.1:5000/vessel_positions/upload_vessel_position_csv";

    let csvfile = document.getElementById("file_upload").files[0];

	const formData = new FormData();
    formData.append("csvfile", csvfile, csvfile.name);

    $.ajax({
        url: url,
        type: "POST",
        data:formData,
        processData: false,
        contentType: false,
        success: function(result, textStatus, xhr) {
            alert(result.message);
        }
    })
}

window.initMap = initMap;
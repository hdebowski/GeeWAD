function updateBands() {
    var satellite = document.getElementById('satellite').value;
    updateBandSelect('band1', satellite);
    updateBandSelect('band2', satellite);
    updateBandSelect('band3', satellite);
    var bandsAndDatesSection = document.getElementById('hiding_fields');
    if (satellite === 'Sentinel2' || satellite === 'Landsat8') {
        bandsAndDatesSection.style.display = 'block';
    } else {
        bandsAndDatesSection.style.display = 'none';
    }
}

function updateBandSelect(bandSelectId, satellite) {
    var bandsSelect = document.getElementById(bandSelectId);
    bandsSelect.innerHTML = '';
    var defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.text = "Choose band";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    bandsSelect.appendChild(defaultOption);

    var bands = [];
    if (satellite === 'Sentinel2') {
        bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'];
    } else if (satellite === 'Landsat8') {
        bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11'];
    }

    bands.forEach(function(band) {
    var option = document.createElement('option');
    option.value = band;
    option.text = band;
    bandsSelect.appendChild(option);
    });
}

window.alert = function(message) {
    sendDataToServer(message);
};

function sendDataToServer(message) {
    fetch('/capture-alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ alertMessage: message })
    })
    .then(response => response.json())
    .then(data => console.log('Alert data sent to the server.'))
    .catch(error => console.error('Error:', error));
};

function resetAnalysis() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/reset-analysis", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload();
        }
    };

    xhr.send();
}

function updateBands2() {
    var selectedValue = document.getElementById('index').value;
    var bandsDiv = document.getElementById('bands');

    if(selectedValue && selectedValue !== "" && selectedValue !== "Brak") {
        bandsDiv.style.display = 'none';
    } else {
        bandsDiv.style.display = 'block';
    }
}

function reaload_web(){
    window.location.reload();
}

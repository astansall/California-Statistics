var satellitemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.satellite",
    accessToken: API_KEY
});

var grayscalemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
});

var outdoorsmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.outdoors",
    accessToken: API_KEY
});

var baseMaps = {
    "Satellite": satellitemap,
    "Grayscale": grayscalemap,
    "Outdoors": outdoorsmap
};

var layers = {
    FAULT_LINES: new L.LayerGroup(),
    EARTHQUAKES: new L.LayerGroup()
};

var myMap = L.map("map", {
    center: [39.8283, -98.5795],
    zoom: 5,
    maxBounds: L.latLngBounds([90, -180], [-90, 180]),
    maxBoundsViscosity: 1,
    layers: [
        grayscalemap,
        layers.FAULT_LINES,
        layers.EARTHQUAKES
    ]
});

var overlays = {
    "Fault Lines": layers.FAULT_LINES,
    "Earthquakes": layers.EARTHQUAKES
};

L.control.layers(baseMaps, overlays, {
    collapsed: false
}).addTo(myMap);

d3.json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson", function (quakeData) {
    d3.json("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json", function (platesData) {

        var platefeatures = platesData.features;

        for (var i = 0; i < platefeatures.length; i++) {
            var tectonicplates = L.geoJson(platefeatures[i].geometry, {
                fillOpacity: 0,
                color: "darkslategray"
            })
            tectonicplates.addTo(layers.FAULT_LINES)
        }

        var quakefeatures = quakeData.features;
        
        for (var i = 0; i < quakefeatures.length; i++) {

            var magstyle = quakefeatures[i].properties.mag;

            function magnitudeColor(mag) {
                if (mag > 5) {
                    return "#b30000"
                }
                else if (mag > 4) {
                    return "#e34a33"
                }
                else if (mag > 3) {
                    return "#fc8d59"
                }
                else if (mag > 2) {
                    return "#fdbb84"
                }
                else if (mag > 1) {
                    return "#fdd49e"
                }
                else {
                    return "#fef0d9"
                }
            }

            var quakecoords = quakefeatures[i].geometry.coordinates;

            var earthquake = L.circleMarker([quakecoords[1], quakecoords[0]], {
                radius: (magstyle * 5),
                color: magnitudeColor(magstyle),
                fillColor: magnitudeColor(magstyle),
                fillOpacity: 1
            })
            earthquake.addTo(layers.EARTHQUAKES)
        }

        var legend = L.control({ position: 'bottomright' });

        legend.onAdd = function (map) {

            var div = L.DomUtil.create('div', 'info legend'),
                grades = [0, 1, 2, 3, 4, 5],
                labels = [];

            for (var i = 0; i < grades.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + magnitudeColor(grades[i] + 1) + '"></i> ' +
                    grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
            }

            return div;
        };

        legend.addTo(myMap);

    })
})


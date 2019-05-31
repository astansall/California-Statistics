// connect zip code to input variables. creates combined json
function combineJson(zipVariable) {
  for (var i = 0; i < zipVariable.length; i++) {
    if (zipfeatures[i].properties.ZCTA5CE10 == zipVariable) {
      // make sure links are correct
      var combined = Object.assign({}, zipfeatures[i].properties, zipVariable);
      console.log(combined);
    }
  }
}

// function to build map
function buildMap(variable) {
  var grayscalemap = L.tileLayer(
    "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox.light",
      accessToken: API_KEY
    }
  );

  var baseMaps = {
    Grayscale: grayscalemap
  };

  var layers = {
    ZIP_BOUNDS: new L.LayerGroup(),
    INPUT_VARIABLE: new L.LayerGroup()
  };

  var myMap = L.map("map", {
    center: [32.7157, -117.1611],
    zoom: 10,
    maxBounds: L.latLngBounds([90, -180], [-90, 180]),
    maxBoundsViscosity: 1,
    layers: [grayscalemap, layers.ZIP_BOUNDS, layers.INPUT_VARIABLE]
  });

  var overlays = {
    "Zip Code Boundaries": layers.ZIP_BOUNDS,
    Variable: layers.INPUT_VARIABLE
  };

  L.control
    .layers(baseMaps, overlays, {
      collapsed: false
    })
    .addTo(myMap);

  d3.json(
    "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json",
    function(zipData) {
      var zipfeatures = zipData.features;

      for (var i = 0; i < zipfeatures.length; i++) {
        // console.log(zipfeatures[i].properties.ZCTA5CE10);
        var zipbounds = L.geoJson(zipfeatures[i].geometry, {
          fillOpacity: 0,
          color: "black",
          weight: 1
        });
        zipbounds.addTo(layers.ZIP_BOUNDS);
      }
    }
  );
}

// initial function that will run on load
function init() {
  // input correct html tag
  var selector = d3.select("html tag");

  // update path
  d3.json("/path").then(variableList => {
    variableList.forEach(variable => {
      selector
        .append("option")
        .text(variable)
        .property("value", variable);
    });

    //input initial variable
    const firstVariable = "initial variable";
    buildMap(firstVariable);
  });
}

// changes choropleth when variable is updated
function optionChanged(newVariable) {
  buildCharts(newVariable);
}

// init();

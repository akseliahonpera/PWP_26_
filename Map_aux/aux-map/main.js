
import './style.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';

import Feature from 'ol/Feature.js';
import Overlay from 'ol/Overlay.js';
import Point from 'ol/geom/Point.js';
import VectorLayer from 'ol/layer/Vector.js';
import OGCMapTile from 'ol/source/OGCMapTile.js';
import VectorSource from 'ol/source/Vector.js';
import Icon from 'ol/style/Icon.js';
import Style from 'ol/style/Style.js';
import {fromLonLat} from 'ol/proj.js';

//default values
let markerLonLat = [];
const defaultLong = 25.4625; 
const defaultLat = 65.02914524;
const params = new URLSearchParams(window.location.search);

let lat = parseFloat(params.get('lat') ?? defaultLat);
let lon = parseFloat(params.get('lon')?? defaultLong);
let label = String(params.get('label') ?? "No info");
markerLonLat = [lon,lat]
//dynamic location for the map center and marker, set as [longitude,latitude]


const pointData = label

const markerWebMercator = fromLonLat(markerLonLat);


const iconFeature = new Feature({
  geometry: new Point(markerWebMercator),
  name: pointData
});


// set iconstyle and anchoring
const iconStyle = new Style({
  image: new Icon({
    scale: 0.1,
    anchor: [0.5,1 ],
    anchorXUnits: 'fraction',
    anchorYUnits: 'fraction',
    src: 'data/icon.png',
  }),
});

iconFeature.setStyle(iconStyle);

const vectorSource = new VectorSource({
  features: [iconFeature],
});

const vectorLayer = new VectorLayer({
  source: vectorSource,
});

const rasterLayer = new TileLayer({
    source: new OSM()
});
//map position

const finlandWebMercator = fromLonLat(markerLonLat);

const map = new Map({
  layers: [rasterLayer, vectorLayer],
  target: 'map',
  view: new View({
    center: finlandWebMercator,
    zoom: 12,
  }),
});


const element = document.getElementById('popup');

const popup = new Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
});
map.addOverlay(popup);

let popover;
function disposePopover() {
  if (popover) {
    popover.dispose();
    popover = undefined;
  }
}
// display popup on click
map.on('click', function (evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });
  disposePopover();
  if (!feature) {
    return;
  }
  popup.setPosition(evt.coordinate);
  popover = new bootstrap.Popover(element, {
    placement: 'top',
    html: true,
    content: feature.get('name'),
  });
  popover.show();
});

// change mouse cursor when over marker
map.on('pointermove', function (e) {
  const hit = map.hasFeatureAtPixel(e.pixel);
  map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});
// Close the popup when the map is moved
map.on('movestart', disposePopover);
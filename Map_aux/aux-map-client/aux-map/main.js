import 'ol/ol.css' 
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
import iconUrl from './data/icon.png';
import iconUrlPrimary from './data/icon_primary.png';
//default values


async function getJobList(){
  const url = "http://localhost:3000/mapaux";
  try {
    const response = await fetch(url);
    if(!response.ok){
      throw new Error(`Response status: ${response.status}`);
    }
    const result = await response.json();
    console.log(result);
    return result;
  } catch (error) {
    console.error(error.message);
  }
}

//dynamic location for the map center and marker, set as [longitude,latitude]
////////////////////////////////////////////////////////////////////////
var map = null;
var default_job_name = "Job name not found.";
var default_category = "Category not found.";
var job_name = "";
var category = "";

////////////////////////////////////////////////////////////////////////
function getParamsFromWindow(){
  const params = new URLSearchParams(window.location.search);
  job_name = String(params.get('job_name') ?? default_job_name);
  category = String(params.get('category')?? default_category);
}

function drawMarkers(job_list){
  let iconfeatureList = [];
  let markerList = [];
  let primary_lon_lat = [];
  for(let i=0;i<job_list.length;i++){//

    if(category!=job_list[i]["category"]){
      continue;
    }

    markerList.push({"job_name":job_list[i]["job_name"],
                      "longitude":job_list[i]["longitude"],
                      "latitude":job_list[i]["latitude"],
                      "category":job_list[i]["category"]});

    let pointData = job_list[i]["job_name"]+" || "+job_list[i]["category"];
    let markerMercator = fromLonLat(
      [job_list[i]["longitude"],job_list[i]["latitude"]]
    );
    let iconFeature = new Feature({
      geometry: new Point(
        markerMercator),
        name: pointData
      });

    if(job_name===job_list[i]["job_name"]){
        primary_lon_lat = [job_list[i]["longitude"],job_list[i]["latitude"]];
        const iconStyle = new Style({
        image: new Icon({
        scale: 0.1,
        anchor: [0.5,1 ],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        src: iconUrlPrimary,
      }),
    });
      iconFeature.setStyle(iconStyle);
      iconfeatureList.push(iconFeature);//
    }else{

    const iconStyle = new Style({
      image: new Icon({
        scale: 0.1,
        anchor: [0.5,1 ],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        src: iconUrl,
      }),
    });
    iconFeature.setStyle(iconStyle);
    iconfeatureList.push(iconFeature);//
  }

  }
  const vectorSource = new VectorSource({
      features: iconfeatureList,
    });
  const vectorLayer = new VectorLayer({
      source: vectorSource,
    });

  const rasterLayer = new TileLayer({
      source: new OSM()
  });
  //map position
  //get first position from the list
  const finlandWebMercator = fromLonLat(primary_lon_lat);
  
  map = new Map({
    layers: [rasterLayer, vectorLayer],
    target: 'map',
    view: new View({
      center: finlandWebMercator,
      zoom: 11,
    }),
  });
}

var job_list = await getJobList();
console.log(typeof(job_list));
getParamsFromWindow();
drawMarkers(job_list);
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
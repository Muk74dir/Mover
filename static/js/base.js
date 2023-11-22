
async function initMap(newPosition) {
  const position = { lat: newPosition.lnt, lng: newPosition.lng };
  console.log(position);
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  let map = new Map(document.getElementById("map"), {
    zoom: 15,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Uluru
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "My Location",
  });
}

const config = {
    enableHighAccuracy: true,
    timeout: 10000,
};

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
      (position) => {
          const newPosition = successFunction(position);
          initMap(newPosition);
      },
      errorFunction,
      config
  );
} else {
  console.log("Geolocation is not supported by this browser.");
}

function errorFunction() {
  console.log("Unable to retrieve your location.");
}

function successFunction(position) {
  let lant = position.coords.latitude;
  let long = position.coords.longitude;
  return {lnt: lant, lng: long};
}

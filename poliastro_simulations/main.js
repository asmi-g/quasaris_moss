const viewer = new Cesium.Viewer('cesiumContainer', {
  shouldAnimate: true
});

// Load CZML
Cesium.CzmlDataSource.load('orbit.czml').then(function (czmlDataSource) {
  viewer.dataSources.add(czmlDataSource);
  viewer.clock.shouldAnimate = true;

  // Zoom to entity
  const entity = czmlDataSource.entities.getById('satellite');
  if (entity) {
    //viewer.trackedEntity = entity; // Follow satellite
    viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(0.0, 0.0, 20000000.0) // [lon, lat, height]
    });

  }
}).catch(function (error) {
  console.error("Failed to load CZML:", error);
});

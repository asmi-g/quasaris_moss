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
  const axisLength = 500000; // Shorter line for visualization

  function addAxis(name, unitVector, color) {
    viewer.entities.add({
      name,
      position: new Cesium.CallbackProperty(() => {
        return entity.position.getValue(viewer.clock.currentTime);
      }, false),
      orientation: new Cesium.CallbackProperty(() => {
        return entity.orientation.getValue(viewer.clock.currentTime);
      }, false),
      polyline: {
        positions: new Cesium.CallbackProperty(() => {
          const position = entity.position.getValue(viewer.clock.currentTime);
          const orientation = entity.orientation.getValue(viewer.clock.currentTime);
          if (!position || !orientation) return null;

          const matrix = Cesium.Matrix3.fromQuaternion(orientation);
          const direction = Cesium.Matrix3.multiplyByVector(matrix, unitVector, new Cesium.Cartesian3());
          const end = Cesium.Cartesian3.add(position,
            Cesium.Cartesian3.multiplyByScalar(direction, axisLength, new Cesium.Cartesian3()),
            new Cesium.Cartesian3()
          );

          return [position, end];
        }, false),
        width: 3,
        material: color
      }
    });
  }

  // Add body axes
  addAxis("X Axis", Cesium.Cartesian3.UNIT_X, Cesium.Color.RED);
  addAxis("Y Axis", Cesium.Cartesian3.UNIT_Y, Cesium.Color.GREEN);
  addAxis("Z Axis", Cesium.Cartesian3.UNIT_Z, Cesium.Color.BLUE);
}).catch(function (error) {
  console.error("Failed to load CZML:", error);
});

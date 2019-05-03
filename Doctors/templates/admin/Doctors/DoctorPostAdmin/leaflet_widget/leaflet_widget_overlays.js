<script type="text/javascript">
  window.addEventListener("map:init", function (event) {
    var map = event.detail.map; // Get reference to map

    var geocoder = L.Control.geocoder({
        defaultMarkGeocode: false
    })
    .on('markgeocode', function(e) {
        var bbox = e.geocode.bbox;
        var poly = L.polygon([
             bbox.getSouthEast(),
             bbox.getNorthEast(),
             bbox.getNorthWest(),
             bbox.getSouthWest()
        ]).addTo(map);
        map.fitBounds(poly.getBounds());
    })
    .addTo(map);

});
</script>
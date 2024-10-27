import gpxpy

# Load and parse the GPX file
with open('path_to_your_data_file.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract waypoints, tracks, etc.
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print(f"Point at ({point.latitude},{point.longitude}) -> Elevation: {point.elevation}")

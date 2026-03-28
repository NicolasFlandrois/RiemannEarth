from dataclasses import dataclass
from typing import Tuple

from numpy import arcsin, atan2, clip, cos, deg2rad, inf, isinf, rad2deg, sin, sqrt, square
from tabulate import tabulate


@dataclass
class City:
    name: str
    longitude: float
    latitude: float
    # expected_complex: complex | None


def convert_gps_to_riemann(longitude: float, latitude: float) -> complex:
    """
    Projects Geodetic Coordinates (Lon, Lat) to the Complex Plane via
    Standard Stereographic Projection from the North Pole.

    Conventions:
    - Projection Point: North Pole (90° N)
    - Origin (0+0j): South Pole (-90° S)
    - Prime Meridian (0° Lon): Positive Real Axis
    - 90° East Longitude: Positive Imaginary Axis
    """
    lat_rad = deg2rad(latitude)
    long_rad = deg2rad(longitude)

    denominator = 1 - sin(lat_rad)
    if denominator == 0:
        return complex(inf, inf)

    magnitude = cos(lat_rad) / denominator

    imag = magnitude * sin(long_rad)
    real = magnitude * cos(long_rad)

    return complex(real, imag)


def translate_from_riemann_to_gps(imaginary_projection: complex) -> Tuple[float, float]:
    """
    Inverse the Geodetic Coordinates (Lon, Lat) projection to the Complex Plane via
    Standard Stereographic Projection from the North Pole.
    Translating back from a complex number to a GPS coordinates.

    Conventions:
    - Projection Point: North Pole (90° N)
    - Origin (0+0j): South Pole (-90° S)
    - Prime Meridian (0° Lon): Positive Real Axis
    - 90° East Longitude: Positive Imaginary Axis
    """
    x = imaginary_projection.real
    y = imaginary_projection.imag

    magnitude_sqr = square(x) + square(y)
    magnitude = sqrt(magnitude_sqr)

    if magnitude < 1e-5:
        # South Pole
        return 0.0, -90.0
    if isinf(magnitude):
        # North Pole
        return 0.0, 90.0

    sin_lat = (magnitude_sqr - 1) / (magnitude_sqr + 1)
    lat_rad = arcsin(clip(sin_lat, -1.0, 1.0))

    # long_rad = atan2(x, -y)
    long_rad = atan2(y, x)

    return rad2deg(long_rad), rad2deg(lat_rad)


def verify_round_trip(city: City) -> bool:
    """Verifies that translate(convert(city)) == city within tolerance."""
    z = convert_gps_to_riemann(city.longitude, city.latitude)
    lon_rt, lat_rt = translate_from_riemann_to_gps(z)

    # Normalize longitude difference to [-180, 180]
    d_lon = abs(lon_rt - city.longitude)
    if d_lon > 180:
        d_lon = 360 - d_lon
    d_lat = abs(lat_rt - city.latitude)

    tolerance = 1e-6
    is_valid = (d_lon < tolerance) and (d_lat < tolerance)

    return is_valid


def main():
    # Streographic projection
    # Riemann Sphere
    # Applied to location on the world globe
    cities = [
        City(name="shanghai", longitude=121.458060, latitude=31.222220),
        City(name="los angeles", longitude=-118.242766, latitude=34.0536909),
        City(name="tokyo", longitude=139.7638947, latitude=35.67686),
        City(name="new york city", longitude=-74.005966, latitude=40.714272),
        City(name="london", longitude=-0.09184, latitude=51.512791),
        City(name="dubai", longitude=55.304722, latitude=22.258169),
        City(name="paris", longitude=2.3586, latitude=48.853401),
        City(name="sydney", longitude=151.208435, latitude=-33.867779),
        City(name="helsinki", longitude=24.93545, latitude=60.16952),
        City(name="Reykjavík", longitude=-21.895411, latitude=64.135483),
        City(name="buenos aires", longitude=-60.0, latitude=-36.0),
        City(name="auckland", longitude=174.766663, latitude=-36.866669),
        # Edge cases
        City(name="North Pole", longitude=0.0, latitude=90.0),  # Near North pole
        City(name="South Pole", longitude=0.0, latitude=-90.0),  # Near South pole
        City(name="greenwich", longitude=0.0, latitude=51.0),
        City(name="antipode of greenwich (shy south of new zealand)", longitude=180.0, latitude=51.0),
        City(name='"NULL ISLAND" (O°, 0°)', longitude=0.0, latitude=0.0),
        City(name="Equator & 90°E Intersection", longitude=90.0, latitude=0.0),
        City(name="Date Line Equator Point (Antipode of Null Island)", longitude=180.0, latitude=0.0),
        City(name="Equator & 90°W Intersection", longitude=90.0, latitude=0.0),
    ]
    table_data = []
    headers = ["City", "Input (Lon, Lat)", "Complex (z)", "Recovered", "Status"]

    all_passed = True
    for city in cities:
        z = convert_gps_to_riemann(city.longitude, city.latitude)
        lon_rt, lat_rt = translate_from_riemann_to_gps(z)

        passed = verify_round_trip(city)
        status = "✓ PASS" if passed else "✗ FAIL"
        if not passed:
            all_passed = False

        # Format output
        if isinf(z.real):
            z_str = "∞ (Infinity)"
        else:
            z_str = f"{z.real:.4f}{'+' if z.imag >= 0 else ''}{z.imag:.4f}j"

        table_data.append(
            [
                city.name.title(),
                f"{city.longitude:>6.2f}, {city.latitude:>6.2f}",
                z_str,
                f"{lon_rt:>6.2f}, {lat_rt:>6.2f}",
                status,
            ]
        )

    print(tabulate(table_data, headers=headers, tablefmt="github", stralign="right"))
    print("\n\n", "-" * 50, end="\n\n")
    print(
        f"Final Result: {'All tests PASSED. Implementation is mathematically consistent.' if all_passed else 'Some tests FAILED.'}"
    )
    print("\n\n", "=" * 50, end="\n\n")
    print("Adding 2 locations, would result in which other location?")
    city1 = City(name="tokyo", longitude=139.7638947, latitude=35.67686)
    city2 = City(name="dubai", longitude=55.304722, latitude=22.258169)
    city1_i = convert_gps_to_riemann(city1.longitude, city2.latitude)
    city2_i = convert_gps_to_riemann(city2.longitude, city2.latitude)
    mistery_location_i = city1_i + city2_i
    mistery_location_gps = translate_from_riemann_to_gps(mistery_location_i)
    print(f"""By Adding the Riemann Sphere projection of
    {city1.name.title()} (Longitude: {city1.longitude}, latitude: {city1.latitude}, Riemann Projection: {city1_i})
with
    {city2.name.title()} (Longitude: {city2.longitude}, latitude: {city2.latitude}, Riemann Projection: {city2_i}),
we get the new location of:
    Riemann projection: {mistery_location_i}
    GPS Coordinates:
        Longitude: {mistery_location_gps[0]}
        Latitude: {mistery_location_gps[1]}

e.g.: In Tokyo + Dubai exemple, the coordinates should be (Longitude: 97.53430835°, Latitude: 41.23449361903485°) designating this location on a map: China, Gansu, Subei Mongol Autonomous County, Mazongshan
""")


if __name__ == "__main__":
    main()

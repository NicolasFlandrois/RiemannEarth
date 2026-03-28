# Riemann Sphere Geospatial Stereographic Projection Applied to Earth

A simple Python implementation of the **Stereographic Projection** mapping Earth's geodetic coordinates (Latitude/Longitude) to the complex plane via the **Riemann Sphere**.

This project serves as a scientific verification tool, demonstrating mathematically consistent bidirectional transformations ($\mathbb{S}^2 \leftrightarrow \mathbb{C}$) adhering to standard complex analysis conventions. Well, you know, Just for Fun!

It is a truth universally acknowledged, that Earth can be assimilated as a Sphere... and locations can be defined as complex numbers by applying the Riemann Sphere.

## 📐 Mathematical Background

### The Riemann Sphere
In complex analysis, the **Riemann Sphere** is a model of the extended complex plane ($\mathbb{C} \cup \{\infty\}$). It represents the complex numbers on the surface of a sphere, providing a geometric interpretation of infinity.

*   **Wikipedia:** [Riemann Sphere](https://en.wikipedia.org/wiki/Riemann_sphere)
*   **Concept:** Every point on the complex plane corresponds to exactly one point on the sphere, except for the "point at infinity," which corresponds to the projection pole.

### Project Specifications & Conventions
This implementation strictly follows the **Standard Scientific Definition**:

1.  **Projection Source:** **North Pole** ($90^\circ$ N).
    - A line is drawn from the North Pole through a point on the sphere to intersect the equatorial plane.
2.  **Mapping of Poles:**
    - **South Pole** ($-90^\circ$ S) $\mapsto$ **Origin** ($0 + 0i$).
    - **North Pole** ($+90^\circ$ N) $\mapsto$ **Point at Infinity** ($\infty$).
3.  **Axis Alignment (Euler Convention):**
    - **[Prime Meridian](https://en.wikipedia.org/wiki/Prime_meridian)** ($0^\circ$ Longitude) $\mapsto$ **Positive Real Axis** ($+x$). In other words the International Reference Meridian, defined by the International Earth Rotation and Reference Systems Service, and internationally recognised as Meridian 0° since 1984... also called Greenwich Merdian in younder years.
    - **$90^\circ$ East** $\mapsto$ **Positive Imaginary Axis** ($+y$).
    - Formula: $z = r(\cos \lambda + i \sin \lambda)$, where $\lambda$ is longitude.

## 🚀 Installation & Execution

This project uses standard Python libraries (`numpy`, `tabulate`, `dataclasses`). We recommend using **`uv`** for fast, reliable dependency management, though `pip` works equally well.

### Option A: Using `uv` (Recommended)
[`uv`](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

1.  **Sync dependencies and create the virtual environment:**
    ```bash
    uv sync
    ```

2.  **Run the script:**
    ```bash
    uv run main.py
    ```

### Option B: Using standard `pip`

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    Or use your prefered environment manager of choice (pyenv, etc).

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## 📊 Output Example

The script performs a round-trip verification (Geo $\to$ Complex $\to$ Geo) for various cities and edge cases (Poles, Equator).

```text
| City            |   Input (Lon, Lat) |           Complex (z) |        Recovered | Status   |
|:----------------|-------------------:|----------------------:|-----------------:|:---------|
| Shanghai        |     121.46,  31.22 |      1.5146+0.9266j   |  121.46,  31.22  | ✓ PASS   |
| Los Angeles     |    -118.24,  34.05 |     -1.6587+0.8910j   | -118.24,  34.05  | ✓ PASS   |
| Tokyo           |     139.76,  35.68 |      1.2589+1.4878j   |  139.76,  35.68  | ✓ PASS   |
| Singapore       |     103.80,   1.20 |      0.9917+0.2436j   |  103.80,   1.20  | ✓ PASS   |
| Equator/Prime   |       0.00,   0.00 |      1.0000+0.0000j   |    0.00,   0.00  | ✓ PASS   |
| North Pole      |       0.00,  90.00 |                    ∞  |    0.00,  90.00  | ✓ PASS   |
| South Pole      |       0.00, -90.00 |      0.0000+0.0000j   |    0.00, -90.00  | ✓ PASS   |
```

## 🧪 Verification Logic

The implementation guarantees **bijectivity** within floating-point precision limits:
1.  **Forward Projection:** Uses $r = \frac{\cos \phi}{1 - \sin \phi}$ and standard Euler phase mapping.
2.  **Inverse Projection:** Uses $ \phi = \arcsin\left(\frac{r^2 - 1}{r^2 + 1}\right) $ and $\lambda = \operatorname{atan2}(y, x)$.
3.  **Edge Cases:**
    *   **South Pole:** Explicitly handled to return $(0, -90)$ avoiding $\operatorname{atan2}(0,0)$ ambiguity.
    *   **North Pole:** Handled via IEEE 754 infinity propagation, correctly recovering $90^\circ$ latitude.

## 📄 License
This exercise is provided for scientific education and verification purposes, and is under MIT LICENCE © 2026.

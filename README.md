# 🧊 3D Crystal Lattice & Nanostructure Visualizer + XRD Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crystal-lattice-xrd-simulator-ghsyqvicoyhfh4vv7remt8.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An interactive web application built for materials science students, crystallographers, and nanotechnology researchers to visualize **3D atomic unit cells and supercells**, calculate **crystallographic properties**, and simulate **Powder X-Ray Diffraction (XRD)** patterns in real time.

---

## 🚀 Live Demo

👉 **[Launch Interactive Web App](https://crystal-lattice-xrd-simulator-ghsyqvicoyhfh4vv7remt8.streamlit.app/)**

---

## ✨ Key Features

- **Interactive 3D Atomic Models:** Rotate, zoom, and inspect **1×1×1 unit cells** and **2×2×2 supercells** across key crystal systems:
  - **FCC** — Copper (Cu, *Fm-3m*)
  - **BCC** — Alpha-Iron (α-Fe, *Im-3m*)
  - **Diamond Cubic** — Silicon (Si, *Fd-3m*)
  - **Rock Salt** — Sodium Chloride (NaCl, *Fm-3m*)
  - **Zinc Blende** — ZnS / GaAs (*F-43m*)
  - **Cubic Perovskite** — BaTiO₃ / SrTiO₃ (*Pm-3m*)
  - **Wurtzite (Hexagonal)** — Zinc Oxide (ZnO, *P6₃mc*)
- **Live Lattice Parameter Tuning:** Dynamically adjust lattice constants (*a* and *c* in Å), atomic sphere scale, nearest-neighbor bonds, and unit cell wireframes.
- **Real-Time Crystallographic Metrics:** Automatically computes Unit Cell Volume (Å³), Theoretical Density (g/cm³), Atomic Packing Factor (APF), and Coordination Number.
- **Physics-Based Powder XRD Simulation:**
  - Supports **Cu Kα** (1.5406 Å), **Co Kα** (1.7889 Å), **Mo Kα** (0.7107 Å), and **Cr Kα** (2.2897 Å) anode sources.
  - Evaluates structure factors (*F<sub>hkl</sub>*), systematic extinction rules, atomic scattering factors, and Lorentz–polarization corrections.
  - Simulates nanocrystal size peak broadening using the **Debye–Scherrer equation** and **Pseudo-Voigt** peak profiles.
- **Bragg Reflections Table & CSV Export:** View indexed Miller planes *(hkl)*, 2θ peak positions, interplanar *d*-spacings (Å), multiplicities, and download simulated XRD spectra as `.csv` files.

---

## 📐 Theoretical Background & Equations

### 1. Bragg's Law & Interplanar Spacing (*d<sub>hkl</sub>*)
Diffraction peaks occur at angles *θ* satisfying Bragg's condition:

> **nλ = 2 d<sub>hkl</sub> sin(θ)**

- **Cubic Crystal Systems:**
  > **1 / d<sub>hkl</sub>² = (h² + k² + l²) / a²**

- **Hexagonal Crystal Systems (Wurtzite):**
  > **1 / d<sub>hkl</sub>² = (4 / 3) · [(h² + hk + k²) / a²] + (l² / c²)**

### 2. Structure Factor (*F<sub>hkl</sub>*)
Reflection intensities and systematic absences are governed by summing atomic scattering factors *f<sub>j</sub>* over all basis atoms at fractional coordinates *(u<sub>j</sub>, v<sub>j</sub>, w<sub>j</sub>)*:

> **F<sub>hkl</sub> = ∑ f<sub>j</sub> exp[ 2πi (h·u<sub>j</sub> + k·v<sub>j</sub> + l·w<sub>j</sub>) ]**

### 3. Debye–Scherrer Nanocrystallite Broadening
Peak full-width at half-maximum (*β*, in radians) scales inversely with crystallite size *D*:

> **β = (K · λ) / (D · cos θ)**  *(with shape factor K = 0.9)*

---

## 🛠️ Tech Stack

- **Frontend & Hosting:** Streamlit
- **Scientific Computing:** NumPy, Pandas
- **3D & 2D Interactive Visualization:** Plotly (`go.Scatter3d` & `go.Scatter`)

---

## 💻 Local Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DulsaraPrasad/crystal-lattice-xrd-simulator.git](https://github.com/DulsaraPrasad/crystal-lattice-xrd-simulator.git)
   cd crystal-lattice-xrd-simulator

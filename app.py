import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="3D Crystal Lattice & XRD Simulator", layout="wide")

st.title("🧊 3D Crystal Lattice & Nanostructure Visualizer + XRD Simulator")
st.markdown(
    "Explore interactive **3D atomic unit cells & supercells**, calculate **Atomic Packing Factor (APF)** "
    "and theoretical density, and simulate real-time **Powder X-Ray Diffraction (XRD)** patterns."
)

# ---------------------------------------------------------------------------
# Crystallographic Database (Fractional Coordinates, Atomic Numbers Z, Masses)
# ---------------------------------------------------------------------------
CRYSTAL_STRUCTURES = {
    "FCC — Copper (Cu)": {
        "system": "Cubic (Fm-3m)",
        "default_a": 3.615,
        "default_c": 3.615,
        "atoms_per_cell": 4,
        "apf": 0.74,
        "coordination": 12,
        "species": {
            "Cu": {"Z": 29, "mass": 63.546, "radius": 1.28, "color": "#EA580C"},
        },
        "basis": [
            ("Cu", [0.0, 0.0, 0.0]),
            ("Cu", [0.5, 0.5, 0.0]),
            ("Cu", [0.5, 0.0, 0.5]),
            ("Cu", [0.0, 0.5, 0.5]),
        ],
    },
    "BCC — Alpha-Iron (α-Fe)": {
        "system": "Cubic (Im-3m)",
        "default_a": 2.866,
        "default_c": 2.866,
        "atoms_per_cell": 2,
        "apf": 0.68,
        "coordination": 8,
        "species": {
            "Fe": {"Z": 26, "mass": 55.845, "radius": 1.24, "color": "#475569"},
        },
        "basis": [
            ("Fe", [0.0, 0.0, 0.0]),
            ("Fe", [0.5, 0.5, 0.5]),
        ],
    },
    "Diamond Cubic — Silicon (Si)": {
        "system": "Cubic (Fd-3m)",
        "default_a": 5.431,
        "default_c": 5.431,
        "atoms_per_cell": 8,
        "apf": 0.34,
        "coordination": 4,
        "species": {
            "Si": {"Z": 14, "mass": 28.085, "radius": 1.11, "color": "#2563EB"},
        },
        "basis": [
            ("Si", [0.0, 0.0, 0.0]),
            ("Si", [0.5, 0.5, 0.0]),
            ("Si", [0.5, 0.0, 0.5]),
            ("Si", [0.0, 0.5, 0.5]),
            ("Si", [0.25, 0.25, 0.25]),
            ("Si", [0.75, 0.75, 0.25]),
            ("Si", [0.75, 0.25, 0.75]),
            ("Si", [0.25, 0.75, 0.75]),
        ],
    },
    "Rock Salt — Sodium Chloride (NaCl)": {
        "system": "Cubic (Fm-3m)",
        "default_a": 5.640,
        "default_c": 5.640,
        "atoms_per_cell": 8,
        "apf": 0.67,
        "coordination": 6,
        "species": {
            "Na+": {"Z": 11, "mass": 22.990, "radius": 1.02, "color": "#7C3AED"},
            "Cl-": {"Z": 17, "mass": 35.450, "radius": 1.81, "color": "#16A34A"},
        },
        "basis": [
            ("Na+", [0.0, 0.0, 0.0]),
            ("Na+", [0.5, 0.5, 0.0]),
            ("Na+", [0.5, 0.0, 0.5]),
            ("Na+", [0.0, 0.5, 0.5]),
            ("Cl-", [0.5, 0.0, 0.0]),
            ("Cl-", [0.0, 0.5, 0.0]),
            ("Cl-", [0.0, 0.0, 0.5]),
            ("Cl-", [0.5, 0.5, 0.5]),
        ],
    },
    "Zinc Blende — ZnS / GaAs": {
        "system": "Cubic (F-43m)",
        "default_a": 5.410,
        "default_c": 5.410,
        "atoms_per_cell": 8,
        "apf": 0.34,
        "coordination": 4,
        "species": {
            "Zn": {"Z": 30, "mass": 65.38, "radius": 1.22, "color": "#0284C7"},
            "S": {"Z": 16, "mass": 32.06, "radius": 1.05, "color": "#EAB308"},
        },
        "basis": [
            ("Zn", [0.0, 0.0, 0.0]),
            ("Zn", [0.5, 0.5, 0.0]),
            ("Zn", [0.5, 0.0, 0.5]),
            ("Zn", [0.0, 0.5, 0.5]),
            ("S", [0.25, 0.25, 0.25]),
            ("S", [0.75, 0.75, 0.25]),
            ("S", [0.75, 0.25, 0.75]),
            ("S", [0.25, 0.75, 0.75]),
        ],
    },
    "Cubic Perovskite — BaTiO₃ / SrTiO₃": {
        "system": "Cubic (Pm-3m)",
        "default_a": 3.905,
        "default_c": 3.905,
        "atoms_per_cell": 5,
        "apf": 0.68,
        "coordination": 12,
        "species": {
            "Sr/Ba": {"Z": 38, "mass": 87.62, "radius": 1.44, "color": "#0D9488"},
            "Ti": {"Z": 22, "mass": 47.867, "radius": 0.61, "color": "#3B82F6"},
            "O": {"Z": 8, "mass": 15.999, "radius": 1.40, "color": "#EF4444"},
        },
        "basis": [
            ("Sr/Ba", [0.0, 0.0, 0.0]),
            ("Ti", [0.5, 0.5, 0.5]),
            ("O", [0.5, 0.5, 0.0]),
            ("O", [0.5, 0.0, 0.5]),
            ("O", [0.0, 0.5, 0.5]),
        ],
    },
    "Wurtzite (Hexagonal) — ZnO": {
        "system": "Hexagonal (P6₃mc)",
        "default_a": 3.250,
        "default_c": 5.207,
        "atoms_per_cell": 4,
        "apf": 0.48,
        "coordination": 4,
        "species": {
            "Zn": {"Z": 30, "mass": 65.38, "radius": 0.74, "color": "#0284C7"},
            "O": {"Z": 8, "mass": 15.999, "radius": 1.38, "color": "#EF4444"},
        },
        "basis": [
            ("Zn", [1.0 / 3.0, 2.0 / 3.0, 0.0]),
            ("Zn", [2.0 / 3.0, 1.0 / 3.0, 0.5]),
            ("O", [1.0 / 3.0, 2.0 / 3.0, 0.382]),
            ("O", [2.0 / 3.0, 1.0 / 3.0, 0.882]),
        ],
    },
}

# X-Ray Anode Sources (Wavelength in Angstroms)
XRAY_SOURCES = {
    "Cu Kα (λ = 1.5406 Å)": 1.5406,
    "Co Kα (λ = 1.7889 Å)": 1.7889,
    "Mo Kα (λ = 0.7107 Å)": 0.7107,
    "Cr Kα (λ = 2.2897 Å)": 2.2897,
}

# ---------------------------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------------------------
st.sidebar.header("1. Crystal Structure")
selected_name = st.sidebar.selectbox("Select Lattice / Nanostructure", list(CRYSTAL_STRUCTURES.keys()), index=0)
cryst = CRYSTAL_STRUCTURES[selected_name]
is_hexagonal = "Hexagonal" in cryst["system"]

st.sidebar.header("2. Lattice Parameters (Å)")
a_param = st.sidebar.slider(
    "Lattice Parameter a (Å)",
    min_value=2.0,
    max_value=8.0,
    value=float(cryst["default_a"]),
    step=0.005,
)

if is_hexagonal:
    c_param = st.sidebar.slider(
        "Lattice Parameter c (Å)",
        min_value=2.5,
        max_value=10.0,
        value=float(cryst["default_c"]),
        step=0.005,
    )
else:
    c_param = a_param

st.sidebar.header("3. 3D Supercell & Display")
supercell_n = st.sidebar.radio("Supercell Expansion", [1, 2], index=0, format_func=lambda x: f"{x}×{x}×{x} Unit Cells")
atom_scale = st.sidebar.slider("Atomic Sphere Scale", 0.4, 1.6, 1.0, 0.1)
show_bonds = st.sidebar.checkbox("Show Nearest-Neighbor Bonds", value=True)
show_cell_box = st.sidebar.checkbox("Show Unit Cell Wireframe", value=True)

st.sidebar.header("4. XRD Simulation Settings")
xray_label = st.sidebar.selectbox("X-Ray Anode Source", list(XRAY_SOURCES.keys()), index=0)
wavelength = XRAY_SOURCES[xray_label]
crystallite_size_nm = st.sidebar.slider(
    "Nanocrystal Size D (nm) — Scherrer Broadening",
    min_value=5.0,
    max_value=100.0,
    value=25.0,
    step=1.0,
)
two_theta_range = st.sidebar.slider("2θ Scan Range (degrees)", 10.0, 120.0, (15.0, 90.0))

# ---------------------------------------------------------------------------
# Crystallographic Math & Supercell Coordinate Generation
# ---------------------------------------------------------------------------
def frac_to_cart(frac_coords, a, c, hexagonal=False):
    u, v, w = frac_coords
    if hexagonal:
        x = a * u + a * np.cos(2 * np.pi / 3) * v
        y = a * np.sin(2 * np.pi / 3) * v
        z = c * w
    else:
        x = a * u
        y = a * v
        z = a * w
    return np.array([x, y, z])


# Build atom list including boundary images on cell faces/edges/corners for visual completeness
atoms_list = []
for ix in range(supercell_n):
    for iy in range(supercell_n):
        for iz in range(supercell_n):
            for sp, frac in cryst["basis"]:
                # Include periodic images at fractional coordinate == 0 on upper boundaries
                shifts_x = [0, 1] if (ix == supercell_n - 1 and np.isclose(frac[0], 0.0)) else [0]
                shifts_y = [0, 1] if (iy == supercell_n - 1 and np.isclose(frac[1], 0.0)) else [0]
                shifts_z = [0, 1] if (iz == supercell_n - 1 and np.isclose(frac[2], 0.0)) else [0]
                for sx in shifts_x:
                    for sy in shifts_y:
                        for sz in shifts_z:
                            f_pos = [frac[0] + ix + sx, frac[1] + iy + sy, frac[2] + iz + sz]
                            cart = frac_to_cart(f_pos, a_param, c_param, is_hexagonal)
                            atoms_list.append((sp, cart))

# Unit cell volume & theoretical density
if is_hexagonal:
    cell_volume = (np.sqrt(3) / 2.0) * (a_param ** 2) * c_param  # Å^3
else:
    cell_volume = a_param ** 3  # Å^3

total_mass_amu = sum(cryst["species"][sp]["mass"] for sp, _ in cryst["basis"])
avogadro = 6.02214076e23
density_gcm3 = (total_mass_amu / avogadro) / (cell_volume * 1e-24)

# ---------------------------------------------------------------------------
# Top KPI Metrics Row
# ---------------------------------------------------------------------------
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Crystal System", cryst["system"])
m2.metric("Unit Cell Volume", f"{cell_volume:.2f} Å³")
m3.metric("Theoretical Density", f"{density_gcm3:.2f} g/cm³")
m4.metric("Atomic Packing (APF)", f"{cryst['apf']:.2f}")
m5.metric("Coordination No.", f"{cryst['coordination']}")

# ---------------------------------------------------------------------------
# XRD Diffraction Physics Calculation (Bragg's Law + Structure Factor F_hkl)
# ---------------------------------------------------------------------------
def simulate_xrd(cryst_dict, a, c, lam, d_nm, tt_min, tt_max, hexagonal=False):
    # Generate all candidate (h, k, l) planes up to index 6
    hkl_indices = []
    for h in range(-6, 7):
        for k in range(-6, 7):
            for l in range(-6, 7):
                if h == 0 and k == 0 and l == 0:
                    continue
                hkl_indices.append((h, k, l))

    reflections = {}
    for h, k, l in hkl_indices:
        if hexagonal:
            inv_d2 = (4.0 / 3.0) * ((h ** 2 + h * k + k ** 2) / (a ** 2)) + (l ** 2) / (c ** 2)
        else:
            inv_d2 = (h ** 2 + k ** 2 + l ** 2) / (a ** 2)

        d_hkl = 1.0 / np.sqrt(inv_d2)
        sin_theta = lam / (2.0 * d_hkl)
        if sin_theta >= 1.0:
            continue

        theta_rad = np.arcsin(sin_theta)
        two_theta = np.degrees(2.0 * theta_rad)
        if two_theta < tt_min or two_theta > tt_max:
            continue

        # Atomic scattering factor approximation f(s) ~ Z * exp(-B * s^2)
        s = sin_theta / lam
        F_complex = 0.0 + 0.0j
        for sp, frac in cryst_dict["basis"]:
            Z = cryst_dict["species"][sp]["Z"]
            f_atom = Z * np.exp(-1.5 * (s ** 2))
            phase = 2.0 * np.pi * (h * frac[0] + k * frac[1] + l * frac[2])
            F_complex += f_atom * np.exp(1j * phase)

        F_sq = float(np.abs(F_complex) ** 2)
        if F_sq < 1e-3:  # Systematic absence (extinction rule)
            continue

        # Lorentz-Polarization factor
        lp_factor = (1.0 + np.cos(2.0 * theta_rad) ** 2) / (
            (np.sin(theta_rad) ** 2) * np.cos(theta_rad)
        )
        intensity_contrib = F_sq * lp_factor

        # Group equivalent planes by rounded 2theta
        key = round(two_theta, 3)
        if key not in reflections:
            reflections[key] = {
                "2theta": two_theta,
                "d_hkl": d_hkl,
                "intensity": 0.0,
                "hkl": (abs(h), abs(k), abs(l)),
                "multiplicity": 0,
            }
        reflections[key]["intensity"] += intensity_contrib
        reflections[key]["multiplicity"] += 1
        # Prefer positive/canonical (hkl) label
        if h >= 0 and k >= 0 and l >= 0:
            reflections[key]["hkl"] = (h, k, l)

    if not reflections:
        return pd.DataFrame(), np.linspace(tt_min, tt_max, 1000), np.zeros(1000)

    peaks_df = pd.DataFrame(list(reflections.values())).sort_values("2theta").reset_index(drop=True)
    max_int = peaks_df["intensity"].max()
    peaks_df["Rel. Intensity (%)"] = (peaks_df["intensity"] / max_int) * 100.0
    peaks_df["Plane (hkl)"] = peaks_df["hkl"].apply(lambda x: f"({x[0]}{x[1]}{x[2]})")

    # Continuous diffraction pattern using Scherrer FWHM + Pseudo-Voigt profile
    tt_grid = np.linspace(tt_min, tt_max, 2000)
    pattern = np.zeros_like(tt_grid)
    K_scherrer = 0.9
    D_angstrom = d_nm * 10.0

    for _, row in peaks_df.iterrows():
        tt0 = row["2theta"]
        theta0_rad = np.radians(tt0 / 2.0)
        # Scherrer FWHM in radians -> degrees (plus small instrumental broadening 0.08 deg)
        beta_rad = (K_scherrer * lam) / (D_angstrom * np.cos(theta0_rad))
        fwhm_deg = np.degrees(beta_rad) + 0.08
        sigma = fwhm_deg / (2.0 * np.sqrt(2.0 * np.log(2.0)))
        gamma = fwhm_deg / 2.0

        gaussian = np.exp(-0.5 * ((tt_grid - tt0) / sigma) ** 2)
        lorentzian = 1.0 / (1.0 + ((tt_grid - tt0) / gamma) ** 2)
        profile = 0.6 * gaussian + 0.4 * lorentzian
        pattern += row["Rel. Intensity (%)"] * profile

    if pattern.max() > 0:
        pattern = (pattern / pattern.max()) * 100.0

    return peaks_df, tt_grid, pattern


peaks_df, tt_grid, xrd_intensity = simulate_xrd(
    cryst,
    a_param,
    c_param,
    wavelength,
    crystallite_size_nm,
    two_theta_range[0],
    two_theta_range[1],
    is_hexagonal,
)

# ---------------------------------------------------------------------------
# Side-by-Side 3D Crystal Viewer & Live XRD Spectrum
# ---------------------------------------------------------------------------
col_3d, col_xrd = st.columns([1.05, 1.15])

with col_3d:
    st.subheader("3D Interactive Atomic Structure")
    fig_3d = go.Figure()

    # Plot atoms grouped by species
    for sp_name, sp_info in cryst["species"].items():
        coords = np.array([pos for sp, pos in atoms_list if sp == sp_name])
        if len(coords) == 0:
            continue
        fig_3d.add_trace(
            go.Scatter3d(
                x=coords[:, 0],
                y=coords[:, 1],
                z=coords[:, 2],
                mode="markers",
                name=f"{sp_name} (r = {sp_info['radius']} Å)",
                marker=dict(
                    size=sp_info["radius"] * 13 * atom_scale,
                    color=sp_info["color"],
                    opacity=0.95,
                    line=dict(width=1.5, color="#FFFFFF"),
                ),
                hovertemplate=(
                    f"<b>{sp_name}</b><br>"
                    "x: %{x:.2f} Å<br>y: %{y:.2f} Å<br>z: %{z:.2f} Å<extra></extra>"
                ),
            )
        )

    # Nearest-neighbor bonds
    if show_bonds and len(atoms_list) > 1:
        all_coords = np.array([pos for _, pos in atoms_list])
        dist_matrix = np.linalg.norm(all_coords[:, None, :] - all_coords[None, :, :], axis=-1)
        nonzero_dists = dist_matrix[dist_matrix > 0.1]
        if len(nonzero_dists) > 0:
            min_bond = np.min(nonzero_dists)
            bond_cutoff = min_bond * 1.12
            bx, by, bz = [], [], []
            n_atoms = len(all_coords)
            for i in range(n_atoms):
                for j in range(i + 1, n_atoms):
                    if 0.1 < dist_matrix[i, j] <= bond_cutoff:
                        bx.extend([all_coords[i, 0], all_coords[j, 0], None])
                        by.extend([all_coords[i, 1], all_coords[j, 1], None])
                        bz.extend([all_coords[i, 2], all_coords[j, 2], None])
            fig_3d.add_trace(
                go.Scatter3d(
                    x=bx,
                    y=by,
                    z=bz,
                    mode="lines",
                    name="Bonds",
                    line=dict(color="rgba(148, 163, 184, 0.65)", width=4),
                    hoverinfo="skip",
                )
            )

    # Unit cell wireframe edges
    if show_cell_box:
        corners_frac = [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ]
        corners = [frac_to_cart(cf, a_param, c_param, is_hexagonal) for cf in corners_frac]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]
        ex, ey, ez = [], [], []
        for u, v in edges:
            ex.extend([corners[u][0], corners[v][0], None])
            ey.extend([corners[u][1], corners[v][1], None])
            ez.extend([corners[u][2], corners[v][2], None])
        fig_3d.add_trace(
            go.Scatter3d(
                x=ex,
                y=ey,
                z=ez,
                mode="lines",
                name="Unit Cell",
                line=dict(color="#0F172A", width=3, dash="dash"),
                hoverinfo="skip",
            )
        )

    fig_3d.update_layout(
        height=490,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
        scene=dict(
            xaxis_title="x (Å)",
            yaxis_title="y (Å)",
            zaxis_title="z (Å)",
            aspectmode="data",
            bgcolor="rgba(248, 250, 252, 0.9)",
        ),
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with col_xrd:
    st.subheader(f"Simulated Powder XRD Pattern ({xray_label.split()[0]} Kα)")
    fig_xrd = go.Figure()

    fig_xrd.add_trace(
        go.Scatter(
            x=tt_grid,
            y=xrd_intensity,
            mode="lines",
            name="Simulated XRD",
            line=dict(color="#2563EB", width=2.2),
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.12)",
        )
    )

    if not peaks_df.empty:
        major_peaks = peaks_df[peaks_df["Rel. Intensity (%)"] >= 8.0]
        fig_xrd.add_trace(
            go.Scatter(
                x=major_peaks["2theta"],
                y=major_peaks["Rel. Intensity (%)"] + 3.5,
                mode="text",
                text=major_peaks["Plane (hkl)"],
                textposition="top center",
                textfont=dict(size=11, color="#0F172A"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig_xrd.update_layout(
        height=490,
        margin=dict(l=10, r=10, t=25, b=10),
        xaxis_title="Diffraction Angle 2θ (degrees)",
        yaxis_title="Relative Intensity (a.u.)",
        yaxis=dict(range=[0, 118]),
        template="plotly_white",
        hovermode="x unified",
    )
    st.plotly_chart(fig_xrd, use_container_width=True)

# ---------------------------------------------------------------------------
# Bragg Reflections Table & Export
# ---------------------------------------------------------------------------
st.subheader("Bragg Diffraction Peaks & Interplanar Spacings (d-spacing)")
if not peaks_df.empty:
    display_peaks = peaks_df[["Plane (hkl)", "2theta", "d_hkl", "multiplicity", "Rel. Intensity (%)"]].copy()
    display_peaks.columns = ["Miller Indices (hkl)", "2θ (deg)", "d-Spacing (Å)", "Multiplicity", "Rel. Intensity (%)"]
    display_peaks["2θ (deg)"] = display_peaks["2θ (deg)"].round(3)
    display_peaks["d-Spacing (Å)"] = display_peaks["d-Spacing (Å)"].round(4)
    display_peaks["Rel. Intensity (%)"] = display_peaks["Rel. Intensity (%)"].round(2)

    st.dataframe(display_peaks, use_container_width=True, hide_index=True)

    export_df = pd.DataFrame({"2Theta_deg": np.round(tt_grid, 4), "Intensity_au": np.round(xrd_intensity, 4)})
    st.download_button(
        label="📥 Download Simulated XRD Pattern (CSV)",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name=f"simulated_xrd_{selected_name.split()[0].lower()}.csv",
        mime="text/csv",
    )
else:
    st.warning("No Bragg reflections fall within the selected 2θ range and X-ray wavelength.")
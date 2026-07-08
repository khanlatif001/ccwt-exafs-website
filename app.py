import io
import os

import numpy as np
import plotly.graph_objects as go
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from ccwt import compute_ccwt, CCWTError

app = Flask(__name__)

_session_secret = os.environ.get("SESSION_SECRET")
if not _session_secret:
    if os.environ.get("FLASK_DEBUG") == "1" or os.environ.get("REPL_ID"):
        # Fall back to a random per-process secret in dev so the app still
        # runs without a configured secret; sessions just won't persist
        # across restarts. Never used if SESSION_SECRET is set.
        _session_secret = os.urandom(32).hex()
    else:
        raise RuntimeError("SESSION_SECRET environment variable must be set.")
app.secret_key = _session_secret

ALLOWED_EXTENSIONS = {"dat", "txt", "csv", "xafs"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

COLORSCALES = [
    "Jet", "Rainbow", "HSV", "Portland", "Picnic", "Earth",
    "Viridis", "Plasma", "Inferno", "Magma", "Cividis",
    "Turbo", "Electric", "Hot", "Blackbody",
    "YlGnBu", "YlOrRd", "Blues", "Greens", "Purples", "Reds", "Greys",
    "RdBu", "RdYlBu", "RdYlGn", "Spectral",
    "Twilight", "Bluered",
]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_dat(file_stream, filename):
    """Load two-column (k, chi(k)) whitespace- or comma-separated data."""
    text = file_stream.read().decode("utf-8", errors="replace")

    is_csv = filename.lower().endswith(".csv")
    delimiter = "," if is_csv else None

    try:
        data = np.loadtxt(io.StringIO(text), comments="#", delimiter=delimiter)
    except ValueError:
        # Fall back to the other delimiter in case the extension doesn't
        # match the actual formatting (e.g. a comma-separated .dat file).
        fallback_delimiter = None if is_csv else ","
        try:
            data = np.loadtxt(io.StringIO(text), comments="#", delimiter=fallback_delimiter)
        except ValueError:
            raise CCWTError(
                "Could not parse the data file. Expected two columns of numbers "
                "(whitespace- or comma-separated): k and chi(k)."
            )

    if data.ndim != 2 or data.shape[1] < 2:
        raise CCWTError("Data file must have at least two columns: k and chi(k).")
    return data[:, 0], data[:, 1]


def float_field(form, name, default):
    raw = form.get(name, "").strip()
    if raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        raise CCWTError(f"'{name}' must be a number.")


def int_field(form, name, default):
    raw = form.get(name, "").strip()
    if raw == "":
        return default
    try:
        return int(float(raw))
    except ValueError:
        raise CCWTError(f"'{name}' must be an integer.")


def build_exafs_figure(knew, xnew):
    fig = go.Figure(data=[go.Scatter(x=knew, y=xnew, mode="lines", line=dict(color="#2563eb"))])
    fig.update_layout(
        title="Interpolated EXAFS Data",
        xaxis_title="k (Å⁻¹)",
        yaxis_title="χ(k)",
        template="plotly_white",
        margin=dict(l=60, r=30, t=50, b=50),
        height=380,
    )
    return fig


def build_ft_figure(freq, ft_magnitude):
    fig = go.Figure(data=[go.Scatter(x=freq * np.pi, y=ft_magnitude, mode="lines", line=dict(color="#7c3aed"))])
    fig.update_layout(
        title="Fourier Transform",
        xaxis_title="R (Å)",
        yaxis_title="FT Magnitude",
        template="plotly_white",
        margin=dict(l=60, r=30, t=50, b=50),
        height=380,
        xaxis=dict(range=[0, 6]),
    )
    return fig


def build_wavelet_figure(knew, r, zi):
    zmin = float(np.nanmin(zi))
    zmax = float(np.nanmax(zi))
    zmid = 0.5 * (zmin + zmax)
    zspread = zmax - zmin
    contrast_levels = np.linspace(0.4, 1.0, 7)

    fig = go.Figure(
        data=[go.Heatmap(
            z=zi, x=knew, y=r, colorscale="Jet", zmin=zmin, zmax=zmax,
            colorbar=dict(title="Amplitude"),
        )]
    )

    color_buttons = [
        dict(method="restyle", label=scale, args=[{"colorscale": [scale]}])
        for scale in COLORSCALES
    ]

    slider_steps = []
    for level in contrast_levels:
        zmin_step = zmid - 0.5 * zspread * level
        zmax_step = zmid + 0.5 * zspread * level
        slider_steps.append(dict(
            label=f"{int(level * 100)}%", method="restyle",
            args=[{"zmin": [zmin_step], "zmax": [zmax_step]}],
        ))

    fig.update_layout(
        title=dict(text="Continuous Cauchy Wavelet Transform", x=0.5, xanchor="center"),
        xaxis_title="k (Å⁻¹)",
        yaxis_title="R (Å)",
        template="plotly_white",
        height=560,
        margin=dict(l=70, r=30, t=110, b=110),
        updatemenus=[dict(
            buttons=color_buttons, direction="down", pad={"r": 10, "t": 10},
            showactive=True, x=0.0, xanchor="left", y=1.14, yanchor="top",
            bgcolor="#f3f4f6", bordercolor="#9ca3af", borderwidth=1, active=0,
        )],
        sliders=[dict(
            active=len(slider_steps) - 1, currentvalue={"prefix": "Contrast: "},
            pad={"t": 50}, steps=slider_steps, bordercolor="#e5e7eb", borderwidth=1,
            x=0.0, xanchor="left", y=-0.16, yanchor="top",
        )],
    )
    return fig


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("datafile")
    if file is None or file.filename == "":
        flash("Please choose a data file to upload.")
        return redirect(url_for("index"))
    if not allowed_file(file.filename):
        flash("Unsupported file type. Please upload a .dat, .txt, .csv, or .xafs file.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)

    try:
        kold, xold = parse_dat(file.stream, filename)

        form = request.form
        n = int_field(form, "n", 200)
        ri = float_field(form, "ri", 0.2)
        rf = float_field(form, "rf", 6.0)
        na = int_field(form, "na", 200)
        kin_raw = form.get("kin", "").strip()
        kfin_raw = form.get("kfin", "").strip()
        kin = float(kin_raw) if kin_raw else None
        kfin = float(kfin_raw) if kfin_raw else None

        result = compute_ccwt(kold, xold, n=n, ri=ri, rf=rf, na=na, kin=kin, kfin=kfin)
    except CCWTError as exc:
        flash(str(exc))
        return redirect(url_for("index"))
    except Exception:
        flash("Could not parse the data file. Expected two whitespace-separated columns: k and chi(k).")
        return redirect(url_for("index"))

    exafs_fig = build_exafs_figure(result["knew"], result["xnew"])
    ft_fig = build_ft_figure(result["freq"], result["ft_magnitude"])
    wavelet_fig = build_wavelet_figure(result["knew"], result["r"], result["wavelet_magnitude"])

    # The wavelet plot renders first in results.html, so it must be the one
    # that loads the Plotly.js library (via CDN); the others reuse it.
    plot_config = {"displaylogo": False, "responsive": True}
    wavelet_html = wavelet_fig.to_html(full_html=False, include_plotlyjs="cdn", config=plot_config)
    exafs_html = exafs_fig.to_html(full_html=False, include_plotlyjs=False, config=plot_config)
    ft_html = ft_fig.to_html(full_html=False, include_plotlyjs=False, config=plot_config)

    params = {"n": n, "ri": ri, "rf": rf, "na": na, "kin": kin, "kfin": kfin}

    return render_template(
        "results.html",
        filename=filename,
        exafs_html=exafs_html,
        ft_html=ft_html,
        wavelet_html=wavelet_html,
        params=params,
        n_points=len(kold),
    )


@app.errorhandler(413)
def too_large(_e):
    flash("File is too large. Maximum size is 5 MB.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

# ccwt-exafs-website

# Continuous Cauchy Wavelet Transform (CCWT) for EXAFS Signals

A web-based analysis tool designed to compute the Continuous Cauchy Wavelet Transform (CCWT) of Extended X-ray Absorption Fine Structure (EXAFS) data. This application provides a qualitative, time-frequency-style view of an EXAFS $\chi(k)$ signal, jointly resolving contributions in both k-space and R-space without the windowing artifacts associated with a standard Fourier transform.

---

## 🚀 Features

* **File Upload Support:** Accept two-column data files (`.dat`, `.txt`, `.csv`) containing $k$ and $\chi(k)$ values.
* **CCWT Analysis:** Performs localized wave analysis using the Cauchy wavelet basis.
* **Interactive Visualization:** Generates dynamic EXAFS plots and interactive CCWT heatmaps using Plotly.
* **Configurable Parameters:** Advanced parameter configurations available for customized signal processing.
* **Responsive Web Interface:** Built using HTML, CSS, and Python backend components.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask/Streamlit framework)
* **Frontend:** HTML5, CSS3, JavaScript
* **Data Visualization:** Plotly
* **Signal Processing:** Custom wavelets module (`ccwt.py`)
* **Package Manager:** `uv` / `pyproject.toml`

---

## 📂 Project Structure

```text
├── sample_data/          # Contains example data (e.g., k2_sample.dat)
├── static/               # CSS styles and client-side JavaScript assets
├── templates/            # HTML templates for webpage structure
├── app.py                # Main application handler and web service configuration
├── ccwt.py               # Algorithmic logic for the Cauchy wavelet transform
├── main.py               # Project execution entry point
├── pyproject.toml        # Project dependencies and configuration
└── README.md             # Project documentation

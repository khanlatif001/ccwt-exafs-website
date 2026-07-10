# ccwt-exafs-website

# Continuous Cauchy Wavelet Transform (CCWT) for EXAFS Signals

A web-based scientific application for analyzing **Extended X-ray Absorption Fine Structure (EXAFS)** data using the **Continuous Cauchy Wavelet Transform (CCWT)**.

The application provides a qualitative **time-frequency-style view** of EXAFS $\chi(k)$ oscillations, enabling simultaneous visualization of structural contributions in both **k-space** and **R-space**. Unlike conventional Fourier transform approaches, CCWT preserves localized information and reduces artifacts associated with fixed window functions.

---

## 🌐 Online Run App / Analyze EXAFS Data

### 🆓 Free Deployment
https://ccwt-exafs-website.onrender.com

### 🚀 Premium Deployment
https://ccwt-exafs-website--latifkhn.replit.app

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
```

---

## 🔬 Method

The Continuous Cauchy Wavelet Transform (CCWT) implemented in this project is based on:

Munoz, M., Argoul, P., & Farges, F. (2003).
*Continuous Cauchy wavelet transform analyses of EXAFS spectra: A qualitative approach.*
**American Mineralogist**, **88**, 694–700.

---

## 📚 References

1. Khan, L. U., Jabeen, N., *et al.* (2021).
   *Investigating local structure of ion-implanted (Ni²⁺) and thermally annealed rocksalt CoO film by EXAFS simulation using evolutionary algorithm.*
   **ACS Applied Energy Materials**, **4**(3), 2049–2055.
   https://doi.org/10.1021/acsaem.0c02676

2. Khan, L. U., Khan, Z. U., Blois, L., Tabassam, L., Brito, H. F., & Figueroa, S. J. A. (2023).
   *Strategy to probe the local atomic structure of luminescent rare earth complexes by X-ray absorption near-edge spectroscopy simulation using a machine learning-based PyFitIt approach.*
   **Inorganic Chemistry**, **62**(6), 2738–2750.
   https://doi.org/10.1021/acs.inorgchem.2c03850



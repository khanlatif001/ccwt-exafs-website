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


## 🔬 References

1. Khan, L. U., Jabeen, N., & et al. (2021). Investigating local structure of ion-implanted (Ni2+) and thermally annealed rocksalt CoO film by EXAFS simulation using evolutionary algorithm. ACS Applied Energy Materials, 4(3), 2049–2055. https://doi.org/10.1021/acsaem.0c02740
2. Khan, L. U., Khan, Z. U., Blois, L., Tabassam, L., Brito, H. F., & Figueroa, S. J. A. (2023). Strategy to probe the local atomic structure of luminescent rare earth complexes by X-ray absorption near-edge spectroscopy simulation using a machine learning-based PyFitIt approach. Inorganic Chemistry, 62(6), 2738–2750. https://doi.org/10.1021/acs.inorgchem.2c03823

## 🔬 Method

Original code: http://www.univ-mlv.fr/~farges/waw

Munoz M., Argoul P., & Farges F. (2003). Continuous Cauchy wavelet transform analyses of EXAFS spectra: a qualitative approach. American Mineralogist, 88, 694–700.

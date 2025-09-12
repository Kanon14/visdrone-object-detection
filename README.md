# visdrone-object-detection
Aims to explore modern deep learning techniques, such as YOLO or other object detection frameworks, to address challenges like small object detection, dense scenes, and varying scales.

# Project Setup
### Prerequisites
- Python 3.10+
- PyTorch Cuda 1.8+ [[Download PyTorch Cuda](https://pytorch.org/)]
- Compatible cuda toolkit and cudnn installed on your machine [[Nvidia GPU Capability](https://developer.nvidia.com/cuda-gpus)] [[Download Cuda Toolkit](https://developer.nvidia.com/cuda-toolkit)] (Note: You must have a [Nvidia Developer Account](https://developer.nvidia.com/login))
- Anaconda or Miniconda installed on your machine [[Download Anaconda](https://www.anaconda.com/download)] OR
- UV installed on your machine [[Install UV](https://docs.astral.sh/uv/getting-started/installation/)]

### Installation
1. **Clone the repository:**
```bash
git clone https://github.com/Kanon14/visdrone-object-detection.git
cd visdrone-object-detection
```

2. **Create and activate an environment:**
```bash
# Conda setup
conda create -n visdrone python=3.10 -y
conda activate visdrone

# uv setup
uv venv --python 3.10
.venv/Scripts/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## How to Run
1. **Execute the project:**
```bash
streamlit run streamlit_app.py
```
2. **Then, access the application via your web browser:**
```bash
open http://localhost:<port>
```

## Acknowledgements
- **[Roboflow](https://roboflow.com/):** For dataset hosting and augmentation tools.
- **[Ultralytics](https://www.ultralytics.com/):** For the YOLO object detection framework.
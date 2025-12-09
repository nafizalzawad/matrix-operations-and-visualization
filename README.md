# Anime Style Cartoonifier using Python and OpenCV

This project transforms real-world images into anime or cartoon style artwork using classical image processing techniques. The system does not require machine learning or neural networks and instead relies on mathematically interpretable filters, clustering, and edge detection methods. A user-friendly Tkinter interface is included for image upload, visualization, and saving outputs.

---

## Features

- Converts any uploaded image into anime style
- Uses a six step processing pipeline:
  1. Image preprocessing  
  2. Bilateral filter for edge-preserving smoothing  
  3. K-means clustering for color quantization  
  4. Canny edge detection for fine outlines  
  5. Adaptive thresholding for strong black contours  
  6. Mask based composition for final cartoon output
- GUI built with Tkinter
- Viewable intermediate processing steps
- Save final output as PNG or JPG

---

## Technologies Used

- Python 3  
- OpenCV  
- NumPy  
- PIL (Pillow)  
- Matplotlib  
- Tkinter  
- EasyGUI  

---

## Project Structure

project/
│
├── cartoonify.py # Main application
├── README.md # Documentation
├── requirements.txt # Package dependencies
└── sample_images/ # Optional sample inputs

---

## Installation

1. Clone the repository:
bash
git clone https://github.com/your-username/anime-cartoonifier.git
cd anime-cartoonifier
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Run the application:

bash
Copy code
python cartoonify.py
Steps:

Click "Cartoonify an Image" to upload an image

View intermediate stages using "View Process Steps"

Save the final anime output using "Save Cartoon Image"

Mathematical Pipeline (Summary)
Bilateral Filtering
Edge-preserving smoothing:
I′(p) = (1 / Wp) Σ I(q) fs(||p−q||) fr(|I(p)−I(q)|)

K-Means Color Quantization
Reduces RGB values to K cluster centers

Canny Edge Detection
G = sqrt(Gx² + Gy²)

Adaptive Thresholding
Pixel-level thresholding based on local neighborhood intensity

Final Composition
AnimeImage = ColorQuantized AND InvertedEdgeMask

Sample Output
You may add before and after images here.

Contributors
Mahmudul Hasan — 0432220005101006

Anona Ayshi Rozario — 0432220005101011

Tasnuba Akter — 0432220005101014

Nafiz Al Zawad — 0432220005101041

License
This project is open-source and free to use for academic and educational purposes.

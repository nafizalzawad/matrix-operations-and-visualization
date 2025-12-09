import cv2 # for image processing
import easygui # to open the filebox
import numpy as np # to store image
import imageio # to read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox, Label, Button, filedialog
from PIL import ImageTk, Image

# Global variables to store image data and widget references
global ReSized6 
global process_images 
global final_image_label 

# Initialize main window
top=tk.Tk()
top.geometry('800x600') 
top.title('Cartoonify Your Image !')
top.configure(background='white')

# Label for displaying the final cartoon image (placeholder)
final_image_label = Label(top, background='white')
final_image_label.pack(pady=10)

# --- Button Functions (Mostly unchanged) ---

def upload():
    """Opens a file dialog for the user to select an image."""
    ImagePath=easygui.fileopenbox()
    if ImagePath:
        cartoonify(ImagePath)

def view_process():
    """Displays the Matplotlib plot of the 6-step cartoonification process."""
    if 'process_images' in globals():
        fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
        fig.suptitle('Anime/Cartoon Process Steps', fontsize=16)
        
        titles = ["1. Original", "2. Bilateral Filter", "3. Canny Edges", 
                  "4. Adaptive Threshold Edges", "5. K-Means Quantized Color", "6. Final Anime Style"] 
                  
        for i, ax in enumerate(axes.flat):
            ax.imshow(process_images[i], cmap='gray' if i in [2, 3] else None) 
            ax.set_title(titles[i], fontsize=8)

        plt.show()
    else:
        messagebox.showinfo(title="Error", message="Please cartoonify an image first.")

def save():
    """Saves the final cartoon image to the user's computer."""
    global ReSized6
    if 'ReSized6' in globals():
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"), 
                                                       ("JPEG files", "*.jpg"), 
                                                       ("All files", "*.*")])
        if path:
            cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
            newName = os.path.basename(path)
            I = f"Image saved successfully as {newName}"
            tk.messagebox.showinfo(title="Image Saved", message=I)
    else:
        messagebox.showinfo(title="Error", message="No cartoon image to save yet.")


# --- EXPERT IMAGE PROCESSING FUNCTION (The Core Change is in the FINAL COMPOSITION) ---

def cartoonify(ImagePath):
    """Processes the image using a multi-step pipeline for an enhanced anime style."""
    global ReSized6
    global process_images
    
    # Read and convert the image
    originalmage = cv2.imread(ImagePath)
    originalmage_rgb = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    if originalmage_rgb is None:
        messagebox.showerror("Error", "Can not find any image. Choose appropriate file")
        return

    # 1. Store Original Image
    ReSized1 = cv2.resize(originalmage_rgb, (500, 300)) 

    # --- Color Smoothing and Quantization ---

    # 2. Bilateral Filter (Aggressive Smoothing)
    color_smoothed = cv2.bilateralFilter(originalmage_rgb, d=15, sigmaColor=250, sigmaSpace=250)
    ReSized2 = cv2.resize(color_smoothed, (500, 300))

    # Color Quantization (K-Means)
    k = 8 
    data = np.float32(color_smoothed).reshape(-1, 3)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    quantized_image = center[label.flatten()].reshape(originalmage_rgb.shape)
    ReSized5 = cv2.resize(quantized_image, (500, 300)) # Store quantized image

    # --- Edge Detection (The Sharp Lines) ---
    
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    
    # 3. Canny Edge Detector (Finer details)
    canny_edges = cv2.Canny(grayScaleImage, threshold1=100, threshold2=300) 
    ReSized3 = cv2.resize(canny_edges, (500, 300))

    # 4. Aggressive Adaptive Threshold (Thick outlines)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 7)
    adaptive_edges = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 15) 
    ReSized4 = cv2.resize(adaptive_edges, (500, 300))

    # Combine Edges: Keep the area black if EITHER is black (bitwise_or on inverted images, or bitwise_and on raw)
    # Using bitwise_and on the raw masks (where black=0) keeps black only where both agree. Let's use bitwise_or on the inverted:
    
    # Simple and robust: create the final edge mask (0=black, 255=white)
    final_edge_mask = cv2.bitwise_and(adaptive_edges, canny_edges)
    
    # --- 6. Final Anime Composition (The Fix) ---

    # 1. Invert the mask: white_mask will be white (255) where we want color, and black (0) where we want lines.
    white_mask = cv2.bitwise_not(final_edge_mask) 
    
    # 2. Convert the 1-channel white_mask to 3 channels to apply to the color image
    white_mask_3chan = cv2.cvtColor(white_mask, cv2.COLOR_GRAY2BGR)
    
    # 3. Apply the 3-channel white_mask to the quantized image. This preserves color only where there are NO lines.
    colored_area = cv2.bitwise_and(quantized_image, white_mask_3chan)

    # 4. The lines are already black (0) in the colored_area image (due to the mask), 
    # so colored_area is the final anime image.
    cartoonImage = colored_area

    # Store the final image
    ReSized6 = cv2.resize(cartoonImage, (500, 300))

    # Store all images for the process view function
    process_images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    # Display the final cartoon image
    img_pil = Image.fromarray(ReSized6)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    final_image_label.config(image=img_tk)
    final_image_label.image = img_tk 
    
    # Ensure buttons are packed
    save_button.pack_forget() 
    process_button.pack_forget() 
    
    save_button.pack(side=tk.TOP, pady=10)
    process_button.pack(side=tk.TOP, pady=10)


# --- GUI Buttons Setup (Unchanged) ---

upload_button = Button(top, text="🖼️ Cartoonify an Image", command=upload, padx=10, pady=5)
upload_button.configure(background='#364156', foreground='white', font=('calibri', 12, 'bold'))
upload_button.pack(side=tk.TOP, pady=20) 

save_button = Button(top, text="💾 Save Cartoon Image", command=save, padx=10, pady=5)
save_button.configure(background='#364156', foreground='white', font=('calibri', 12, 'bold'))

process_button = Button(top, text="📈 View Process Steps", command=view_process, padx=10, pady=5)
process_button.configure(background='#364156', foreground='white', font=('calibri', 12, 'bold'))


top.mainloop()
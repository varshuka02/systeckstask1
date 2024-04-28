import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageToSketchConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")

        self.input_image = None
        self.sketch_image = None
        self.line_thickness = 1
        self.contrast_value = 1.0
        self.brightness_value = 0
        self.saturation_value = 1.0
        self.color_filter = "None"
        self.smoothing_value = 0
        self.texture_intensity_value = 0
        self.brush_style = "Solid"
        self.blend_mode = "Normal"
        self.noise_level_value = 0

        self.create_widgets()

    def create_widgets(self):
        # Frame for picture preview
        self.preview_frame = tk.LabelFrame(self.root, text="Preview")
        self.preview_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Picture Preview
        self.preview_label = tk.Label(self.preview_frame)
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Frame for adjustments
        self.param_frame = tk.LabelFrame(self.root, text="Adjust Parameters")
        self.param_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Upload Button
        self.upload_btn = tk.Button(self.param_frame, text="Upload Image", command=self.upload_image)
        self.upload_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        # Convert Button
        self.convert_btn = tk.Button(self.param_frame, text="Convert to Sketch", command=self.convert_to_sketch,
                                     state=tk.DISABLED)
        self.convert_btn.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        # Save Button
        self.save_btn = tk.Button(self.param_frame, text="Save Sketch", command=self.save_sketch, state=tk.DISABLED)
        self.save_btn.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        # Parameters layout
        self.parameters_layout()

    def parameters_layout(self):
        # Line Thickness Slider
        self.line_thickness_label = tk.Label(self.param_frame, text="Line Thickness:")
        self.line_thickness_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.line_thickness_slider = tk.Scale(self.param_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                               command=self.update_line_thickness)
        self.line_thickness_slider.set(1)
        self.line_thickness_slider.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Contrast Slider
        self.contrast_label = tk.Label(self.param_frame, text="Contrast:")
        self.contrast_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        self.contrast_slider = tk.Scale(self.param_frame, from_=0, to=2, resolution=0.01, orient=tk.HORIZONTAL,
                                         command=self.update_contrast)
        self.contrast_slider.set(1.0)
        self.contrast_slider.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        # Brightness Slider
        self.brightness_label = tk.Label(self.param_frame, text="Brightness:")
        self.brightness_label.grid(row=5, column=0, pady=5, padx=5, sticky="w")
        self.brightness_slider = tk.Scale(self.param_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                           command=self.update_brightness)
        self.brightness_slider.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

        # Saturation Slider
        self.saturation_label = tk.Label(self.param_frame, text="Saturation:")
        self.saturation_label.grid(row=6, column=0, pady=5, padx=5, sticky="w")
        self.saturation_slider = tk.Scale(self.param_frame, from_=0, to=2, resolution=0.01, orient=tk.HORIZONTAL,
                                           command=self.update_saturation)
        self.saturation_slider.set(1.0)
        self.saturation_slider.grid(row=6, column=1, pady=5, padx=5, sticky="ew")

        # Color Filter
        self.color_filter_label = tk.Label(self.param_frame, text="Color Filter:")
        self.color_filter_label.grid(row=7, column=0, pady=5, padx=5, sticky="w")
        self.color_filter_combo = ttk.Combobox(self.param_frame, values=["None", "Sepia", "Black and White", "Vintage"],
                                               state="readonly")
        self.color_filter_combo.bind("<<ComboboxSelected>>", lambda event: self.update_color_filter())
        self.color_filter_combo.current(0)
        self.color_filter_combo.grid(row=7, column=1, pady=5, padx=5, sticky="ew")

        # Smoothing Slider
        self.smoothing_label = tk.Label(self.param_frame, text="Smoothing:")
        self.smoothing_label.grid(row=8, column=0, pady=5, padx=5, sticky="w")
        self.smoothing_slider = tk.Scale(self.param_frame, from_=0, to=10, orient=tk.HORIZONTAL,
                                          command=self.update_smoothing)
        self.smoothing_slider.grid(row=8, column=1, pady=5, padx=5, sticky="ew")

        # Texture Intensity Slider
        self.texture_intensity_label = tk.Label(self.param_frame, text="Texture Intensity:")
        self.texture_intensity_label.grid(row=9, column=0, pady=5, padx=5, sticky="w")
        self.texture_intensity_slider = tk.Scale(self.param_frame, from_=0, to=10, orient=tk.HORIZONTAL,
                                                  command=self.update_texture_intensity)
        self.texture_intensity_slider.grid(row=9, column=1, pady=5, padx=5, sticky="ew")

        # Brush Style
        self.brush_style_label = tk.Label(self.param_frame, text="Brush Style:")
        self.brush_style_label.grid(row=10, column=0, pady=5, padx=5, sticky="w")
        self.brush_style_var = tk.StringVar(self.param_frame)
        self.brush_style_var.set("Solid")
        self.brush_style_menu = tk.OptionMenu(self.param_frame, self.brush_style_var, "Solid", "Dotted", "Dashed",
                                               command=self.update_brush_style)
        self.brush_style_menu.grid(row=10, column=1, pady=5, padx=5, sticky="ew")

        # Blend Mode
        self.blend_mode_label = tk.Label(self.param_frame, text="Blend Mode:")
        self.blend_mode_label.grid(row=11, column=0, pady=5, padx=5, sticky="w")
        self.blend_mode_var = tk.StringVar(self.param_frame)
        self.blend_mode_var.set("Normal")
        self.blend_mode_menu = tk.OptionMenu(self.param_frame, self.blend_mode_var, "Normal", "Multiply", "Screen",
                                              "Overlay", command=self.update_blend_mode)
        self.blend_mode_menu.grid(row=11, column=1, pady=5, padx=5, sticky="ew")

        # Noise Level Slider
        self.noise_level_label = tk.Label(self.param_frame, text="Noise Level:")
        self.noise_level_label.grid(row=12, column=0, pady=5, padx=5, sticky="w")
        self.noise_level_slider = tk.Scale(self.param_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                            command=self.update_noise_level)
        self.noise_level_slider.grid(row=12, column=1, pady=5, padx=5, sticky="ew")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg; *.jpeg; *.png")])
        if file_path:
            self.input_image = cv2.imread(file_path)
            self.show_image(self.input_image)
            self.convert_btn.config(state=tk.NORMAL)

    def convert_to_sketch(self):
        # Apply parameters
        gray_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
        inverted_gray_image = 255 - gray_image
        blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
        inverted_blurred_image = 255 - blurred_image
        self.sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        # Apply contrast
        self.sketch_image = cv2.addWeighted(self.sketch_image, self.contrast_value, np.zeros_like(self.sketch_image),
                                             0, self.brightness_value)

        # Apply color filter
        if self.color_filter == "Sepia":
            self.sketch_image = cv2.cvtColor(self.sketch_image, cv2.COLOR_GRAY2BGR)
            self.sketch_image = cv2.applyColorMap(self.sketch_image, cv2.COLORMAP_SEPIA)
            self.sketch_image = cv2.cvtColor(self.sketch_image, cv2.COLOR_BGR2GRAY)
        elif self.color_filter == "Black and White":
            _, self.sketch_image = cv2.threshold(self.sketch_image, 128, 255, cv2.THRESH_BINARY)
        elif self.color_filter == "Vintage":
            pass
            
        self.show_image(self.sketch_image)
        self.save_btn.config(state=tk.NORMAL)

    def update_line_thickness(self, value):
        self.line_thickness = int(value)

    def update_contrast(self, value):
        self.contrast_value = float(value)

    def update_brightness(self, value):
        self.brightness_value = int(value)

    def update_saturation(self, value):
        self.saturation_value = float(value)

    def update_color_filter(self):
        self.color_filter = self.color_filter_combo.get()

    def update_smoothing(self, value):
        self.smoothing_value = int(value)

    def update_texture_intensity(self, value):
        self.texture_intensity_value = int(value)

    def update_brush_style(self):
        self.brush_style = self.brush_style_var.get()

    def update_blend_mode(self):
        self.blend_mode = self.blend_mode_var.get()

    def update_noise_level(self, value):
        self.noise_level_value = int(value)

    def show_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if hasattr(self, 'preview_label'):
            self.preview_label.config(image=image)
            self.preview_label.image = image
        else:
            self.preview_label = tk.Label(self.preview_frame, image=image)
            self.preview_label.image = image
            self.preview_label.pack(fill=tk.BOTH, expand=True)

    def save_sketch(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                             ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, self.sketch_image)
            messagebox.showinfo("Success", "Sketch saved successfully!")

def main():
    root = tk.Tk()
    app = ImageToSketchConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()


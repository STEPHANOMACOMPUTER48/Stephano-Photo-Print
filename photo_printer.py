import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class PhotoPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software ya Kuprint Picha")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self.image_path = None
        self.cropped_img = None
        
        header = tk.Label(root, text="Programu ya Kuprint Picha", font=("Arial", 16, "bold"), fg="#2c3e50")
        header.pack(pady=15)
        
        self.btn_browse = tk.Button(root, text="1. Chagua Picha", command=self.load_image, font=("Arial", 11), bg="#3498db", fg="white", padx=10, pady=5)
        self.btn_browse.pack(pady=5)
        
        self.lbl_file = tk.Label(root, text="Hujachagua picha yoyote", font=("Arial", 9, "italic"), fg="#7f8c8d")
        self.lbl_file.pack(pady=5)
        
        lbl_size = tk.Label(root, text="2. Chagua Template ya Kuprint:", font=("Arial", 11, "bold"))
        lbl_size.pack(pady=10)
        
        self.size_option = tk.StringVar(value="Passport8_4x6")
        
        sizes = [
            ("Passport 8 kwenye Karatasi ya 4x6 / 10x15 cm", "Passport8_4x6"),
            ("Passport 8 kwenye Karatasi ya 5x7 inch", "Passport8_5x7"),
            ("Passport 12 kwenye Karatasi ya A4", "Passport12_A4"),
            ("Full Page A4 (Picha 1 Inayojaza Ukurasa)", "A4_Full")
        ]
        
        for text, mode in sizes:
            rb = tk.Radiobutton(root, text=text, variable=self.size_option, value=mode, font=("Arial", 10))
            rb.pack(anchor="w", padx=40, pady=4)
            
        self.btn_print = tk.Button(root, text="3. Print Picha Moja kwa Moja", command=self.generate_print_layout, font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", padx=10, pady=8)
        self.btn_print.pack(pady=20)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_file.config(text=f"Picha iliyochaguliwa: {filename}", fg="#27ae60")
            self.open_crop_window()

    def open_crop_window(self):
        # Kioo cha Kurekebisha Picha (Crop & Resize)
        crop_win = tk.Toplevel(self.root)
        crop_win.title("Rekebisha Picha (Crop & Resize)")
        crop_win.geometry("400x450")
        
        lbl_info = tk.Label(crop_win, text="Hakikisha Sura ipo Katikati", font=("Arial", 10, "bold"))
        lbl_info.pack(pady=5)

        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)

        lbl_img = tk.Label(crop_win, image=img_tk)
        lbl_img.image = img_tk
        lbl_img.pack(pady=10)

        def confirm_crop():
            # Inachukua picha na kuisawazisha moja kwa moja kwa uwiano sahihi (Auto-Center Crop)
            raw_img = Image.open(self.image_path)
            w, h = raw_img.size
            
            # Weka uwiano wa Passport (3.5x4.5)
            target_ratio = 3.5 / 4.5
            current_ratio = w / h
            
            if current_ratio > target_ratio:
                # Picha ni pana sana, kata pembeni
                new_w = int(h * target_ratio)
                offset = (w - new_w) // 2
                self.cropped_img = raw_img.crop((offset, 0, offset + new_w, h))
            else:
                # Picha ni ndefu sana, kata juu na chini
                new_h = int(w / target_ratio)
                offset = (h - new_h) // 2
                self.cropped_img = raw_img.crop((0, offset, w, offset + new_h))
                
            crop_win.destroy()
            messagebox.showinfo("Imerekebishwa", "Picha imerekebishwa kikamilifu tayari kwa ku-print!")

        btn_ok = tk.Button(crop_win, text="Sawa, Tumia Picha Hii", command=confirm_crop, bg="#3498db", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_ok.pack(pady=10)

    def generate_print_layout(self):
        if not self.image_path:
            messagebox.showwarning("Tahadhari", "Tafadhali chagua picha kwanza!")
            return

        try:
            mode = self.size_option.get()
            img = self.cropped_img if self.cropped_img else Image.open(self.image_path)
            
            pass_w, pass_h = 413, 531
            img_passport = img.resize((pass_w, pass_h), Image.Resampling.LANCZOS)

            if mode == "Passport8_4x6":
                canvas_w, canvas_h = 1200, 1800
                canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
                start_x, start_y = 60, 120
                gap_x, gap_y = 30, 40
                
                for r in range(4):
                    for c in range(2):
                        x = start_x + c * (pass_w + gap_x)
                        y = start_y + r * (pass_h + gap_y)
                        canvas.paste(img_passport, (x, y))

            elif mode == "Passport8_5x7":
                canvas_w, canvas_h = 1500, 2100
                canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
                start_x, start_y = 120, 150
                gap_x, gap_y = 60, 60
                
                for r in range(4):
                    for c in range(2):
                        x = start_x + c * (pass_w + gap_x)
                        y = start_y + r * (pass_h + gap_y)
                        canvas.paste(img_passport, (x, y))

            elif mode == "Passport12_A4":
                canvas_w, canvas_h = 2480, 3508
                canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
                start_x, start_y = 200, 200
                gap_x, gap_y = 100, 100
                
                for r in range(3):
                    for c in range(4):
                        x = start_x + c * (pass_w + gap_x)
                        y = start_y + r * (pass_h + gap_y)
                        canvas.paste(img_passport, (x, y))

            elif mode == "A4_Full":
                canvas_w, canvas_h = 2480, 3508
                canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
                margin = 100
                img_resized = img.resize((canvas_w - (2 * margin), canvas_h - (2 * margin)), Image.Resampling.LANCZOS)
                canvas.paste(img_resized, (margin, margin))

            temp_path = os.path.join(os.environ.get("TEMP", "."), "print_job.png")
            canvas.save(temp_path)
            os.startfile(temp_path, "print")
                
        except Exception as e:
            messagebox.showerror("Kosa", f"Kuna tatizo limetokea: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoPrinterApp(root)
    root.mainloop()

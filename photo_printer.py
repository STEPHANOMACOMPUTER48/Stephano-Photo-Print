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
            self.open_manual_crop_window()

    def open_manual_crop_window(self):
        crop_win = tk.Toplevel(self.root)
        crop_win.title("Kata Picha Wewe Mwenyewe (Manual Crop)")
        crop_win.geometry("450x550")
        
        lbl_info = tk.Label(crop_win, text="Buruza (Drag) Mouse kwenye picha ili uchague eneo:", font=("Arial", 9, "bold"))
        lbl_info.pack(pady=5)

        raw_img = Image.open(self.image_path)
        
        # Scaling image for display canvas
        disp_w, disp_h = 400, 400
        img_copy = raw_img.copy()
        img_copy.thumbnail((disp_w, disp_h))
        
        scale_x = raw_img.width / img_copy.width
        scale_y = raw_img.height / img_copy.height
        
        img_tk = ImageTk.PhotoImage(img_copy)
        
        canvas = tk.Canvas(crop_win, width=img_copy.width, height=img_copy.height, cursor="cross")
        canvas.pack(pady=5)
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk
        
        rect = [None]
        start_pos = [0, 0]

        def on_press(event):
            start_pos[0], start_pos[1] = event.x, event.y
            if rect[0]:
                canvas.delete(rect[0])
            rect[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

        def on_drag(event):
            canvas.coords(rect[0], start_pos[0], start_pos[1], event.x, event.y)

        def confirm_manual_crop():
            coords = canvas.coords(rect[0])
            if not coords or abs(coords[2] - coords[0]) < 10 or abs(coords[3] - coords[1]) < 10:
                # Kama hakuchagua, tumia picha yote
                self.cropped_img = raw_img
            else:
                x1, y1, x2, y2 = coords
                # Hakikisha vipimo ni sahihi kuanzia kushoto kwenda kulia
                rx1 = int(min(x1, x2) * scale_x)
                ry1 = int(min(y1, y2) * scale_y)
                rx2 = int(max(x1, x2) * scale_x)
                ry2 = int(max(y1, y2) * scale_y)
                self.cropped_img = raw_img.crop((rx1, ry1, rx2, ry2))
                
            crop_win.destroy()
            messagebox.showinfo("Imerekebishwa", "Picha imekatwa vizuri kama ulivyochagua!")

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)

        btn_ok = tk.Button(crop_win, text="Kamilisha na Tumia Picha Hii", command=confirm_manual_crop, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
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

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class PhotoPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software ya Kuprint Picha")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        self.image_path = None
        
        header = tk.Label(root, text="Programu ya Kuprint Picha", font=("Arial", 16, "bold"), fg="#2c3e50")
        header.pack(pady=15)
        
        self.btn_browse = tk.Button(root, text="Chagua Picha", command=self.load_image, font=("Arial", 11), bg="#3498db", fg="white", px=10, py=5)
        self.btn_browse.pack(pady=5)
        
        self.lbl_file = tk.Label(root, text="Hujachagua picha yoyote", font=("Arial", 9, "italic"), fg="#7f8c8d")
        self.lbl_file.pack(pady=5)
        
        lbl_size = tk.Label(root, text="Chagua Saizi na Mipangilio:", font=("Arial", 11, "bold"))
        lbl_size.pack(pady=10)
        
        self.size_option = tk.StringVar(value="Passport")
        
        sizes = [
            ("Passport Size (Picha 12 kwenye A4)", "Passport"),
            ("Picha za 5x7 (Picha 2 kwenye A4)", "5x7"),
            ("Full A4 (Picha 1 kwenye Ukurasa)", "A4")
        ]
        
        for text, mode in sizes:
            rb = tk.Radiobutton(root, text=text, variable=self.size_option, value=mode, font=("Arial", 10))
            rb.pack(anchor="w", padx=60, pady=2)
            
        self.btn_print = tk.Button(root, text="Tengeneza Ukurasa wa Ku-print (PDF)", command=self.generate_print_layout, font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", px=10, py=8)
        self.btn_print.pack(pady=25)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_file.config(text=f"Picha iliyochaguliwa: {filename}", fg="#27ae60")

    def generate_print_layout(self):
        if not self.image_path:
            messagebox.showwarning("Tahadhari", "Tafadhali chagua picha kwanza!")
            return

        try:
            a4_width, a4_height = 2480, 3508
            a4_canvas = Image.new("RGB", (a4_width, a4_height), "white")
            
            img = Image.open(self.image_path)
            mode = self.size_option.get()
            
            if mode == "Passport":
                pass_w, pass_h = 413, 531
                img_resized = img.resize((pass_w, pass_h), Image.Resampling.LANCZOS)
                
                start_x, start_y = 200, 200
                gap_x, gap_y = 100, 100
                
                for r in range(3):
                    for c in range(4):
                        x = start_x + c * (pass_w + gap_x)
                        y = start_y + r * (pass_h + gap_y)
                        a4_canvas.paste(img_resized, (x, y))
                        
            elif mode == "5x7":
                w_5x7, h_5x7 = 1500, 2100
                img_resized = img.resize((w_5x7, h_5x7), Image.Resampling.LANCZOS)
                a4_canvas.paste(img_resized, (490, 200))
                a4_canvas.paste(img_resized, (490, 2400))
                
            elif mode == "A4":
                margin = 100
                img_resized = img.resize((a4_width - (2 * margin), a4_height - (2 * margin)), Image.Resampling.LANCZOS)
                a4_canvas.paste(img_resized, (margin, margin))

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Documents", "*.pdf")],
                title="Hifadhi Ukurasa wa Kuprint"
            )
            
            if save_path:
                a4_canvas.save(save_path, "PDF", resolution=300.0)
                messagebox.showinfo("Mafanikio", f"File limehifadhiwa kikamilifu!\n\nLocation: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Kosa", f"Kuna tatizo limetokea: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoPrinterApp(root)
    root.mainloop()

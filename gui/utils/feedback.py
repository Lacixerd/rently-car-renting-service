import tkinter as tk
from tkinter import messagebox

class FeedbackService:
    @staticmethod
    def show(success, message):
        if success:
            messagebox.showinfo("Başarılı", message)
        else:
            messagebox.showerror("Hata", message)
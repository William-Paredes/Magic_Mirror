from tkinter import *

from time import strftime
from modules import weather, oura, quotes

from PIL import Image, ImageTk

quote_font = ("Noto Mono Bold", 30)
style_font = ("Noto Mono Bold", 35)



class MagicMirror(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(bg='black')
        

        self.im = ImageTk.PhotoImage(file = "./static/images/01d.png")
        
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.quoteFrame = Frame(self.master, background='black')
        # self.topFrame = Frame(self.master, bg = 'black', width=screen_width/3 , height=screen_height/3)
        # self.btmFrame = Frame(self.master, bg = 'black', width=screen_width/3 , height=screen_height/3)
        # self.mdlFrame = Frame(self.master, bg = 'black', width=screen_width/3 , height=screen_height/3)

        self.quoteFrame.grid(row=3, column=0, columnspan=3)
        self.master.grid_columnconfigure(1, weight = 1)
        self.master.grid_rowconfigure(3, weight = 1)

        self.draw_widgets()
        self.grid_widgets()

        self.time()


    def draw_widgets(self):
        self.clock_label =  Label(self.master, text="Time", background='black', foreground='white',font=style_font)
        self.date_label =  Label(self.master, text="Time", background='black', foreground='white',font=style_font)
        
        self.weather_image = Label(self.master, image = self.im, background='black')
        self.weather_label = Label(self.master, text="Current Weather", background='black', foreground='white',font=style_font)
        self.weather_description = Label(self.master, text="Weather Description", foreground='white', background='black',font=style_font) 
        
        self.oura_day_label = Label(self.master, text="Oura", background='black', foreground='white',font=style_font)
        self.oura_sleep_label = Label(self.master, text="Oura", background='black', foreground='white',font=style_font)
        self.oura_score_label = Label(self.master, text="Oura", background='black', foreground='white',font=style_font)
        
        self.quote_label = Message(self.quoteFrame, text="Quote", width = round(self.screen_width/3), background='black', foreground='white', font=quote_font)
        self.quote_author_label = Label(self.quoteFrame, text="Author", background='black', foreground='white', font=quote_font)
    def grid_widgets(self):
        self.clock_label.grid(row = 0, column = 0, sticky = W, pady = 2, padx=30)
        self.date_label.grid(row=0, column=1, sticky= EW, padx = 20, pady = 2)

        self.weather_image.grid(row= 0, column= 2, sticky=E)
        self.weather_label.grid(row = 0, column = 3, sticky = W, padx=(0,30), pady = 2)
        self.weather_description.grid(row = 2, column = 2, columnspan=2, sticky = E, padx=30)
        
        self.oura_day_label.grid(row = 5, column = 0, sticky = W, padx=30)
        self.oura_sleep_label.grid(row = 6, column = 0, sticky = W, padx=30)
        self.oura_score_label.grid(row = 7, column = 0, sticky = W, padx=30, pady=(0,30))
        
        self.quote_label.grid(sticky = NSEW)
        self.quote_author_label.grid(row=2, sticky=EW, pady= 20)
        

    def time(self):
        self.string = strftime('%I:%M %p')
        self.date = strftime('%a, %b %d')
        self.clock_label.config(text=self.string)
        self.date_label.config(text=self.date)
        self.clock_label.after(1000,self.time)

    def weather_update(self): 
        print('Updated weather')
        weather_data = weather.weather_request()
        image_name = weather_data['icon']
        icon = ImageTk.PhotoImage(file = f"./static/images/{image_name}.png")

        self.weather_label.config(text=f"{weather_data['temperature']}°")
        self.weather_description.config(text=weather_data['description'])
        self.weather_image.config(image=icon)
        self.weather_image.image = icon 
        self.weather_label.after(1800000, self.weather_update)

    def oura_update(self):
        oura_data = oura.oura_ring()
        self.oura_day_label.config(text = oura_data['sleep_date'])
        self.oura_score_label.config(text = oura_data['sleep_score'])
        self.oura_sleep_label.config(text = oura_data['sleep_duration'])
        self.oura_day_label.after(1800000, self.oura_update)
        

    def quote_update(self):
        quoteOfTheHour = quotes.quote_request()
        print(quoteOfTheHour)
        self.quote_label.config(text = f"{quoteOfTheHour['quote']}")
        self.quote_author_label.config(text= f"-{quoteOfTheHour['author']}")
        self.quote_label.after(3600000, self.quote_update)


root = Tk()
app = MagicMirror(master=root)

#SETUP
app.time()
app.oura_update()
app.weather_update()
app.quote_update()
app.mainloop()
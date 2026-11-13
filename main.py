
from tkinter import *
from time import strftime
from modules import weather, oura, quotes, spotify
import os
import sys
from PIL import Image, ImageTk
import calendar
from io import BytesIO
import requests

quote_font = ("Noto Mono Bold", 30)
style_font = ("Noto Mono Bold", 35)
weather_font = ("Noto Mono Bold", 30)
song_font = ("Noto Mono Bold", 45)
album_art_size = (500, 500)

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ['DISPLAY'] = ':0.0'


class MagicMirror(Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.configure(bg='black')

        self.im = ImageTk.PhotoImage(
            file="./static/images/01d.png"
        )

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.draw_frame()
        self.draw_widgets()
        self.grid_widgets()

        self.time()

    # --------------------------------------------------
    # FRAMES
    # --------------------------------------------------

    def draw_frame(self):

        self.headerFrame = Frame(
            self.master,
            background='black'
        )

        self.quoteFrame = Frame(
            self.master,
            background='black'
        )

        self.songFrame = Frame(
            self.master,
            background='black'
        )

        self.weatherFrame = Frame(
            self.headerFrame,
            background='black'
        )

        self.grid_frame()

    def grid_frame(self):

        # Header - Full screen width
        self.headerFrame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Quote - Bottom right
        self.quoteFrame.grid(
            row=7,
            column=0,
            sticky="se",
            padx=30
        )

        # Spotify - Bottom left
        self.songFrame.grid(
            row=7,
            column=0,
            sticky="sw",
            padx=30
        )

        # Header columns
        self.headerFrame.grid_columnconfigure(
            0, weight=0
        )

        self.headerFrame.grid_columnconfigure(
            1, weight=1
        )

        self.headerFrame.grid_columnconfigure(
            2, weight=0
        )

        # Main window configuration
        self.master.grid_columnconfigure(
            0, weight=1
        )

        self.master.grid_rowconfigure(
            0, weight=0
        )

        self.master.grid_rowconfigure(
            7, weight=1
        )

    # --------------------------------------------------
    # WIDGETS
    # --------------------------------------------------

    def draw_widgets(self):

        # Clock
        self.clock_label = Label(
            self.headerFrame,
            text="Time",
            background='black',
            foreground='white',
            font=style_font
        )

        # Date
        self.date_label = Label(
            self.headerFrame,
            text="Date",
            background='black',
            foreground='white',
            font=style_font
        )

        # Weather
        self.weather_image = Label(
            self.weatherFrame,
            image=self.im,
            background='black'
        )

        self.weather_label = Label(
            self.weatherFrame,
            text="Current Weather",
            background='black',
            foreground='white',
            font=style_font
        )

        self.weather_description = Label(
            self.master,
            text="Weather Description",
            foreground='white',
            background='black',
            font=style_font
        )

        # Spotify Album Artwork
        self.album_art_label = Label(
        self.songFrame,
        background='black'
        )

        # Spotify Now Playing
        self.spotify_label = Label(
            self.songFrame,
            text="♫ Nothing playing",
            background='black',
            foreground='white',
            font=song_font
        )

        self.spotify_artist_label = Label(
            self.songFrame,
            text="",
            background='black',
            foreground='gray',
            font=style_font
        )

        # Quote
        self.quote_label = Message(
            self.quoteFrame,
            text="Quote",
            width=round(self.screen_width / 3),
            background='black',
            foreground='white',
            font=weather_font
        )

        self.quote_author_label = Label(
            self.quoteFrame,
            text="Author",
            background='black',
            foreground='white',
            font=weather_font
        )

    # --------------------------------------------------
    # GRID LAYOUT
    # --------------------------------------------------

    def grid_widgets(self):

        # Clock - Left
        self.clock_label.grid(
            row=0,
            column=0,
            sticky=W,
            padx=30,
            pady=2
        )

        # Date - Center
        self.date_label.grid(
            row=0,
            column=1,
            sticky="",
            pady=2
        )

        # Weather - Right
        self.weatherFrame.grid(
            row=0,
            column=2,
            sticky=E,
            padx=(10, 30),
            pady=2
        )

        # Weather icon and temperature
        self.weather_image.pack(
            side=LEFT
        )

        self.weather_label.pack(
            side=LEFT,
            padx=(10, 0)
        )

        # Weather description - Right aligned
        self.weather_description.grid(
            row=2,
            column=0,
            sticky=E,
            padx=30
        )

        # Spotify - Bottom left
        self.album_art_label.pack(
            anchor=SW,
            pady=(0, 15)
        )

        self.spotify_label.pack(
            anchor=SW,
            pady=2
        )

        self.spotify_artist_label.pack(
            anchor=SW,
            pady=2
        )

        # Quote - Bottom right
        self.quote_label.pack(
            anchor=E
        )

        self.quote_author_label.pack(
            anchor=E
        )

    # --------------------------------------------------
    # CLOCK
    # --------------------------------------------------

    def time(self):

        self.string = strftime('%I:%M %p')
        self.date = strftime('%a, %b %d')

        self.clock_label.config(
            text=self.string
        )

        self.date_label.config(
            text=self.date
        )

        self.clock_label.after(
            1000,
            self.time
        )

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    def weather_update(self):

        print('Updated weather')

        weather_data = weather.weather_request()

        image_name = weather_data['icon']

        icon = ImageTk.PhotoImage(
            file=f"./static/images/{image_name}.png"
        )

        self.weather_label.config(
            text=f"{weather_data['temperature']}°"
        )

        self.weather_description.config(
            text=weather_data['description']
        )

        self.weather_image.config(
            image=icon
        )

        self.weather_image.image = icon

        self.weather_label.after(
            1800000,
            self.weather_update
        )

    # --------------------------------------------------
    # QUOTES
    # --------------------------------------------------

    def quote_update(self):

        quoteOfTheHour = quotes.quote_request()

        print(quoteOfTheHour)

        self.quote_label.config(
            text=f"{quoteOfTheHour['quote']}"
        )

        self.quote_author_label.config(
            text=f"- {quoteOfTheHour['author']}"
        )

        self.quote_label.after(
            3600000,
            self.quote_update
        )

    # --------------------------------------------------
    # SPOTIFY
    # --------------------------------------------------

        
    def spotify_update(self):

        try:

            track = spotify.currently_playing()

            if track is None:

                self.spotify_label.config(text="")
                self.spotify_artist_label.config(text="")
                self.album_art_label.config(image="")
                self.album_art_label.image = None

            else:

                if track["is_playing"]:

                    self.spotify_label.config(
                        text=f"{track['name']}"
                    )

                    self.spotify_artist_label.config(
                        text=f"by {track['artist']}"
                    )

                else:

                    self.spotify_label.config(
                        text=f"Ⅱ {track['name']}"
                    )

                    self.spotify_artist_label.config(
                        text=f"Paused • {track['artist']}"
                    )

                # Download and display album artwork
                image_url = track.get("image_url")

                if image_url:

                    response = requests.get(
                        image_url,
                        timeout=10
                    )

                    response.raise_for_status()

                    artwork = Image.open(
                        BytesIO(response.content)
                    )

                    artwork = artwork.resize(
                        album_art_size,
                        Image.Resampling.LANCZOS
                    )

                    album_image = ImageTk.PhotoImage(artwork)

                    self.album_art_label.config(
                        image=album_image
                    )

                    # Keep a reference to prevent garbage collection
                    self.album_art_label.image = album_image

                else:

                    self.album_art_label.config(image="")
                    self.album_art_label.image = None

        except Exception as e:

            print(f"Spotify error: {e}")

        # Check Spotify every 15 seconds
        self.spotify_label.after(
            15000,
            self.spotify_update
        )



# --------------------------------------------------
# MAIN
# --------------------------------------------------

root = Tk()

root.attributes('-fullscreen', True)

app = MagicMirror(master=root)

# SETUP
app.time()
app.spotify_update()
app.weather_update()
app.quote_update()

app.mainloop()

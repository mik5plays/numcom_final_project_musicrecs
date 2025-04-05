from commands import *
from tkinter import ttk

def create_window_track_info(window, url, title, album_title, artist, tags, img_tk=None):

    # For creating new windows, but we recycle the old one each time.
    for widget in window.winfo_children():
        widget.destroy()

    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((250,250))
        img_tk = ImageTk.PhotoImage(img)
    except:
        # resorting to default image
        response = requests.get("https://cdn-icons-png.flaticon.com/512/46/46499.png")
        img = Image.open(BytesIO(response.content))
        img = img.resize((250,250))
        img_tk = ImageTk.PhotoImage(img)

    image_label = tk.Label(
        window,
        image=img_tk,
        pady=20
    )

    title_and_artist_label = tk.Label(
        window,
        text=f"{title}\n{artist}",
        font=("Ubuntu", 15, "bold"),
        padx=20,
        wraplength=300,
    )

    album_label = tk.Label(
        window,
        text=f"{album_title}",
        font=("Ubuntu", 13, "italic"),
        wraplength=300,
        padx=20,
        pady=5
    )

    # Construct a list of tags
    top_tags = ", ".join([x.lower() for x in tags])

    genre_label = tk.Label(
        window,
        text=top_tags,
        font=("Ubuntu", 10),
        bg="#f0f0f0",
        fg="#777777",  # Light gray for tags
        relief="sunken",
        padx=5,
        wraplength=300,
    )

    image_label.pack(fill="x", expand=True)
    title_and_artist_label.pack(fill="x", expand=True)
    album_label.pack(fill="x", expand=True)
    genre_label.pack(fill="x", expand=True)

    window.img_tk = img_tk
    return img_tk

def create_lyrics_info(window, url, title, album_title, artist, tags):

    for widget in window.winfo_children():
        widget.destroy()

    lyrics = get_lyrics(artist, title)

    container = tk.Frame(window, bg="#f0f0f0")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#f0f0f0", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    lyrics_frame = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=lyrics_frame, anchor="nw")

    lyrics_label = tk.Label(
        lyrics_frame,
        text=lyrics,
        font=("Ubuntu", 10),
        bg="#f0f0f0",
        fg="#777777",
        relief="sunken",
        padx=5,
        wraplength=300,
        justify="left"
    )

    lyrics_label.pack(fill="x", expand=True)

    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    lyrics_frame.bind("<Configure>", configure_scrollregion)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

def create_window_artist_info(window, url, artist, tags):

    for widget in window.winfo_children():
        widget.destroy()

    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((250,250))
        img_tk = ImageTk.PhotoImage(img)
    except:
        # resorting to default image
        response = requests.get("https://cdn-icons-png.flaticon.com/512/46/46499.png")
        img = Image.open(BytesIO(response.content))
        img = img.resize((250,250))
        img_tk = ImageTk.PhotoImage(img)

    image_label = tk.Label(
        window,
        image=img_tk,
        pady=20
    )

    artist_label = tk.Label(
        window,
        text=f"{artist}",
        font=("Ubuntu", 15, "bold"),
        padx=20,
        wraplength=300,
    )

    top_tags = ", ".join([x.lower() for x in tags])

    genre_label = tk.Label(
        window,
        text=top_tags,
        font=("Ubuntu", 10),
        bg="#f0f0f0",
        fg="#777777",  # Light gray for tags
        relief="sunken",
        padx=5,
        wraplength=300,
    )

    image_label.pack(fill="x", expand=True)
    artist_label.pack(fill="x", expand=True)
    genre_label.pack(fill="x", expand=True)

    window.img_tk = img_tk
    return img_tk

def search_artist():
    START_WINDOW.destroy()

    query = input("Enter a search query (for an artist)\n> ")
    print(f"Searching for {query}...")
    print(f"{DIVIDER}\nHere are the top three results, choose the one that you want.\n{DIVIDER}")

    results = search_for_artists(query)
    resultIndex = [0]

    def cycle_through_frames():
        resultIndex[0] = (resultIndex[0] + 1) % len(results)

        artist_info = get_artist_info(results[resultIndex[0]]['name'])
        create_window_artist_info(ARTISTS_WINDOW_FRAME, *artist_info)

    def choose_artist():
        nonlocal results, resultIndex, ARTISTS_WINDOW_FRAME

        def close_window():
            ARTISTS_WINDOW.destroy()

        def cycle_through_frames_suggestions():
            resultIndex[0] = (resultIndex[0] + 1) % len(results)

            artist_info = get_artist_info(results[resultIndex[0]]['name'])
            create_window_artist_info(ARTISTS_WINDOW_FRAME, *artist_info)

        chosen_artist_info = get_artist_info(results[resultIndex[0]]['name'])
        url, artist, tags = chosen_artist_info

        print(f"{DIVIDER}\nYou have chosen {artist}. Finding recommendations...\n{DIVIDER}")

        for widget in ARTISTS_WINDOW.winfo_children():
            widget.destroy()

        results = get_similar_artist_info(artist)
        resultIndex = [0]

        ARTISTS_WINDOW.title("Similar Tracks")

        ARTISTS_WINDOW_FRAME = tk.Frame(ARTISTS_WINDOW, width=400)
        ARTISTS_WINDOW_FRAME.pack(fill="x", expand=True)

        artist_info = get_artist_info(results[resultIndex[0]]['name'])
        create_window_artist_info(ARTISTS_WINDOW_FRAME, *artist_info)

        CYCLE_BUTTON = tk.Button(ARTISTS_WINDOW, text="Next Recommendation", command=cycle_through_frames_suggestions, padx=5, pady=5)
        CYCLE_BUTTON.pack()

        CLOSE_BUTTON = tk.Button(ARTISTS_WINDOW, text="Close", command=close_window, padx=5, pady=5)
        CLOSE_BUTTON.pack()

    ARTISTS_WINDOW = tk.Tk()
    ARTISTS_WINDOW.title("Search Results")

    ARTISTS_WINDOW_FRAME = tk.Frame(ARTISTS_WINDOW, width=400)
    ARTISTS_WINDOW_FRAME.pack()

    artist_info = get_artist_info(results[resultIndex[0]]['name'])
    create_window_artist_info(ARTISTS_WINDOW_FRAME, *artist_info)

    CYCLE_BUTTON = tk.Button(ARTISTS_WINDOW, text="Cycle Result", command=cycle_through_frames, padx=5, pady=5)
    CYCLE_BUTTON.pack(side=tk.LEFT)

    CHOOSE_SONG = tk.Button(ARTISTS_WINDOW, text="Choose Artist", bg="#00FF00", command=choose_artist, padx=5, pady=5)
    CHOOSE_SONG.pack(side=tk.RIGHT)

    ARTISTS_WINDOW.mainloop()

def search_song():
    START_WINDOW.destroy()

    query = input("Enter a search query (for a song)\n> ")
    print(f"Searching for {query}...")
    print(f"{DIVIDER}\nHere are the top three results, choose the one that you want.\n{DIVIDER}")

    results = search_for_tracks(query)
    resultIndex = [0]

    def cycle_through_frames():
        resultIndex[0] = (resultIndex[0] + 1) % len(results)

        track_info = get_track_info(results[resultIndex[0]]['artist'], results[resultIndex[0]]['name'])
        create_window_track_info(SONGS_WINDOW_FRAME, *track_info)

    def choose_song():
        nonlocal results, resultIndex, SONGS_WINDOW_FRAME

        LYRICS_WINDOW = tk.Tk()
        LYRICS_WINDOW.title("Lyrics")

        def close_window():
            SONGS_WINDOW.destroy()
            LYRICS_WINDOW.destroy()

        def cycle_through_frames_suggestions():
            resultIndex[0] = (resultIndex[0] + 1) % len(results)

            track_info = get_track_info(results[resultIndex[0]]['artist']['name'], results[resultIndex[0]]['name'])
            create_window_track_info(SONGS_WINDOW_FRAME, *track_info)
            create_lyrics_info(LYRICS_WINDOW_FRAME, *track_info)

        chosen_track_info = get_track_info(results[resultIndex[0]]['artist'], results[resultIndex[0]]['name'])
        url, title, album_title, artist, tags = chosen_track_info
        print(f"{DIVIDER}\nYou have chosen {title} by {artist}. Finding recommendations...\n{DIVIDER}")

        for widget in SONGS_WINDOW.winfo_children():
            widget.destroy()

        results = get_similar_track_info(artist, title)
        resultIndex = [0]

        SONGS_WINDOW.title("Similar Tracks")

        LYRICS_WINDOW_FRAME = tk.Frame(LYRICS_WINDOW, width=400)
        SONGS_WINDOW_FRAME = tk.Frame(SONGS_WINDOW, width=400)

        SONGS_WINDOW_FRAME.pack(fill="x", expand=True)
        LYRICS_WINDOW_FRAME.pack(fill="x", expand=True)

        track_info = get_track_info(results[resultIndex[0]]['artist']['name'], results[resultIndex[0]]['name'])
        create_window_track_info(SONGS_WINDOW_FRAME, *track_info)
        create_lyrics_info(LYRICS_WINDOW_FRAME, *track_info)

        CYCLE_BUTTON = tk.Button(SONGS_WINDOW, text="Next Recommendation", command=cycle_through_frames_suggestions, padx=5, pady=5)
        CYCLE_BUTTON.pack()

        CLOSE_BUTTON = tk.Button(SONGS_WINDOW, text="Close", command=close_window, padx=5, pady=5)
        CLOSE_BUTTON.pack()

        LYRICS_WINDOW.mainloop()

    SONGS_WINDOW = tk.Tk()
    SONGS_WINDOW.title("Search Results")

    SONGS_WINDOW_FRAME = tk.Frame(SONGS_WINDOW, width=400)
    SONGS_WINDOW_FRAME.pack()

    track_info = get_track_info(results[resultIndex[0]]['artist'], results[resultIndex[0]]['name'])
    create_window_track_info(SONGS_WINDOW_FRAME, *track_info)

    CYCLE_BUTTON = tk.Button(SONGS_WINDOW, text="Cycle Result", command=cycle_through_frames, padx=5, pady=5)
    CYCLE_BUTTON.pack(side=tk.LEFT)

    CHOOSE_SONG = tk.Button(SONGS_WINDOW, text="Choose Song", bg="#00FF00", command=choose_song, padx=5, pady=5)
    CHOOSE_SONG.pack(side=tk.RIGHT)

    SONGS_WINDOW.mainloop()

"""
The Main Program
- mix of tkinter + using the Python terminal
"""

DIVIDER = "***********************"
print(f"{DIVIDER}\n Music Recommendation Tool\n> Enter an artist or song, then you'll get recommendations!\n{DIVIDER}")

finished = False

def end_program():
    global finished
    finished = True
    START_WINDOW.quit()

while not finished:

    START_WINDOW = tk.Tk()
    START_WINDOW.title("Music Recommendation Tool")

    ARTIST_BUTTON = tk.Button(
        START_WINDOW,
        text="I want an artist!",
        relief="raised",
        font=("Arial", 10),
        command=search_artist)
    ARTIST_BUTTON.pack(side='left', padx=50, pady=20)

    SONG_BUTTON = tk.Button(
        START_WINDOW,
        text="I want a song!",
        relief="raised",
        padx=10,
        font=("Arial", 10),
        command=search_song)
    SONG_BUTTON.pack(side='left', padx=50, pady=20)

    EXIT_BUTTON = tk.Button(
        START_WINDOW,
        text="Finish",
        relief="raised",
        fg="#FF0000",
        padx=10,
        font=("Arial", 10),
        anchor="e",
        command=end_program)
    EXIT_BUTTON.pack(pady=5)

    START_WINDOW.mainloop() # show the first window

print(f"{DIVIDER}\nThanks for using this tool!\n{DIVIDER}")
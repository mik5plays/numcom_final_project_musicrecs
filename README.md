# numcom_final_project_musicrecs
Rudimentary Python-based music recommendation tool

A rudimentary Python program that utilizes last.fm’s API and Tkinter to create a quick and simple tool that recommends artists or songs based on given search queries. As of now, it handles basic searches for artists and songs + gives a list of recommendations. Note that it is small, and I do plan on adding more features in the foreseeable future as a way to practice writing more sophisticated programs + fully utilizing APIs.

I chose to use last.fm’s API because Spotify’s API deprecated its “Get Recommendations” API which used to be really useful for finding recommendations and creating curated playlists. However, there is still use for Spotify’s API which I might integrate into my program full-time later.

I am aware that this project technically doesn’t utilize any concepts taught in Numerical Computation, but its main purpose is just to help utilize my skill set and improve on small but significant “life” skills such as properly reading docs, troubleshooting, and making my programs more modular.

List of current features:
- Search that gives multiple curated results, allowing the user to choose the one that is most accurate (or what they want the most)
- A carousel of similar artists and songs based on last.fm’s API, and some contextual information that might be useful for the user.

Proposed features (will do in my own time):
- Genre recommendations
- Generating short playlists based on similar tracks, can be done by utilizing other API’s including and not limited to Spotify.
- Moving away from Tkinter in favour of a more comprehensive and customizable GUI, currently looking to learn more about Flask.
- Cleaning the code to make it more modular (this does include restructuring and creating classes, right now the program does what it is supposed to but it is quite messy)

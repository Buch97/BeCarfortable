import random
import vlc
import time

from server.mainServer import FilmScene

scenes = [FilmScene("Seven", 6, "dramatic"), FilmScene("Sixth sense", 144, "dramatic"), FilmScene("Boyz n the hood", 222, "dramatic"),
          FilmScene("Braveheart", 354, "dramatic"), FilmScene("Forrest gump", 564, "dramatic"), FilmScene("Scarface", 694, "dramatic"),
          FilmScene("Terminator 2", 873, "dramatic"), FilmScene("E.T.", 947, "dramatic"), FilmScene("The godfather", 1033, "dramatic"),
          FilmScene("Inglorious basterds", 1229, "dramatic"), FilmScene("Life", 1601, "comic"), FilmScene("Austin powers", 1643, "comic"),
          FilmScene("Happy gilmore", 1718, "comic"), FilmScene("Old school", 1782, "comic"), FilmScene("Anchorman", 1830, "comic"), FilmScene("Wedding crashers", 1907, "comic"),
          FilmScene("Walkhard", 1960, "comic"), FilmScene("Talladega nights", 2032, "comic"), FilmScene("Superbad", 2129, "comic"), FilmScene("The 40 year old virgin", 2211, "comic")]

clip_duration = 1478
def vlc_player():
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("videos/top_movie_scenes.mp4")

    # start playing video
    media.get_mrl()
    player.set_media(media)
    player.play()

    while True:
        scene_number = random.randrange(0, len(scenes), 1)
        print(scenes[scene_number].get_title())
        player.set_time(scenes[scene_number].get_starting_time() * 1000)
        #if scene_number == len(scenes):
         #   time.sleep(clip_duration - scenes[scene_number].get_starting_time())
        #else:
          #  time.sleep(scenes[scene_number + 1].get_starting_time() - scenes[scene_number].get_starting_time())
        time.sleep(2)
        scenes.pop(scene_number)
        # if negative emotion detected jump to next happy scene
          # while mood remain negative
           # play scene
          # continue
        if len(scenes) == 0:
            quit()



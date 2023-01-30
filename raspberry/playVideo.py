import random
import vlc
import time

from raspberry.film_scene import FilmScene

dramatic_scenes = [FilmScene("Seven", 6, "dramatic"), FilmScene("Sixth sense", 144, "dramatic"), FilmScene("Boyz n the hood", 222, "dramatic"),
          FilmScene("Braveheart", 354, "dramatic"), FilmScene("Forrest gump", 564, "dramatic"), FilmScene("Scarface", 694, "dramatic"),
          FilmScene("Terminator 2", 873, "dramatic"), FilmScene("E.T.", 947, "dramatic"), FilmScene("The godfather", 1033, "dramatic"),
          FilmScene("Inglorious basterds", 1229, "dramatic")]

comic_scenes = [FilmScene("Life", 1601, "comic"), FilmScene("Austin powers", 1643, "comic"),
          FilmScene("Happy gilmore", 1718, "comic"), FilmScene("Old school", 1782, "comic"), FilmScene("Anchorman", 1830, "comic"), FilmScene("Wedding crashers", 1907, "comic"),
          FilmScene("Walkhard", 1960, "comic"), FilmScene("Talladega nights", 2032, "comic"), FilmScene("Superbad", 2129, "comic"), FilmScene("The 40 year old virgin", 2211, "comic")]


clip_duration = 1478


def vlc_player(emotion):
    global skip
    needToSkip = False
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("videos/top_movie_scenes.mp4")

    # start playing video
    media.get_mrl()
    player.set_media(media)
    player.play()

    while True:
        scenes = []

        if needToSkip is False:
            scenes = comic_scenes + dramatic_scenes
        elif needToSkip is True and emotion == "sad":
            scenes = comic_scenes
        elif needToSkip is True and emotion == "happy":
            scenes = dramatic_scenes

        scene_number = random.randrange(0, len(scenes), 1)
        print(scenes[scene_number].get_title())
        player.set_time(scenes[scene_number].get_starting_time() * 1000)
        if scene_number == len(scenes):
            duration = clip_duration - scenes[scene_number].get_starting_time()
        else:
            duration = scenes[scene_number + 1].get_starting_time() - scenes[scene_number].get_starting_time()
        elapsed = 0
        while elapsed < duration or skip is True:
            time.sleep(1)
            elapsed += 1
        if skip is True:
            needToSkip = True
            skip = False

        if needToSkip is False:
            if scene_number < 10:
                comic_scenes.pop(scene_number)
            else:
                dramatic_scenes.pop(scene_number % len(comic_scenes))
        elif needToSkip is True and emotion == "sad":
            dramatic_scenes.pop(scene_number)
        elif needToSkip is True and emotion == "happy":
            comic_scenes.pop(scene_number)

        if len(scenes) == 0:
            quit()



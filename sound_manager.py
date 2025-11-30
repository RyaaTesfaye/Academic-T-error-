import pygame

class SoundManager:
    def __init__(self):
        self.sfx_files = {
            "laser": "lib/sfx/laser_mini.wav",
            "bomb": "lib/sfx/explosion_enem.wav",
            "glitch": "lib/sfx/glitch_char.wav"
        }
        self.sfx = {}
        
        self.bgm_playlist = [
            {"name": "33x", "path": "lib/sfx/BGM_PERUNGGU.ogg"},
            {"name": "Hampstead", "path": "lib/sfx/BGM_HAMPSTEAD.ogg"}
        ]
        self.current_bgm_index = 0 

        self.load_all_sfx()
        
        self.load_current_bgm()

    def load_all_sfx(self):
        for name, file_path in self.sfx_files.items():
            try:
                sound = pygame.mixer.Sound(file_path)
                sound.set_volume(0.7)
                self.sfx[name] = sound
            except Exception as e:
                print(f"Gagal load SFX '{name}': {e}")
                self.sfx[name] = None

    def load_current_bgm(self):
        if not self.bgm_playlist: 
            return
        
        song = self.bgm_playlist[self.current_bgm_index]
        try:
            pygame.mixer.music.load(song["path"])
            pygame.mixer.music.set_volume(0.2)
        except Exception as e:
            print(f"Gagal load BGM '{song['name']}': {e}")

    def next_bgm(self):
        self.current_bgm_index = (self.current_bgm_index + 1) % len(self.bgm_playlist)
        self.load_current_bgm()
        self.play_bgm(loops=-1)

    def prev_bgm(self):
        self.current_bgm_index = (self.current_bgm_index - 1) % len(self.bgm_playlist)
        self.load_current_bgm()
        self.play_bgm(loops=-1)

    def get_current_bgm_name(self):
        if not self.bgm_playlist: 
            return "No Music"
        return self.bgm_playlist[self.current_bgm_index]["name"]

    def play_sfx(self, name):
        if name in self.sfx and self.sfx[name]:
            self.sfx[name].play()

    def play_bgm(self, loops=-1):
        try:
            if not pygame.mixer.music.get_busy(): 
                pygame.mixer.music.play(loops=loops)
        except:
            pass
            
    def force_play_bgm(self):
        try:
            pygame.mixer.music.play(loops=-1)
        except:
            pass

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def pause_bgm(self):
        pygame.mixer.music.pause()

    def unpause_bgm(self):
        pygame.mixer.music.unpause()
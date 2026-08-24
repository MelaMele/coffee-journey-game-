import pgzrun
import random

# የስክሪን ስፋት እና ቁመት
WIDTH = 800
HEIGHT = 600

# የጨዋታው ርዕስ
TITLE = "የቡና ጉዞ፡ ከካፋ እስከ ዓለም - ደረጃ 1"

# ገጸ-ባህሪያት (Actors)
kaldi = Actor('kaldi')
kaldi.pos = (100, 500)  # የካልዲ መነሻ ቦታ

coffee = Actor('coffee')
coffee.pos = (random.randint(100, 700), random.randint(100, 500))

# ውጤት እና ደረጃ
score = 0
game_over = False

def draw():
    """በስክሪኑ ላይ ምስሎችን እና ጽሁፎችን መሳያ"""
    screen.clear()
    
    # የካፋ ደን የጀርባ ስዕል
    screen.blit('kaffa_bg', (0, 0))
    
    # ገጸ-ባህሪያትን መሳል
    kaldi.draw()
    coffee.draw()
    
    # የቡና መቁጠሪያ (Scoreboard)
    screen.draw.text(f"የተሰበሰበ ቡና: {score}/10", (20, 20), fontsize=35, color="yellow")
    
    # 10 ቡና ሲሰበሰብ የሚወጣ የደስታ መግለጫ
    if game_over:
        screen.draw.text("እንኳን ደስ አለዎት!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=55, color="white")
        screen.draw.text("የካፋን ደን በውጤታማነት አጠናቀዋል!", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=40, color="gold")

def update():
    """የካልዲ እንቅስቃሴ እና የጨዋታው ህግጋት"""
    global score, game_over
    
    if game_over:
        return

    # በቁልፍ ሰሌዳው ቀስቶች የካልዲ እንቅስቃሴ
    if keyboard.left and kaldi.left > 0:
        kaldi.x -= 5
    if keyboard.right and kaldi.right < WIDTH:
        kaldi.x += 5
    if keyboard.up and kaldi.top > 0:
        kaldi.y -= 5
    if keyboard.down and kaldi.bottom < HEIGHT:
        kaldi.y += 5

    # ካልዲ የቡና ፍሬውን ሲነካው
    if kaldi.colliderect(coffee):
        score += 1
        # የቡና ፍሬውን ወደ አዲስ ቦታ መቀየር
        coffee.pos = (random.randint(100, 700), random.randint(100, 500))
        
    # 10 ቡና ሲሰበስብ ጨዋታው ያበቃል
    if score >= 10:
        game_over = True

# ጨዋታውን ማስነሻ
pgzrun.go()

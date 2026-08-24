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
coffee.pos = (random.randint(50, 750), random.randint(50, 450))

# ውጤት እና መቁጠሪያ
score = 0
game_over = False

def draw():
    """ስክሪኑ ላይ ያሉትን ነገሮች መሳያ"""
    screen.clear()
    # የጀርባ ስዕል (ካለ)
    try:
        screen.blit('kaffa_bg', (0, 0))
    except:
        screen.fill((34, 139, 34))  # የካፋ ደን አረንጓዴ ቀለም
    
    kaldi.draw()
    coffee.draw()
    
    # የቡና ፍሬ መቁጠሪያ (Scoreboard)
    screen.draw.text(f"የተሰበሰበ ቡና: {score}", (20, 20), fontsize=35, color="yellow")
    
    if game_over:
        screen.draw.text("እንኳን ደስ አለዎት! የካፋን ደን ጨርሰዋል!", center=(WIDTH//2, HEIGHT//2), fontsize=45, color="white")

def update():
    """የገጸ-ባህሪያት እንቅስቃሴ እና ሎጂክ"""
    global score, game_over
    
    if game_over:
        return

    # የካልዲ እንቅስቃሴ (በአራቱ ቀስቶች)
    if keyboard.left and kaldi.left > 0:
        kaldi.x -= 5
    if keyboard.right and kaldi.right < WIDTH:
        kaldi.x += 5
    if keyboard.up and kaldi.top > 0:
        kaldi.y -= 5
    if keyboard.down and kaldi.bottom < HEIGHT:
        kaldi.y += 5

    # ካልዲ የቡና ፍሬውን ሲነካው (Collision Detection)
    if kaldi.colliderect(coffee):
        score += 1
        # ቡናውን አዲስ ቦታ ላይ በዘፈቀደ (Random) ማስቀመጥ
        coffee.pos = (random.randint(50, 750), random.randint(50, 450))
        
    # 10 ቡና ሲሰበስብ ደረጃውን ያልፋል
    if score >= 10:
        game_over = True

# ጨዋታውን ማስጀመሪያ
pgzrun.go()

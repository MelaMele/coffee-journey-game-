import pgzrun
import random
import asyncio

# የስክሪን ስፋት እና ቁመት
WIDTH = 800
HEIGHT = 600

# የጨዋታው ርዕስ
TITLE = "የቡና ጉዞ፡ ከካፋ እስከ ዓለም - ደረጃ 2"

# ገጸ-ባህሪያት (Actors)
kaldi = Actor('kaldi')
kaldi.pos = (100, 500)

coffee = Actor('coffee')
coffee.pos = (random.randint(100, 700), random.randint(100, 500))

# ደረጃ 2፡ ተንቀሳቃሽ መሰናክል (መጀመሪያ ካልዲ እንዳይነካው ራቅ ብሎ ይጀምራል)
hyena = Actor('coffee')  # ምስል እስኪዘጋጅ የቡናን/ባዶ ምስል ይጠቀማል
hyena.pos = (400, 300)
hyena_speed = 4

# ጨዋታ ሁኔታዎች
score = 0
lives = 3
game_over = False
won = False

def draw():
    """በስክሪኑ ላይ ምስሎችን እና ጽሁፎችን መሳያ"""
    screen.clear()
    
    # የካፋ ደን የጀርባ ስዕል
    screen.blit('kaffa_bg', (0, 0))
    
    # ገጸ-ባህሪያትን መሳል
    kaldi.draw()
    coffee.draw()
    
    # ተንቀሳቃሽ መሰናክሉን በጽሁፍና በቀይ ቅርፅ ማሳየት
    screen.draw.filled_circle(hyena.pos, 20, "red")
    screen.draw.text("አደጋ!", center=hyena.pos, fontsize=20, color="white")
    
    # የቡና እና የህይወት መቁጠሪያ (Dashboard)
    screen.draw.text(f"የተሰበሰበ ቡና: {score}/15", (20, 20), fontsize=30, color="yellow")
    screen.draw.text(f"ህይወት (Lives): {'❤️ ' * lives}", (20, 60), fontsize=30, color="red")
    
    # 15 ቡና ሲሰበሰብ የሚወጣ የደስታ መግለጫ
    if won:
        screen.draw.text("እንኳን ደስ አለዎት!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=50, color="white")
        screen.draw.text("ደረጃ 2ን በስኬት አጠናቀዋል!", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=40, color="gold")
        
    # ህይወት ሲያልቅ
    if game_over and not won:
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=60, color="red")
        screen.draw.text("በድጋሚ ለመሞከር ገጹን Refresh ያድርጉ", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update():
    """የካልዲ እና የመሰናክሉ እንቅስቃሴ"""
    global score, lives, game_over, won, hyena_speed
    
    if game_over or won:
        return

    # 1. የካልዲ እንቅስቃሴ
    if keyboard.left and kaldi.left > 0:
        kaldi.x -= 5
    if keyboard.right and kaldi.right < WIDTH:
        kaldi.x += 5
    if keyboard.up and kaldi.top > 0:
        kaldi.y -= 5
    if keyboard.down and kaldi.bottom < HEIGHT:
        kaldi.y += 5

    # 2. የመሰናክሉ (Hyena) አውቶማቲክ እንቅስቃሴ (ወደ ግራና ቀኝ)
    hyena.x += hyena_speed
    if hyena.right >= WIDTH or hyena.left <= 0:
        hyena_speed = -hyena_speed  # አቅጣጫ መቀየር

    # 3. ካልዲ ቡና ሲሰበስብ
    if kaldi.colliderect(coffee):
        score += 1
        coffee.pos = (random.randint(100, 700), random.randint(100, 500))
        
    # 4. ካልዲ ከመሰናክሉ ጋር ሲጋጭ
    if kaldi.colliderect(hyena):
        lives -= 1
        kaldi.pos = (100, 500)  # ካልዲ ወደ መጀመሪያ ቦታው ይመለሳል
        if lives <= 0:
            game_over = True
            
    # 5. 15 ቡና ሲደርስ ማሸነፍ
    if score >= 15:
        won = True
        game_over = True

# ለWeb (Pygbag) እና ለLocal ማስነሻ የሚያገለግል Async Main loop
async def main():
    while True:
        update()
        draw()
        await asyncio.sleep(0)

# በዌብ ላይ ሲሆን የሚሰራው
asyncio.run(main())

import pgzrun
import random
import asyncio
import time

# የስክሪን ስፋት እና ቁመት
WIDTH = 800
HEIGHT = 600

# የጨዋታው ርዕስ
TITLE = "የቡና ጉዞ፡ ከካፋ እስከ ዓለም - ደረጃ 3 (የአዲስ አበባ ንግድ)"

# ገጸ-ባህሪያት (Actors)
kaldi = Actor('kaldi')
kaldi.pos = (100, 500)

# ሁለቱ የቡና አይነቶች
raw_coffee = Actor('coffee')
raw_coffee.pos = (random.randint(100, 700), random.randint(100, 500))

roasted_coffee = Actor('coffee')
roasted_coffee.pos = (random.randint(100, 700), random.randint(100, 500))

# ተንቀሳቃሽ መሰናክል
obstacle = Actor('coffee')
obstacle.pos = (400, 200)
obstacle_speed = 5

# የጨዋታ ሁኔታዎች
coins = 0
lives = 3
timer = 60  # 60 ሰከንድ ገደብ
start_time = time.time()

game_over = False
won = False

def draw():
    """በስክሪኑ ላይ ምስሎችን እና ጽሁፎችን መሳያ"""
    screen.clear()
    
    # የጀርባ ቀለም (ለከተማ/ንግድ ቦታ የሚሆን)
    screen.fill((34, 139, 34))
    
    # ገጸ-ባህሪያትን መሳል
    kaldi.draw()
    raw_coffee.draw()
    
    # የተቆላ ቡናን በልዩ ቀለም (ወርቃማ) አጉልቶ ማሳየት
    roasted_coffee.draw()
    screen.draw.circle(roasted_coffee.pos, 25, "gold")
    
    # መሰናክል
    screen.draw.filled_circle(obstacle.pos, 20, "purple")
    screen.draw.text("መሰናክል", center=obstacle.pos, fontsize=16, color="white")
    
    # ዳሽቦርድ (የመረጃ ሰሌዳ)
    screen.draw.text(f"ካፒታል: {coins}/50 ETB", (20, 20), fontsize=28, color="yellow")
    screen.draw.text(f"ህይወት: {'❤️ ' * lives}", (20, 55), fontsize=28, color="red")
    screen.draw.text(f"ቀርቲ ጊዜ: {max(0, timer)} ሰከንድ", (20, 90), fontsize=28, color="cyan")
    
    # ማሸነፍ
    if won:
        screen.draw.text("እንኳን ደስ አለዎት!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=50, color="white")
        screen.draw.text("የቡና ንግዱን በታላቅ ስኬት አጠናቀዋል!", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=35, color="gold")
        
    # መሸነፍ
    if game_over and not won:
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=60, color="red")
        screen.draw.text("ጊዜ ወይም ህይወት አልቋል። በድጋሚ ይሞክሩ!", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update():
    """የጨዋታው ዋና ሎጂክ"""
    global coins, lives, timer, start_time, game_over, won, obstacle_speed
    
    if game_over or won:
        return

    # 1. የጊዜ መቁጠሪያ
    elapsed = int(time.time() - start_time)
    timer = 60 - elapsed
    if timer <= 0:
        game_over = True

    # 2. የካልዲ እንቅስቃሴ
    if keyboard.left and kaldi.left > 0:
        kaldi.x -= 6
    if keyboard.right and kaldi.right < WIDTH:
        kaldi.x += 6
    if keyboard.up and kaldi.top > 0:
        kaldi.y -= 6
    if keyboard.down and kaldi.bottom < HEIGHT:
        kaldi.y += 6

    # 3. የመሰናክል እንቅስቃሴ
    obstacle.x += obstacle_speed
    if obstacle.right >= WIDTH or obstacle.left <= 0:
        obstacle_speed = -obstacle_speed

    # 4. ቡና መሰብሰብ
    # ያልተቆላ ቡና (+1 ካፒታል)
    if kaldi.colliderect(raw_coffee):
        coins += 1
        raw_coffee.pos = (random.randint(100, 700), random.randint(100, 500))
        
    # የተቆላ ቡና (+3 ካፒታል)
    if kaldi.colliderect(roasted_coffee):
        coins += 3
        roasted_coffee.pos = (random.randint(100, 700), random.randint(100, 500))

    # 5. ከመሰናክል ጋር መጋጨት
    if kaldi.colliderect(obstacle):
        lives -= 1
        kaldi.pos = (100, 500)
        if lives <= 0:
            game_over = True

    # 6. የድል ሁኔታ (50 ካፒታል ሲደርስ)
    if coins >= 50:
        won = True
        game_over = True

# Async Loop ለ Web (Pygbag)
async def main():
    while True:
        update()
        draw()
        await asyncio.sleep(0)

asyncio.run(main())

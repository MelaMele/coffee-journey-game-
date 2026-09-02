import pgzrun
import random
import asyncio
import time

# የስክሪን ስፋት እና ቁመት
WIDTH = 800
HEIGHT = 600

# የጨዋታው ርዕስ
TITLE = "የቡና ጉዞ፡ ከካፋ እስከ ዓለም - ደረጃ 4 (ዓለም አቀፍ ኤክስፖርት)"

# ገጸ-ባህሪያት (Actors)
kaldi = Actor('kaldi')
kaldi.pos = (100, 500)

# የኤክስፖርት ቡና ኮንቴይነር
export_coffee = Actor('coffee')
export_coffee.pos = (random.randint(150, 650), random.randint(150, 450))

# የዓለም አቀፍ ኤክስፖርት ወደብ (Target Ship Zone)
ship_zone = Rect((650, 50), (120, 100))

# ተንቀሳቃሽ የሎጂስቲክስ መሰናክሎች
obstacle1 = Actor('coffee')
obstacle1.pos = (300, 150)
obs1_speed = 4

obstacle2 = Actor('coffee')
obstacle2.pos = (500, 400)
obs2_speed = -5

# የጨዋታ ሁኔታዎች
has_coffee = False  # ካልዲ ቡና ጭኗል ወይ?
export_score = 0     # የኤክስፖርት ነጥብ
lives = 3
timer = 90           # 90 ሰከንድ
start_time = time.time()

game_over = False
won = False

def draw():
    """በስክሪኑ ላይ ምስሎችን እና ጽሁፎችን መሳያ"""
    screen.clear()
    
    # የዓለም ገበያ/የወደብ የጀርባ ቀለም (ጥቁር ሰማያዊ)
    screen.fill((25, 25, 112))
    
    # የኤክስፖርት ወደብ (Ship Zone) መሳል
    screen.draw.filled_rect(ship_zone, (0, 128, 128))
    screen.draw.rect(ship_zone, "gold")
    screen.draw.text("ዓለም አቀፍ\nወደብ (Ship)", center=ship_zone.center, fontsize=20, color="white")
    
    # ገጸ-ባህሪያትን መሳል
    kaldi.draw()
    if not has_coffee:
        export_coffee.draw()
        screen.draw.circle(export_coffee.pos, 22, "cyan")
    
    # ካልዲ ቡና ተሸክሞ ከሆነ ማሳያ
    if has_coffee:
        screen.draw.text("☕ ቡና ተጭኗል!", (kaldi.x - 40, kaldi.y - 50), fontsize=18, color="yellow")

    # መሰናክሎችን መሳል
    screen.draw.filled_circle(obstacle1.pos, 18, "red")
    screen.draw.filled_circle(obstacle2.pos, 18, "orange")
    
    # የመረጃ ሰሌዳ (Dashboard)
    screen.draw.text(f"የኤክስፖርት ገቢ: ${export_score}/100", (20, 20), fontsize=28, color="gold")
    screen.draw.text(f"ህይወት: {'❤️ ' * lives}", (20, 55), fontsize=28, color="red")
    screen.draw.text(f"ቀሪ ጊዜ: {max(0, timer)} ሰከንድ", (20, 90), fontsize=28, color="cyan")
    
    # ታላቅ ማሸነፍ
    if won:
        screen.draw.text("🏆 እንኳን ደስ አለዎት! 🏆", center=(WIDTH//2, HEIGHT//2 - 40), fontsize=48, color="gold")
        screen.draw.text("የኢትዮጵያን ቡና በዓለም አቀፍ ደረጃ አግንነዋል!", center=(WIDTH//2, HEIGHT//2 + 10), fontsize=32, color="white")
        screen.draw.text("ሙሉ የቡና ጉዞ ጨዋታውን አጠናቀዋል!", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=28, color="yellow")
        
    # መሸነፍ
    if game_over and not won:
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2 - 20), fontsize=60, color="red")
        screen.draw.text("ጊዜ ወይም ህይወት አልቋል። በድጋሚ ይሞክሩ!", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=28, color="white")

def update():
    """የጨዋታው ዋና ሎጂክ"""
    global has_coffee, export_score, lives, timer, start_time, game_over, won, obs1_speed, obs2_speed
    
    if game_over or won:
        return

    # 1. የጊዜ መቁጠሪያ
    elapsed = int(time.time() - start_time)
    timer = 90 - elapsed
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

    # 3. የመሰናክሎች እንቅስቃሴ
    obstacle1.y += obs1_speed
    if obstacle1.bottom >= HEIGHT or obstacle1.top <= 0:
        obs1_speed = -obs1_speed

    obstacle2.x += obs2_speed
    if obstacle2.right >= WIDTH or obstacle2.left <= 0:
        obs2_speed = -obs2_speed

    # 4. ቡና መጫን
    if not has_coffee and kaldi.colliderect(export_coffee):
        has_coffee = True

    # 5. ቡናውን ወደ ኤክስፖርት ወደብ ማድረስ
    if has_coffee and ship_zone.collidepoint(kaldi.pos):
        export_score += 20
        has_coffee = False
        export_coffee.pos = (random.randint(150, 650), random.randint(150, 450))

    # 6. ከመሰናክል ጋር መጋጨት
    if kaldi.colliderect(obstacle1) or kaldi.colliderect(obstacle2):
        lives -= 1
        has_coffee = False  # የጫነው ቡና ይወድቃል
        kaldi.pos = (100, 500)
        if lives <= 0:
            game_over = True

    # 7. የድል ሁኔታ (100 ዶላር የኤክስፖርት ገቢ ሲገኝ)
    if export_score >= 100:
        won = True
        game_over = True

# Async Loop ለ Web (Pygbag)
async def main():
    while True:
        update()
        draw()
        await asyncio.sleep(0)

asyncio.run(main())

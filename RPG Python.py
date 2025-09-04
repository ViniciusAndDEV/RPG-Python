import random
import os
import time

# -------------------------
# HELPERS
# -------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds=1.5):
    time.sleep(seconds)

# -------------------------
# PLAYER CLASS
# -------------------------
class Player:
    def __init__(self, name, life=10, damage=2):
        self.name = name
        self.life = life
        self.max_life = life
        self.damage = damage
        self.items = []         
        self.weapon = None      

    def show_life(self):
        bar = "█|" * self.life
        empty = "  " * (self.max_life - self.life)
        print(f"{self.name} LIFE")
        print("   " + bar + empty)

    def attack(self, target):
        total_damage = self.damage
        if self.weapon:
            total_damage += self.weapon
        target.take_damage(total_damage)
        print(f"{self.name} attacked {target.name} causing {total_damage} damage!")

    def take_damage(self, dmg):
        self.life = max(0, self.life - dmg)
        self.show_life()

    def is_alive(self):
        return self.life > 0

    # -------------------------
    # ITEM & WEAPON SYSTEM
    # -------------------------
    def pick_item(self, item):
        clear_screen()
        if item >= 6:  
            if self.weapon:
                print(f"You found a weapon (+{item} dmg). Your current weapon is (+{self.weapon} dmg).")
                choice = input("Do you want to equip the new weapon? (y/n): ").lower()
                if choice == "y":
                    self.weapon = item
                    print(f"You equipped the new weapon! (+{item} dmg)")
                else:
                    print("You decided to keep your current weapon.")
            else:
                self.weapon = item
                print(f"You obtained a new weapon! (+{item} damage)")
        else:  # itens de cura
            if len(self.items) < 5:
                self.items.append(item)
                print(f"You picked item {item}. Inventory: {self.items}")
            else:
                print(f"Inventory full! Current items: {self.items}")
                swap = input("Do you want to swap an item? (y/n): ").lower()
                if swap == "y":
                    for idx, it in enumerate(self.items):
                        print(f"{idx+1}: Item {it}")
                    choice = int(input("Choose item number to replace: ")) - 1
                    if 0 <= choice < len(self.items):
                        removed = self.items.pop(choice)
                        self.items.append(item)
                        print(f"Replaced item {removed} with item {item}")
        pause(2)
        clear_screen()

    def use_item(self):
        if not self.items:
            print("No items to use!")
            pause(1)
            clear_screen()
            return
        print(f"Inventory: {self.items}")
        choice = int(input("Choose item number to use: ")) - 1
        if 0 <= choice < len(self.items):
            item = self.items.pop(choice)
            self.life = min(self.max_life, self.life + item)
            print(f"You used item {item} and healed {item} life points!")
        else:
            print("Invalid choice!")
        pause(1)
        clear_screen()

    # -------------------------
    # BONFIRE SYSTEM
    # -------------------------
    def bonfire(self):
        clear_screen()
        print("~ BONFIRE ~ You can use your items freely to heal!")
        while True:
            if not self.items:
                print("No items to use. You are fully healed or out of items.")
                pause(2)
                break
            self.show_life()
            print(f"Inventory: {self.items}")
            choice = input("Choose item number to use or 'q' to leave bonfire: ").lower()
            if choice == 'q':
                break
            if choice.isdigit():
                choice = int(choice) - 1
                if 0 <= choice < len(self.items):
                    item = self.items.pop(choice)
                    self.life = min(self.max_life, self.life + item)
                    print(f"You used item {item} and healed {item} life points!")
                    pause(1)
                    clear_screen()
                else:
                    print("Invalid choice!")
            else:
                print("Invalid input!")

# -------------------------
# MOB CLASS
# -------------------------
class Mob:
    def __init__(self, name, life_range, dmg_range):
        self.name = name
        self.life = random.randint(*life_range)
        self.max_life = self.life
        self.min_dmg, self.max_dmg = dmg_range
        self.alive = True

    def show_life(self):
        bar = "█|" * self.life
        empty = "  " * (self.max_life - self.life)
        print(f"{self.name} LIFE")
        print("   " + bar + empty)

    def attack(self, target):
        dmg = random.randint(self.min_dmg, self.max_dmg)
        target.take_damage(dmg)
        print(f"{self.name} attacked {target.name} causing {dmg} damage!")

    def take_damage(self, dmg):
        self.life = max(0, self.life - dmg)
        self.show_life()
        if self.life <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive

# -------------------------
# MOB TEMPLATES
# -------------------------
mob_templates = {
    1: ("Slime", (4, 6), (1, 3)),
    2: ("Goblin", (5, 7), (1, 3)),
    3: ("Giant Rat", (3, 5), (1, 2)),
    4: ("Orc", (8, 12), (3, 5)),
    5: ("Skeleton", (9, 13), (3, 6)),
    6: ("Dragon Boss", (30, 50), (4, 8))
}

def choose_mob(wave):
    if wave <= 3:
        mob_id = random.randint(1, 3)
    elif wave <= 9:
        mob_id = random.randint(4, 5)
    else:
        mob_id = 6
    name, life_range, dmg_range = mob_templates[mob_id]
    return Mob(name, life_range, dmg_range)

# -------------------------
# DROP SYSTEM
# -------------------------
def drop_item(wave):
    if wave % 2 == 0:
        item = random.randint(6, 10)  
    else:
        item = random.randint(1, 5)   
    return item

# -------------------------
# GAME LOOP
# -------------------------
def game():
    clear_screen()
    print(
        "--------------------------------------------------\n"
        "█▀▀█ █▀▀█ █▀▀█   █▀▀█ █░░▒█ ▀▀█▀▀ █░▒█ █▀▀▀█ █▄░▒█\n"
        "█▄▄▀ █▄▄█ █░▄▄   █▄▄█ █▄▄▄█ ░▒█░░ █▀▀█ █░░▒█ █▒█▒█\n"
        "█░▒█ █░░░ █▄▄█   █░░░ ░▒█░░ ░▒█░░ █░▒█ █▄▄▄█ █░░▀█\n"
        "--------------------------------------------------"
    )
    pause()
    clear_screen()

    player_name = input("Enter your character name: ")
    player = Player(player_name)
    wave = 1

    while True:
        # -----------------
        # BONFIRE AFTER WAVE 5
        # -----------------
        if wave == 6:
            print("~You reached a bonfire!~ Heal and prepare for the next waves.")
            player.bonfire()

        # -----------------
        # BONFIRE BEFORE BOSS
        # -----------------
        if wave == 10:
            print("~You reached a bonfire before the boss!~ Heal and prepare well!")
            player.bonfire()

        clear_screen()
        print(f"--- Wave {wave} ---")
        mob = choose_mob(wave)
        print(f"A {mob.name} appeared! Life: {mob.life}")
        pause(1)
        mob.show_life()
        player.show_life()
        pause(1)

        # -----------------
        # COMBAT LOOP
        # -----------------
        while player.is_alive() and mob.is_alive():
            action = input("\nDo you want to (1) Attack or (2) Use item? ")
            clear_screen()
            if action == "1":
                player.attack(mob)
            elif action == "2":
                player.use_item()
            else:
                print("Invalid choice!")
                pause(1)
                clear_screen()
                continue

            pause(1)
            if mob.is_alive():
                mob.attack(player)
                pause(1)

        # -----------------
        # POST COMBAT
        # -----------------
        if not player.is_alive():
            print("\nGame Over! You died.")
            break

        print(f"\nYou defeated {mob.name}!")
        pause(1)

        # drop item
        item = drop_item(wave)
        player.pick_item(item)

        wave += 1
        if wave > 10:
            print("\nCongratulations! You defeated all waves and the boss!")
            break

# -------------------------
# START GAME
# -------------------------
if __name__ == "__main__":
    game()

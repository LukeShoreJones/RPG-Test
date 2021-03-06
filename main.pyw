import math
import numpy
import os
import pygame as pg
import random
import shutil
import time

from globals import *
from sprites import *
from map import *

def set_preview_one(unit):
    g.preview_one = unit
    if unit != None:
        g.preview_one_name.set_content(unit.name)
        g.preview_one_str.set_content(str(unit.stats[0]))
        g.preview_one_con.set_content(str(unit.stats[1]))
        g.preview_one_int.set_content(str(unit.stats[2]))
        g.preview_one_wis.set_content(str(unit.stats[3]))
        g.preview_one_dex.set_content(str(unit.stats[4]))
        g.preview_one_lck.set_content(str(unit.stats[5]))

        g.preview_one_weapon_name.set_content(str(unit.weapon.get('name')))
        if unit.weapon.get('power') == 0 and unit.weapon.get('heal') != 0:
            g.preview_one_weapon_text.set_content(['Healing: ' + str(unit.weapon.get('healing')), 'Range: ' + str(unit.weapon.get('range')), 'Stat: ' + STAT_NAMES[unit.weapon.get('stat')]])
        else:
            g.preview_one_weapon_text.set_content(['Power: ' + str(unit.weapon.get('power')), 'Range: ' + str(unit.weapon.get('range')), 'Stat: ' + STAT_NAMES[unit.weapon.get('stat')]])

        if unit.trait != {}:
            g.preview_one_trait_name.set_content(unit.trait.get('name'))
            g.preview_one_trait_text.auto_set_lines(unit.trait.get('desc'), 97)
        else:
            g.preview_one_trait_name.set_content('')
            g.preview_one_trait_text.set_content([])

        g.preview_one_hp_bar.set_img(g)

    else:
        g.preview_one_name.set_content('')
        g.preview_one_str.set_content('')
        g.preview_one_con.set_content('')
        g.preview_one_int.set_content('')
        g.preview_one_wis.set_content('')
        g.preview_one_dex.set_content('')
        g.preview_one_lck.set_content('')

        g.preview_one_weapon_name.set_content('')
        g.preview_one_weapon_text.set_content([])

        g.preview_one_trait_name.set_content('')
        g.preview_one_trait_text.set_content([])


def set_preview_two(unit):
    g.preview_two = unit
    if unit != None:
        g.preview_two_name.set_content(unit.name)
        g.preview_two_str.set_content(str(unit.stats[0]))
        g.preview_two_con.set_content(str(unit.stats[1]))
        g.preview_two_int.set_content(str(unit.stats[2]))
        g.preview_two_wis.set_content(str(unit.stats[3]))
        g.preview_two_dex.set_content(str(unit.stats[4]))
        g.preview_two_lck.set_content(str(unit.stats[5]))

        g.preview_two_weapon_name.set_content(str(unit.weapon.get('name')))
        if unit.weapon.get('power') == 0 and unit.weapon.get('heal') != 0:
            g.preview_two_weapon_text.set_content(['Healing: ' + str(unit.weapon.get('healing')), 'Range: ' + str(unit.weapon.get('range')), 'Stat: ' + STAT_NAMES[unit.weapon.get('stat')]])
        else:
            g.preview_two_weapon_text.set_content(['Power: ' + str(unit.weapon.get('power')), 'Range: ' + str(unit.weapon.get('range')), 'Stat: ' + STAT_NAMES[unit.weapon.get('stat')]])

        if unit.trait != {}:
            g.preview_two_trait_name.set_content(unit.trait.get('name'))
            g.preview_two_trait_text.auto_set_lines(unit.trait.get('desc'), 97)
        else:
            g.preview_two_trait_name.set_content('')
            g.preview_two_trait_text.set_content([])

        g.preview_two_hp_bar.set_img(g)

    else:
        g.preview_two_name.set_content('')
        g.preview_two_str.set_content('')
        g.preview_two_con.set_content('')
        g.preview_two_int.set_content('')
        g.preview_two_wis.set_content('')
        g.preview_two_dex.set_content('')
        g.preview_two_lck.set_content('')

        g.preview_two_weapon_name.set_content('')
        g.preview_two_weapon_text.set_content([])

        g.preview_two_trait_name.set_content('')
        g.preview_two_trait_text.set_content([])


def import_unit(unit_id, pos, team):
    stats = []

    name = g.unit_dict.get(unit_id).get('name')
    gender = g.unit_dict.get(unit_id).get('gender')
    img = str(g.unit_dict.get(unit_id).get('img'))

    for stat_name in STAT_NAMES:
        stats.append(g.unit_dict.get(unit_id).get('stats').get(stat_name.lower()))
    hp = MAX_HP
    weapon = g.weapon_dict.get(g.unit_dict.get(unit_id).get('weapon'))

    trait = g.trait_dict.get(g.unit_dict.get(unit_id).get('trait'))

    return Unit(team, False, name, gender, img, stats, hp, weapon, trait, pos)

def random_unit(pos, elite, team):
    stats = []
    gender = random.choice(('Male', 'Female'))

    if gender == 'Male':
        name = random.choice(g.first_names_male)
    elif gender == 'Female':
        name = random.choice(g.first_names_female)

    if DIFFICULTY == 'easy':
        if elite:
            stats = copy.copy(EASY_ELITE_STAT_SPREAD)
        else:
            stats = copy.copy(EASY_STAT_SPREAD)
    elif DIFFICULTY == 'hard':
        if elite:
            stats = copy.copy(HARD_ELITE_STAT_SPREAD)
        else:
            stats = copy.copy(HARD_STAT_SPREAD)
    else:
        if elite:
            stats = copy.copy(NORMAL_ELITE_STAT_SPREAD)
        else:
            stats = copy.copy(NORMAL_STAT_SPREAD)

    random.shuffle(stats)
    hp = MAX_HP

    weapons = list(range(len(g.weapon_dict)))
    random.shuffle(weapons)
    for w in weapons:
        if g.weapon_dict.get(w).get('stat') == stats.index(max(stats[0], stats[2])):
            weapon = w
            break

    img = str(random.choice(g.weapon_dict.get(w).get('unit imgs')))
    weapon = g.weapon_dict.get(weapon)

    if (elite and DIFFICULTY == 'normal') or DIFFICULTY == 'hard':
        traits = list(range(len(g.trait_dict)))
        random.shuffle(traits)
        for t in traits:
            if g.trait_dict.get(t).get('type') == 'none':
                trait = g.trait_dict.get(t)
                break
            elif g.trait_dict.get(t).get('type') == 'damage' and weapon.get('power') != 0:
                trait = g.trait_dict.get(t)
                break
            elif g.trait_dict.get(t).get('type') == 'ranged damage' and weapon.get('power') != 0 and weapon.get('range') > 1:
                trait = g.trait_dict.get(t)
                break
            elif g.trait_dict.get(t).get('type') == 'healing' and weapon.get('healing') != 0:
                trait = g.trait_dict.get(t)
                break
    else:
        trait = {}

    return Unit(team, elite, name, gender, img, stats, hp, weapon, trait, pos)


def get_pos_atk_range(red, posy, posx):
    g.distance = 0
    g.pos_attack_range = copy.deepcopy(g.map.matrix)
    get_pos_atk_range_loop(red, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])


def get_pos_atk_range_loop(red, posy, posx, adjacent_tiles):
    weapon_range = red.weapon.get('range')
    for i in range(4):
        if g.distance < weapon_range and g.pos_attack_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
            g.distance += 1
            posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
            g.pos_attack_range[posy][posx] = 1

            get_pos_atk_range_loop(red, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

        elif g.distance == weapon_range:
            g.distance -= 1
            return

    g.distance -= 1


def mouse_down(button):
    if button == 1: #LEFT MOUSE BUTTON
        for tile in g.attack_tiles:
            if g.gridx == tile.grid_pos[0] and g.gridy == tile.grid_pos[1]:
                click_attack_tile(tile)
                return

        for tile in g.heal_tiles:
            if g.gridx == tile.grid_pos[0] and g.gridy == tile.grid_pos[1]:
                click_heal_tile(tile)
                return

        if g.attack_tiles == [] and g.heal_tiles == []:
            for tile in g.move_tiles:
                if g.gridx == tile.grid_pos[0] and g.gridy == tile.grid_pos[1]:
                    if g.turn % 2 == 0 and g.mode == 'mp':
                        for red in g.reds:
                            if tile.grid_pos == red.grid_pos and red != g.selected_unit:
                                g.move_tiles = []
                                g.selected_unit = None
                                return
                        click_move_tile(tile)
                        return
                    else:
                        for blue in g.blues:
                            if tile.grid_pos == blue.grid_pos and blue != g.selected_unit:
                                g.move_tiles = []
                                g.selected_unit = None
                                return
                        click_move_tile(tile)
                        return

            for blue in g.blues:
                if g.turn % 2 == 1 and g.gridx == blue.grid_pos[0] and g.gridy == blue.grid_pos[1] and blue.active:
                    g.colour = 'blue'
                    click_unit(blue)
                    return

            for red in g.reds:
                if g.turn % 2 == 0 and g.gridx == red.grid_pos[0] and g.gridy == red.grid_pos[1] and red.active:
                    g.colour = 'red'
                    click_unit(red)
                    return

            g.selected_unit = None

        g.move_tiles = []

    elif button == 3:
        g.move_tiles = []
        if g.attack_tiles != [] or g.heal_tiles != []:
            g.attack_tiles = []
            g.heal_tiles = []
            set_inactive(g.selected_unit)
            g.selected_unit.set_img(g)
            g.selected_unit = None

        else:
            g.selected_unit = None


def click_unit(unit):
    g.selected_unit = unit

    g.move_tiles = []
    g.pre_move_tiles = []
    pg.mixer.Sound.play(g.click)
    for row in range(len(unit.move_range)):
        for column in range(len(unit.move_range[row])):
            if unit.move_range[row][column] == 1:
                g.move_tiles.append(MoveTile((column,row),g.colour))


def click_move_tile(tile):
    g.start_pos = (g.selected_unit.pos[0],g.selected_unit.pos[1])
    g.end_pos = (tile.grid_pos[0]*WIDTH,tile.grid_pos[1]*HEIGHT)

    g.dy = (g.end_pos[1]-g.start_pos[1])/MOVE_STEPS
    g.dx = (g.end_pos[0]-g.start_pos[0])/MOVE_STEPS

    g.state = 'animating'
    g.animation = 'player move'
    g.move_complete = False


def click_attack_tile(tile):
    for defender in g.defenders:
        if defender.grid_pos[0] == tile.grid_pos[0] and defender.grid_pos[1] == tile.grid_pos[1]:
            g.attacker = (g.selected_unit)
            g.defender = defender
            g.state = 'combat'
            g.stage = 'attacker attack'
            break


def click_heal_tile(tile):
    for attacker in g.attackers:
        if attacker.grid_pos[0] == tile.grid_pos[0] and attacker.grid_pos[1] == tile.grid_pos[1]:
            g.attacker = (g.selected_unit)
            g.defender = attacker
            g.state = 'combat'
            g.stage = 'heal'
            break


def get_adjacent_trait(trait, defender, defenders):
    for d in defenders:
        distance = (d.grid_pos[0] - defender.grid_pos[0], d.grid_pos[1] - defender.grid_pos[1])
        adjacent = (abs(distance[0]) == 0 and abs(distance[1]) == 1) or (abs(distance[0]) == 1 and abs(distance[1]) == 0)
        if adjacent and d.trait.get('effect') == trait:
            return d

    return None


def damage_calc(attacker, defender, attacker_2, defender_2):
    dodge_roll = random.randint(1,100)
    crit_roll = random.randint(1,100)
    dmg = attacker.stats[attacker.weapon.get('stat')] * attacker.weapon.get('power')
    defence_stat = attacker.weapon.get('stat') + 1

    attacker_base_dmg = max(math.floor(dmg / defender.stats[defence_stat]), 1)
    attacker_dmg = random.randint(attacker_base_dmg-1, attacker_base_dmg+1)

    dodge_threshold = 1.5 * defender.stats[4]
    if defender.trait.get('effect') == 'rush' and (defender.hp / MAX_HP) <= defender.trait.get('health'):
        dodge_threshold *= defender.trait.get('mod')

    if dodge_roll <= dodge_threshold:
        attacker_dmg = 0
        attacker_hit = 'miss'
    else:
        attacker_dmg = attacker_base_dmg
        attacker_hit = 'hit'
        if crit_roll <= 1.5 * attacker.stats[5]:
            attacker_dmg *= 2
            attacker_hit = 'crit'

    dodge_roll = random.randint(1,100)
    crit_roll = random.randint(1,100)
    dmg = attacker_2.stats[attacker_2.weapon.get('stat')] * attacker_2.weapon.get('power')
    defence_stat = attacker_2.weapon.get('stat') + 1

    defender_base_dmg = math.floor(dmg / defender_2.stats[defence_stat])
    defender_dmg = max(random.randint(defender_base_dmg-1, defender_base_dmg+1), 1)

    dodge_threshold = 1.5 * defender_2.stats[4]
    if attacker.trait.get('effect') == 'rush' and (defender_2.hp / MAX_HP) <= defender_2.trait.get('health'):
        dodge_threshold *= defender_2.trait.get('mod')

    if dodge_roll <= dodge_threshold:
        defender_dmg = 0
        defender_hit = 'miss'
    else:
        defender_dmg = defender_base_dmg
        defender_hit = 'hit'
        if crit_roll <= 1.5 * attacker_2.stats[5]:
            defender_dmg *= 2
            defender_hit = 'crit'

    return (attacker_base_dmg, attacker_dmg, attacker_hit, defender_base_dmg, defender_dmg, defender_hit)


def heal_calc(attacker, defender):
    crit_roll = random.randint(1,100)

    base_heal = math.floor(attacker.stats[attacker.weapon.get('stat')] * attacker.weapon.get('healing') / 6)
    heal = min(random.randint(base_heal-1, base_heal+1), MAX_HP-defender.hp)

    if crit_roll <= 1.5 * attacker.stats[5]:
        heal = min(heal*2,  MAX_HP-defender.hp)
        hit = 'crit'
    else:
        hit = 'hit'

    return (heal, hit)


def turn_over():
    found_active = 0

    if g.mode == 'sp' or g.turn % 2 == 1:
        for blue in g.blues:
            if blue.active:
                found_active = 1
                break
    else:
        for red in g.reds:
            if red.active:
                found_active = 1
                break

    if found_active == 0:
        return True
    else:
        return False


def write_settings():
    g.settings['master volume'] = int(g.settings.get('master volume') * 100)
    g.settings['sfx'] = int(g.settings.get('sfx') * 100)
    g.settings['music'] = int(g.settings.get('music') * 100)
    with open('settings.yml', 'w') as outfile:
        yaml.dump(g.settings, outfile)


def update_volumes():
    for step in g.steps:
        step.set_volume(g.settings.get('master volume') * g.settings.get('sfx'))
    g.hit.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.2)
    g.miss.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.3)
    g.crit.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.2)
    g.heal_hit.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.6)
    g.heal_crit.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.2)
    g.click.set_volume(g.settings.get('master volume') * g.settings.get('sfx') * 0.5)

    pg.mixer.music.set_volume(g.settings.get('master volume') * g.settings.get('music') * 0.4)


def move(moving, end_pos):
    moving.pos = (moving.pos[0]+g.dx, moving.pos[1]+g.dy)

    if not pg.mixer.get_busy():
        step = random.randint(0,3)
        pg.mixer.Sound.play(g.steps[step])

    g.move_complete = True
    if g.dx > 0 and moving.pos[0] < end_pos[0]:
        g.move_complete = False
    elif g.dx < 0 and moving.pos[0] > end_pos[0]:
        g.move_complete = False
    elif g.dy > 0 and moving.pos[1] < end_pos[1]:
        g.move_complete = False
    elif g.dy < 0 and moving.pos[1] > end_pos[1]:
        g.move_complete = False

    time.sleep(MOVE_TIME)


def set_damage(attackers, defenders):
    g.defender_guardian = get_adjacent_trait('guardian', g.defender, defenders)
    g.attacker_guardian = get_adjacent_trait('guardian', g.attacker, attackers)

    if g.defender_guardian is not None:
        if g.attacker_guardian is not None:
            (g.attacker_base_dmg, g.attacker_dmg, g.attacker_hit, g.defender_base_dmg, g.defender_dmg, g.defender_hit) = damage_calc(g.attacker, g.defender_guardian, g.defender, g.attacker_guardian)
            g.attacker_base_dmg = math.floor(g.attacker_base_dmg * g.defender_guardian.trait.get('mod'))
            g.attacker_dmg = max(math.floor(g.attacker_dmg * g.defender_guardian.trait.get('mod')), 1)
            g.defender_base_dmg = math.floor(g.defender_base_dmg * g.attacker_guardian.trait.get('mod'))
            g.defender_dmg = max(math.floor(g.defender_dmg * g.attacker_guardian.trait.get('mod')), 1)
        else:
            (g.attacker_base_dmg, g.attacker_dmg, g.attacker_hit, g.defender_base_dmg, g.defender_dmg, g.defender_hit) = damage_calc(g.attacker, g.defender_guardian, g.defender, g.attacker)
            g.attacker_base_dmg = math.floor(g.attacker_base_dmg * g.defender_guardian.trait.get('mod'))
            g.attacker_dmg = max(math.floor(g.attacker_dmg * g.defender_guardian.trait.get('mod')), 1)
    else:
        if g.attacker_guardian is not None:
            (g.attacker_base_dmg, g.attacker_dmg, g.attacker_hit, g.defender_base_dmg, g.defender_dmg, g.defender_hit) = damage_calc(g.attacker, g.defender, g.defender, g.attacker_guardian)
            g.defender_base_dmg = math.floor(g.defender_base_dmg * g.attacker_guardian.trait.get('mod'))
            g.defender_dmg = max(math.floor(g.defender_dmg * g.attacker_guardian.trait.get('mod')), 1)
        else:
            (g.attacker_base_dmg, g.attacker_dmg, g.attacker_hit, g.defender_base_dmg, g.defender_dmg, g.defender_hit) = damage_calc(g.attacker, g.defender, g.defender, g.attacker)

    if g.attacker.trait.get('effect') == 'berserk' and (g.attacker.hp / MAX_HP) <= g.attacker.trait.get('health'):
        g.attacker_dmg *= g.attacker.trait.get('atk mod')

    elif g.attacker.trait.get('effect') == 'execute' and (g.defender.hp / MAX_HP) <= g.attacker.trait.get('health'):
        g.attacker_hit = 'crit'

    g.attacker_battle_cry = get_adjacent_trait('battle cry', g.attacker, attackers)
    g.defender_battle_cry = get_adjacent_trait('battle cry', g.defender, defenders)
    if g.attacker_battle_cry is not None:
        g.attacker_dmg *= g.attacker_battle_cry.trait.get('mod')
    if g.defender_battle_cry is not None:
        g.defender_dmg *= g.defender_battle_cry.trait.get('mod')

    if g.defender.trait.get('effect') == 'berserk' and (g.defender.hp / MAX_HP) <= g.defender.trait.get('health'):
        g.attacker_dmg *= g.defender.trait.get('def mod')

    g.defender_blessing = get_adjacent_trait('blessing', g.defender, defenders)
    g.attacker_blessing = get_adjacent_trait('blessing', g.attacker, attackers)
    if g.defender_blessing is not None:
        g.attacker_dmg *= g.defender_blessing.trait.get('mod')
    if g.attacker_blessing is not None:
        g.defender_dmg *= g.attacker_blessing.trait.get('mod')


def set_healing():
    (g.heal, g.attacker_hit) = heal_calc(g.attacker, g.defender)
    if g.attacker.trait.get('effect') == 'miracle' and (g.defender.hp / MAX_HP) <= g.attacker.trait.get('health'):
        g.attacker_hit = 'crit'


def heal_return():
    if g.attacker_hit == 'hit':
        pg.mixer.Sound.play(g.heal_hit)
    else:
        pg.mixer.Sound.play(g.heal_crit)

    g.defender.hp += g.heal
    g.defender.set_hp_img(g)
    g.preview_two_hp_bar.set_img(g)

    g.state = 'animating'
    g.animation = 'heal return'


def wildfire(attacker, defender, defenders):
    count = 0
    for d in defenders:
        distance = (d.grid_pos[0] - defender.grid_pos[0], d.grid_pos[1] - g.defender.grid_pos[1])
        if (abs(distance[0]) == 0 and abs(distance[1]) == 1) or (abs(distance[0]) == 1 and abs(distance[1]) == 0):
            count += 1
            (attacker_base_dmg, attacker_dmg, attacker_hit, defender_base_dmg, defender_dmg, defender_hit) = damage_calc(attacker, d, d, attacker)
            dmg = max(math.floor(attacker_dmg * attacker.trait.get('mod')), 1)
            if d.hp <= dmg:
                defenders.remove(d)
            else:
                d.hp -= dmg
                d.set_hp_img(g)
            if count == 4:
                break


def pierce(attacker, defender, defenders):
    target_angle = math.atan2(defender.grid_pos[1] - attacker.grid_pos[1], defender.grid_pos[0] - attacker.grid_pos[0])
    target_distance = math.sqrt((defender.grid_pos[0] - attacker.grid_pos[0])**2 + (defender.grid_pos[1] - attacker.grid_pos[1])**2)
    count = 0
    for d in defenders:
        angle = math.atan2(d.grid_pos[1] - attacker.grid_pos[1], d.grid_pos[0] - attacker.grid_pos[0])
        distance = math.sqrt((d.grid_pos[0] - attacker.grid_pos[0])**2 + (d.grid_pos[1] - attacker.grid_pos[1])**2)
        if angle == target_angle and distance < target_distance:
            count += 1
            (attacker_base_dmg, attacker_dmg, attacker_hit, defender_base_dmg, defender_dmg, defender_hit) = damage_calc(attacker, d, d, attacker)
            dmg = max(math.floor(attacker_dmg * attacker.trait.get('mod')), 1)
            if d.hp <= dmg:
                defenders.remove(d)
            else:
                d.hp -= dmg
                d.set_hp_img(g)
            if count == attacker.weapon.get('range') - 1:
                break


def attacker_return(defenders):
    if g.attacker_hit == 'hit':
        pg.mixer.Sound.play(g.hit)
    elif g.attacker_hit == 'crit':
        pg.mixer.Sound.play(g.crit)
    else:
        pg.mixer.Sound.play(g.miss)

    if g.attacker.trait.get('effect') == 'wildfire':
        wildfire(g.attacker, g.defender, defenders)
    elif g.attacker.trait.get('effect') == 'pierce':
        pierce(g.attacker, g.defender, defenders)

    if g.defender_guardian is None:
        defender = g.defender
    else:
        defender = g.defender_guardian

    if defender.hp <= g.attacker_dmg:
        defenders.remove(defender)
        if g.attacker.trait.get('effect') == 'warpath':
            g.warpath = True
    else:
        defender.hp -= g.attacker_dmg
        defender.set_hp_img(g)
        g.preview_two_hp_bar.set_img(g)

    g.state = 'animating'
    g.animation = 'attacker return'


def defender_return(attackers):
    if g.defender_hit == 'hit':
        pg.mixer.Sound.play(g.hit)
    elif g.defender_hit == 'crit':
        pg.mixer.Sound.play(g.crit)
    else:
        pg.mixer.Sound.play(g.miss)

    if g.defender.trait.get('effect') == 'wildfire':
        wildfire(g.defender, g.attacker, attackers)
    elif g.defender.trait.get('effect') == 'pierce':
        pierce(g.defender, g.attacker, attackers)

    if g.attacker_guardian is None:
        attacker = g.attacker
    else:
        attacker = g.attacker_guardian

    if attacker.hp <= g.defender_dmg:
        attackers.remove(attacker)

    else:
        attacker.hp -= g.defender_dmg
        attacker.set_hp_img(g)
        g.preview_one_hp_bar.set_img(g)

    g.state = 'animating'
    g.animation = 'defender return'


def set_inactive(unit):
    unit.active = False
    if unit.trait.get('effect') == 'alchemy':
        unit.hp = min(unit.hp + MAX_HP * unit.trait.get('heal'), MAX_HP)
        unit.set_hp_img(g)


class Game:
    def __init__(self):
        # initialise game window
        pg.init()

        self.selected_slider = None

        self.unit_dict = yaml.load(open('content/units.yml'))
        self.weapon_dict = yaml.load(open('content/weapons.yml'))
        self.trait_dict = yaml.load(open('content/traits.yml'))
        self.first_names_male = open("content/names/first_names_male.txt", "r").read().split(', ')
        self.first_names_female = open("content/names/first_names_female.txt", "r").read().split(', ')

        self.settings = yaml.load(open('settings.yml'))
        self.settings['master volume'] = self.settings.get('master volume') / 100
        self.settings['sfx'] = self.settings.get('sfx') / 100
        self.settings['music'] = self.settings.get('music') / 100

        self.steps = []
        for i in range(4):
            self.steps.append(pg.mixer.Sound('content/sounds/step' + str(i+1) + '.ogg'))
        self.hit = pg.mixer.Sound('content/sounds/hit.ogg')
        self.miss = pg.mixer.Sound('content/sounds/miss.ogg')
        self.crit = pg.mixer.Sound('content/sounds/crit.ogg')
        self.heal_hit = pg.mixer.Sound('content/sounds/heal_hit.ogg')
        self.heal_crit = pg.mixer.Sound('content/sounds/heal_crit.ogg')
        self.click = pg.mixer.Sound('content/sounds/click.ogg')

        for step in self.steps:
            step.set_volume(self.settings.get('master volume') * self.settings.get('sfx'))
        self.hit.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.2)
        self.miss.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.3)
        self.crit.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.2)
        self.heal_hit.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.6)
        self.heal_crit.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.2)
        self.click.set_volume(self.settings.get('master volume') * self.settings.get('sfx') * 0.5)

        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load("content/img/icon.png"))

        self.game_height = DISPLAY_HEIGHT - HEIGHT * 2

        self.options_dialogue_title = DialogueBox((DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0))
        self.options_dialogue_pause = DialogueBox((469, 256), ((DISPLAY_WIDTH - 469) / 2, (self.game_height - 256) / 2))
        self.options_title = CenterText("Options", (DISPLAY_WIDTH / 2, (self.game_height - 186) / 2), 40, WHITE)
        self.options_done = MenuOption(self, 'Done', 25, WHITE,((DISPLAY_WIDTH - 414) / 2, (self.game_height + 164) / 2), 5, False)

        self.options_text = []
        self.options_text.append(Text('Master Volume', ((DISPLAY_WIDTH - 414) / 2, (self.game_height - 125) / 2), 23, WHITE))
        self.options_text.append(Text('SFX', ((DISPLAY_WIDTH - 414) / 2, (self.game_height - 45) / 2), 23, WHITE))
        self.options_text.append(Text('Music', ((DISPLAY_WIDTH - 414) / 2, (self.game_height + 33) / 2), 23, WHITE))

        self.sliders = []
        self.sliders.append(Slider((200, 5), ((DISPLAY_WIDTH - 66) / 2, (self.game_height - 101) / 2), self.settings, 'master volume', DIMGREY, LIGHTGREY, WHITE, self))
        self.sliders.append(Slider((200, 5), ((DISPLAY_WIDTH - 66) / 2, (self.game_height - 21) / 2), self.settings, 'sfx', DIMGREY, LIGHTGREY, WHITE, self))
        self.sliders.append(Slider((200, 5), ((DISPLAY_WIDTH - 66) / 2, (self.game_height + 59) / 2), self.settings, 'music', DIMGREY, LIGHTGREY, WHITE, self))

        if FULLSCREEN:
            self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        self.clock = pg.time.Clock()

        self.fade = Fade()
        self.running = True


    def new(self):
        self.state = 'turn'
        self.preview_one = None
        self.preview_two = None
        self.selected_unit = None

        self.frame = 0
        self.warpath = False
        self.turn = 1

        self.blues = []
        self.reds = []
        self.pre_move_tiles = []
        self.move_tiles = []
        self.attack_tiles = []
        self.heal_tiles = []

        self.bg = Background()
        self.preview_box = PreviewBox()
        self.cursor = Cursor()

        self.previews = pg.sprite.Group()

        self.previews.add(PreviewPortrait(1))
        self.previews.add(PreviewWeaponImg(1))
        self.previews.add(PreviewTraitImg(1))
        self.previews.add(PreviewPortrait(2))
        self.previews.add(PreviewWeaponImg(2))
        self.previews.add(PreviewTraitImg(2))

        self.preview_one_hp_bar = PreviewHPBar(1)
        self.preview_two_hp_bar = PreviewHPBar(2)

        self.preview_one_name = Text("", (150, self.game_height+16), 17, WHITE)
        self.preview_one_str = Text("", (175, self.game_height+42), 17, WHITE)
        self.preview_one_con = Text("", (226, self.game_height+42), 17, WHITE)
        self.preview_one_int = Text("", (175, self.game_height+68), 17, WHITE)
        self.preview_one_wis = Text("", (226, self.game_height+68), 17, WHITE)
        self.preview_one_dex = Text("", (175, self.game_height+94), 17, WHITE)
        self.preview_one_lck = Text("", (226, self.game_height+94), 17, WHITE)

        self.preview_one_weapon_name = Text("", (282, self.game_height+16), 17, WHITE)
        self.preview_one_weapon_text = MultiLineText([], (259, self.game_height+40), 15, WHITE)

        self.preview_one_trait_name = Text("", (390, self.game_height+16), 17, WHITE)
        self.preview_one_trait_text = MultiLineText([], (367, self.game_height+40), 13, WHITE)

        self.preview_two_name = Text("", (628, self.game_height+16), 17, WHITE)
        self.preview_two_str = Text("", (653, self.game_height+42), 17, WHITE)
        self.preview_two_con = Text("", (704, self.game_height+42), 17, WHITE)
        self.preview_two_int = Text("", (653, self.game_height+68), 17, WHITE)
        self.preview_two_wis = Text("", (704, self.game_height+68), 17, WHITE)
        self.preview_two_dex = Text("", (653, self.game_height+94), 17, WHITE)
        self.preview_two_lck = Text("", (704, self.game_height+94), 17, WHITE)

        self.preview_two_weapon_name = Text("", (760, self.game_height+16), 17, WHITE)
        self.preview_two_weapon_text = MultiLineText([], (736, self.game_height+40), 15, WHITE)

        self.preview_two_trait_name = Text("", (868, self.game_height+16), 17, WHITE)
        self.preview_two_trait_text = MultiLineText([], (845, self.game_height+40), 13, WHITE)

        self.previews.add(self.preview_one_hp_bar)
        self.previews.add(self.preview_two_hp_bar)

        self.previews.add(self.preview_one_name)
        self.previews.add(self.preview_one_str)
        self.previews.add(self.preview_one_con)
        self.previews.add(self.preview_one_int)
        self.previews.add(self.preview_one_wis)
        self.previews.add(self.preview_one_dex)
        self.previews.add(self.preview_one_lck)

        self.previews.add(self.preview_one_weapon_name)
        self.previews.add(self.preview_one_weapon_text)

        self.previews.add(self.preview_one_trait_name)
        self.previews.add(self.preview_one_trait_text)

        self.previews.add(self.preview_two_name)
        self.previews.add(self.preview_two_str)
        self.previews.add(self.preview_two_con)
        self.previews.add(self.preview_two_int)
        self.previews.add(self.preview_two_wis)
        self.previews.add(self.preview_two_dex)
        self.previews.add(self.preview_two_lck)

        self.previews.add(self.preview_two_weapon_name)
        self.previews.add(self.preview_two_weapon_text)

        self.previews.add(self.preview_two_trait_name)
        self.previews.add(self.preview_two_trait_text)

        self.turn_dialogue = DialogueBox((180, 32), (6, self.game_height-38))
        self.turn_text = Text("", (12, self.game_height-35), 20, WHITE)

        self.turn_change_dialogue = DialogueBox((DISPLAY_WIDTH, 80), (0, (self.game_height-10)/2))
        self.turn_change_text = CenterText("", (DISPLAY_WIDTH/2, (self.game_height+70)/2), 70, WHITE)

        self.end_screen_dialogue = DialogueBox((256, 128), ((DISPLAY_WIDTH-256)/2, (self.game_height-128)/2))

        self.pause_dialogue = DialogueBox((256, 256), ((DISPLAY_WIDTH-256)/2, (self.game_height-256)/2))
        self.pause_title = CenterText("Paused", (DISPLAY_WIDTH/2, (self.game_height-186)/2), 40, WHITE)

        self.pause_options = []
        self.pause_options.append(MenuOption(self, 'Resume', 25, WHITE, ((DISPLAY_WIDTH - 206) / 2, (self.game_height - 126) / 2), 5, False))
        self.pause_options.append(MenuOption(self, 'Options', 25, WHITE, ((DISPLAY_WIDTH - 206) / 2, (self.game_height - 46) / 2), 5, False))
        self.pause_options.append(MenuOption(self, 'Surrender', 25, WHITE, ((DISPLAY_WIDTH - 206) / 2, (self.game_height + 34) / 2), 5, False))

        self.attackers = self.blues
        self.defenders = self.reds

        if self.mode == 'sp':
            self.map = Map(os.path.join("content/maps-singleplayer", self.map_choice, "map.tmx"))
            self.map.data = yaml.load(open(os.path.join("content/maps-singleplayer", self.map_choice, "data.yml")))

            self.map_img = self.map.make_map()
            self.bg.image = pg.image.load(os.path.join("content/maps-singleplayer", self.map_choice, "bg.png"))
            pg.mixer.music.load(os.path.join("content/maps-singleplayer", self.map_choice, "music.ogg"))
            self.turn_text.set_content("Turn " + str(self.turn) + " (Player)")

            for spawn in self.map.red_spawns:
                pos = (spawn[1], spawn[2])
                elite = spawn[0] in self.map.data.get('elites')
                self.reds.append(random_unit(pos, elite, 'red'))
        else:
            self.map = Map(os.path.join("content/maps-multiplayer", self.map_choice, "map.tmx"))
            self.map.data = yaml.load(open(os.path.join("content/maps-multiplayer", self.map_choice, "data.yml")))

            self.map_img = self.map.make_map()
            self.bg.image = pg.image.load(os.path.join("content/maps-multiplayer", self.map_choice, "bg.png"))
            pg.mixer.music.load(os.path.join("content/maps-multiplayer", self.map_choice, "music.ogg"))
            self.turn_text.set_content("Turn " + str(self.turn) + " (Blue)")

            for red_id, spawn in zip(RED_PARTY, self.map.red_spawns):
                pos = (spawn[1], spawn[2])
                self.reds.append(import_unit(red_id, pos, 'red'))

            self.red_cam = RedCamera(g)

        self.blue_cam = BlueCamera(g)
        self.cam = self.blue_cam

        for blue_id, spawn in zip(BLUE_PARTY, self.map.blue_spawns):
            pos = (spawn[1], spawn[2])
            self.blues.append(import_unit(blue_id, pos, 'blue'))

        for blue in self.blues:
            blue.get_range(g)
        for red in self.reds:
            red.get_range(g)

        pg.mixer.music.play(-1)
        self.fade.start_fade_in(g)
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()


    def events(self):
        # game loop - events
        self.x, self.y = pg.mouse.get_pos()
        pressed = pg.key.get_pressed()
        if self.state == 'paused':
            for option in self.pause_options:
                if option.rect.collidepoint((self.x, self.y)):
                    option.hover()
                else:
                    option.no_hover()


        elif self.state == 'options':
            if self.options_done.rect.collidepoint((self.x, self.y)):
                self.options_done.hover()
            else:
                self.options_done.no_hover()

        mouse_pressed = pg.mouse.get_pressed()
        if self.state == 'options' and mouse_pressed[0] == 1:
            if self.selected_slider is None:
                for slider in self.sliders:
                    if slider.bar.rect.collidepoint((self.x, self.y)):
                        slider.set_selected_slider(g)

            else:
                self.volume_length = max(0, min(self.x - self.selected_slider.bar.pos[0], 200))
                self.volume_length = self.volume_length - self.volume_length % 2

                if self.selected_slider.button.pos[0] != self.selected_slider.button.default_pos[0] + self.volume_length:
                    self.selected_slider.fill_bar.update_width(max(0, self.volume_length))
                    self.selected_slider.button.update_pos((self.selected_slider.button.default_pos[0] + self.volume_length, self.selected_slider.button.pos[1]))

                    self.settings[self.selected_slider.button.volume_type] = (math.e ** (self.volume_length / 200) - 1) / (math.e - 1)
                    self.settings[self.selected_slider.button.volume_type] = (math.e ** (self.volume_length / 200) - 1) / (math.e - 1)
                    update_volumes()


        elif self.state == 'options' and self.selected_slider is not None:
            self.selected_slider.unset_selected_slider(g)

        elif self.state != 'paused' and self.state != 'options' and self.state != 'animating':
            self.gridx, self.gridy = self.x//(WIDTH) + self.cam.posx//(WIDTH), self.y//(HEIGHT) + self.cam.posy//(HEIGHT)

            self.hovered_unit = None

            if self.y < self.game_height:
                pg.mouse.set_visible(False)
            else:
                pg.mouse.set_visible(True)

            for blue in self.blues:
                if self.gridx == blue.grid_pos[0] and self.gridy == blue.grid_pos[1]:
                    self.hovered_unit = blue

                    if self.attack_tiles == [] and self.heal_tiles == []:
                        blue.get_range(g)
                        self.pre_move_tiles = []
                        for row in range(len(blue.move_range)):
                            for column in range(len(blue.move_range[row])):
                                if blue.move_range[row][column] == 1 and self.move_tiles == []:
                                        self.pre_move_tiles.append(PreMoveTile((column,row),'blue',blue.active))
                                        self.pre_move_tiles[-1].set_img(self)

            for red in self. reds:
                if self. gridx == red.grid_pos[0] and self.gridy == red.grid_pos[1]:
                    self.hovered_unit = red

                    if self.attack_tiles == [] and self.heal_tiles == []:
                        red.get_range(g)
                        self.pre_move_tiles = []
                        for row in range(len(red.move_range)):
                            for column in range(len(red.move_range[row])):
                                if red.move_range[row][column] == 1 and self.move_tiles == []:
                                    self.pre_move_tiles.append(PreMoveTile((column,row),'red',red.active))
                                    self.pre_move_tiles[-1].set_img(self)

            if self.hovered_unit == None:
                self.pre_move_tiles = []

            if (self.mode != 'sp' or self.turn % 2 == 1):
                if self.selected_unit == None or self.selected_unit == self.hovered_unit:
                    set_preview_one(self.hovered_unit)
                    set_preview_two(None)
                elif self.hovered_unit != self.selected_unit:
                    set_preview_one(self.selected_unit)
                    set_preview_two(self.hovered_unit)
                else:
                    set_preview_one(None)
                    set_preview_two(None)

                if (self.cam.posx > 0) and (pressed[pg.K_LEFT] or pressed[pg.K_a]):
                    self.cam.posx -= WIDTH
                if (DISPLAY_WIDTH < self.map.width-self.cam.posx) and (pressed[pg.K_RIGHT] or pressed[pg.K_d]):
                    self.cam.posx += WIDTH
                if (self.cam.posy > 0) and (pressed[pg.K_UP] or pressed[pg.K_w]):
                    self.cam.posy -= HEIGHT
                if (self.game_height < self.map.height-self.cam.posy) and (pressed[pg.K_DOWN] or pressed[pg.K_s]):
                    self.cam.posy += HEIGHT

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                write_settings()
                self.running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.state != 'paused' and self.state != 'options' and self.state != 'animating':
                    mouse_down(event.button)

                elif self.state == 'paused' and event.button == 1:
                    for option in self.pause_options:
                        if option.rect.collidepoint((self.x, self.y)):
                            if option.content == 'Resume':
                                pg.mixer.Sound.play(self.click)
                                self.state = self.old_state
                                pg.mouse.set_visible(False)

                            elif option.content == 'Options':
                                option.no_hover()
                                pg.mixer.Sound.play(self.click)
                                self.state = 'options'

                            elif option.content == 'Surrender':
                                pg.mixer.Sound.play(self.click)
                                self.state = self.old_state
                                if self.mode == 'sp' or self.turn % 2 != 0:
                                    self.result = 'red'
                                else:
                                    self.result = 'blue'
                                self.playing = False

                elif self.state == 'options' and event.button == 1 and self.options_done.rect.collidepoint((self.x, self.y)):
                    pg.mixer.Sound.play(self.click)
                    self.state = 'paused'

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.state == 'options':
                        pg.mixer.Sound.play(self.click)
                        self.state = 'paused'

                    elif self.state == 'paused':
                        pg.mixer.Sound.play(self.click)
                        self.state = self.old_state
                        pg.mouse.set_visible(False)

                    else:
                        pg.mixer.Sound.play(self.click)
                        self.old_state = self.state
                        self.state = 'paused'
                        pg.mouse.set_visible(True)


    def update(self):
        # game loop - update
        if self.state == 'start screen':
            self.x, self.y = pg.mouse.get_pos()

            if self.start_screen_map.width*2 < DISPLAY_WIDTH or self.start_screen_map.height*2 < DISPLAY_HEIGHT:
                start_x = (self.start_screen_pos[0] % (WIDTH*2)) - WIDTH*2
                y = (self.start_screen_pos[1] % (HEIGHT*2)) - HEIGHT*2

                while y < DISPLAY_HEIGHT:
                    x = start_x
                    while x < DISPLAY_WIDTH:
                        if (
                            (x < self.start_screen_pos[0])
                            or (x >= self.start_screen_pos[0] + self.start_screen_map.width*2)
                            or (y < self.start_screen_pos[1])
                            or (y >= self.start_screen_pos[1] + self.start_screen_map.height*2)
                        ):
                            self.screen.blit(self.start_screen_bg, (x, y))
                        x += WIDTH*2
                    y += HEIGHT*2

            self.screen.blit(self.start_screen_map_img, self.start_screen_pos)
            self.start_screen_overlay.update(self)

            self.title_text.update(self)

            if self.stage == 'root':
                for option in self.title_options:
                    if option.rect.collidepoint((self.x, self.y)):
                        option.hover()
                    else:
                        option.no_hover()
                    option.update(self)

            elif self.stage == 'options':
                for option in self.title_options:
                    option.update(self)

                if self.options_done.rect.collidepoint((self.x, self.y)):
                    self.options_done.hover()
                else:
                    self.options_done.no_hover()

                self.options_dialogue_title.update(g)
                self.options_title.update(g)
                self.options_done.update(g)

                for text in self.options_text:
                    text.update(g)
                for slider in self.sliders:
                    slider.update(g)

            elif self.stage == 'choose sp':
                self.sp_title.update(self)
                self.scrollbar_bg.update(self)
                self.scrollbar.update(self)
                self.back_option.update(self)

                for i in range(self.map_scroll_index, min(len(self.sp_options), self.map_scroll_index+self.map_list_size)):
                    if self.sp_options[i].rect.collidepoint((self.x, self.y)):
                        path = os.path.join(self.maps_sp[i][0], "preview.png")
                        if os.path.exists(path):
                            self.map_preview_img.set_img(path)
                        else:
                            self.map_preview_img.set_blank()

                        self.map_preview_description.auto_set_lines(self.maps_sp[i][1].get('description'), 380)
                        self.map_preview_creator.set_content("Creator: " + self.maps_sp[i][1].get('creator'))

                        self.map_preview_box_1.update(self)
                        self.map_preview_box_2.update(self)
                        self.map_preview_img.update(self)
                        self.map_preview_description.update(self)
                        self.map_preview_creator.update(self)
                        self.sp_options[i].hover()

                    else:
                        self.sp_options[i].no_hover()
                    self.sp_options[i].update(self)

                if self.back_option.rect.collidepoint((self.x, self.y)):
                    self.back_option.hover()
                else:
                    self.back_option.no_hover()

            elif self.stage == 'choose mp':
                self.mp_title.update(self)
                self.scrollbar_bg.update(self)
                self.scrollbar.update(self)
                self.back_option.update(self)

                for i in range(self.map_scroll_index, min(len(self.mp_options), self.map_scroll_index + self.map_list_size)):
                    if self.mp_options[i].rect.collidepoint((self.x, self.y)):
                        path = os.path.join(self.maps_mp[i][0], "preview.png")
                        if os.path.exists(path):
                            self.map_preview_img.set_img(path)
                        else:
                            self.map_preview_img.set_blank()
                        self.map_preview_description.auto_set_lines(self.maps_mp[i][1].get('description'), 380)
                        self.map_preview_creator.set_content("Creator: " + self.maps_mp[i][1].get('creator'))

                        self.map_preview_box_1.update(self)
                        self.map_preview_box_2.update(self)
                        self.map_preview_img.update(self)
                        self.map_preview_description.update(self)
                        self.map_preview_creator.update(self)

                        self.mp_options[i].hover()
                    else:
                        self.mp_options[i].no_hover()

                    self.mp_options[i].update(self)

                if self.back_option.rect.collidepoint((self.x, self.y)):
                    self.back_option.hover()
                else:
                    self.back_option.no_hover()

            start_screen_pos = list(self.start_screen_pos)
            if start_screen_pos[0] + self.start_screen_velx < self.start_screen_minx or start_screen_pos[0] + self.start_screen_velx > 0:
                self.start_screen_velx *= -1
            if start_screen_pos[1] + self.start_screen_vely < self.start_screen_miny or start_screen_pos[1] + self.start_screen_vely > 0:
                self.start_screen_vely *= -1
            start_screen_pos[0] += self.start_screen_velx
            start_screen_pos[1] += self.start_screen_vely
            self.start_screen_pos = tuple(start_screen_pos)


        elif self.state == 'turn':
            self.bg.update(self)
            self.screen.blit(self.map_img, (-self.cam.posx,-self.cam.posy))

            for tile in self.pre_move_tiles:
                tile.update(self)
            for tile in self.move_tiles:
                tile.update(self)
            for tile in self.attack_tiles:
                tile.update(self)
            for tile in self.heal_tiles:
                tile.update(self)
            for blue in self.blues:
                blue.update(self)
            for red in self.reds:
                red.update(self)

            self.cursor.update(self)
            self.preview_box.update(self)
            self.turn_dialogue.update(self)
            self.turn_text.update(self)

            self.previews.update(self)

            if self.blues == [] and self.reds == []:
                self.result = "tie"
                self.playing = False
            elif self.reds == []:
                self.result = "blue"
                self.playing = False
            elif self.blues == []:
                self.result = "red"
                self.playing = False

            if turn_over():
                self.state = 'animating'
                self.animation = 'turn end'

        elif self.state == 'paused' or self.state == 'options':
            self.bg.update(self)
            self.screen.blit(self.map_img, (-self.cam.posx,-self.cam.posy))

            for tile in self.pre_move_tiles:
                tile.update(self)
            for tile in self.move_tiles:
                tile.update(self)
            for tile in self.attack_tiles:
                tile.update(self)
            for tile in self.heal_tiles:
                tile.update(self)
            for blue in self.blues:
                blue.update(self)
            for red in self.reds:
                red.update(self)

            self.preview_box.update(self)
            self.turn_dialogue.update(self)
            self.turn_text.update(self)

            self.previews.update(self)

            if self.state == 'paused':
                self.pause_dialogue.update(g)
                self.pause_title.update(g)
                for option in self.pause_options:
                    option.update(g)

            elif self.state == 'options':
                self.options_dialogue_pause.update(g)
                self.options_title.update(g)
                self.options_done.update(g)
                for text in self.options_text:
                    text.update(g)
                for slider in self.sliders:
                    slider.update(g)

        elif self.state == 'combat':
            if self.stage == 'heal':
                set_healing()
                if self.defender.pos[0] > self.attacker.pos[0]:
                    self.dx = 8
                elif self.defender.pos[0] < self.attacker.pos[0]:
                    self.dx = -8
                else:
                    self.dx = 0

                if self.defender.pos[1] > self.attacker.pos[1]:
                    self.dy = 8
                elif self.defender.pos[1] < self.attacker.pos[1]:
                    self.dy = -8
                else:
                    self.dy = 0

                self.state = 'animating'
                self.animation = 'heal'

            elif self.stage == 'heal return':
                heal_return()

            elif self.stage == 'attacker attack':
                set_damage(self.attackers, self.defenders)
                if self.defender.pos[0] > self.attacker.pos[0]:
                    self.dx = 8
                elif self.defender.pos[0] < self.attacker.pos[0]:
                    self.dx = -8
                else:
                    self.dx = 0

                if self.defender.pos[1] > self.attacker.pos[1]:
                    self.dy = 8
                elif self.defender.pos[1] < self.attacker.pos[1]:
                    self.dy = -8
                else:
                    self.dy = 0

                self.state = 'animating'
                self.animation = 'attacker attack'

            elif self.stage == 'attacker return':
                attacker_return(self.defenders)

            elif self.stage == 'defender attack':
                if (self.mode == 'sp' and self.defender in self.reds) or (self.mode == 'mp' and self.defender in self.defenders):
                    self.defender.get_atk_range(g)

                    if self.defender.attack_range[self.attacker.grid_pos[1]][self.attacker.grid_pos[0]] == 1 and self.defender.weapon.get('power') != 0:
                        self.state = 'animating'
                        self.animation = 'defender attack'
                    else:
                        self.stage = 'end'
                else:
                    self.stage = 'end'

            elif self.stage == 'defender return':
                defender_return(self.attackers)

            else:
                self.attack_tiles = []
                self.heal_tiles = []

                if not self.warpath:
                    set_inactive(self.attacker)
                    self.attacker.set_img(g)
                else:
                    self.warpath = False

                self.selected_unit = None

                self.state = 'turn'

        elif self.state == 'enemy turn':
            if self.stage == 'start':
                self.frame += 1
                if self.frame == 30:
                    self.frame = 0
                    self.state = 'enemy turn'
                    self.stage = 'move'

            elif self.stage == 'move':
                self.attacker = None
                for red_ in self.reds:
                    if red_.active:
                        self.attacker = red_
                        break

                if self.attacker == None:
                    self.cam.posx, self.cam.posy = self.true_camera_posx, self.true_camera_posy

                    self.state = 'animating'
                    self.animation = 'turn end'

                else:
                    move_options = []
                    self.attack_move_options = []
                    self.ranged_attack_move_options = []
                    self.heal_move_options = []

                    self.attacker.get_range(g)

                    for y in range(len(self.attacker.move_range)):
                        bad_option = False
                        row = numpy.array(self.attacker.move_range[y])
                        indices = numpy.where(row == 1)[0]
                        for i in indices:
                            for red in self.reds:
                                if (i, y) == red.grid_pos and red != self.attacker:
                                    bad_option = True
                                    break
                            if not bad_option:
                                move_options.append((i, y))

                    self.can_heal_self = False
                    for o in move_options:
                        get_pos_atk_range(self.attacker, o[1], o[0])

                        if self.attacker.weapon.get('power') > 0:
                            for blue in self.blues:
                                blue.get_atk_range(self)
                                (self.attacker_base_dmg, self.attacker_dmg, self.attacker_hit, self.defender_base_dmg, self.defender_dmg, self.defender_hit) = damage_calc(self.attacker, blue, blue, self.attacker)
                                if self.pos_attack_range[blue.grid_pos[1]][blue.grid_pos[0]] == 1 and (blue.hp <= self.attacker_base_dmg or self.attacker.hp > self.defender_base_dmg or blue.attack_range[self.attacker.grid_pos[1]][self.attacker.grid_pos[0]] == 0):
                                    self.attack_move_options.append(o)
                                    adjacent_tiles = [(o[1], o[0]+1), (o[1]-1, o[0]), (o[1], o[0]-1), (o[1]+1, o[0])]
                                    if (blue.grid_pos[1], blue.grid_pos[0]) not in adjacent_tiles:
                                        self.ranged_attack_move_options.append(o)

                        if self.attacker.weapon.get('healing') > 0:
                            for red in self.reds:
                                if self.pos_attack_range[red.grid_pos[1]][red.grid_pos[0]] == 1 and red.hp < MAX_HP:
                                    if red == self.attacker:
                                        self.can_heal_self = True
                                    else:
                                        self.heal_move_options.append(o)

                    if self.heal_move_options != []:
                        chosen_option = random.choice(self.heal_move_options)
                    elif self.can_heal_self:
                        chosen_option = random.choice(move_options)
                    elif self.ranged_attack_move_options != []:
                        chosen_option = random.choice(self.ranged_attack_move_options)
                    elif self.attack_move_options != []:
                        chosen_option = random.choice(self.attack_move_options)
                    else:
                        chosen_option = random.choice(move_options)

                    self.start_pos = (self.attacker.pos[0], self.attacker.pos[1])
                    self.end_pos = (chosen_option[0]*WIDTH, chosen_option[1]*HEIGHT)

                    self.dy = (self.end_pos[1] - self.start_pos[1]) / MOVE_STEPS
                    self.dx = (self.end_pos[0] - self.start_pos[0]) / MOVE_STEPS

                    if (
                        self.start_pos[0]-self.cam.posx < 0
                        or self.start_pos[0]-self.cam.posx >= DISPLAY_WIDTH
                        or self.start_pos[1]-self.cam.posy < 0
                        or self.start_pos[1]-self.cam.posy >= self.game_height
                        or self.end_pos[0]-self.cam.posx < 0
                        or self.end_pos[0]-self.cam.posx >= DISPLAY_WIDTH
                        or self.end_pos[1]-self.cam.posy < 0
                        or self.end_pos[1]-self.cam.posy >= self.game_height
                    ):
                        self.cam.posx = min(max(self.start_pos[0] - 448, 0), self.map.width - DISPLAY_WIDTH)
                        self.cam.posy = min(max(self.start_pos[1] - 256, 0), self.map.height - self.game_height)

                    while self.start_pos[0]-self.cam.posx < 0:
                        self.cam.posx -= 64
                    while self.start_pos[0]-self.cam.posx >= DISPLAY_WIDTH:
                        self.cam.posx += 64
                    while self.start_pos[1]-self.cam.posy < 0:
                        self.cam.posy -= 64
                    while self.start_pos[1]-self.cam.posy >= self.game_height:
                        self.cam.posy += 64

                    while self.end_pos[0]-self.cam.posx < 0:
                        self.cam.posx -= 64
                    while self.end_pos[0]-self.cam.posx >= DISPLAY_WIDTH:
                        self.cam.posx += 64
                    while self.end_pos[1]-self.cam.posy < 0:
                        self.cam.posy -= 64
                    while self.end_pos[1]-self.cam.posy >= self.game_height:
                        self.cam.posy += 64

                    set_preview_one(self.attacker)
                    set_preview_two(None)

                    self.moving = self.attacker
                    self.state = 'animating'
                    self.animation = 'enemy move'
                    self.move_complete = False

            elif self.stage == 'act':
                attack_options = []
                ranged_attack_options = []
                heal_options = []

                self.attacker.get_atk_range(self)
                if self.heal_move_options != [] or self.can_heal_self:
                    for red in self.reds:
                        if self.attacker.attack_range[red.grid_pos[1]][red.grid_pos[0]] == 1 and red.hp < MAX_HP:
                            heal_options.append(red)

                    self.defender = random.choice(heal_options)
                    set_healing()
                    set_preview_two(self.defender)
                    self.state = 'animating'
                    self.animation = 'heal'

                elif self.attack_move_options != []:
                    for blue in self.blues:
                        if self.attacker.attack_range[blue.grid_pos[1]][blue.grid_pos[0]] == 1:
                            attack_options.append(blue)

                            adjacent_tiles = [(self.attacker.grid_pos[1], self.attacker.grid_pos[0]+1),
                                                (self.attacker.grid_pos[1]-1, self.attacker.grid_pos[0]),
                                                (self.attacker.grid_pos[1], self.attacker.grid_pos[0]-1),
                                                (self.attacker.grid_pos[1]+1, self.attacker.grid_pos[0])]

                            if (blue.grid_pos[1], blue.grid_pos[0]) not in adjacent_tiles:
                                ranged_attack_options.append(blue)

                    if ranged_attack_options != []:
                        self.defender = random.choice(ranged_attack_options)
                    else:
                        self.defender = random.choice(attack_options)

                    set_damage(self.reds, self.blues)
                    set_preview_two(self.defender)
                    self.state = 'animating'
                    self.animation = 'attacker attack'


                else:
                    self.stage = 'end'

                if self.stage != 'end':
                    if self.defender.pos[0] > self.attacker.pos[0]:
                        self.dx = 8
                    elif self.defender.pos[0] < self.attacker.pos[0]:
                        self.dx = -8
                    else:
                        self.dx = 0

                    if self.defender.pos[1] > self.attacker.pos[1]:
                        self.dy = 8
                    elif self.defender.pos[1] < self.attacker.pos[1]:
                        self.dy = -8
                    else:
                        self.dy = 0

            elif self.stage == 'heal return':
                heal_return()

            elif self.stage == 'attacker return':
                attacker_return(self.blues)

            elif self.stage == 'defender attack':
                if self.defender in self.blues and self.defender.attack_range[self.attacker.grid_pos[1]][self.attacker.grid_pos[0]] == 1 and self.defender.weapon.get('power') != 0:
                    self.state = 'animating'
                    self.animation = 'defender attack'
                else:
                    self.stage = 'end'

            elif self.stage == 'defender return':
                defender_return(self.reds)

            else:
                self.state = 'animating'
                if not self.warpath:
                    self.animation = 'enemy set inactive'
                else:
                    self.animation = 'enemy move delay'
                    self.warpath = False

        elif self.state == 'animating':
            self.screen.blit(self.map_img, (-self.cam.posx,-self.cam.posy))

            for blue in self.blues:
                blue.update(self)
            for red in self.reds:
                red.update(self)

            self.preview_box.update(self)
            self.turn_dialogue.update(self)
            self.turn_text.update(self)

            self.previews.update(self)

            if self.animation == 'player move':
                if not self.move_complete:
                    move(self.selected_unit, self.end_pos)

                else:
                    self.selected_unit.pos = self.end_pos
                    self.selected_unit.grid_pos = (int(self.selected_unit.pos[0]/WIDTH), int(self.selected_unit.pos[1]/HEIGHT))
                    self.move_tiles = []
                    self.heal_tiles = []

                    self.selected_unit.get_atk_range(g)

                    if self.selected_unit.weapon.get('power') != 0:
                        for j in range(len(self.defenders)):
                            if self.selected_unit.attack_range[self.defenders[j].grid_pos[1]][self.defenders[j].grid_pos[0]] == 1:
                                self.attack_tiles.append(AttackTile((self.defenders[j].grid_pos[0], self.defenders[j].grid_pos[1])))

                    if self.selected_unit.weapon.get('healing') != 0:
                        for j in range(len(self.attackers)):
                            if self.selected_unit.attack_range[self.attackers[j].grid_pos[1]][self.attackers[j].grid_pos[0]] == 1 and self.attackers[j].hp < MAX_HP:
                                self.heal_tiles.append(HealTile((self.attackers[j].grid_pos[0], self.attackers[j].grid_pos[1])))

                    self.state = 'turn'
                    if self.attack_tiles == [] and self.heal_tiles == []:
                        set_inactive(self.selected_unit)
                        self.selected_unit.set_img(g)
                        self.selected_unit = None


            elif self.animation == 'enemy move':
                if not self.move_complete:
                    move(self.moving, self.end_pos)

                else:
                    self.moving.pos = self.end_pos
                    self.moving.grid_pos = (int(self.moving.pos[0]/WIDTH), int(self.moving.pos[1]/HEIGHT))
                    self.state = 'enemy turn'
                    self.stage = 'act'

            elif self.animation == 'heal':
                self.attacker.pos = (self.attacker.pos[0]+self.dx, self.attacker.pos[1]+self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'heal return'

            elif self.animation == 'heal return':
                self.attacker.pos = (self.attacker.pos[0]-self.dx, self.attacker.pos[1]-self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    self.attacker.grid_pos = (int(self.attacker.pos[0]/WIDTH), int(self.attacker.pos[1]/HEIGHT))
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'end'

            elif self.animation == 'attacker attack':
                self.attacker.pos = (self.attacker.pos[0]+self.dx, self.attacker.pos[1]+self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'attacker return'

            elif self.animation == 'attacker return':
                self.attacker.pos = (self.attacker.pos[0]-self.dx, self.attacker.pos[1]-self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    self.attacker.grid_pos = (int(self.attacker.pos[0]/WIDTH), int(self.attacker.pos[1]/HEIGHT))
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'defender attack'

            elif self.animation == 'defender attack':
                self.defender.pos = (self.defender.pos[0]-self.dx, self.defender.pos[1]-self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'defender return'

            elif self.animation == 'defender return':
                self.defender.pos = (self.defender.pos[0]+self.dx, self.defender.pos[1]+self.dy)
                self.frame += 1
                time.sleep(MOVE_TIME)

                if self.frame == 4:
                    self.frame = 0
                    self.defender.grid_pos = (int(self.defender.pos[0]/WIDTH), int(self.defender.pos[1]/HEIGHT))
                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                    else:
                        self.state = 'combat'
                    self.stage = 'end'

            elif self.animation == 'enemy set inactive':
                self.frame += 1
                if self.frame == 10:
                    set_inactive(self.attacker)
                    self.attacker.set_img(g)
                    self.frame = 0
                    self.animation = 'enemy move delay'

            elif self.animation == 'enemy move delay':
                self.frame += 1
                if self.frame == 20:
                    self.frame = 0
                    self.state = 'enemy turn'
                    self.stage = 'move'

            elif self.animation == 'turn end':
                set_preview_one(None)
                set_preview_two(None)

                self.turn += 1
                if self.mode == 'sp' and self.turn % 2 == 0:
                    self.turn_change_text.set_content('ENEMY TURN')
                    self.turn_text.set_content("Turn " + str(self.turn) + " (Enemy)")
                    self.true_camera_posx, self.true_camera_posy = self.cam.posx, self.cam.posy

                    for red in self.reds:
                        red.active = True
                        red.set_img(g)
                    for blue in self.blues:
                        blue.set_img(g)

                elif self.mode == 'sp':
                    self.turn_change_text.set_content('PLAYER TURN')
                    self.turn_text.set_content("Turn " + str(self.turn) + " (Player)")

                    for blue in self.blues:
                        blue.active = True
                        blue.set_img(g)
                        blue.get_range(g)
                    for red in self.reds:
                        red.set_img(g)

                elif self.turn % 2 == 0:
                    self.turn_change_text.set_content('RED TURN')
                    self.turn_text.set_content("Turn " + str(self.turn) + " (Red)")
                    self.attackers = self.reds
                    self.defenders = self.blues
                    self.cam = self.red_cam

                    for unit in self.defenders:
                        unit.set_img(g)
                    for unit in self.attackers:
                        unit.active = True
                        unit.set_img(g)
                        unit.get_range(g)

                else:
                    self.turn_change_text.set_content('BLUE TURN')
                    self.turn_text.set_content("Turn " + str(self.turn) + " (Blue)")
                    self.attackers = self.blues
                    self.defenders = self.reds
                    self.cam = self.blue_cam

                    for unit in self.defenders:
                        unit.set_img(g)
                    for unit in self.attackers:
                        unit.active = True
                        unit.set_img(g)
                        unit.get_range(g)

                self.animation = 'turn change'

            elif self.animation == 'turn change':
                self.frame += 1

                if self.frame < 90:
                    self.bg.turn_change_update(g)
                    self.turn_change_dialogue.update(g)
                    self.turn_change_text.update(g)
                elif self.frame == 90:
                    self.frame = 0
                    self.bg.update(g)

                    if self.mode == 'sp' and self.turn % 2 == 0:
                        self.state = 'enemy turn'
                        self.stage = 'start'
                    else:
                        self.state = 'turn'

        pg.display.update()


    def start_screen(self):
            # show start screen
            self.state = 'start screen'
            self.stage = 'root'

            self.maps_sp = []
            self.maps_mp = []
            self.title_options = []
            self.sp_options = []
            self.mp_options = []

            for dir in os.listdir("content/maps-singleplayer"):
                full_dir = os.path.join("content/maps-singleplayer", dir)
                self.maps_sp.append((full_dir, yaml.load(open(os.path.join(full_dir, "data.yml")))))

            for dir in os.listdir("content/maps-multiplayer"):
                full_dir = os.path.join("content/maps-multiplayer", dir)
                self.maps_mp.append((full_dir, yaml.load(open(os.path.join(full_dir, "data.yml")))))

            self.maps = self.maps_sp + self.maps_mp
            start_screen_map = random.choice(self.maps)

            self.start_screen_map = Map(os.path.join(start_screen_map[0], "map.tmx"))
            self.start_screen_map_img = self.start_screen_map.make_map()
            self.start_screen_map_img = pg.transform.scale2x(self.start_screen_map_img)

            self.start_screen_bg = pg.image.load(os.path.join(start_screen_map[0], "bg.png"))
            self.start_screen_bg = pg.transform.scale2x(self.start_screen_bg)

            self.start_screen_overlay = StartScreenOverlay(10)
            self.title_text = Text(TITLE, (70,70), 50, WHITE)

            self.title_options.append(MenuOption(self, 'Single Player', 30, WHITE, (70, 170), 7, False))
            self.title_options.append(MenuOption(self, 'Multiplayer', 30, WHITE, (70, 220), 7, False))
            self.title_options.append(MenuOption(self, 'Options', 30, WHITE, (70, 270), 7, False))
            self.title_options.append(MenuOption(self, 'Configure Game', 30, WHITE, (70, 320), 7, False))

            self.sp_title = Text('Single Player', (70, 170), 30, WHITE)
            self.mp_title = Text('Multiplayer', (70, 170), 30, WHITE)

            self.map_list_size = (DISPLAY_HEIGHT - 220) // 40 - 1
            self.scrollbar_bg_length = 40 * self.map_list_size - 15
            self.scrollbar_bg = Bar((5, self.scrollbar_bg_length), DIMGREY, (70, 220))
            self.scrollbar = Scrollbar((5, 0), WHITE, (70, 220))

            for map, i in zip(self.maps_sp, range(len(self.maps_sp))):
                self.sp_options.append(MenuOption(self, map[0].split('\\')[1], 25, WHITE, (90, 215 + i*40), 5, False))

            for map, i in zip(self.maps_mp, range(len(self.maps_mp))):
                self.mp_options.append(MenuOption(self, map[0].split('\\')[1], 25, WHITE, (90, 215 + i*40), 5,  False))

            self.back_option = MenuOption(self, 'Back to Mode Select', 20, WHITE, (70, 215 + self.map_list_size * 40), 5, False)

            self.map_preview_box_1 = DialogueBox((420, 420), (490, 40))
            self.map_preview_img = MapPreviewImg((416, 416), self.map_preview_box_1)

            self.map_preview_box_2 = DialogueBox((420, 130), (490, 470))
            self.map_preview_description = MultiLineText([], (500, 476), 20, WHITE)
            self.map_preview_creator = Text("", (500, 570), 20, LIGHTGREY)

            self.start_screen_minx = min(0, DISPLAY_WIDTH-self.start_screen_map.width*2)
            self.start_screen_miny = min(0, DISPLAY_HEIGHT-self.start_screen_map.height*2)

            if self.start_screen_map.width*2 < DISPLAY_WIDTH:
                start_screen_posx = DISPLAY_WIDTH - self.start_screen_map.width*2
                self.start_screen_velx = 0
            else:
                start_screen_posx = random.randint(self.start_screen_minx,0)
                self.start_screen_velx = random.randint(-int(START_SCREEN_SPEED), int(START_SCREEN_SPEED))/10

            if self.start_screen_map.height*2 < DISPLAY_HEIGHT:
                start_screen_posy = (DISPLAY_HEIGHT - self.start_screen_map.height*2)/2
                self.start_screen_vely = 0
            else:
                start_screen_posy = random.randint(self.start_screen_miny,0)
                self.start_screen_vely = random.choice((math.sqrt((START_SCREEN_SPEED/10)**2 - self.start_screen_velx**2), -math.sqrt((START_SCREEN_SPEED/10)**2 - self.start_screen_velx**2)))

            self.start_screen_pos = (start_screen_posx, start_screen_posy)
            self.fade.end_fade_in(self)

            pg.mixer.music.load('content/music/title_screen.ogg')
            pg.mixer.music.set_volume(self.settings.get('master volume') * self.settings.get('music') * 0.4)
            pg.mixer.music.play(-1)

            waiting = True
            while waiting:
                self.clock.tick(FPS)
                self.update()

                mouse_pressed = pg.mouse.get_pressed()
                if self.stage == 'options' and mouse_pressed[0] == 1:
                    if self.selected_slider is None:
                        for slider in self.sliders:
                            if slider.bar.rect.collidepoint((self.x, self.y)):
                                slider.set_selected_slider(g)

                    else:
                        self.volume_length = max(0, min(self.x - self.selected_slider.bar.pos[0], 200))
                        self.volume_length = self.volume_length - self.volume_length % 2

                        if self.selected_slider.button.pos[0] != self.selected_slider.button.default_pos[0] + self.volume_length:
                            self.selected_slider.fill_bar.update_width(max(0, self.volume_length))
                            self.selected_slider.button.update_pos((self.selected_slider.button.default_pos[0] + self.volume_length, self.selected_slider.button.pos[1]))

                            self.settings[self.selected_slider.button.volume_type] = (math.e ** (self.volume_length / 200) - 1) / (math.e - 1)
                            update_volumes()

                elif self.stage == 'options' and self.selected_slider is not None:
                    self.selected_slider.unset_selected_slider(g)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        write_settings()
                        self.running = False
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.stage == 'root':
                                for option in self.title_options:
                                    if option.rect.collidepoint((self.x, self.y)):
                                        if option.content == 'Single Player':
                                            pg.mixer.Sound.play(self.click)
                                            self.stage = 'choose sp'
                                            self.map_scroll_index = 0
                                            self.max_map_scroll_index = max(len(self.maps_sp) - self.map_list_size, 0)
                                            self.scrollbar.update_length(self.scrollbar_bg_length // (self.max_map_scroll_index + 1))
                                            self.scrollbar.adjust_length(g)
                                            self.scrollbar.set_pos(g)
                                        elif option.content == 'Multiplayer':
                                            pg.mixer.Sound.play(self.click)
                                            self.stage = 'choose mp'
                                            self.map_scroll_index = 0
                                            self.max_map_scroll_index = max(len(self.maps_mp) - self.map_list_size, 0)
                                            self.scrollbar.update_length(self.scrollbar_bg_length // (self.max_map_scroll_index + 1))
                                            self.scrollbar.adjust_length(g)
                                            self.scrollbar.set_pos(g)
                                        elif option.content == 'Options':
                                            option.no_hover()
                                            pg.mixer.Sound.play(self.click)
                                            self.stage = 'options'
                                        elif option.content == 'Configure Game':
                                            pg.mixer.Sound.play(self.click)
                                            os.startfile('content')

                            elif self.stage == 'choose sp':
                                for i in range(self.map_scroll_index, min(len(self.sp_options), self.map_scroll_index+self.map_list_size)):
                                    if self.sp_options[i].rect.collidepoint((self.x, self.y)):
                                        self.mode = 'sp'
                                        self.map_choice = self.sp_options[i].content
                                        pg.mixer.music.stop()
                                        pg.mixer.Sound.play(self.click)
                                        pg.mouse.set_visible(False)
                                        self.fade.start_fade_out(self)
                                        waiting = False

                                if self.back_option.rect.collidepoint((self.x, self.y)):
                                    pg.mixer.Sound.play(self.click)
                                    self.stage = 'root'

                            elif self.stage == 'choose mp':
                                for i in range(self.map_scroll_index, min(len(self.mp_options), self.map_scroll_index+self.map_list_size)):
                                    if self.mp_options[i].rect.collidepoint((self.x, self.y)):
                                        self.mode = 'mp'
                                        self.map_choice = self.mp_options[i].content
                                        pg.mixer.music.stop()
                                        pg.mixer.Sound.play(self.click)
                                        pg.mouse.set_visible(False)
                                        self.fade.start_fade_out(self)
                                        waiting = False

                                if self.back_option.rect.collidepoint((self.x, self.y)):
                                    pg.mixer.Sound.play(self.click)
                                    self.stage = 'root'

                            elif self.stage == 'options':
                                if self.options_done.rect.collidepoint((self.x, self.y)):
                                    pg.mixer.Sound.play(self.click)
                                    self.stage = 'root'

                        elif self.stage == 'choose sp' or self.stage == 'choose mp':
                            if self.stage == 'choose sp':
                                options = self.sp_options
                            else:
                                options = self.mp_options

                            j = 0
                            if event.button == 4 and self.map_scroll_index > 0:
                                pg.mixer.Sound.play(self.click)
                                self.map_scroll_index -= 1
                                self.scrollbar.adjust_length(g)
                                self.scrollbar.set_pos(g)
                                for i in range(self.map_scroll_index,min(len(options), self.map_scroll_index + self.map_list_size)):
                                    options[i].pos = (options[i].pos[0], 215 + j * 40)
                                    options[i].update_base_pos_rect()
                                    j += 1

                            elif event.button == 5 and self.map_scroll_index < self.max_map_scroll_index:
                                pg.mixer.Sound.play(self.click)
                                self.map_scroll_index += 1
                                self.scrollbar.adjust_length(g)
                                self.scrollbar.set_pos(g)
                                for i in range(self.map_scroll_index, min(len(options), self.map_scroll_index + self.map_list_size)):
                                    options[i].pos = (options[i].pos[0], 215 + j * 40)
                                    options[i].update_base_pos_rect()
                                    j += 1

                    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and (self.stage == 'choose sp' or self.stage == 'choose mp' or self.stage == 'options'):
                        pg.mixer.Sound.play(self.click)
                        self.stage = 'root'


    def end_screen(self):
        # show end screen (game over)
        if not self.running:
            return

        pg.mouse.set_visible(True)
        if self.result == 'blue':
            if self.mode == 'sp':
                self.end_text = CenterText(WIN_TEXT, (DISPLAY_WIDTH/2,self.game_height/2-15), 40, WHITE)
            else:
                self.end_text = CenterText("Blue Wins", (DISPLAY_WIDTH/2,self.game_height/2-15), 40, WHITE)

        elif self.result == 'red':
            if self.mode == 'sp':
                self.end_text = CenterText(LOSE_TEXT, (DISPLAY_WIDTH/2,self.game_height/2-15), 40, WHITE)
            else:
                self.end_text = CenterText("Red Wins", (DISPLAY_WIDTH/2,self.game_height/2-15), 40, WHITE)

        elif self.result == 'tie':
            self.end_text = CenterText(TIE_TEXT, (DISPLAY_WIDTH/2,self.game_height/2-15), 40, WHITE)
        self.end_sub_text = CenterText("Press any key", (DISPLAY_WIDTH/2,self.game_height/2+25 ), 20, WHITE)

        self.screen.blit(self.map_img, (-self.cam.posx,-self.cam.posy))

        for blue in self.blues:
            blue.update(self)
        for red in self.reds:
            red.update(self)

        self.preview_box.update(self)
        self.turn_dialogue.update(self)
        self.turn_text.update(self)

        self.end_screen_dialogue.update(self)
        self.end_text.update(self)
        self.end_sub_text.update(self)

        pg.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    write_settings()
                    self.running = False
                elif event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button != 4 and event.button != 5):
                    pg.mixer.music.stop()
                    pg.mixer.Sound.play(self.click)
                    self.fade.end_fade_out(self)
                    waiting = False
                    self.start_screen()


g = Game()
g.start_screen()

while g.running:
    g.new()
    g.end_screen()

pg.quit()

import os
import requests

url = "https://census.lithafalcon.cc/get/ps2/item?name.en={0}&c:lang=en&c:show=item_id," \
      "name.en&c:join=item_to_weapon^inject_at:fire_mode_2(weapon^show:weapon_id(" \
      "weapon_to_fire_group^on:weapon_id^to:weapon_id(fire_group^on:fire_group_id^to:fire_group_id(" \
      "fire_group_to_fire_mode^on:fire_group_id^to:fire_group_id^list:1^inject_at:aiming_state(" \
      "fire_mode_2^on:fire_mode_id^to:fire_mode_id^inject_at:stats^list:1^show:fire_mode_id%27player_state_group_id" \
      "%27bullet_arc_kick_angle%27fire_ammo_per_shot%27fire_burst_count%27fire_pellets_per_shot%27recoil_angle_max" \
      "%27recoil_angle_min%27recoil_first_shot_modifier%27recoil_horizontal_max%27recoil_horizontal_min" \
      "%27recoil_horizontal_tolerance%27recoil_magnitude_max%27recoil_magnitude_min%27cof_recoil(" \
      "player_state_group_2^on:player_state_group_id^inject_at:cof_stats^show:cof_max%27cof_min))))))&c:join" \
      "=item_to_weapon^inject_at:ammo_stats^show:weapon_id(weapon_ammo_slot^on:weapon_id^to:weapon_id^show:clip_size)"


class BurstPattern:
    def __init__(self):
        self.name = ""
        self.recoil_stats = {
            "recoil_angle_max": 0,
            "recoil_angle_min": 0,
            "recoil_horizontal_tolerance": 0,
            "recoil_horizontal_max": 0,
            "recoil_horizontal_min": 0,
            "recoil_first_shot_modifier": 0,
            "recoil_magnitude_max": 0,
            "recoil_magnitude_min": 0
        }

        self.cof_stats = {
            "cof_max": 0,
            "cof_min": 0,
            "cof_recoil": 0
        }
        self.ammo = 0

    def set_stats_api(self, weapon_name):
        self.name = weapon_name
        data = requests.get(url.format(weapon_name)).json()
        print(data)

        weapon_data = data['item_list'][0]['fire_mode_2']['weapon_id_join_weapon']['weapon_id_join_weapon_to_fire_group']['fire_group_id_join_fire_group']['aiming_state'][1]['stats'][0]
        weapon_ammo = data['item_list'][0]['ammo_stats']['weapon_id_join_weapon_ammo_slot']['clip_size']
        self.ammo = weapon_ammo
        #print(weapon_data)
        #print(weapon_ammo)

        for stat in self.recoil_stats:
            if stat == 'cof_recoil':
                self.cof_stats['cof_recoil'] = weapon_data['cof_recoil']
                continue
            self.recoil_stats[stat] = weapon_data[stat]

        for stat in self.cof_stats:
            if stat == 'cof_recoil':
                continue
            self.cof_stats[stat] = weapon_data['cof_stats'][stat]

        print(self.recoil_stats)
        print(self.cof_stats)

    def run(self):
        return

    def iterate_recoil(self):
        return

    def iterate_cof(self):
        return

import datetime
import os

import auraxium
import requests

SERVICE_ID = os.getenv('SERVICE_ID')
TEST = False


async def item_added_updater(bot):
    print("doing stuff")
    client = auraxium.event.EventClient(service_id="s:" + str(SERVICE_ID))
    channel = bot.get_channel(1020419264798261328)
    war_assets_list = ["A.N.V.I.L. (Light)", "A.N.V.I.L. (Medium)", "A.N.V.I.L. (Heavy)", "Orbital Strike",
                       "Steel Rain"]

    @client.trigger(auraxium.event.ItemAdded, worlds=[13])
    async def itemadded_action_test(event):
        if TEST:
            if event.context == "GuildBankWithdrawal":
                print(event)
                char_id = event.character_id
                character_outfit_data = requests.get(
                    "https://census.daybreakgames.com/s:{0}/get/ps2:v2/outfit_member?character_id={1}&c:join=outfit^show:alias&c:join=character^show:name".format(
                        SERVICE_ID, char_id)).json()["outfit_member_list"][0]
                if character_outfit_data["outfit_id_join_outfit"]["alias"] == "HOT" or \
                        character_outfit_data["outfit_id_join_outfit"]["alias"] == "1VS4" or \
                        character_outfit_data["outfit_id_join_outfit"]["alias"] == "BAWC" or \
                        character_outfit_data["outfit_id_join_outfit"]["alias"] == "DIOR":
                    item_name = requests.get(
                        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/item?item_id={1}&c:show=name".format(
                            SERVICE_ID,
                            event.item_id)).json()[
                        "item_list"][0]["name"]["en"]
                    output = "; " + item_name + ";" + character_outfit_data["outfit_id_join_outfit"]["alias"] + ";" + \
                             character_outfit_data["character_id_join_character"]["name"][
                                 "first"] + "; zone_id: " + str(event.zone_id)
                    print(output)
                    log_output(output, "../log/ws.log", "%d/%m/%y;%H:%M:%S")
        else:
            if event.context == "GuildBankWithdrawal":
                char_id = event.character_id
                character_outfit_data = requests.get(
                    "https://census.daybreakgames.com/s:{0}/get/ps2:v2/outfit_member?character_id={1}&c:join=outfit^show:alias&c:join=character^show:name".format(
                        SERVICE_ID, char_id)).json()["outfit_member_list"][0]

                if character_outfit_data["outfit_id_join_outfit"]["alias"] == "H":
                    item_name = requests.get(
                        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/item?item_id={1}&c:show=name".format(
                            SERVICE_ID, event.item_id)).json()["item_list"][0]["name"]["en"]

                    # if item_name in war_assets_list:
                    if item_name in war_assets_list:
                        discord_output = datetime.datetime.now().strftime("%H:%M") + "; **" + item_name + "**; called by " + \
                                         character_outfit_data["character_id_join_character"]["name"]["first"]
                        await channel.send(discord_output)

                    output = "; " + item_name + ";" + character_outfit_data["outfit_id_join_outfit"]["alias"] + ";" + \
                             character_outfit_data["character_id_join_character"]["name"][
                                 "first"] + ";zone_id:" + str(event.zone_id)
                    print(output)
                    log_output(output, "../log/ws.log", "%d/%m/%y;%H:%M:%S")

                if character_outfit_data["outfit_id_join_outfit"]["alias"] == "RMIS":
                    item_name = requests.get(
                        "https://census.daybreakgames.com/s:{0}/get/ps2:v2/item?item_id={1}&c:show=name".format(
                            SERVICE_ID,
                            event.item_id)).json()[
                        "item_list"][0]["name"]["en"]
                    output = ";" + item_name + ";" + character_outfit_data["outfit_id_join_outfit"]["alias"] + ";" + \
                             character_outfit_data["character_id_join_character"]["name"]["first"] + ";zone_id:" + str(event.zone_id)
                    print(output)
                    log_output(output, "../log/ws.log", "%d/%m/%y;%H:%M:%S")

    @bot.slash_command(name="websocket_start")
    async def websocket_start(inter):
        print(inter)
        await client.connect()
        await inter.response.send_message("Websocket is running!")


def log_output(output, file, format):
    with open(file, "a+") as f:
        f.write(datetime.datetime.now().strftime(format) + str(output) + "\n")

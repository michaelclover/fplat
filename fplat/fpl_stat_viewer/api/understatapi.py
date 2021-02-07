# e.g.
# documentation at: https://readthedocs.org/projects/understat/downloads/pdf/latest/

'''from understat import Understat

import asyncio
import json
import aiohttp

async def understat_latest():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        player = await understat.get_league_players(
            "epl", 2018,
            player_name="Paul Pogba",
            team_title="Manchester United"
        )

        # write to file
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/understat.json'), 'w') as f:
            json.dump(player, f, ensure_ascii=False)

def get_understat_latest():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(understat_latest())'''

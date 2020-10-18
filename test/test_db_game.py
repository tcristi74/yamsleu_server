import logging
import logging.config
import random
import json
from dotenv import load_dotenv
import sys
import os
import pathlib
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from data.db_config import DbConfig # pylint: disable=F0401
from data.db_game import DbGame # pylint: disable=F0401
import datetime
import pytest

@pytest.fixture()
def db_play():
    print("setup")
    db_config_instance = DbConfig()
    db_play = DbGame(db_config_instance)
    yield db_play
    print("teardown")


@pytest.fixture()
def users_ids():
    print("setup")
    db_config_instance = DbConfig()
    db_play = DbGame(db_config_instance)
    res = db_play.get_query("select * from public.users limit 100")
    assert res[1]==None
    assert len(res[0][0])>2
    limit = min(len(res[0]),100)
    id = random.randint(0,limit-2)

    user1=res[0][id][0]
    user2=res[0][id+1][0]

    yield (user1,user2)
    print("teardown")

class TestDbGames():

    def test_create_game(self,db_play):

        res = db_play.new_game("game test 18")
        assert res[1]==None
        assert int(res[0])>0
        pytest.game_id=res[0]

    
    def test_create_play(self,db_play,users_ids):

        res = db_play.new_play([users_ids[0],users_ids[1]],pytest.game_id)
        assert res[1]==None
        pytest.player_id=res[0][0]

    def test_update_game(self,db_play,users_ids):
        update_dic = {
                    "started_at": datetime.datetime.now(),
                    "status": "started",
                    "game_comments": "this is a test",
                    "winner_id": pytest.player_id,
                    "score": 1000
                    }
        res = db_play.update_game(update_dic,pytest.game_id)
        assert res[1]==None



    def test_update_play(self,db_play,users_ids):

        update_dic = {
                  "current_position": -1,
                  "comments": "this is a test",
                  "current_score": 1000
                  }
        res = db_play.update_play(update_dic,pytest.game_id,users_ids[0])
        assert res[1]==None

    def test_update_tabel(self,db_play,users_ids):
        res = db_play.update_tabel("I1","3",pytest.game_id,users_ids[0],9)
        assert res[1]==None

    def test_get_plays(self,db_play):
        res = db_play.get_game_plays(pytest.game_id)
        assert res[1]==None


    def test_get_games_with_filters(self,db_play,users_ids):
        filters = {
                  "plays.user_id": users_ids[0]
                  }
        res = db_play.get_games(filters)
        assert res[1]==None



    




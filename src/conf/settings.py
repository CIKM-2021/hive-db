import os
from typing import List
from pydantic import BaseSettings
from google.oauth2 import service_account


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REGION: str = "asia-southeast1"
    SERVICE: str = "hive-api"
    VERSION: str = "v1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SUPPORTED_FIELDS = "block_id,id,previous,signing_key,timestamp,transaction_ids,witness,witness_signature,operations,operations.value.account,operations.value.amount,operations.value.allow_curation_rewards,operations.value.allow_votes,operations.value.author,operations.value.body,operations.value.expiration,operations.value.fee,operations.value.id,operations.value.json_str,operations.value.memo,operations.value.memo_key,operations.value.parent_author,operations.value.parent_permlink,operations.value.reward_hbd,operations.value.reward_hive,operations.value.reward_vests,operations.value.title,operations.value.voter,operations.value.weight,operations.value.witness"
    FIRST_BLOCK = "'42000001_43245905_01'"
    END_BLOCK = "'61318973_61422747_48'"
    PREFIX: str = f"{SERVICE}/{VERSION}"
    GOOGLE_KEY_FILE: str = ".env/Steemit-e706b5b8cead.json"
    HIVE_KEY: str = "WrrXP6szu06wlLQVfAM3b0FD8i4612zc"
    TABLES: str = "block_data_*"
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        env_file = ".env"

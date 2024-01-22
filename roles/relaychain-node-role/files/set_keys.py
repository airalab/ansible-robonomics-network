import os, json, argparse
import pandas as pd

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils import hasher


def main(target_mnemonic=None, rotate_keys_result=None, endpoint=None):
    substrate = SubstrateInterface(
        url="wss://"+endpoint,
        # ss58_format=42,
        type_registry_preset="rococo",
    )
    target_keypair = Keypair.create_from_mnemonic(target_mnemonic)

    print("Target: ", target_keypair.ss58_address)

    ### SET KEYS ###
    keys = {
        'grandpa': '0x'+rotate_keys_result[2:66], # '0x 0df6340dd9 b4a95d3ed1 ea0549005b 79eb632cd2 f4f0db1016 29add5aa16 3419',
        'babe': '0x'+rotate_keys_result[66:130],#4ca1fee15a5e51708d8bbae192020aecadd6e30d7217a077ebfcbed9e732db6a',
        'im_online': '0x'+rotate_keys_result[130:194],#'0x62d29e3e17f588fc8b5e3f7bb471b5c217180707ecff893531899fb325452b24',
        'para_validator': '0x'+rotate_keys_result[194:258], #'0xbc396f09d36adafb6413f99eeef574ee88883db56013fe80067dd4548376f213',
        'para_assignment': '0x'+rotate_keys_result[258:322], #'0xae85d8ef248ef4e68fb7b65cb0908d4226ea41c598495c29ec538d316c6c4923',
        'authority_discovery': '0x'+rotate_keys_result[322:386], #'0xa0e7ecb5640f11a3e73b4fa6e66510fa453b721e29b9c361d53cd806bfecc778',
        'beefy': '0x'+rotate_keys_result[386:], #'0x0362a70ca8d426e8cdc55ad8cc9912fef6bc2410c7c540d8d169058d14718ceb7b',
    }
    print("KEYS: ",keys)

    set_keys_call = substrate.compose_call(
        call_module='Session', 
        call_function='set_keys',
        call_params={
            "keys": keys,
            # "keys": {
            #     'grandpa': '0x 0df6340dd9 b4a95d3ed1 ea0549005b 79eb632cd2 f4f0db1016 29add5aa16 3419',
            #     'babe': '0x4ca1fee15a5e51708d8bbae192020aecadd6e30d7217a077ebfcbed9e732db6a',
            #     'im_online': '0x62d29e3e17f588fc8b5e3f7bb471b5c217180707ecff893531899fb325452b24',
            #     'para_validator': '0xbc396f09d36adafb6413f99eeef574ee88883db56013fe80067dd4548376f213',
            #     'para_assignment': '0xae85d8ef248ef4e68fb7b65cb0908d4226ea41c598495c29ec538d316c6c4923',
            #     'authority_discovery': '0xa0e7ecb5640f11a3e73b4fa6e66510fa453b721e29b9c361d53cd806bfecc778',
            #     'beefy':                '0x0362a70ca8d426e8cdc55ad8cc9912fef6bc2410c7c540d8d169058d14718ceb7b',
            #     }, 
            "proof": "0x01"
        }
    )
    set_keys_extrinsic = substrate.create_signed_extrinsic(call=set_keys_call, keypair=target_keypair)

    try:
        print("Set keys: ")
        receipt = substrate.submit_extrinsic(set_keys_extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'. Weight: '{}', total fee: '{}'.".format(receipt.extrinsic_hash, receipt.block_hash, receipt.weight, receipt.total_fee_amount))
    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))
    ### \SET KEYS ###

    return None


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--target_mnemonic', '-M', required=True, help='New validator address')
    parser.add_argument('--rotate_keys_result', '-K', required=True, help='Rotate keys result')
    parser.add_argument('--endpoint', '-E', required=True, help='Public Relay endpoint')
    args=parser.parse_args()

    main(target_mnemonic=args.target_mnemonic, rotate_keys_result=args.rotate_keys_result, endpoint=args.endpoint)
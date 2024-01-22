import os, json, argparse, time
import pandas as pd

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils import hasher


def main(target_addr=None, sudo_mnemonic=None, endpoint=None):
    substrate = SubstrateInterface(
        url="wss://"+endpoint,
        type_registry_preset="rococo",
    )
    sudo_keypair = Keypair.create_from_mnemonic(sudo_mnemonic)

    print("Sudo: ", sudo_keypair.ss58_address)

    ### SET BALANCE ###
    sudo_set_balance_call = substrate.compose_call(
        call_module='Sudo', 
        call_function='sudo',
        call_params={
            "call": {
                "call_module": 'Balances', 
                "call_function": 'set_balance',
                "call_args":{
                    "who": target_addr,
                    "new_free": 100000000000000,
                    "new_reserved": 10
                }
            }
        }
    )
    sudo_set_balance_extrinsic = substrate.create_signed_extrinsic(call=sudo_set_balance_call, keypair=sudo_keypair)

    # Send set_balance_extrinsic
    try:
        print("Set balance for validator: ")
        receipt = substrate.submit_extrinsic(sudo_set_balance_extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'. Weight: '{}', total fee: '{}'.".format(receipt.extrinsic_hash, receipt.block_hash, receipt.weight, receipt.total_fee_amount))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))
    ### \SET BALANCE ###
    
    substrate.close()
    return None


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--target_addr', '-T', required=True, help='New validator address')
    parser.add_argument('--sudo_mnemonic', '-S', required=True, help='Sudo mnemonic')
    parser.add_argument('--endpoint', '-E', required=True, help='Public Relay endpoint')
    args=parser.parse_args()

    main(target_addr=args.target_addr, sudo_mnemonic=args.sudo_mnemonic, endpoint=args.endpoint)
    time.sleep(12)
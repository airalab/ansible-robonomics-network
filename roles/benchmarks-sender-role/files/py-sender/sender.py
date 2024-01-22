import json, argparse, time, sched
from datetime import datetime, timedelta
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from multiprocessing import Process, current_process


parser=argparse.ArgumentParser()
parser.add_argument('--config', '-c', default="config.json", help='Config file path')
# parser.add_argument('--cores_number', '-n', required=True, default=1, help='Number of used cores')
args=parser.parse_args()


def schedule_it(scheduler, frequency, duration, callable, *args):
    no_of_events = int( duration / frequency )
    priority = 1 # not used, lets you assign execution order to events scheduled for the same time
    for i in range(no_of_events):
        delay = i * frequency
        scheduler.enter( delay, priority, callable, args)

def send_tx(substrate, keypair, nonce_gen, call_module, call_function, call_params):
    # print(call_params)
    call = substrate.compose_call(
        call_module = call_module,
        call_function = call_function,
        call_params = call_params
    )
    nonce=next(nonce_gen)
    print(nonce)
    extrinsic = substrate.create_signed_extrinsic(
        call=call, 
        keypair=keypair, 
        nonce=nonce,
        era={'period': 20}        
    )
    # try:
    r = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
    # except SubstrateRequestException as e:
    #     print(e)
    #     print("Exception nonce: ", nonce)
    #     # time.sleep(5)
    #     # r = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
    return None


def main(config):
    print('connecting to', config['request_url'], '...')
    substrate = SubstrateInterface(
        url=config['request_url'],
        # url="ws://127.0.0.1:9944",
        # url="wss://mercury.frontier.rpc.robonomics.network",
        ss58_format=32,
        type_registry_preset="substrate-node-template",
        type_registry={
            "types": {
                "Record": "Vec<u8>",
                "<T as frame_system::Config>::AccountId": "AccountId",
                "RingBufferItem": {
                    "type": "struct",
                    "type_mapping": [
                        ["timestamp", "Compact<u64>"],
                        ["payload", "Vec<u8>"],
                    ],
                },
            }
        }
    )
    print('ok')

    start_time = datetime.now()
    start_block = substrate.get_block_number(substrate.get_chain_head())
    print(
            "Start txs send to the chain",
            "\nStart time: ", start_time,
            "\nStart block: ", start_block,
            "\nSend frequency: ", config["send_frequency"], "txs per second",
            "\nSend duration: ", config["send_duration"], "seconds"
        )

    procs = []
    for sender in config['senders']:

        substrate = SubstrateInterface(
            url=config['request_url'],
            ss58_format=32,
            type_registry_preset="substrate-node-template",
            type_registry={
                "types": {
                    "Record": "Vec<u8>",
                    "<T as frame_system::Config>::AccountId": "AccountId",
                    "RingBufferItem": {
                        "type": "struct",
                        "type_mapping": [
                            ["timestamp", "Compact<u64>"],
                            ["payload", "Vec<u8>"],
                        ],
                    },
                }
            }
        )
        keypair = Keypair.create_from_seed(sender)
        current_nonce = substrate.get_account_nonce(keypair.ss58_address)
        print(current_nonce)

        # Nonce generator for current address
        nonce_gen = ( i for i in range(current_nonce, current_nonce + (config["send_frequency"] * config["send_duration"])) )

        scheduler = sched.scheduler(time.time, time.sleep)
        schedule_it(
            scheduler,
            1/config["send_frequency"], 
            config["send_duration"], 
            send_tx, 
            substrate, 
            keypair, 
            nonce_gen,
            config['call_module'],
            config['call_function'], 
            config['call_params']
        )

        proc = Process(target=scheduler.run)
        procs.append(proc)
        proc.start()
        
    for proc in procs:
        proc.join()
        
    print(
        "\n****************************",
        "\nSend duration: ", config["send_duration"], 
        "\nReal time: ", datetime.now() - start_time,
        "\nSended txs: ", config["send_frequency"] * config["send_duration"] * len(config["senders"]), 
    )


if __name__ == "__main__":
    with open(args.config, 'r') as f:
        config = json.load(f)
    # print(config)
    # cores_number = int(args.cores_number)
    main(config)
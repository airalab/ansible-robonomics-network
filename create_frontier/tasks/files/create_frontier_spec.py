#!/usr/bin/env python3
import argparse, simplejson, json


def change_dict_value(d, key, new_value):
    # print(key in d)
    if key in d:
        d[key] = new_value
    else:
        print("Field ['"+key+"'] not exists in the rococo_local_testnet spec")
    return None
 

def main(config_path, input_spec_path, output_spec_path, balances_path, session_keys_path, sudo_addr):
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    with open(input_spec_path, "r") as input_spec_file:
        data = json.load(input_spec_file)

    with open(balances_path, "r") as balances_path_file:
        balances = json.load(balances_path_file)

    with open(session_keys_path, "r") as session_keys_file:
        session_keys = json.load(session_keys_file)

    change_dict_value(data, "name", config['spec']['name'])
    change_dict_value(data, "id", config['spec']['id'])
    change_dict_value(data, "chainType", config['spec']['chainType'])
    change_dict_value(data, "telemetryEndpoints", [["/dns/"+config["spec"]["telemetryUrl"]+"/tcp/443/x-parity-wss/%2Fsubmit%2F", 0]])
    change_dict_value(data, "protocolId", config['spec']['protocolId'])
    change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["registrar"], "nextFreeParaId", config['spec']['nextFreeParaId'])
    change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["balances"], "balances", balances)
    change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["session"], "keys", session_keys)
    change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["sudo"], "key", sudo_addr)
    # change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["bridgeRococoGrandpa"], "owner", sudo_addr)
    # change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["bridgeWococoGrandpa"], "owner", sudo_addr)
    # change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["bridgeRococoMessages"], "owner", sudo_addr)
    # change_dict_value(data["genesis"]["runtime"]["runtime_genesis_config"]["bridgeWococoMessages"], "owner", sudo_addr)

    # Using simplejson for pretty json in output file
    output_spec_file = open(output_spec_path, "w")
    output_spec_file.write(simplejson.dumps(data, indent=4))
    output_spec_file.close()


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--config_path', '-C', required=True, help='Path to  config file')
    parser.add_argument('--input_spec_path', '-I', required=True, help='Path to input spec')
    parser.add_argument('--output_spec_path', '-O', required=True, help='Path to output spec')
    parser.add_argument('--sudo_addr', '-s', required=True, help='Sudo addr ss58')
    parser.add_argument('--balances_path', '-B', required=True, help='Path to balances.json')
    parser.add_argument('--session_keys_path', '-S', required=True, help='Path to session.json')
    args=parser.parse_args()

    main(
        args.config_path, 
        args.input_spec_path, 
        args.output_spec_path,
        args.balances_path,
        args.session_keys_path,
        args.sudo_addr
    )
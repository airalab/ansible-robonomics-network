import { ApiPromise, WsProvider } from "@polkadot/api";
import { Keyring } from "@polkadot/keyring";
import config from "../config.json";

export const keyring = new Keyring({
  ss58Format: 42,
  type: "sr25519",
});

export default async function () {
  return await ApiPromise.create({
    provider: new WsProvider(config.api),
    types: {
      LiabilityIndex: "Vec<u8>",
      TechnicalReport: "Vec<u8>",
      Parameter: "Vec<u8>",
      Record: "Vec<u8>",
      TechnicalParam: "Vec<u8>",
      EconomicalParam: "{}",
      ProofParam: "MultiSignature",
    },
  });
}

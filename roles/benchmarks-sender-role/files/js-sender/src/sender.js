import getApi, { keyring } from "./api";
import config from "../config.json";
import keys from "../keys.json";

function sendSubstrate(api, account, data, nonce) {
  const tx = api.tx.datalog.record(data);
  return tx.signAndSend(account, {
    nonce,
  });
}

export async function loop(api, pairs, nonce) {
  const list = [];
  for (const pair of pairs) {
    list.push(sendSubstrate(api, pair.pair, config.data, pair.nonce + nonce));
  }
  return Promise.all(list);
}

function timeout(t) {
  return new Promise((res) => {
    setTimeout(() => {
      res();
    }, t);
  });
}

async function main() {
  const api = await getApi();
  try {
    const pairs = [];
    for (const m of keys) {
      const pair = keyring.addFromUri(m);
      const nonce = await api.rpc.system.accountNextIndex(pair.address);
      pairs.push({ pair, nonce: Number(nonce) });
    }

    const start = Date.now();
    console.log("Start", new Date(start).toLocaleString());

    const count = config.count;
    const time = config.time;
    const steps = config.steps;
    let count_tx = 0;
    let i = 0;

    const count_accounts = pairs.length;

    for (let step = 0; step < steps; step++) {
      let count_tx_step = 0;
      const start_step = Date.now();
      for (let sub_step = 0; sub_step < count; sub_step++) {
        const d = Date.now() - start_step;
        if (d > time) {
          break;
        }
        await loop(api, pairs, i);
        i++;
        count_tx = count_tx + count_accounts;
        count_tx_step = count_tx_step + count_accounts;
      }
      const end_step = Date.now();
      const d = end_step - start_step;
      if (d < time) {
        await timeout(time - d);
      }

      console.log(
        "step",
        step,
        (end_step - start_step) / 1000 + "s",
        "tx",
        count_tx_step
      );
    }

    const end = Date.now();
    console.log("End", new Date(end).toLocaleString());
    console.log("Duration", (end - start) / 1000 + "s");
    console.log("tx count", count_tx);
    // await timeout(15000);
    process.exit(0);
  } catch (error) {
    console.log("error", error);
  }
}
main();

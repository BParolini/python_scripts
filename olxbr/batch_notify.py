import argparse
import time

import requests

parse = argparse.ArgumentParser(prog="batch_notify", description="Notifies listings")
parse.add_argument("-e", "--env", choices=["prod", "qa", "local"], required=True)
parse.add_argument(
    "-a",
    "--actions",
    choices=["crude", "unit", "exporter", "notify", "dedup"],
    required=True
)
parse.add_argument("-f", "--file", required=True)
parse.add_argument("-l", "--lines", required=True)
parse.add_argument("-w", "--wait", required=False)

args = parse.parse_args()

environments = {
    "prod": "https://listings-api.re-listings.prod.olxbr.io/v4/listings/actions",
    "qa": "https://listings-api.re-listings.preprod.olxbr.io/v4/listings/actions",
    "local": "http://localhost:8080/v4/listings/actions",
}

actions = {
    "crude": "notify-to-crude",
    "unit": "notify-to-unit",
    "exporter": "notify-to-exporter",
    "notify": "notify",
    "dedup": "notify-dedup-image?force=true",
}

endpoint = f"{environments[args.env]}/{actions[args.actions]}"
wait_time: int = int(args.wait) if args.wait else 20

with open(args.file) as file:
    lines = file.readlines()

print(f"Endpoint: {endpoint}")
print(f"Wait time: {wait_time}")
print(f"File: {args.file} - {len(lines)} lines")
print(f"Lines per iteration: {args.lines}")
print()

# Spliting file lines into chunks
chunks = [lines[i:i + args.lines]
                     for i in range(0, len(lines), args.lines)]
print(f"Chunks: {len(chunks)}")

for idx, chunk in enumerate(chunks):
    print(f"Sending chunk {idx}/{len(chunks)}")

    ids = ",".join(chunk)
    print(f"Request {endpoint}")
    print(f"{ids:<80}")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(endpoint, headers=headers, json=f"[{ids}]")

    print(f"Request response: {response.status_code}")

    time.sleep(wait_time)

import json
import time

import yaml
from metaflow import FlowSpec, environment, kubernetes, resources, step


class CityLatencyFlow(FlowSpec):
    @kubernetes(secrets=["aws-credentials"])
    @environment(
        vars={
            "AWS_DEFAULT_REGION": "us-east-1",
        }
    )
    @resources(cpu=1, memory=1024)
    @step
    def start(self):
        # Read config
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.cities = cfg["cities"]
        # Prepare list of (code, num)
        self.city_list = [(c["code"], c["num"]) for c in self.cities]
        self.next(self.process_city, foreach="city_list")

    @kubernetes(secrets=["aws-credentials"])
    @environment(
        vars={
            "AWS_DEFAULT_REGION": "us-east-1",
        }
    )
    @resources(cpu=1, memory=2048)
    @step
    def process_city(self):
        # In a foreach branch: self.input holds one item from city_list
        code, num = self.input
        print(f"[{code}] starting loop up to {num}")
        start_time = time.time()
        for i in range(num):
            print(f"[{code}] i = {i}")
            time.sleep(1)
        elapsed = time.time() - start_time
        result = {"city": code, "latency_seconds": round(elapsed, 2)}
        # store result artifact
        self.result = result
        print(f"[{code}] done, latency = {elapsed:.2f}")
        self.next(self.join_results)

    @kubernetes(secrets=["aws-credentials"])
    @environment(
        vars={
            "AWS_DEFAULT_REGION": "us-east-1",
        }
    )
    @resources(cpu=1, memory=2048)
    @step
    def join_results(self, inputs):
        # inputs is a list of branch tasks
        latencies = {}
        for inp in inputs:
            res = inp.result
            latencies[res["city"]] = res["latency_seconds"]
        self.latencies = latencies
        print("Aggregated latencies:", self.latencies)
        self.next(self.end)

    @kubernetes(secrets=["aws-credentials"])
    @environment(
        vars={
            "AWS_DEFAULT_REGION": "us-east-1",
        }
    )
    @resources(cpu=1, memory=2048)
    @step
    def end(self):
        # Optionally write out to file, or print JSON
        print("Final latencies dict:", self.latencies)
        # write to JSON file
        with open("latencies.json", "w") as f:
            json.dump(self.latencies, f)
        print("Wrote latencies.json")


if __name__ == "__main__":
    CityLatencyFlow()

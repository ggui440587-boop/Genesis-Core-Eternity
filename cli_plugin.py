import argparse
class CLIPlugin:
    def __init__(self):
        p = argparse.ArgumentParser()
        p.add_argument("--interval", type=int, default=10)
        self.args, _ = p.parse_known_args()
    def get_settings(self): return False, self.args.interval

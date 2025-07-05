# aeva_dimengate_void.py

import os


class DimenGateVoid:
    def __init__(self):
        self.void_dir = "assets/data/void_dump"
        os.makedirs(self.void_dir, exist_ok=True)

    def erase_data(self, filename="discarded.txt"):
        void_path = os.path.join(self.void_dir, filename)
        with open(void_path, "w") as f:
            f.write("Purged to Void. No trace remains.\n")
        print(f"[DimenGate:Void] {filename} sent to digital void.")


# Example
if __name__ == "__main__":
    void = DimenGateVoid()
    void.erase_data("intrusion.log")

# ~/aeva/aeva_prismatrix.py

import os
from datetime import datetime
from modules.utilities import ensure_dir, get_device_info

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Prismatrix] ⚠️ OpenCV (cv2) not available. Visual simulations limited.")


class Prismatrix:
    def __init__(
            self,
            brain=None,
            output_dir="assets/data/visual_simulations"):
        self.brain = brain
        self.output_dir = output_dir
        ensure_dir(self.output_dir)
        self.device_info = get_device_info()
        print(
            "[Prismatrix] 🧩 Quantum visual deconstruction online on:",
            self.device_info['node'])

    def deconstruct_scene(self, frame_path):
        if not CV2_AVAILABLE:
            print("[Prismatrix] ❌ OpenCV is not installed. Cannot perform analysis.")
            return None

        if not isinstance(frame_path, str) or not os.path.exists(frame_path):
            print(f"[Prismatrix] 🚫 Invalid frame path: {frame_path}")
            return None

        print(f"[Prismatrix] 🌀 Analyzing frame: {frame_path}")
        img = cv2.imread(frame_path)
        if img is None:
            print(
                f"[Prismatrix] 🛑 Failed to read image data from: {frame_path}")
            return None

        result = {
            "device": self.device_info,
            "timestamp": self._timestamp()
        }

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result["grayscale"] = self._save_image(gray, "gray")

        edges = cv2.Canny(gray, 75, 150)
        result["edges"] = self._save_image(edges, "edges")

        contours_img = self._extract_contours(img, edges)
        result["contours"] = self._save_image(contours_img, "contours")

        if self.brain and hasattr(self.brain, "memory"):
            self.brain.memory.save_memory_entry("visual_analysis", result)

        print("[Prismatrix] ✅ Scene analysis complete.")
        return result

    def _extract_contours(self, image, edge_map):
        contours_img = image.copy()
        contours, _ = cv2.findContours(
            edge_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(contours_img, contours, -1, (0, 255, 0), 1)
        return contours_img

    def _save_image(self, image, prefix="output"):
        filename = f"{prefix}_{self._timestamp()}.png"
        path = os.path.join(self.output_dir, filename)
        success = cv2.imwrite(path, image)
        if success:
            print(f"[Prismatrix] 📸 Saved: {path}")
        else:
            print(f"[Prismatrix] ❌ Failed to save: {path}")
        return path

    def _timestamp(self):
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


# Optional test block
if __name__ == "__main__":
    prism = Prismatrix()
    test_file = "sample_input.jpg"
    result = prism.deconstruct_scene(test_file)
    if result:
        for k, v in result.items():
            print(f"{k}: {v}")

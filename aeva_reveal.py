# aeva_reveal.py

import cv2
import os
import json
import numpy as np
from datetime import datetime
from skimage import restoration
from PIL import Image, ImageFilter


class AevaReveal:
    def __init__(self, save_path="assets/data/revealed"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)
        self.log = []

    def _save_log(self):
        with open(os.path.join(self.save_path, "reveal_log.json"), "w") as f:
            json.dump(self.log, f, indent=4)

    def _log(self, action, source, result):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "source": source,
            "result": result
        }
        self.log.append(entry)
        self._save_log()
        print(f"[Reveal] {action} complete → {result}")

    def deblur(self, input_path):
        img = cv2.imread(input_path)
        if img is None:
            print("[Reveal] Invalid image.")
            return None

        kernel = np.array([[1, 4, 6, 4, 1],
                           [4, 16, 24, 16, 4],
                           [6, 24, 36, 24, 6],
                           [4, 16, 24, 16, 4],
                           [1, 4, 6, 4, 1]]) / 256

        deblurred = cv2.filter2D(img, -1, kernel)
        filename = os.path.join(
            self.save_path, f"deblurred_{
                os.path.basename(input_path)}")
        cv2.imwrite(filename, deblurred)
        self._log("Deblur", input_path, filename)
        return filename

    def denoise(self, input_path):
        img = cv2.imread(input_path)
        if img is None:
            print("[Reveal] Invalid image.")
            return None

        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        filename = os.path.join(
            self.save_path, f"denoised_{
                os.path.basename(input_path)}")
        cv2.imwrite(filename, denoised)
        self._log("Denoise", input_path, filename)
        return filename

    def decensor_blur(self, input_path):
        try:
            pil_image = Image.open(input_path).convert("RGB")
            sharpened = pil_image.filter(
                ImageFilter.UnsharpMask(
                    radius=2, percent=150, threshold=3))
            filename = os.path.join(
                self.save_path, f"decensored_{
                    os.path.basename(input_path)}")
            sharpened.save(filename)
            self._log("Decensor-Blur", input_path, filename)
            return filename
        except Exception as e:
            print(f"[Reveal] Error in decensoring: {e}")
            return None

    def enhance_video(self, input_path):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("[Reveal] Failed to open video.")
            return None

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_file = os.path.join(
            self.save_path, f"enhanced_{
                os.path.basename(input_path)}")
        out = cv2.VideoWriter(
            output_file, fourcc, 20.0, (int(
                cap.get(3)), int(
                cap.get(4))))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
            frame = cv2.filter2D(frame, -1, np.ones((3, 3), np.float32) / 9)
            out.write(frame)

        cap.release()
        out.release()
        self._log("EnhanceVideo", input_path, output_file)
        return output_file


# Example Usage
if __name__ == "__main__":
    reveal = AevaReveal()
    reveal.deblur("input_image.png")
    reveal.denoise("input_image.png")
    reveal.decensor_blur("input_image.png")
    reveal.enhance_video("input_video.mp4")

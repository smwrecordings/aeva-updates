# aeva_vision.py

from PIL import Image, ImageEnhance, ImageFilter
import imageio.v2 as imageio
import os
import numpy as np


class VisionModule:
    def __init__(self, brain=None):
        self.brain = brain
        self.vision_path = "assets/vision/logs"
        os.makedirs(self.vision_path, exist_ok=True)

    def scan_environment(self, image_path="assets/data/vision/latest.jpg"):
        try:
            print("[AevaVision] Scanning environment...")
            image = Image.open(image_path).convert("RGB")
            summary = self.analyze_image(image)
            print(f"[AevaVision] Scan complete: {summary}")
        except Exception as e:
            print(f"[AevaVision] Error during scan: {e}")

    def analyze_image(self, image):
        size = image.size
        mode = image.mode
        brightness = ImageEnhance.Brightness(image).enhance(1.0)
        color_data = np.array(brightness)
        avg_color = tuple(np.mean(color_data, axis=(0, 1)).astype(int))

        return {
            "Resolution": f"{size[0]}x{size[1]}",
            "Mode": mode,
            "Average Color (RGB)": avg_color
        }

    def save_snapshot(self, input_path, output_name="snapshot.jpg"):
        try:
            image = Image.open(input_path)
            save_path = os.path.join(self.vision_path, output_name)
            image.save(save_path)
            print(f"[AevaVision] Snapshot saved as {save_path}")
        except Exception as e:
            print(f"[AevaVision] Snapshot error: {e}")

    def enhance_image(
            self,
            path,
            output="enhanced.jpg",
            sharpness=2.0,
            contrast=1.5):
        try:
            image = Image.open(path)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)
            out_path = os.path.join(self.vision_path, output)
            image.save(out_path)
            print(f"[AevaVision] Image enhanced and saved to {out_path}")
        except Exception as e:
            print(f"[AevaVision] Enhancement failed: {e}")

    def apply_filter(self, path, filter_type="EDGE_ENHANCE"):
        try:
            image = Image.open(path)
            filter_map = {
                "BLUR": ImageFilter.BLUR,
                "CONTOUR": ImageFilter.CONTOUR,
                "DETAIL": ImageFilter.DETAIL,
                "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
                "SHARPEN": ImageFilter.SHARPEN,
                "SMOOTH": ImageFilter.SMOOTH
            }
            filtered = image.filter(
                filter_map.get(
                    filter_type.upper(),
                    ImageFilter.EDGE_ENHANCE))
            output_path = os.path.join(
                self.vision_path, f"{
                    filter_type.lower()}_filtered.jpg")
            filtered.save(output_path)
            print(
                f"[AevaVision] {filter_type} filter applied and saved to {output_path}")
        except Exception as e:
            print(f"[AevaVision] Filter application error: {e}")


# Optional test run
if __name__ == "__main__":
    vision = AevaVision()
    vision.scan_environment()

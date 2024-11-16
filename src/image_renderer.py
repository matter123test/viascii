from PIL import Image

from src.utils import clear_screen


class ImageRenderer:
    def __init__(self, args) -> None:
        self.args = args

    def pixel_to_ascii(self, brightness) -> str:
        numchars = len(self.args.grayscale)
        return self.args.grayscale[int(brightness / 255 * (numchars - 1))]

    def rgb_to_ansi_bg(self, r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"  # ANSI background color

    def rgb_to_ansi_fg(self, r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"  # ANSI foreground color

    def image_to_ascii_rgb(self, image) -> str:
        ascii_image = ""

        width, height = self.args.dimensions
        image = image.resize((width, height))

        pixels = image.load()

        for x in range(width):
            line = ""
            for y in range(height):
                r, g, b = pixels[x, y]
                brightness = int(
                    0.299 * r + 0.587 * g + 0.114 * b
                )  # Calculate brightness
                ascii_char = self.pixel_to_ascii(brightness)
                bg_color = self.rgb_to_ansi_bg(r, g, b)  # Get ANSI color code
                fg_color = self.rgb_to_ansi_fg(
                    min(255, r + self.args.contrast),
                    min(255, g + self.args.contrast),
                    min(255, b + self.args.contrast),
                )  # Change the font's contrast

                line += f"{fg_color}{bg_color}{ascii_char}\033[0m"  # Reset color after each char

            ascii_image += line + "\n"

        return ascii_image

    def image_to_ascii_bw(self, image) -> str:
        ascii_image = ""

        width, height = self.args.dimensions
        image = image.resize((width, height))

        pixels = image.load()

        for x in range(width):
            line = ""
            for y in range(height):
                brightness = pixels[x, y]
                ascii_char = self.pixel_to_ascii(brightness)
                line += ascii_char
            ascii_image += line + "\n"

        return ascii_image

    def print_image(self, image_path, is_rgb: bool, angle: int) -> None:
        clear_screen()

        if is_rgb:
            rgb_image = Image.open(image_path).convert("RGB")
            rgb_image = rgb_image.rotate(angle)
            rgb_ascii_image = self.image_to_ascii_rgb(rgb_image)

            ascii_image = rgb_ascii_image
        else:
            bw_image = Image.open(image_path).convert("L")
            bw_image = bw_image.rotate(angle)
            bw_ascii_image = self.image_to_ascii_bw(bw_image)

            ascii_image = bw_ascii_image

        print(ascii_image)

        if self.args.savepath is not None:
            self.save_image(ascii_image)

    def save_image(self, ascii_image: str) -> None:
        with open(self.args.savepath, "w") as f:
            f.write(ascii_image)

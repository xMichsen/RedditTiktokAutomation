from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class ImageService:
    def __init__(self, width=800, background_color=(26, 26, 27),
                 text_color=(255, 255, 255), font_path=None, font_size=32):
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.font_path = font_path or "./fonts/reddit_sans/RedditSans-VariableFont_wght.ttf"
        self.normal_font = "./fonts/reddit_sans/RedditSans-VariableFont_wght.ttf"
        self.font_size = font_size
        # Font for username and upvotes/downvotes
        self.small_font_size = int(font_size * 0.6)
        self.small_font = ImageFont.truetype(self.normal_font, self.small_font_size)
        self.avatar_size = (50, 50)  # Size of the avatar

    def create_reddit_style_image(self, text, output_path, subreddit, username="", upvote_arrow_path='./assets/heart.png', bubble_path='./assets/bubble.png'):
        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            print("Error: Cannot open font file. Please ensure the font path is correct.")
            return

        # Wrapping text
        wrap_width = 45  # Adjust as needed
        wrapped_text = textwrap.fill(text, width=wrap_width)
        lines = wrapped_text.split('\n')

        # Setting line height
        ascent, descent = font.getmetrics()
        line_height = ascent + descent  # Adding 10 pixels for spacing between lines

        # Calculating total text height
        total_text_height = line_height * len(lines)

        # Header height (avatar, username, subreddit)
        header_height = max(self.avatar_size[1], self.small_font_size * 2 + 10) + 40  # 20 pixels padding

        # Calculating total image height
        total_height = header_height + total_text_height + 25  # 20 pixels padding at the bottom

        # Creating a new image with the calculated height
        img = Image.new('RGB', (self.width, total_height), color=self.background_color)
        draw = ImageDraw.Draw(img)

        # Adding user avatar from image in the top left corner
        try:
            avatar_image = Image.open('./assets/avatar.png').convert("RGBA")
            avatar_image = avatar_image.resize(self.avatar_size)
            avatar_position = (10, 10)
            img.paste(avatar_image, avatar_position, avatar_image)
        except IOError:
            print("Error: Cannot open avatar image. Ensure the path is correct.")
            return

        # Drawing username in the top left corner
        username_text = f"u/{username}"
        username_position = (self.avatar_size[0] + 20, 10)
        draw.text(username_position, username_text, fill=self.text_color, font=self.small_font)

        # Drawing subreddit name below the username
        subreddit_text = f"r/{subreddit}"
        subreddit_position = (username_position[0], username_position[1] + self.small_font_size + 5)
        draw.text(subreddit_position, subreddit_text, fill=self.text_color, font=self.small_font)

        # Calculating subreddit text width
        subreddit_text_width = draw.textlength(subreddit_text, font=self.small_font)

        # Drawing the time ago the post was made (3m, 4y, 2h)
        time_ago_text = "• 3m"
        time_ago_position = (subreddit_position[0] + subreddit_text_width + 5, subreddit_position[1])
        draw.text(time_ago_position, time_ago_text, fill=self.text_color, font=self.small_font)

        # Drawing heart icon with upvotes count and bubble icon with comments count in the bottom left corner
        upvotes_and_comments_text = "99+"
        upvote_arrow = Image.open(upvote_arrow_path).convert("RGBA")
        bubble = Image.open(bubble_path).convert("RGBA")
        upvote_arrow = upvote_arrow.resize((20, 20))
        bubble = bubble.resize((20, 20))
        upvote_arrow_position = (20, total_height - 30)
        bubble_position = (upvote_arrow_position[0] + 65, upvote_arrow_position[1])
        img.paste(upvote_arrow, upvote_arrow_position, upvote_arrow)
        img.paste(bubble, bubble_position, bubble)
        draw.text((upvote_arrow_position[0] + 25, upvote_arrow_position[1] - 3), upvotes_and_comments_text, fill='lightgray', font=self.small_font)
        draw.text((bubble_position[0] + 25, bubble_position[1] - 3), upvotes_and_comments_text, fill='lightgray', font=self.small_font)
        
        # Drawing share icon and share text next to it in the bottom right corner
        share_text = "Share"
        share_icon = Image.open('./assets/share.png').convert("RGBA")
        share_icon = share_icon.resize((20, 20))
        share_icon_position = (self.width - 90, total_height - 30)
        img.paste(share_icon, share_icon_position, share_icon)
        draw.text((share_icon_position[0] + 25, share_icon_position[1] - 3), share_text, fill='lightgray', font=self.small_font)

        # Starting y position for text (below the header)
        y = header_height

        # Drawing each line of text
        for line in lines:
            draw.text((20, y), line, fill=self.text_color, font=font, anchor="lm", align="left")
            y += line_height

        # Saving the image
        os.makedirs('./output_images', exist_ok=True)
        img.save(output_path)
        print(f"Image saved as {output_path}.")

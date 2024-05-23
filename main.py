from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import userInfo
import requests
import os
import warnings
import subprocess
import platform

warnings.filterwarnings("ignore", category=DeprecationWarning)

class CreateEnvelope:
    def __init__(self):
        self.is_date = False
        self.sender_name = ""
        self.sender_address = ""
        self.sender_dist_city = ""
        self.receiver_address = ""
        self.jail_name = ""
        self.relative_name = ""
        self.dorm_num = ""
        self.receiver_name = ""
        self.jail_city = ""

    def create_envelope(self):
        """Create an envelope with the given information."""
        todays_date = datetime.today().strftime('%d/%m/%Y')

        # Create a blank envelope
        template = Image.open('background.png').resize((680, 491), resample=Image.LANCZOS)
        
        # Add the logo to the envelope
        logo = Image.open('logo-dark.png').resize((60,45), resample=Image.LANCZOS)
        template.paste(logo, (596,22), logo)

        # Add the date to the envelope
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('./GoudyBookletter1911-Regular.ttf', size=14)
        
        if (self.is_date):
            draw.text((596,65), todays_date, font=font, fill="black")

        # Add the sender address to the envelope
        font = ImageFont.truetype('./Lobster-Regular.ttf', size=32)
        draw.text((21,20), "Aracı Firma: Mektupevi.com", font=font, fill="black")
        draw.text((21,60), f"Gönderen: {self.sender_name}", font=font, fill="black")
        font = ImageFont.truetype('./GoudyBookletter1911-Regular.ttf', size=21)
        y_after_sender = self.draw_sender_address(template, self.sender_address, font, 21, 106)

        # Add the sender district info to the envelope
        if self.sender_dist_city:
            y = y_after_sender + 2
            draw.text((21, y), self.sender_dist_city, font=font, fill="black")

        # Add the receiver jail address to the envelope
        max_width = 658
        y_after_sender = self.draw_receiver_address(template, self.receiver_address, font, max_width, 21, 450)- 27
        
        # Add additional receiver infos to the envelope
        draw.text((21, y_after_sender), self.jail_name, font=font, fill="black")
        
        if self.relative_name:
            y_after_sender -= 27
            draw.text((21, y_after_sender), "Baba Adı: " + self.relative_name, font=font, fill="black")

        if self.dorm_num:
            y_after_sender -= 27
            draw.text((21, y_after_sender), "Koğuş No: " + self.dorm_num, font=font, fill="black")

        y_after_sender -= 27
        bold_font = ImageFont.truetype("./GoudyBookletter1911-Regular.ttf", 21)
        draw.text((21, y_after_sender), "Alıcı: ", font=bold_font, fill="black", weight=700)
        draw.text((21, y_after_sender), "Alıcı: ", font=bold_font, fill="black", weight=700)
        draw.text((21, y_after_sender), "Alıcı: ", font=bold_font, fill="black", weight=700)
        draw.text((21 + draw.textsize("Alıcı: ", font=bold_font)[0], y_after_sender), self.receiver_name, font=font, fill="black")

        # Create directories
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') if platform.system() == 'Windows' else os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        zarflar_dir = os.path.join(desktop_path, "Zarflar")
        sender_dir = os.path.join(zarflar_dir, self.sender_name.replace(' ', '_'))

        os.makedirs(sender_dir, exist_ok=True)

        # Save the envelope
        try:
            envelope_path = os.path.join(sender_dir, "envelope.png")
            template.save(envelope_path)
            self.open_envelope_directory(envelope_path)
            print("Zarf başarıyla kaydedildi:", envelope_path)
        except Exception as e:
            print("Zarf kaydedilirken bir hata oluştu. Hata:", e)

    def open_envelope_directory(self, envelope_path):
        """Opens the directory containing the saved envelope."""
        try:
            if platform.system() == "Windows":
                os.startfile(os.path.dirname(envelope_path))
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", os.path.dirname(envelope_path)])
            else:  # Linux
                subprocess.Popen(['xdg-open', os.path.dirname(envelope_path)])
        except Exception as e:
            print("Klasör açılırken bir hata oluştu:", e)


    def draw_sender_address(self, image, text, font, start_x, start_y):
        """Draw the sender address on the envelope. Return the y-coordinate after the address."""
        draw = ImageDraw.Draw(image)
        wrapped_text = textwrap.fill(text, width=75)

        # Metni yazdır
        y = start_y
        for line in wrapped_text.split("\n"):
            width, height = draw.textsize(line, font=font)
            draw.text((start_x, y), line, font=font, fill="black")
            y += height

        return y
    
    def draw_receiver_address(self, image, text, font, max_width, start_x, start_y):
        """Draw the receiver address on the envelope. Return the y-coordinate after the address."""
        draw = ImageDraw.Draw(image)
        wrapped_text = textwrap.fill(text, width=75)

        # Birden fazla satır varsa en üstten başla, aksi halde parametre olarak verilen start_y'den başla
        if "\n" in wrapped_text:
            start_y = start_y - 25  # En üstten başla
        else:
            start_y = start_y  # Parametre olarak verilen start_y'den başla

        # Metni yazdır
        y = start_y
        for line in wrapped_text.split("\n"):
            width, height = draw.textsize(line, font=font)
            # Yazının genişliği, maksimum genişlikten büyükse bir sonraki satıra geç
            if width > max_width:
                y += height
                start_y -= height  # Yeni başlangıç y koordinatını ayarla
                draw.text((start_x, start_y), line, font=font, fill="black")
            else:
                draw.text((start_x, y), line, font=font, fill="black")
            y += height

        return start_y
    
    def main(self):
        """Main function that creates an envelope."""
        print("Mektup Evi - Mektup Zarfı Oluşturucu")

        # Get the sender information
        self.sender_name = input("Gönderenin Adı ve Soyadı: ")
        self.sender_address = input("Gönderenin Adresi: ")
        self.sender_dist_city = input("Gönderenin İlçe ve Şehri: ").upper()

        # Get the receiver information
        self.receiver_name = input("\nAlıcının Adı ve Soyadı: ")
        self.relative_name = input("Alıcının Baba Adı (Bilinmiyorsa Boş Bırakılabilir): ")
        self.dorm_num = input("Alıcının Koğuş Numarası (Bilinmiyorsa Boş Bırakılabilir): ")

        while True:
            self.jail_city = input("Hapishanenin Şehri: ")

            if self.jail_city == "":
                print("Hapishane şehri boş bırakılamaz. Lütfen tekrar deneyiniz.")
                continue

            try:
                response = requests.get(f"{userInfo.api_link}/{self.jail_city}")
                response.raise_for_status()
                jail_datas = response.json()
            except requests.exceptions.RequestException as e:
                print("Hapishane bilgisi alınırken bir hata oluştu. Lütfen tekrar deneyiniz.")
                continue

            if 'error' in jail_datas:
                print("Hapishane bulunamadı. Lütfen tekrar deneyiniz.")
                continue
            elif len(jail_datas) == 0:
                print("Hapishane bulunamadı. Lütfen tekrar deneyiniz.")
                continue
            else:
                break

        # Print each jail data with a number prefix
        for index, jail_data in enumerate(jail_datas, start=1):
            print(f"{index}) {jail_data['name']}")

        # Let the user choose an option
        selection = input("Lütfen Bir Hapishane Seçin (1, 2, 3, ...): ")
        
        # Ask the user if they want to add the date
        self.is_date = input("Tarih eklemek ister misiniz? (E/H): ").lower()
        
        if self.is_date == "e":
            self.is_date = True
        else: 
            self.is_date = False

        # Validate the selection
        while True:
            if selection.isdigit() and 1 <= int(selection) <= len(jail_datas):
                selected_jail = jail_datas[int(selection) - 1]
                print("Seçilen Hapishane:", selected_jail['name'])
                self.jail_name = selected_jail['name']
                self.receiver_address = selected_jail['adres']
                break
            else:
                print("Geçersiz Seçim.")
        
        self.create_envelope()


if __name__ == "__main__":
    create_envelope = CreateEnvelope()
    create_envelope.main()
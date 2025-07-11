import os, sys, tkinter, asyncio, random, logging, threading
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QMovie, QKeyEvent
from PySide6 import QtCore
from dotenv import load_dotenv
from PySide6 import QtAsyncio
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s")

# Fetch screen resolution

scr = tkinter.Tk()
width = scr.winfo_screenwidth()
height = scr.winfo_screenheight()

# Fetch filepaths

load_dotenv()
BLINK_R, BLINK_L = os.getenv("BLINK_R"), os.getenv("BLINK_L")
RUN_R, RUN_L = os.getenv("RUN_R"), os.getenv("RUN_L")
WAG_R, WAG_L = os.getenv("WAG_R"), os.getenv("WAG_L")
TALK_R, TALK_L = os.getenv("TALK_R"), os.getenv("TALK_L")
API_KEY = os.getenv("API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") 


# Define classes for GUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.setWindowTitle('SIR ALARIC THE NOBLE')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(width * 0.7, height * 0.85, 200, 200)
        self.setFixedSize(200, 200)
        self.set_sprite(BLINK_R)

        self.user_input = ''

        self.terminal = QLineEdit()
        self.terminal.setWindowTitle('Enter your prompt')
        self.terminal.setFixedSize(500, 50)
        self.terminal.show()
        self.terminal.returnPressed.connect(self.rec_message)

    def set_sprite(self, sprite):
        self.label = QLabel()
        self.movie = QMovie(sprite)
        self.label.setFixedSize(200, 200)
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()
        self.setCentralWidget(self.label)

    def send_message(self, message):
        client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
        elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"),)
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": '''You are a desktop assistant in the form of a dog.
                    Your name is Sir Alaric and you speak old timey english, interspersed with random woofs.
                   '''},  
        {"role": "user", "content": message}],
        stream=False
        )

        audio = elevenlabs.text_to_speech.convert(
        text=response.choices[0].message.content,
        voice_id="fATgBRI8wg5KkDFg8vBd",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        )

        print(response.choices[0].message.content)
        play(audio)


    def rec_message(self):
        self.user_input = str(self.terminal.text())
        self.terminal.clear()
        ch_thread = threading.Thread(target=self.send_message, args=(self.user_input,))
        ch_thread.start()
        logging.info(f"Sending prompt '{self.user_input}'...")

    def switch_sprite(self, sprite):
        self.movie.stop()
        self.label.clear()
        self.set_sprite(sprite)
        logging.info("Changing animation...")

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            logging.info("Closing the program...")
            sys.exit()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == QtCore.Qt.Key_Tab:
            if self.terminal.isVisible():
                self.terminal.hide()
                logging.info("Hiding terminal...")
            else:
                self.terminal.show()
                logging.info("Showing terminal...")

    async def running(self):
        roll = random.randrange(0, 2)
        time_roll = random.randrange(1, 5)
        if roll == 0:
            self.switch_sprite(RUN_L)
            for i in range(0, time_roll):
                new_pos = self.x() - 20
                self.move(new_pos, self.y())
                await asyncio.sleep(0.5)
            self.switch_sprite(BLINK_L)
        else:
            self.switch_sprite(RUN_R)
            for i in range(0, time_roll):
                new_pos = self.x() + 20
                self.move(new_pos, self.y())
                await asyncio.sleep(0.5)
            self.switch_sprite(BLINK_R)
        logging.info("Running animation initiated...")

    async def animation_loop(self):
        logging.info("Animation loop started...")
        while True:
            cur_action = random.randrange(0, 100)

            if cur_action < 10:
                await self.running()
            elif cur_action < 30 and cur_action > 11:
                self.switch_sprite(BLINK_L)
            elif cur_action < 50 and cur_action > 31:
                self.switch_sprite(BLINK_R)
            elif cur_action < 70 and cur_action > 51:
                self.switch_sprite(WAG_L)
            elif cur_action < 90 and cur_action > 71:
                self.switch_sprite(WAG_R)
            else:
                await asyncio.sleep(5)

            logging.info("Sleeping animation loop...")    
            await asyncio.sleep(random.randrange(3, 5))

    
app = QApplication(sys.argv)
main = MainWindow()
main.show()
QtAsyncio.run(main.animation_loop())
QtAsyncio.run()
from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import asyncio
from g4f.client import AsyncClient


async def main(input_text):
    client = AsyncClient()

    response = await client.images.generate(
        prompt=f"{input_text}",
        model="flux",
        response_format="url"
    )

    image_url = response.data[0].url
    return image_url


def open_new_window(event=None):
    input_text = entry.get()
    entry.delete(0, END)
    url_tag = asyncio.run(main(input_text))
    if url_tag:
        create_new_window(url_tag, input_text)


def create_new_window(url_tag, input_text):
    img = load_image(url_tag)
    if img:
        new_window = Toplevel()
        new_window.title(f'Сгенерированная картинка: {input_text}')
        new_window.geometry('600x480')
        label = Label(new_window, image=img)
        label.pack()
        label.image = img


def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img.thumbnail((600, 480), Image.Resampling.LANCZOS)  # подгонка изображения под нужный нам размер
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f'Произошла ошибка {e}')
        return None


window = Tk()
window.title('Генерация картинок')
window.geometry('400x160')

label = Label(window, text='Какую картинку нужно сгенерировать?')
label.pack(pady=5)

entry = Entry(window)
entry.pack(pady=5)
entry.bind('<Return>', open_new_window)

button = Button(window, text='Отправить', command=open_new_window)
button.pack(pady=5)

window.mainloop()

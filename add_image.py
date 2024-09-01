import fitz

from parameters import tooth_data, image_data


def image_to_pdf(image,tooth, page):
    barcode_file = f"templates/images/icons/{image}_{tooth_data[tooth]['type']}.png"

    # Задаем параметры ширины и высоты изображения
    image_width = image_data[image]["width"]  # ширина изображения
    image_height = image_data[image]["height"]  # высота изображения

    # Координаты верхнего левого угла изображения (например, 0, 0)
    x0 = tooth_data[tooth]["x"] + image_data[image]["delta"]
    y0 = image_data[image]["y"]

    # Рассчитываем прямоугольник изображения
    image_rectangle = fitz.Rect(x0, y0, x0 + image_width, y0 + image_height)

    # Добавляем изображение с изменением пропорций
    page.insert_image(image_rectangle, filename=barcode_file, keep_proportion=False)

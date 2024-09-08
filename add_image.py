import fitz

from parameters import tooth_data, image_data


def image_to_pdf(image,tooth, page):
    tooth_type = tooth_data[tooth]["type"]
    barcode_file = f"templates/images/icons/{image}_{tooth_type}_{tooth_data[tooth]['name']}.png"

    # Задаем параметры ширины и высоты изображения
    image_width = image_data[image][tooth_type]["width"]  # ширина изображения
    image_height = image_data[image][tooth_type]["height"]  # высота изображения

    # Координаты верхнего левого угла изображения (например, 0, 0)
    x0 = tooth_data[tooth]["x"] + image_data[image][tooth_type]["delta"]
    y0 = image_data[image][tooth_type]["y"]

    # Рассчитываем прямоугольник изображения
    image_rectangle = fitz.Rect(x0, y0, x0 + image_width, y0 + image_height)

    try:
        # Добавляем изображение с изменением пропорций
       page.insert_image(image_rectangle, filename=barcode_file, keep_proportion=False)
    except:
        pass

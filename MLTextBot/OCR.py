import easyocr


async def OCR(file_path):
    reader = easyocr.Reader(["ru", "en"])
    result = reader.readtext(file_path, detail=0, paragraph=True)

    result_text = ""
    for line in result:
        result_text += f"{line}\n"

    return result_text


def main():
    file_path = input("Enter a file path: ")
    print(text_recognition(file_path=file_path))


if __name__ == "__main__":
    main()

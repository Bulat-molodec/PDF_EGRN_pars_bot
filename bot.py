import os
import csv
from io import BytesIO, TextIOWrapper
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tabula

TOKEN = ''


def flatten_list(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def process_pdf(pdf_file_path):
    pdf_tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, lattice=True)

    data_to_write = []
    extracted_labels = set()

    for table in pdf_tables:
        unite = table.values.tolist()
        flattened_list = flatten_list(unite)

        for index, sours in enumerate(flattened_list):
            if isinstance(sours, str) and 'Дата и номер' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Кадастровый номер' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Местоположение' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Номер, тип этажа, на котором расположено' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Площадь' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Назначение' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Количество этажей' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Год ввода в эксплуатацию' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Кадастровая стоимость' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Правообладатель' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Ограничение прав и обременение объектов недвижимости' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Категория земель' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Виды разрешенного использования' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Основная характеристика' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Наименование' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Наименование' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Номер, тип этажа, на котором расположено помещение' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Правообладатель (правообладатели)' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)
            elif isinstance(sours, str) and 'Наименование' in sours:
                total = f'{flattened_list[index + 1]}'
                if total not in extracted_labels:
                    data_to_write.append([total])
                    extracted_labels.add(total)

    return data_to_write


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я первая версия PDF_EGRN_pars_бота, по-этому я могу ошибаться. Лучше переправерь мой резульат. В будущем, при возникновении ошибок и пожелания пользователей я исправлюсь. Сейчас можешь отсылать мне ЕГРН файл в формате PDF, я предоставлю тебе всю необходимую информацию в CSV файле.")


def handle_pdf(update, context):
    file = update.message.document
    if file.mime_type == 'application/pdf':

        file_path = f"downloads/{file.file_name}"
        file.get_file().download(file_path)
        csv_data = process_pdf(file_path)
        csv_buffer = BytesIO()
        text_io_wrapper = TextIOWrapper(csv_buffer, encoding='cp1251', write_through=True)
        writer = csv.writer(text_io_wrapper, dialect='excel')

        for row in csv_data:
            writer.writerow(row)

        csv_buffer.seek(0)
        context.bot.send_document(chat_id=update.effective_chat.id, document=csv_buffer, filename="result.csv")
        os.remove(file_path)


def handle_non_pdf(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, отправьте файл PDF. Я обрабатываю только его.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), handle_pdf))

    dp.add_handler(MessageHandler(~Filters.document.mime_type("application/pdf"), handle_non_pdf))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

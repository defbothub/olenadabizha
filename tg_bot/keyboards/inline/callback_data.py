from aiogram.utils.callback_data import CallbackData

temp_callback = CallbackData("temp", "title", "name")
calendar_callback = CallbackData("date", "title", "arg1", "arg2", "arg3", "arg4")
time_callback = CallbackData("time", "title", "hour", "minute")
contact_callback = CallbackData("contact", "title", "name", "number")
question_callback = CallbackData("question", "title", "category", "subcategory")

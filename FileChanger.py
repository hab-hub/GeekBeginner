import tkinter as tk
from tkinter import filedialog
from PIL import Image
import moviepy.editor as mp
import pydub
import filetype

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("すべてのファイル", "*.*")])
    if file_path:
        file_path_label.config(text=file_path)

        # ファイルタイプをチェック
        kind = filetype.guess(file_path)
        if kind is None:
            # 不明なファイルタイプ
            extension_menu["menu"].delete(0, "end")
            target_extension_var.set("")
            convert_button.config(state="disabled")
        else:
            # ファイルタイプに基づいて利用可能な変換オプションを更新
            file_type = kind.mime.split("/")[0]
            if file_type in ["image", "video", "audio"]:
                extension_menu["menu"].delete(0, "end")
                if file_type == "image":
                    extensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]
                elif file_type == "video":
                    extensions = ["mp4", "avi", "mkv", "mov"]
                elif file_type == "audio":
                    extensions = ["mp3", "wav", "ogg", "flac"]
                else:
                    extensions = []
                
                for extension in extensions:
                    extension_menu["menu"].add_command(label=extension, command=lambda value=extension: target_extension_var.set(value))
                convert_button.config(state="normal")
            else:
                # 不明なファイルタイプ
                extension_menu["menu"].delete(0, "end")
                target_extension_var.set("")
                convert_button.config(state="disabled")

def clear_file_selection():
    global file_path
    file_path = ""
    file_path_label.config(text="")
    extension_menu["menu"].delete(0, "end")
    target_extension_var.set("")
    convert_button.config(state="disabled")
    result_label.config(text="")

def convert_file_extension():
    global file_path

    # 目標の拡張子を取得
    target_extension = target_extension_var.get()

    if file_path:
        # 保存先のフォルダを選択
        save_directory = save_directory_var.get()

        if save_directory:
            try:
                # ファイルタイプをチェック
                kind = filetype.guess(file_path)
                if kind is None:
                    result_label.config(text="ファイルの種類が不明です。")
                    return

                # 新しいファイル名を生成
                file_name = file_path.rsplit('/', 1)[-1]
                new_file_name = file_name.rsplit('.', 1)[0] + '.' + target_extension

                # 保存先のパスを生成
                new_file_path = save_directory + '/' + new_file_name

                # ファイルタイプに基づいて変換を実行
                file_type = kind.mime.split("/")[0]
                if file_type == "image":
                    image = Image.open(file_path)
                    image.save(new_file_path)
                elif file_type == "video":
                    video = mp.VideoFileClip(file_path)
                    video.write_videofile(new_file_path, codec='libx264')
                elif file_type == "audio":
                    audio = pydub.AudioSegment.from_file(file_path)
                    audio.export(new_file_path, format=target_extension)

                # 完了メッセージを表示
                result_label.config(text=f"変換完了：{new_file_path}")
            except Exception as e:
                result_label.config(text="変換エラー")
        else:
            result_label.config(text="保存先を指定してください。")
    else:
        result_label.config(text="ファイルが選択されていません。")

# GUIウィンドウの作成
window = tk.Tk()
window.title("FileChanger")
window.geometry("500x300")

# ファイル選択フレームを作成
file_frame = tk.Frame(window)
file_frame.pack(pady=20)

# ファイル選択ボタンとクリアボタンを配置
select_button = tk.Button(file_frame, text="ファイルを選択", command=open_file_dialog)
select_button.pack(side="left", padx=10)

clear_button = tk.Button(file_frame, text="ファイルをクリア", command=clear_file_selection)
clear_button.pack(side="left", padx=10)

# ファイルパス表示フレームを作成
file_path_frame = tk.Frame(window)
file_path_frame.pack(pady=10)

# ファイルパスを表示するラベルを作成
file_path_label = tk.Label(file_path_frame, text="")
file_path_label.pack()

# 拡張子の指定フレームを作成
extension_frame = tk.Frame(window)
extension_frame.pack(pady=10)

extension_label = tk.Label(extension_frame, text="変換する拡張子：")
extension_label.pack(side="left")

target_extension_var = tk.StringVar()
target_extension_var.set("---")

extension_menu = tk.OptionMenu(extension_frame, target_extension_var, "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico")
extension_menu.pack(side="left", padx=10)

# 保存先の指定フレームを作成
save_frame = tk.Frame(window)
save_frame.pack(pady=10)

save_label = tk.Label(save_frame, text="保存先：")
save_label.pack(side="left")

save_directory_var = tk.StringVar()
save_directory_entry = tk.Entry(save_frame, textvariable=save_directory_var, width=30)
save_directory_entry.pack(side="left", padx=10)

def select_save_directory():
    save_directory = filedialog.askdirectory()
    save_directory_var.set(save_directory)

save_button = tk.Button(save_frame, text="参照", command=select_save_directory)
save_button.pack(side="left")

# 変換開始ボタンを配置
convert_button = tk.Button(window, text="変換開始", command=convert_file_extension)
convert_button.pack(pady=10)

# 変換結果表示用のラベルを配置
result_label = tk.Label(window, text="")
result_label.pack(pady=5)  # 変換結果表示用のラベルをボタンの下に配置

# GUIイベントループの開始
window.mainloop()
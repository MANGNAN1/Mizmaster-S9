import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import pandas as pd
import os

# CSV 파일 읽기 (파일 경로에 주의하세요)
csv_file = "henchies.csv"

# 파일이 존재하는지 먼저 확인합니다
if not os.path.isfile(csv_file):
    messagebox.showerror("파일 오류", f"{csv_file} 파일을 찾을 수 없습니다.")
    exit()

# 다양한 인코딩으로 시도
try:
    henches_df = pd.read_csv(csv_file, encoding='utf-8')  # 기본 'utf-8'로 시도
except UnicodeDecodeError:
    try:
        henches_df = pd.read_csv(csv_file, encoding='euc-kr')  # 'euc-kr'로 시도
    except Exception as e:
        messagebox.showerror("파일 오류", f"{csv_file} 파일을 읽을 수 없습니다. 오류: {e}")
        exit()

class HenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("헨치 도감")
        self.root.geometry("470x600")

        self.create_widgets()

    def create_widgets(self):
        # 헨치 이름 입력 및 검색 버튼
        ttk.Label(self.root, text="헨치 이름을 입력하세요:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.hench_name_var = tk.StringVar()
        self.hench_entry = ttk.Entry(self.root, textvariable=self.hench_name_var)
        self.hench_entry.grid(row=0, column=1, padx=10, pady=10)
        self.hench_entry.bind("<Return>", self.search_hench)

        ttk.Button(self.root, text="검색", command=self.search_hench).grid(row=0, column=2, padx=10, pady=10)

        # 헨치 정보 표시
        self.info_frame = ttk.LabelFrame(self.root, text="헨치 정보")
        self.info_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.info_labels = {
            "이름": ttk.Label(self.info_frame, text="이름:"),
            "서식지": ttk.Label(self.info_frame, text="서식지:"),
            "선공 여부": ttk.Label(self.info_frame, text="선공 여부:"),
            "득 여부": ttk.Label(self.info_frame, text="득 여부:"),
            "레벨": ttk.Label(self.info_frame, text="레벨:"),
            "공격 타입": ttk.Label(self.info_frame, text="공격 타입:"),
            "속성": ttk.Label(self.info_frame, text="속성:")
        }

        for i, (key, label) in enumerate(self.info_labels.items()):
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            setattr(self, f"hench_{key}", ttk.Label(self.info_frame, text=""))
            getattr(self, f"hench_{key}").grid(row=i, column=1, sticky="w", padx=10, pady=5)

        self.hench_image_label = ttk.Label(self.info_frame)
        self.hench_image_label.grid(row=0, column=2, rowspan=7, padx=10, pady=10)

        # 조합식 정보
        self.combo_frame = ttk.LabelFrame(self.root, text="조합식")
        self.combo_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.combo_frame, text="메인:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(self.combo_frame, text="서브:").grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.main_combo_labels = []
        self.sub_combo_labels = []

    def search_hench(self, event=None):
        hench_name = self.hench_name_var.get().strip().lower()  # 검색어를 소문자로 변환

        # 한국명 또는 호주명으로 검색 (소문자로 비교)
        hench = henches_df[(henches_df['이름'].str.strip().str.lower() == hench_name) | 
                           (henches_df['호주명'].str.strip().str.lower() == hench_name)]

        if not hench.empty:
            hench = hench.iloc[0]
            self.update_info(hench)
        else:
            messagebox.showinfo("헨치 도감", "헨치를 찾을 수 없습니다.")

    def update_info(self, hench):
        for key in self.info_labels.keys():
            label = getattr(self, f"hench_{key}")
            if key == "이름":
                label.config(text=f"{hench['이름']} / {hench['호주명']}")
            else:
                label.config(text=hench[key])

        img_path = os.path.join("헨치사진", hench["이미지"])
        img = Image.open(img_path)

        # GIF 이미지의 첫 번째 프레임을 사용
        if img_path.lower().endswith(".gif"):
            img = next(ImageSequence.Iterator(img))

        img = img.resize((150, 150), Image.LANCZOS)
        self.hench_img = ImageTk.PhotoImage(img)
        self.hench_image_label.config(image=self.hench_img)

        # 기존 조합식 레이블 제거
        for label in self.main_combo_labels + self.sub_combo_labels:
            label.destroy()

        # 새로운 조합식 레이블 생성
        self.main_combo_labels = []
        self.sub_combo_labels = []

        combo_mains = hench["조합식 메인"].split(';')
        combo_subs = hench["조합식 서브"].split(';')

        for i, (main, sub) in enumerate(zip(combo_mains, combo_subs)):
            main_label = ttk.Label(self.combo_frame, text=main)
            main_label.grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            self.main_combo_labels.append(main_label)

            sub_label = ttk.Label(self.combo_frame, text=sub)
            sub_label.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            self.sub_combo_labels.append(sub_label)

if __name__ == "__main__":
    root = tk.Tk()
    app = HenchApp(root)
    root.mainloop()

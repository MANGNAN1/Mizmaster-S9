import openpyxl
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import pandas as pd
import os
import re
import sys

def resource_path(relative_path):
    """ 리소스의 절대 경로를 반환합니다. 개발 환경과 PyInstaller 빌드 환경을 모두 지원합니다. """
    try:
        # PyInstaller는 임시 폴더를 만들고 _MEIPASS에 경로를 저장합니다
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 엑셀 파일 읽기 (파일 경로에 주의하세요)
excel_file = resource_path("henchies.xlsx")

# 파일이 존재하는지 먼저 확인합니다
if not os.path.isfile(excel_file):
    messagebox.showerror("파일 오류", f"{excel_file} 파일을 찾을 수 없습니다.")
    exit()

# 다양한 인코딩으로 시도할 필요 없음
try:
    henches_df = pd.read_excel(excel_file)
except Exception as e:
    messagebox.showerror("파일 오류", f"{excel_file} 파일을 읽을 수 없습니다. 오류: {e}")
    exit()

# 이름과 호주명을 소문자로 정규화하여 컬럼 추가
henches_df['정규화된_이름'] = henches_df['이름'].str.replace(r'[\W\d]', '', regex=True).str.strip().str.lower()
henches_df['정규화된_호주명'] = henches_df['호주명'].str.replace(r'[\W\d]', '', regex=True).str.strip().str.lower()

class HenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("헨치 도감")
        self.root.geometry("620x900")
        
        # 현대적인 테마 적용
        style = ttk.Style()
        style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic'
        
        self.create_widgets()

    def create_widgets(self):
        # 메인 프레임 생성
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 헨치 이름 입력 및 검색 버튼
        ttk.Label(main_frame, text="헨치 이름을 입력하세요:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.hench_name_var = tk.StringVar()
        self.hench_entry = ttk.Entry(main_frame, textvariable=self.hench_name_var, font=("Helvetica", 12), width=30)
        self.hench_entry.grid(row=0, column=1, padx=10, pady=10)
        self.hench_entry.bind("<Return>", self.search_hench)

        ttk.Button(main_frame, text="검색", command=self.search_hench, width=10).grid(row=0, column=2, padx=10, pady=10)

        # 헨치 정보 표시
        self.info_frame = ttk.LabelFrame(main_frame, text="헨치 정보", padding="10 10 10 10")
        self.info_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.info_labels = {
            "이름": ttk.Label(self.info_frame, text="이름:", font=("Helvetica", 10)),
            "서식지": ttk.Label(self.info_frame, text="서식지:", font=("Helvetica", 10)),
            "선공 여부": ttk.Label(self.info_frame, text="선공 여부:", font=("Helvetica", 10)),
            "득 여부": ttk.Label(self.info_frame, text="득 여부:", font=("Helvetica", 10)),
            "레벨": ttk.Label(self.info_frame, text="레벨:", font=("Helvetica", 10)),
            "공격 타입": ttk.Label(self.info_frame, text="공격 타입:", font=("Helvetica", 10)),
            "속성": ttk.Label(self.info_frame, text="속성:", font=("Helvetica", 10)),
            "시세": ttk.Label(self.info_frame, text="시세:", font=("Helvetica", 10))
        }

        for i, (key, label) in enumerate(self.info_labels.items()):
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            setattr(self, f"hench_{key}", ttk.Label(self.info_frame, text="", font=("Helvetica", 10)))
            getattr(self, f"hench_{key}").grid(row=i, column=1, sticky="w", padx=10, pady=5)

        self.hench_image_label = ttk.Label(self.info_frame)
        self.hench_image_label.grid(row=0, column=2, rowspan=9, padx=10, pady=10)

        # 조합식 정보
        self.combo_frame = ttk.LabelFrame(main_frame, text="조합식", padding="10 10 10 10")
        self.combo_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.combo_frame, text="메인:", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(self.combo_frame, text="서브:", font=("Helvetica", 10)).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(self.combo_frame, text="상위 헨치:", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=10, pady=5)

        self.main_combo_labels = []
        self.sub_combo_labels = []
        self.upper_combo_labels = []

        # 믹스레벨 계산기 관련 위젯
        self.mix_level_frame = ttk.LabelFrame(main_frame, text="믹스레벨 계산기", padding="10 10 10 10")
        self.mix_level_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.show_mix_calc_button = ttk.Button(main_frame, text="믹스레벨 계산기 보이기", command=self.toggle_mix_calc)
        self.show_mix_calc_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.mix_level_frame.grid_remove()  # 초기에 숨겨진 상태로 설정

        # 메인코어 및 서브코어 레벨 입력 필드
        ttk.Label(self.mix_level_frame, text="메인코어 현재 레벨:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(self.mix_level_frame, text="메인코어 맥스 레벨:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(self.mix_level_frame, text="서브코어 현재 레벨:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(self.mix_level_frame, text="서브코어 맥스 레벨:").grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.main_current_level_var = tk.IntVar()
        self.main_max_level_var = tk.IntVar()
        self.sub_current_level_var = tk.IntVar()
        self.sub_max_level_var = tk.IntVar()

        ttk.Entry(self.mix_level_frame, textvariable=self.main_current_level_var, width=10).grid(row=0, column=1, padx=10, pady=5)
        ttk.Entry(self.mix_level_frame, textvariable=self.main_max_level_var, width=10).grid(row=1, column=1, padx=10, pady=5)
        ttk.Entry(self.mix_level_frame, textvariable=self.sub_current_level_var, width=10).grid(row=2, column=1, padx=10, pady=5)
        ttk.Entry(self.mix_level_frame, textvariable=self.sub_max_level_var, width=10).grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self.mix_level_frame, text="계산하기", command=self.calculate_mix_level).grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_mix_calc(self):
        if self.mix_level_frame.winfo_ismapped():
            self.mix_level_frame.grid_remove()
            self.show_mix_calc_button.config(text="믹스레벨 계산기 보이기")
        else:
            self.mix_level_frame.grid()
            self.show_mix_calc_button.config(text="믹스레벨 계산기 숨기기")

    def search_hench(self, event=None):
        hench_name = self.hench_name_var.get().strip().lower()  # 검색어를 소문자로 변환
        cleaned_name = re.sub(r'[\W\d]', '', hench_name)  # 특수 문자와 숫자를 제거
        print(f"Searching for hench: {cleaned_name}")  # 디버그 메시지

        # 한국명 또는 호주명으로 검색 (소문자로 비교)
        hench = henches_df[(henches_df['정규화된_이름'] == cleaned_name) | 
                           (henches_df['정규화된_호주명'] == cleaned_name)]

        print(f"Search result: {hench}")  # 디버그 메시지

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

        img_path = resource_path(os.path.join("헨치사진", hench["이미지"]))
        
        # 사진 파일이 존재하는 경우에만 이미지를 열어서 표시합니다
        if os.path.isfile(img_path):
            img = Image.open(img_path)

            # GIF 이미지의 첫 번째 프레임을 사용
            if img_path.lower().endswith(".gif"):
                img = next(ImageSequence.Iterator(img))

            img = img.resize((150, 150), Image.LANCZOS)
            self.hench_img = ImageTk.PhotoImage(img)
            self.hench_image_label.config(image=self.hench_img)
        else:
            self.hench_image_label.config(image=None)  # 사진이 없을 경우 이미지를 지웁니다

        # 기존 조합식 레이블 제거
        for label in self.main_combo_labels + self.sub_combo_labels + self.upper_combo_labels:
            label.destroy()

        # 새로운 조합식 레이블 생성
        self.main_combo_labels = []
        self.sub_combo_labels = []
        self.upper_combo_labels = []

        combo_mains = str(hench["조합식 메인"]).split(';')
        combo_subs = str(hench["조합식 서브"]).split(';')
        upper_hench = str(hench["상위 헨치"]).split(';')

        max_len = max(len(combo_mains), len(combo_subs), len(upper_hench))

        for i in range(max_len):
            main = combo_mains[i] if i < len(combo_mains) else ""
            sub = combo_subs[i] if i < len(combo_subs) else ""
            upper = upper_hench[i] if i < len(upper_hench) else ""

            main_label = ttk.Button(self.combo_frame, text=main, command=lambda m=main: self.search_hench_name(m))
            main_label.grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            self.main_combo_labels.append(main_label)

            sub_label = ttk.Button(self.combo_frame, text=sub, command=lambda s=sub: self.search_hench_name(s))
            sub_label.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            self.sub_combo_labels.append(sub_label)

            upper_label = ttk.Button(self.combo_frame, text=upper, command=lambda u=upper: self.search_hench_name(u, clean=False))
            upper_label.grid(row=i+1, column=2, sticky="w", padx=10, pady=5)
            self.upper_combo_labels.append(upper_label)

    def search_hench_name(self, hench_name, clean=True):
        # clean이 True이면 특수 문자와 공백, 숫자를 제거하여 검색어로 사용
        if clean:
            cleaned_name = re.sub(r'[\W\d]', '', hench_name).strip().lower()
        else:
            cleaned_name = hench_name.strip().lower()

        # 예외적으로 "1호", "2호", "3호"를 포함한 경우 그대로 사용
        if any(tag in hench_name for tag in ["1호", "2호", "3호"]):
            cleaned_name = hench_name.strip().lower()

        self.hench_name_var.set(cleaned_name)
        self.search_hench()

    def calculate_mix_level(self):
        a = self.main_current_level_var.get()
        b = self.sub_current_level_var.get()
        c = self.main_max_level_var.get()
        d = self.sub_max_level_var.get()

        mix_level = ((a + b) / 2) + ((((100 * a) / c) + ((100 * b) / d)) * 0.05)

        messagebox.showinfo("믹스레벨 계산 결과", f"믹스레벨: {mix_level:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HenchApp(root)
    root.mainloop()

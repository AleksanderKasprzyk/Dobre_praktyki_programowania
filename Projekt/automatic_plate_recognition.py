# AUTOMATIC PLATE RECOGNITION
# ------------------------------------------------------------
# This single file contains:
# - Dataset preparation from CVAT XML to YOLO format
# - YOLO training
# - Plate detection + OCR (EasyOCR)
# - Optional API (FastAPI)
# - Final evaluation (accuracy / IoU / time / grade)
# ------------------------------------------------------------
# Usage:
#   1) Prepare dataset:   py automatic_plate_recognition.py prepare
#   2) Train YOLO:        py automatic_plate_recognition.py train
#   3) Evaluate project:  py automatic_plate_recognition.py eval
#   4) Run API:           py automatic_plate_recognition.py api
#   5) Kolejka:           py -c "from automatic_plate_recognition import consumer_worker; consumer_worker()"
#      Pojedyńczo ------> py -c "from automatic_plate_recognition import producer_add_image; producer_add_image(r'C:\Users\Olek\PycharmProjects\Projekt\dataset\images\1.jpg')"
#      Automatycznie ---> py -c "from automatic_plate_recognition import auto_queue_folder; auto_queue_folder(r'C:\Users\Olek\PycharmProjects\Projekt\dataset\images')"
# ------------------------------------------------------------
# Wywołanie wyniku z pliku queue.sqlite3
"""
py -c "
import sqlite3
c = sqlite3.connect('queue.sqlite3')
for r in c.execute('SELECT id, image_path, status, plate FROM tasks'):
    print(r)
c.close()"
"""
# ------------------------------------------------------------

import os, shutil, random, time, re, uuid, sys, xml.etree.ElementTree as ET
import cv2, torch, easyocr
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File
import uvicorn
import sqlite3

# ---------------- CONFIG ----------------
# Paths to important project resources
DATASET_XML = "dataset/annotations.xml"
IMAGES_DIR  = "dataset/images"
YOLO_DIR    = "dataset_yolo"
MODEL_PATH  = "best.pt"
UPLOAD_DIR  = "uploads"

# ---------------- UTIL ----------------
# Cleans OCR output (only A-Z and 0-9, uppercase)
"""Zamienia wszystko na wielkie litery
re.sub(r'[^A-Z0-9]', '', ...)
[^A-Z0-9] = wszystko co NIE jest literą A–Z lub cyfrą 0–9
'' = usuń"""
def normalize(t):
    return re.sub(r'[^A-Z0-9]', '', t.upper())

# ---------------- DATASET PREP ----------------
# Converts bounding box from CVAT format to YOLO format
# Prepares dataset for YOLO training
def convert_box(size, box):
    dw, dh = 1./size[0], 1./size[1]
    x=(box[0]+box[2])/2; y=(box[1]+box[3])/2; w=box[2]-box[0]; h=box[3]-box[1]
    return (x*dw, y*dh, w*dw, h*dh)


def prepare():
    tree=ET.parse(DATASET_XML); root=tree.getroot(); imgs=root.findall('image')
    random.shuffle(imgs); s=int(len(imgs)*0.7)
    sets={'train':imgs[:s],'val':imgs[s:]}
    if os.path.exists(YOLO_DIR): shutil.rmtree(YOLO_DIR)
    for k in sets:
        os.makedirs(f"{YOLO_DIR}/{k}/images",exist_ok=True)
        os.makedirs(f"{YOLO_DIR}/{k}/labels",exist_ok=True)
    for k,nodes in sets.items():
        for im in nodes:
            name=im.get('name'); w=int(im.get('width')); h=int(im.get('height'))
            shutil.copy(os.path.join(IMAGES_DIR,name), f"{YOLO_DIR}/{k}/images/{name}")
            with open(f"{YOLO_DIR}/{k}/labels/{os.path.splitext(name)[0]}.txt","w") as f:
                for b in im.findall('box'):
                    if b.get('label')=='plate':
                        bb=[float(b.get(x)) for x in ['xtl','ytl','xbr','ybr']]
                        y=convert_box((w,h),bb)
                        f.write(f"0 {y[0]} {y[1]} {y[2]} {y[3]}\n")
    with open('data.yaml','w') as f:
        f.write(f"path: {os.path.abspath(YOLO_DIR)}\ntrain: train/images\nval: val/images\nnames:\n  0: license_plate\n")
    print("Dataset prepared")

# ---------------- TRAIN ----------------
# Trains YOLOv8 detector
def train():
    m=YOLO('yolov8n.pt')
    m.train(data='data.yaml',epochs=40,imgsz=640,device=0 if torch.cuda.is_available() else 'cpu',batch=16,name='yolo_plate_detector')

# ---------------- OCR ----------------
"""
OCR (Optical Character Recognition)
= optyczne rozpoznawanie znaków

Zadanie OCR w tym projekcie:
- wykrycie tablicy rejestracyjnej (YOLO)
- wycięcie fragmentu obrazu z tablicą
- rozpoznanie znaków (EasyOCR)
- wybór najlepszego wyniku tekstowego
"""

class PlateRecognizer:
    def __init__(self):
        # Model YOLO – wykrywanie tablic rejestracyjnych
        self.det = YOLO(MODEL_PATH)

        # EasyOCR – rozpoznawanie liter i cyfr
        self.reader = easyocr.Reader(['pl', 'en'], gpu=torch.cuda.is_available())

    def fix_common_errors(self, text: str) -> str:
        """
        Poprawia najczęstsze błędy OCR
        (np. 0->O, 5->S, 1->I)
        """
        replace_map = {'0': 'O', '1': 'I', '2': 'Z', '5': 'S', '8': 'B'}
        chars = list(text)

        # pierwsze 2 znaki to litery (kod województwa)
        for i in range(min(2, len(chars))):
            if chars[i] in replace_map:
                chars[i] = replace_map[chars[i]]

        return "".join(chars)

    def analyze(self, path: str) -> dict:
        """
        Analiza jednego obrazu:
        - detekcja tablicy
        - OCR
        - wybór najlepszego odczytu
        """
        img = cv2.imread(path)
        if img is None:
            return {"plate": "", "found": False}

        # --- YOLO: wykrycie tablicy ---
        result = self.det(img, conf=0.1, verbose=False)[0]

        # brak wykrytej tablicy
        if not result.boxes:
            return {"plate": "", "found": False}

        # bierzemy najbardziej pewną ramkę
        x1, y1, x2, y2 = map(int, result.boxes[0].xyxy[0])

        # wycinamy obszar tablicy
        crop = img[y1:y2, x1:x2]

        # --- przygotowanie obrazu pod OCR ---
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        best_text = ""
        best_conf = 0.0

        # --- OCR: rozpoznawanie znaków ---
        for (_, text, conf) in self.reader.readtext(gray, detail=1):
            # odrzucamy bardzo niepewne odczyty
            if conf < 0.1:
                continue
            # czyszczenie tekstu
            text = normalize(text)
            # typowa długość tablicy
            if not (5 <= len(text) <= 8):
                continue
            # poprawki typowych błędów OCR
            fixed = self.fix_common_errors(text)
            # wybór najlepszego wyniku
            if conf > best_conf:
                best_text = fixed
                best_conf = conf
        return {"plate": best_text, "found": bool(best_text), "bbox": [x1, y1, x2, y2]}


# ---------------- EVALUATION ----------------
# Computes Accuracy, IoU and processing time
"""IoU – Intersection over Union
IoU = jak dobrze YOLO trafił w tablicę
Czyli:
„Czy prostokąt wykryty przez YOLO pokrywa się z prawdziwą tablicą z XML?”

Accuracy – dokładność OCR
Accuracy = ile tablic zostało przeczytanych idealnie

XML mówi:
„Na tym zdjęciu jest tablica w tym miejscu i ma numer SK293WV”
Na tej podstawie:

YOLO się uczy
OCR jest sprawdzany
liczona jest Accuracy i IoU"""
def eval_project():
    rec = PlateRecognizer()

    tree = ET.parse(DATASET_XML)
    root = tree.getroot()
    results_file = "ocr_results.txt"

    ok = 0
    total = 0
    ious = []

    start_time = time.time()

    with open(results_file, "w", encoding="utf-8") as f:
        for img_node in root.findall("image")[:100]:
            name = img_node.get("name")

            gt_text = ""
            gt_box = None

            for box in img_node.findall("box"):
                if box.get("label") == "plate":
                    gt_box = [float(box.get("xtl")),
                        float(box.get("ytl")),
                        float(box.get("xbr")),
                        float(box.get("ybr"))]
                    attr = box.find("attribute[@name='plate number']")
                    if attr is not None:
                        gt_text = normalize(attr.text)
                    break

            if not gt_text:
                continue

            total += 1

            result = rec.analyze(os.path.join(IMAGES_DIR, name))
            ocr_text = normalize(result.get("plate", ""))

            # zapis do pliku (bez printów)
            f.write(f"IMG: {name}\n")
            f.write(f"GT:  {gt_text}\n")
            f.write(f"OCR: {ocr_text}")
            f.write("  ✔\n" if ocr_text == gt_text else "  ✘\n")
            f.write("-" * 40 + "\n")

            if ocr_text == gt_text:
                ok += 1

            # IoU (jeśli OCR coś wykrył)
            if result.get("found") and gt_box:
                x1, y1, x2, y2 = result["bbox"]
                gx1, gy1, gx2, gy2 = gt_box

                xa = max(x1, gx1)
                ya = max(y1, gy1)
                xb = min(x2, gx2)
                yb = min(y2, gy2)

                inter = max(0, xb - xa) * max(0, yb - ya)
                area_pred = (x2 - x1) * (y2 - y1)
                area_gt = (gx2 - gx1) * (gy2 - gy1)

                iou = inter / (area_pred + area_gt - inter + 1e-6)
                ious.append(iou)

    end_time = time.time()

    accuracy = (ok / total) * 100 if total > 0 else 0
    mean_iou = sum(ious) / len(ious) if ious else 0
    elapsed = end_time - start_time

    print("\n===== FINAL RESULT =====")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"IoU: {mean_iou:.2f}")
    print(f"Time: {elapsed:.2f}s")
    final_grade = calculate_final_grade(accuracy, elapsed)
    print(f"Final grade: {final_grade}")
    print(f"Saved OCR details to: {results_file}")

# ---------------- Normalizacja czasu, dokładności do oceny końcowej ----------------
def calculate_final_grade(accuracy_percent: float, processing_time_sec: float) -> float:
    # Calculates the final grade based on license plate OCR accuracy and processing time.

    # Minimalne wymagania
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0
    # Normalizacja dokładności: 60% → 0.0, 100% → 1.0
    accuracy_norm = (accuracy_percent - 60) / 40
    # Normalizacja czasu: 60s → 0.0, 10s → 1.0
    time_norm = (60 - processing_time_sec) / 50
    # Wynik ważony
    score = 0.7 * accuracy_norm + 0.3 * time_norm
    grade = 2.0 + 3.0 * score
    # Zaokrąglenie do 0.5
    return round(grade * 2) / 2

# ---------------- API ----------------
# Simple REST API for uploading images
app=FastAPI()
rec=PlateRecognizer()
@app.post('/analyze')
def analyze(file:UploadFile=File(...)):
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    p=os.path.join(UPLOAD_DIR,f"{uuid.uuid4()}_{file.filename}")
    with open(p,'wb') as f: shutil.copyfileobj(file.file,f)
    return rec.analyze(p)

# ================= PRODUCER =================
# PRODUCER = część, która DODAJE zadania do kolejki (bazy danych)
def producer_add_image(image_path: str):

    # Połączenie z bazą SQLite (plik queue.sqlite3)
    conn = sqlite3.connect("queue.sqlite3")
    cur = conn.cursor()

    # Utworzenie tabeli tasks, jeśli jeszcze nie istnieje
    # id          – unikalny identyfikator zadania
    # image_path  – ścieżka do obrazu
    # status      – stan zadania (pending / in_progress / done)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            status TEXT)""")

    # Dodanie nowego zadania do kolejki
    # status = 'pending' oznacza, że zadanie czeka na przetworzenie
    cur.execute("INSERT INTO tasks (image_path, status) VALUES (?, 'pending')",(image_path,))
    # Zatwierdzenie zmian i zamknięcie połączenia z bazą
    conn.commit()
    conn.close()
    # Informacja w konsoli (pomocna przy debugowaniu)
    print(f"[PRODUCER] Dodano zadanie: {image_path}")

# Funkcja automatycznie dodająca WSZYSTKIE obrazy z folderu do kolejki
def auto_queue_folder(folder_path: str):

    # Przejście po wszystkich plikach w folderze
    for name in os.listdir(folder_path):
        # Sprawdzamy, czy plik jest obrazem
        if name.lower().endswith((".jpg", ".png", ".jpeg")):
            full_path = os.path.join(folder_path, name)
            # Każdy obraz trafia do kolejki jako osobne zadanie
            producer_add_image(full_path)

# Funkcja inicjalizująca bazę danych
# Wywoływana przez consumer, żeby mieć pewność,
# że tabela istnieje zanim zacznie ją czytać
def init_queue_db():

    conn = sqlite3.connect("queue.sqlite3")
    cur = conn.cursor()
    # Tworzymy tabelę tylko jeśli jej jeszcze nie ma
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            status TEXT)""")
    conn.commit()
    conn.close()


# ================= CONSUMER =================
# CONSUMER = część, która BIERZE zadania z kolejki i je przetwarza
def consumer_worker():
    # Inicjalizacja modelu OCR (YOLO + EasyOCR)
    rec = PlateRecognizer()
    print("[CONSUMER] Startuję...")
    # Upewniamy się, że tabela tasks istnieje
    init_queue_db()

    # Pętla nieskończona – consumer działa cały czas
    while True:
        conn = sqlite3.connect("queue.sqlite3")
        cur = conn.cursor()
        # Pobranie JEDNEGO najstarszego zadania ze statusem 'pending'
        row = cur.execute("""
            SELECT id, image_path FROM tasks
            WHERE status='pending'
            ORDER BY id
            LIMIT 1""").fetchone()
        # Jeśli nie ma żadnych zadań – czekamy
        if row is None:
            print("[CONSUMER] Brak zadań, czekam 5s...")
            conn.close()
            time.sleep(5)
            continue
        # Rozpakowanie danych zadania
        task_id, image_path = row
        print(f"[CONSUMER] Przetwarzam {image_path}")
        # Oznaczenie zadania jako przetwarzane
        cur.execute("UPDATE tasks SET status='in_progress' WHERE id=?",(task_id,))
        conn.commit()
        conn.close()

        # --- GŁÓWNA LOGIKA ---
        # Wywołanie OCR na obrazie
        result = rec.analyze(image_path)
        # Pobranie rozpoznanego numeru tablicy
        plate = result.get("plate", "")
        # Zapis wyniku OCR do bazy danych
        conn = sqlite3.connect("queue.sqlite3")
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET status='done', plate=? WHERE id=?",(plate, task_id))
        conn.commit()
        conn.close()
        # Informacja o zakończeniu zadania
        print(f"[CONSUMER] Gotowe → {plate}")


# ---------------- MAIN ----------------
#       Command line interface
if __name__=='__main__':
    if len(sys.argv)<2: print('prepare | train | eval | api'); sys.exit(0)
    if sys.argv[1]=='prepare': prepare()
    elif sys.argv[1]=='train': train()
    elif sys.argv[1]=='eval': eval_project()
    elif sys.argv[1]=='api': uvicorn.run(app,host='0.0.0.0',port=8000)

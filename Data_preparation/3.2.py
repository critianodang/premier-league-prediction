import pandas as pd

# --- 1. Đọc dữ liệu gốc ---
df = pd.read_csv("team_stats.csv")

# --- 2. Chuẩn hóa tên cột (normalize column names) ---
df.columns = (
    df.columns
      .str.strip()                # bỏ khoảng trắng 2 đầu
      .str.lower()                # viết thường hết
      .str.replace(' ', '_')      # thay space = _
      .str.replace('-', '_')      # thay dấu - = _
      .str.replace(r'[^a-z0-9_]', '', regex=True)  # bỏ ký tự đặc biệt
)

# --- 3. Đổi tên cột dài, trùng, hoặc khó đọc sang dạng ngắn gọn ---
rename_dict = {
    'season': 'season',
    'matchdate': 'match_date',
    'hometeam': 'home_team',
    'awayteam': 'away_team',
    'fulltimehomegoals': 'home_goals',
    'fulltimeawaygoals': 'away_goals',
    'fulltimeresult': 'ft_result',
    'halftimehomegoals': 'ht_home_goals',
    'halftimeawaygoals': 'ht_away_goals',
    'halftimeresult': 'ht_result',
    'homeshots': 'home_shots',
    'awayshots': 'away_shots',
    'homeshotsontarget': 'home_sot',
    'awayshotsontarget': 'away_sot',
    'homecorners': 'home_corners',
    'awaycorners': 'away_corners',
    'homefouls': 'home_fouls',
    'awayfouls': 'away_fouls',
    'homeyellowcards': 'home_yellow',
    'awayyellowcards': 'away_yellow',
    'homeredcards': 'home_red',
    'awayredcards': 'away_red'
}

df = df.rename(columns=rename_dict)

# ---  Xử lý kiểu dữ liệu (đặc biệt là ngày tháng) ---
df["match_date"] = pd.to_datetime(df["match_date"], errors='coerce')

# --- 5. Kiểm tra và xử lý giá trị thiếu (nếu có) ---
df = df.dropna(subset=["home_team", "away_team", "home_goals", "away_goals"])

# --- 6. Loại bỏ các cột không cần thiết cho mô hình (tùy chọn) ---
drop_cols = ["ft_result", "ht_result", "ht_home_goals", "ht_away_goals"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

# --- 7. Sắp xếp lại dữ liệu theo thời gian ---
df = df.sort_values(by="match_date").reset_index(drop=True)

# --- 8. Xuất file  để dùng ở bước 7 ---
df.to_csv("matches_cleaned.csv", index=False)

print("Số cột sau khi làm sạch:", len(df.columns))
print("Các cột hiện có:")
print(df.columns.tolist())

































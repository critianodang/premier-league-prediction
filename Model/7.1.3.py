import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1️⃣ Đọc file dữ liệu sau khi tạo feature
df = pd.read_csv("team_stats_features.csv")

# 2️⃣  mã hóa tên đội (Categorical Encoding)
encoder = LabelEncoder()
# Mã hóa tên đội cho cả đội nhà và đội khách
df["home_team_encoded"] = encoder.fit_transform(df["home_team"])
df["away_team_encoded"] = encoder.fit_transform(df["away_team"])

# 3️⃣ CHỌN CÁC CỘT FEATURE CẦN CHUẨN HÓA (Numerical Scaling)
# Các đặc trưng thống kê trong 5 trận gần nhất (last5) và các chỉ số trận đấu (shots, corners, fouls)
num_features = [col for col in df.columns if
                col.endswith("last5") or
                "shots" in col or
                "corners" in col or
                "fouls" in col]

# 4️⃣ KHỞI TẠO VÀ ÁP DỤNG StandardScaler
scaler = StandardScaler()
# Chuẩn hóa các cột đặc trưng số
df[num_features] = scaler.fit_transform(df[num_features])

# 5️⃣ Lưu dataset đã mã hóa và chuẩn hóa
df.to_csv("matches_encoded_scaled.csv", index=False)

# 6️⃣ Kiểm tra nhanh các cột mới
print(df.head(3)[["home_team", "home_team_encoded", "away_team", "away_team_encoded"]])
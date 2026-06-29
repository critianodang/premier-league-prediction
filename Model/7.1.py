import pandas as pd
df = pd.read_csv('matches_cleaned.csv')
# tạo hàm tính phong độ trung bình 5 trận gần nhất cho mỗi đội
def tinh_phong_do(df, team_prefix):
    """
    Hàm này tính phong độ gần đây cho từng đội
    bao gồm trung bình bàn thắng, sút trúng đích và phạt góc
    trong 5 trận gần nhất.
    """
    df_team = df.copy()

    def calculate_rolling_feature(series):
        # Tính rolling mean trên cửa sổ 5 trận, tối thiểu 1 trận
        rolling_mean = series.rolling(window=5, min_periods=1).mean()
        # Dịch chuyển (shift) kết quả 1 vị trí để lấy giá trị TRƯỚC trận hiện tại
        return rolling_mean.shift(1)
    # Trung bình bàn thắng 5 trận gần nhất
    df_team[f'{team_prefix}_avg_goals_last5'] = (
        df_team.groupby(f'{team_prefix}_team')[f'{team_prefix}_goals']
        .transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    )
    # Trung bình sút trúng đích 5 trận gần nhất
    df_team[f'{team_prefix}_avg_sot_last5'] = (
        df_team.groupby(f'{team_prefix}_team')[f'{team_prefix}_sot']
        .transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    )
    # Trung bình phạt góc 5 trận gần nhất
    df_team[f'{team_prefix}_avg_corners_last5'] = (
        df_team.groupby(f'{team_prefix}_team')[f'{team_prefix}_corners']
        .transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    )
    return df_team

# 4️ Áp dụng hàm cho đội nhà và đội khách
df = tinh_phong_do(df, "home")
df = tinh_phong_do(df, "away")

# 5️ Kiểm tra các cột đặc trưng mới được tạo
print([col for col in df.columns if 'last5' in col])

# 6️ Lưu dữ liệu đã tạo feature để sử dụng cho mô hình hồi quy
df.to_csv("team_stats_features.csv", index=False)

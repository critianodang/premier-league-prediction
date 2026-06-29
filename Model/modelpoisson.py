import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import PoissonRegressor # ⬅️ Thư viện Hồi quy Poisson
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Đọc file dữ liệu ĐÃ MÃ HÓA VÀ CHUẨN HÓA
df = pd.read_csv("matches_encoded_scaled.csv")

# 2️⃣ Chọn các cột feature đầu vào và mục tiêu
# BẮT BUỘC: Thêm các cột 'encoded' để mô hình biết đội nào đang thi đấu
features = [col for col in df.columns if
            'avg' in col or
            'shots' in col or
            'corners' in col or
            'encoded' in col]
target_home = 'home_goals'
target_away = 'away_goals'

# 3️⃣ Chia dữ liệu thành tập huấn luyện và kiểm tra (80/20) CHO CẢ HAI MỤC TIÊU
X_train, X_test, y_train_home, y_test_home = train_test_split(
    df[features], df[target_home], test_size=0.2, random_state=42
)
y_train_away = df.loc[y_train_home.index, target_away]
y_test_away = df.loc[y_test_home.index, target_away]


# 4️⃣ Khởi tạo mô hình Poisson Regression
# Alpha là tham số regularization (L2), giữ giá trị nhỏ để tránh underfitting.
model_home = PoissonRegressor(alpha=1e-6, max_iter=500, tol=1e-3)
model_away = PoissonRegressor(alpha=1e-6, max_iter=500, tol=1e-3)

# 5️⃣ Huấn luyện mô hình cho đội nhà và đội khách (Sử dụng X_train chung)
print("Training Poisson Models...")
model_home.fit(X_train, y_train_home)
model_away.fit(X_train, y_train_away)

# 6️⃣ Dự đoán kết quả trên tập kiểm tra (Sử dụng X_test chung)
y_pred_home = model_home.predict(X_test)
y_pred_away = model_away.predict(X_test)

# 7️⃣ Tính toán các chỉ số đánh giá
mae_home = mean_absolute_error(y_test_home, y_pred_home)
rmse_home = np.sqrt(mean_squared_error(y_test_home, y_pred_home))
r2_home = r2_score(y_test_home, y_pred_home)

mae_away = mean_absolute_error(y_test_away, y_pred_away)
rmse_away = np.sqrt(mean_squared_error(y_test_away, y_pred_away))
r2_away = r2_score(y_test_away, y_pred_away)

# 8️⃣ In kết quả đánh giá (Bổ sung RMSE)
print(" Poisson Home Goals Prediction Results:")
print(f"MAE: {mae_home:.3f}, RMSE: {rmse_home:.3f}, R²: {r2_home:.3f}")
print("Poisson Away Goals Prediction Results:")
print(f"MAE: {mae_away:.3f}, RMSE: {rmse_away:.3f}, R²: {r2_away:.3f}")


# 9️⃣ CHUẨN BỊ VÀ VẼ BIỂU ĐỒ
# Tạo DataFrame cho Home Goals
df_home_results = pd.DataFrame({
    'Actual Goals': y_test_home,
    'Predicted Goals': y_pred_home
})
# Tạo DataFrame cho Away Goals
df_away_results = pd.DataFrame({
    'Actual Goals': y_test_away,
    'Predicted Goals': y_pred_away
})

# 🔟 VẼ BIỂU ĐỒ PHÂN TÁN (SCATTER PLOTS)
plt.figure(figsize=(14, 6))

# --- Biểu đồ 1: Home Goals ---
plt.subplot(1, 2, 1)
sns.scatterplot(x='Actual Goals', y='Predicted Goals', data=df_home_results, alpha=0.7, color='teal')
max_val_home = max(df_home_results['Actual Goals'].max(), df_home_results['Predicted Goals'].max()) + 0.5
plt.plot([0, max_val_home], [0, max_val_home], color='red', linestyle='--', label='Ideal Prediction (y=x)', linewidth=2)
plt.title('Poisson Home Goals: Actual vs. Predicted', fontsize=14, fontweight='bold')
plt.xlabel('Actual Home Goals', fontsize=12)
plt.ylabel('Predicted Home Goals', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlim(0, max_val_home)
plt.ylim(0, max_val_home)


# --- Biểu đồ 2: Away Goals ---
plt.subplot(1, 2, 2)
sns.scatterplot(x='Actual Goals', y='Predicted Goals', data=df_away_results, alpha=0.7, color='purple')
max_val_away = max(df_away_results['Actual Goals'].max(), df_away_results['Predicted Goals'].max()) + 0.5
plt.plot([0, max_val_away], [0, max_val_away], color='red', linestyle='--', label='Ideal Prediction (y=x)', linewidth=2)
plt.title('Poisson Away Goals: Actual vs. Predicted', fontsize=14, fontweight='bold')
plt.xlabel('Actual Away Goals', fontsize=12)
plt.ylabel('Predicted Away Goals', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlim(0, max_val_away)
plt.ylim(0, max_val_away)


plt.tight_layout()
plt.show()
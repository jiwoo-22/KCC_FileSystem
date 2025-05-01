import pandas as pd
import matplotlib.pyplot as plt

plt.switch_backend('Agg')  # GUI 없는 환경에서도 그래프 저장 가능

# MB 단위 변환 함수
def to_mb(size_bytes):
    return size_bytes / (1024 * 1024)

# 데이터 읽기
sizes = []
extents = []
paths = []

with open("extent_result.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        try:
            size = int(parts[0])
            extent = int(parts[1])
            path = " ".join(parts[2:])
            if extent >= 2:
                sizes.append(size)
                extents.append(extent)
                paths.append(path)
        except ValueError:
            continue

# DataFrame 생성
df = pd.DataFrame({
    "size_bytes": sizes,
    "extents": extents,
    "path": paths
})

df["size_MB"] = df["size_bytes"].apply(to_mb)

# 분석 텍스트 저장
with open("extent_2plus_analysis.txt", "w") as f:
    f.write(f"📊 extent가 2개 이상인 파일 수: {len(df)}개\n")
    f.write(f"평균 파일 크기: {df['size_MB'].mean():.2f} MB\n")
    f.write(f"최대 파일 크기: {df['size_MB'].max():.2f} MB\n")
    f.write("\n📄 상위 10개 파일 (크기 기준):\n")
    top10 = df.sort_values(by="size_MB", ascending=False).head(10)
    for _, row in top10.iterrows():
        f.write(f"{row['size_MB']:.2f} MB | extents: {row['extents']} | {row['path']}\n")

# 📈 그래프 저장
plt.figure(figsize=(10, 5))
df["size_MB"].hist(bins=40, color='skyblue', edgecolor='black')
plt.title("File Size Distribution (extent ≥ 2)")
plt.xlabel("File Size (MB)")
plt.ylabel("Number of Files")
plt.grid(True)
plt.tight_layout()
plt.savefig("extent_2plus_histogram.png")

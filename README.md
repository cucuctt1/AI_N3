# Bat Algorithm Benchmark (Python)

Benchmark **Bat Algorithm** trên hàm mục tiêu **Sphere Function**.
Mục tiêu là tối ưu hóa giá trị hàm về gần 0 và theo dõi độ hội tụ theo số vòng lặp.

## Cấu trúc dự án

- `main.py`: Điểm vào chương trình, cấu hình và chạy benchmark.
- `src/Bat.py`: Định nghĩa đối tượng dơi và các hàm cập nhật chính.
- `src/benchmark.py`: Vòng lặp benchmark và thống kê nhiều lần chạy.
- `src/fitness_fnc.py`: Hàm mục tiêu (hiện tại có `sphere`).
- `src/matplot_helper.py`: Hàm vẽ đường cong hội tụ.

## Yêu cầu môi trường

- Python 3.10+

Cài thư viện:

```bash
pip install -r requirement.txt
```

## Cách chạy

```bash
python main.py
```

Chương trình sẽ in:
- Kết quả từng run
- Best/Mean/Std fitness sau khi hoàn tất benchmark
- Nghiệm tốt nhất tìm được
- Biểu đồ hội tụ (nếu `plot=True` trong `main.py`)

## Đường cong hội tụ

> Bạn chỉ cần thêm file ảnh sau vào repo để hiển thị trên GitHub:
> `images/convergence_curve.png`

![Convergence Curve](images/convergence_curve.png)

## Gợi ý tinh chỉnh nhanh

Trong `main.py`, bạn có thể chỉnh:
- `T_MAX`: số vòng lặp
- `N_bats`: số lượng cá thể
- `dim`: số chiều bài toán
- `bounds`: miền tìm kiếm
- `n_runs`: số lần chạy benchmark

## Ghi chú

- Nếu chạy trên môi trường không có giao diện (headless), có thể đặt `plot=False` để tránh bị treo khi hiển thị biểu đồ.

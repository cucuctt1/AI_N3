# Bat Algorithm Benchmark (Python)

Benchmark **Bat Algorithm** trên hàm mục tiêu **Sphere Function**.
Code hiện tại chạy benchmark cho **2 mode hành vi**:
- `global`
- `individual`

và vẽ convergence curve trên cùng một biểu đồ.

## Cấu trúc dự án

- `main.py`: Điểm vào chương trình, cấu hình biến và chạy benchmark.
- `src/Bat.py`: Định nghĩa Bat object + các hàm cập nhật chuyển động/hành vi/local walk.
- `src/benchmark.py`: Vòng lặp benchmark và so sánh `global` vs `individual`.
- `src/fitness_fnc.py`: Hàm mục tiêu (hiện tại dùng `sphere`).
- `src/matplot_helper.py`: Hàm vẽ convergence curve bằng matplotlib.

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

## Biến cấu hình chính (trong `main.py`)

- `T_MAX`: số vòng lặp tối đa.
- `N_bats`: kích thước quần thể.
- `dim`: số chiều bài toán.
- `bounds`: miền tìm kiếm.
- `N_RUNS`: số lần benchmark.

### Hyperparameters Bat Algorithm

- `F_MIN`, `F_MAX`: dải tần số.
- `ALPHA`: hệ số giảm loudness.
- `GAMMA`: hệ số tăng pulse rate.

### Runtime options

- `SEED`: seed cho random để tái lập kết quả.
- `PLOT`: bật/tắt vẽ biểu đồ.
- `VERBOSE`: bật/tắt log chi tiết.
- `AUTO_GAMMA`: tự chỉnh gamma theo `dim`.
- `USE_IMPROVED_LOCAL_WALK`:
	- `False`: dùng local walk cơ bản (`local_random_walk_for_benchmark`).
	- `True`: dùng local walk cải tiến (`improved_local_random_walk_for_benchmark`).

## Kết quả đầu ra

Sau khi chạy, chương trình in:
- Best fitness và best solution cho mode `global`.
- Best fitness và best solution cho mode `individual`.
- Thống kê theo run (Best/Mean/Std) cho từng mode.

Nếu `PLOT=True`, chương trình vẽ convergence curve của cả hai mode trên cùng biểu đồ.

## Hình minh họa convergence

README đang trỏ tới file ảnh sau (bạn có thể thay ảnh của mình):

`images/convergence_curve.png`

![Convergence Curve](images/convergence_curve.png)

## Ghi chú

- Nếu chạy trên môi trường không có GUI (headless), đặt `PLOT=False` để tránh block ở `plt.show()`.

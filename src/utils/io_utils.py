import csv


def save_benchmark_stats_csv(rows, output_dir, filename="benchmark_stats.csv"):
    csv_path = output_dir / filename
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "objective",
                "algorithm",
                "best_fitness",
                "mean_fitness",
                "std_fitness",
                "best_run_index",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    return csv_path

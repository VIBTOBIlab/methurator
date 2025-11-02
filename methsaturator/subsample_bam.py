import subprocess
import os


def subsample_bam(bam_path, percentage, output_dir, seed=42):
    """
    Subsamples a BAM file using samtools according to a percentage.
    """
    bam_dir = os.path.join(output_dir, "bams")
    os.makedirs(bam_dir, exist_ok=True)

    round_pct = round(percentage, 2)
    base_name = os.path.basename(bam_path).replace(
        ".bam", f"_subsample_{round_pct:.1f}.bam"
    )
    output_path = os.path.join(bam_dir, base_name)
    if not os.path.exists(output_path):
        # samtools command
        cmd = [
            "samtools",
            "view",
            "-s",
            str(round_pct),
            "--subsample-seed",
            str(seed),
            "-b",
            bam_path,
            "-o",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        cmd2 = ["samtools", "index", output_path]
        subprocess.run(cmd2, check=True)

    read_count = int(
        subprocess.run(
            ["samtools", "view", "-c", output_path], capture_output=True, text=True
        ).stdout.strip()
    )
    sample_name = os.path.basename(bam_path).split(".", 1)[0]
    sample_stats = [sample_name, round_pct, read_count]
    return sample_stats, output_path

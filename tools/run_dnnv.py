#!/usr/bin/env python
import argparse
import contextlib
import os
import pandas as pd
import select
import shlex
import subprocess as sp
import time

from pathlib import Path
from typing import Optional


def memory_t(value):
    if isinstance(value, int):
        return value
    elif value.lower().endswith("g"):
        return int(value[:-1]) * 1_000_000_000
    elif value.lower().endswith("m"):
        return int(value[:-1]) * 1_000_000
    elif value.lower().endswith("k"):
        return int(value[:-1]) * 1000
    else:
        return int(value)


def _parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=False)

    config_group = parser.add_argument_group("Benchmark Configuration")
    config_group.add_argument(
        "-b",
        "--benchmark",
        type=Path,
        default=Path(__file__).parent,
        metavar="PATH",
        dest="benchmark_path",
        help="The path to the benchmark to be run (default='.')",
    )
    config_group.add_argument(
        "-p",
        "--problems-filename",
        type=str,
        default="problems.csv",
        metavar="NAME",
        help="The name of the csv of the problem set to use (default='problems.csv')",
    )
    config_group.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("results.csv"),
        dest="results_csv",
        help="The path to a csv file in which to save results (default='./results.csv')",
    )

    resmonitor_group = parser.add_argument_group("Resource Management")
    resmonitor_group.add_argument(
        "--resmonitor-path",
        type=str,
        default=Path(__file__).parent / "resmonitor.py",
        metavar="PATH",
    )
    resmonitor_group.add_argument(
        "-T", "--time", default=-1, type=float, help="The max running time in seconds"
    )
    resmonitor_group.add_argument(
        "-M",
        "--memory",
        default=-1,
        type=memory_t,
        help="The max allowed memory in bytes",
    )

    resmonitor_group.add_argument(
        "-n",
        "--ntasks",
        type=int,
        default=1,
        help="The max number of running verification tasks (default=1).",
    )
    return parser.parse_known_args()


@contextlib.contextmanager
def lock(filename: Path, *args, **kwargs):
    lock_filename = filename.with_suffix(".lock")
    try:
        while True:
            try:
                lock_fd = os.open(lock_filename, os.O_CREAT | os.O_WRONLY | os.O_EXCL)
                break
            except IOError as e:
                pass
        yield
    finally:
        os.close(lock_fd)
        os.remove(lock_filename)


def wait(pool, timeout=float("inf")):
    start_t = time.time()
    while timeout < 0 or time.time() - start_t < timeout:
        for index, task in enumerate(pool):
            if task.poll() is not None:
                stdout_lines = task.stdout.readlines()
                for line in stdout_lines:
                    print(f"{{{task.problem_id} (STDOUT)}}: {line.strip()}")
                task.stdout_lines.extend(stdout_lines)
                stderr_lines = task.stderr.readlines()
                for line in stderr_lines:
                    print(f"{{{task.problem_id} (STDERR)}}: {line.strip()}")
                task.stderr_lines.extend(stderr_lines)
                return pool.pop(index)
            for (name, stream, lines, buffer) in [
                # ("STDOUT", task.stdout, task.stdout_lines, task.stdout_buffer),
                ("STDERR", task.stderr, task.stderr_lines, task.stderr_buffer),
            ]:
                while True:
                    ready, _, _ = select.select([stream], [], [], 0)
                    if not ready:
                        break
                    byte = stream.read(1)
                    if not byte:
                        break
                    buffer[0] += byte
                buffered_lines = buffer[0].split("\n")
                buffer[0] = buffered_lines[-1]
                for line in buffered_lines[:-1]:
                    lines.append(line)
                    print(f"{{{task.problem_id} ({name})}}: {line.strip()}")
    for index, task in enumerate(pool):
        if task.poll() is not None:
            stdout_lines = task.stdout.readlines()
            for line in stdout_lines:
                print(f"{{{task.problem_id} (STDOUT)}}: {line.strip()}")
            task.stdout_lines.extend(stdout_lines)
            stderr_lines = task.stderr.readlines()
            for line in stderr_lines:
                print(f"{{{task.problem_id} (STDERR)}}: {line.strip()}")
            task.stderr_lines.extend(stderr_lines)
            return pool.pop(index)
    raise RuntimeError("Timeout while waiting for task completion.")


def parse_verification_output(stdout_lines, stderr_lines):
    total_time: Optional[float] = None
    resmonitor_lines = [line for line in stderr_lines if "(resmonitor)" in line]
    resmonitor_result_line = resmonitor_lines[-1]
    if "finished successfully" in resmonitor_result_line:
        try:
            result_lines = []
            at_result = False
            for line in stdout_lines:
                if line.startswith("dnnv.verifiers"):
                    at_result = True
                elif at_result and ("  result:" in line) or ("  time:" in line):
                    result_lines.append(line.strip())
            result = result_lines[0].split(maxsplit=1)[-1]
            total_time = float(result_lines[1].split()[-1])
        except Exception as e:
            result = f"VerificationRunnerError({type(e).__name__})"
    elif "Out of Memory" in resmonitor_result_line:
        result = "outofmemory"
        total_time = float(resmonitor_lines[-2].split()[-3][:-2])
    elif "Timeout" in resmonitor_result_line:
        result = "timeout"
        total_time = float(resmonitor_lines[-2].split()[-3][:-2])
    else:
        result = "!"
    print("  result:", result)
    print("  total time:", total_time)
    results = {
        "Result": result,
        "TotalTime": total_time,
    }
    return results


def update_results(results_csv, task, results):
    with lock(results_csv):
        df = pd.read_csv(results_csv)
        for key, value in results.items():
            df.loc[(df["ProblemId"] == task.problem_id), key] = value
        df.to_csv(results_csv, index=False)


def main(args, extra_args):
    with lock(args.results_csv):
        if not args.results_csv.exists():
            with open(args.results_csv, "w+") as f:
                f.write("ProblemId,Result,TotalTime\n")
    problems = set()
    problem_df = pd.read_csv(args.benchmark_path / args.problems_filename)
    for row in problem_df.itertuples():
        problems.add(row.problem_id)

    pool = []
    while len(problems) > 0:
        with lock(args.results_csv):
            df = pd.read_csv(args.results_csv)
            for problem_id in df["ProblemId"]:
                problems.discard(problem_id)
            if len(problems) == 0:
                break
            problem_id = problems.pop()
            df = pd.concat([df, pd.DataFrame({"ProblemId": [problem_id]})])
            df.to_csv(args.results_csv, index=False)

        property_filename = (
            problem_df[(problem_df["problem_id"] == problem_id)]["property_filename"]
            .unique()
            .item()
        )
        network_names = (
            problem_df[(problem_df["problem_id"] == problem_id)]["network_names"]
            .item()
            .split(":")
        )
        network_filenames = (
            problem_df[(problem_df["problem_id"] == problem_id)]["network_filenames"]
            .item()
            .split(":")
        )
        networks = " ".join(
            [f"--network {n} {fn}" for n, fn in zip(network_names, network_filenames)]
        )
        resmonitor = f"python {args.resmonitor_path.resolve()}"
        resmonitor_args = f"{resmonitor} -M {args.memory} -T {args.time}"
        extra_args_str = " ".join(extra_args)
        if "parameters" in problem_df:
            problem_args = (
                problem_df[(problem_df["problem_id"] == problem_id)]["parameters"]
                .unique()
                .item()
            )
            if isinstance(problem_args, str):
                extra_args_str = f"{extra_args_str} {problem_args}"
        verifier_args = (
            f"python -m dnnv {property_filename} {networks} {extra_args_str}"
        )
        run_args = f"{resmonitor_args} {verifier_args}"
        print(run_args)

        proc = sp.Popen(
            shlex.split(run_args),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            encoding="utf8",
            bufsize=1,
            cwd=args.benchmark_path,
        )
        proc.problem_id = problem_id
        proc.stdout_buffer = [""]
        proc.stderr_buffer = [""]
        proc.stdout_lines = []
        proc.stderr_lines = []
        pool.append(proc)

        while len(pool) >= args.ntasks:
            finished_task = wait(pool, timeout=2 * args.time)
            print("FINISHED:", " ".join(proc.args))
            results = parse_verification_output(
                finished_task.stdout_lines, finished_task.stderr_lines
            )
            update_results(args.results_csv, finished_task, results)
    while len(pool):
        finished_task = wait(pool, timeout=2 * args.time)
        print("FINISHED:", " ".join(proc.args))
        results = parse_verification_output(
            finished_task.stdout_lines, finished_task.stderr_lines
        )
        update_results(args.results_csv, finished_task, results)


if __name__ == "__main__":
    main(*_parse_args())

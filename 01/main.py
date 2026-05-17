import argparse
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".pdf", ".txt", ".md", ".docx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Videos": {".mp4", ".mov", ".mkv"},
    "Audio": {".mp3", ".wav", ".flac"},
    "Code": {".py", ".js", ".html", ".css", ".toml", ".json", ".lock"},
}


class Arguments(argparse.Namespace):
    folder: str
    apply: bool

    def __init__(self) -> None:
        super().__init__()
        self.folder = "."
        self.apply = False


def get_category(path: Path) -> str:
    extension = path.suffix.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_files(folder: Path) -> list[Path]:
    return sorted(
        (path for path in folder.iterdir() if path.is_file()),
        key=lambda path: path.name.lower(),
    )


def group_files(files: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}

    for path in files:
        category = get_category(path)
        groups.setdefault(category, []).append(path)

    return groups


def print_groups(groups: dict[str, list[Path]]) -> None:
    category_names = [*CATEGORIES, "Others"]

    for category in category_names:
        files = groups.get(category)

        if not files:
            continue

        print(f"{category}/")

        for path in files:
            print(f"  {path.name}")

        print()


def preview_moves(folder: Path) -> None:
    files = get_files(folder)

    if not files:
        print("정리할 파일이 없습니다.")
        return

    print(f"정리할 폴더: {folder}")
    print()

    print_groups(group_files(files))
    print("미리보기라 실제로 이동하지 않았습니다.")


def apply_moves(folder: Path) -> None:
    files = get_files(folder)

    if not files:
        print("정리할 파일이 없습니다.")
        return

    print(f"정리 중: {folder}")
    print()

    moved_files: list[Path] = []
    skipped_files: list[str] = []
    moved_count = 0

    for path in files:
        category = get_category(path)
        target_folder = folder / category
        target_path = target_folder / path.name

        if target_path.exists():
            skipped_files.append(f"{path.name} (같은 이름의 파일이 있음)")
            continue

        try:
            target_folder.mkdir(exist_ok=True)
            _ = path.rename(target_path)
        except OSError as error:
            skipped_files.append(f"{path.name} ({error})")
            continue

        moved_files.append(target_path)
        moved_count += 1

    print_groups(group_files(moved_files))
    print(f"완료: {moved_count}개 이동")

    if skipped_files:
        print()
        print("건너뜀:")

        for name in skipped_files:
            print(f"  {name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="폴더 안 파일을 확장자별로 정리합니다."
    )
    _ = parser.add_argument("folder", nargs="?", default=".", help="정리할 폴더")
    _ = parser.add_argument(
        "--apply",
        action="store_true",
        help="파일을 실제로 이동합니다.",
    )
    args = parser.parse_args(namespace=Arguments())

    folder = Path(args.folder).expanduser()

    if not folder.exists():
        print(f"경로를 찾을 수 없습니다: {folder}")
        raise SystemExit(1)

    if not folder.is_dir():
        print(f"폴더가 아닙니다: {folder}")
        raise SystemExit(1)

    folder = folder.resolve()

    if args.apply:
        apply_moves(folder)
    else:
        preview_moves(folder)


if __name__ == "__main__":
    main()

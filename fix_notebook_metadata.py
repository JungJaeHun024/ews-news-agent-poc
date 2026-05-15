import json
import sys
from pathlib import Path


def clean_notebook(path: str) -> None:
    nb_path = Path(path)

    if not nb_path.exists():
        raise FileNotFoundError(f"Notebook not found: {nb_path}")

    with nb_path.open("r", encoding="utf-8") as f:
        notebook = json.load(f)

    # 1. GitHub 렌더링 오류를 유발하는 widgets metadata 제거
    metadata = notebook.get("metadata", {})
    metadata.pop("widgets", None)
    notebook["metadata"] = metadata

    # 2. Cell 단위 metadata 정리
    for cell in notebook.get("cells", []):
        cell_metadata = cell.get("metadata", {})
        cell_metadata.pop("widgets", None)
        cell_metadata.pop("ExecuteTime", None)
        cell["metadata"] = cell_metadata

        # 3. GitHub 렌더링 안정성을 위해 실행 결과 제거
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    # 4. Notebook format 보정
    notebook["nbformat"] = notebook.get("nbformat", 4)
    notebook["nbformat_minor"] = notebook.get("nbformat_minor", 5)

    with nb_path.open("w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

    print(f"Cleaned notebook metadata: {nb_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_notebook_metadata.py <notebook_path>")
        sys.exit(1)

    clean_notebook(sys.argv[1])
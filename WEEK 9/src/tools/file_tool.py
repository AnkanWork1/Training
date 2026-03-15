# src/tools/file_agent.py

class FileAgent:

    def run(self, payload: dict):

        
        # -------- WRITE --------
        if "file_path" in payload and "content" in payload:
            return self.write_file(payload["file_path"], payload["content"])

        # -------- READ --------
        if "file_path" in payload:
            return self.read_file(payload["file_path"])

        return "FileAgent: unsupported payload"

    # ----------------------------
    # actual tools
    # ----------------------------

    def read_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"File read error: {e}"

    def write_file(self, file_path: str, content: str):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Written to {file_path}"
        except Exception as e:
            return f"File write error: {e}"

    def search_in_file(self, file_path: str, keyword: str):
        results = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, start=1):
                    if keyword in line:
                        results.append(f"{i}: {line.rstrip()}")
        except Exception as e:
            return f"File search error: {e}"

        if not results:
            return "No matching lines found."

        return "\n".join(results)
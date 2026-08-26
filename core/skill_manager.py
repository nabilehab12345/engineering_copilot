import os
import json

class SkillManager:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
        self.index_file = os.path.join(self.skills_dir, "skills_index.json")
        self.load_index()

    def load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r", encoding="utf-8") as f:
                self.skills = json.load(f)
        else:
            self.skills = {}

    def save_skill(self, skill_name: str, description: str, python_code: str):
        path = os.path.join(self.skills_dir, f"{skill_name}.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(python_code)
        self.skills[skill_name] = {"description": description, "file": path}
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.skills, f, indent=4, ensure_ascii=False)
        return f"تم حفظ المهارة '{skill_name}' بنجاح."
import cadquery as cq
import os

def generate_stepped_shaft_cad(d1_mm: float, l1_mm: float, d2_mm: float, l2_mm: float, filename: str = "stepped_shaft.step") -> dict:
    """
    توليد مجسم CAD لعمود متدرج مع مجرى خابور وتصديره كملف STEP
    """
    try:
        # رسم العمود المتدرج
        shaft = (
            cq.Workplane("XY")
            .circle(d1_mm / 2.0).extrude(l1_mm)
            .faces(">Z").workplane()
            .circle(d2_mm / 2.0).extrude(l2_mm)
        )

        export_path = os.path.join("E:\\engineering_copilot", filename)
        cq.exporters.export(shaft, export_path)

        return {
            "status": "success",
            "message": f"CAD model successfully generated and saved to {export_path}",
            "file_path": export_path
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
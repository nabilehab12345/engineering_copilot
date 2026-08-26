import os

def modify_solidworks_dimension(part_file_path: str, dimension_name: str, new_value_mm: float, export_step: bool = True) -> dict:
    """
    الاتصال ببرنامج SolidWorks المفتوح، وتعديل بُعد محدد في الـ Sketch، وإعادة بناء المجسم وتصديره
    """
    try:
        import importlib

        win32com_client = importlib.import_module("win32com.client")
        
        # الاتصال بتطبيق SolidWorks
        sw_app = win32com_client.Dispatch("SldWorks.Application")
        sw_app.Visible = True

        # فتح أو تفعيل ملف القطعة
        doc = sw_app.OpenDoc6(part_file_path, 1, 1, "", 0, 0) # 1 = Part doc
        part = sw_app.ActiveDoc
        
        if not part:
            return {"status": "error", "message": "Failed to open or attach to SolidWorks part document."}

        # تعديل البُعد المطلوب (SolidWorks يتعامل بالأمتار داخلياً)
        dim_param = part.Parameter(dimension_name)
        if dim_param:
            dim_param.SystemValue = new_value_mm / 1000.0  # تحويل المليمتر إلى متر
            part.EditRebuild3() # إعادة بناء المجسم بالأبعاد الجديدة
            part.Save3(1, 0, 0) # حفظ التعديلات
            
            output_step = None
            if export_step:
                output_step = part_file_path.replace(".SLDPRT", ".STEP").replace(".sldprt", ".STEP")
                part.SaveAs3(output_step, 0, 2)
                
            return {
                "status": "success",
                "message": f"Dimension '{dimension_name}' updated to {new_value_mm} mm successfully.",
                "exported_step": output_step
            }
        else:
            return {"status": "error", "message": f"Dimension '{dimension_name}' not found in part."}

    except Exception as e:
        return {"status": "error", "message": f"SolidWorks API execution failed: {str(e)}"}
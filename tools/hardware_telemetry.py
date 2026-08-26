import serial
import json
import time

def stream_and_diagnose_hardware(com_port: str = "COM3", baudrate: int = 115200, duration_seconds: int = 3) -> dict:
    """
    الاتصال بالروبوت الحقيقي، قراءة التليمتري لعدة ثوانٍ، وفحص درجات الحرارة والتيارات وعزم الموتورات
    """
    try:
        readings = []
        start = time.time()
        
        with serial.Serial(com_port, baudrate, timeout=1.0) as ser:
            time.sleep(0.2)
            while time.time() - start < duration_seconds:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        readings.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        if not readings:
            return {"status": "warning", "message": f"Connected to {com_port} but no JSON telemetry data received."}

        # تحليل البيانات المجمعة
        latest = readings[-1]
        max_temp = max([r.get("temp_c", 0) for r in readings])
        max_current = max([r.get("current_a", 0) for r in readings])
        
        warnings = []
        if max_temp > 70.0:
            warnings.append(f"High motor temperature detected: {max_temp} °C")
        if max_current > 15.0:
            warnings.append(f"High peak current detected: {max_current} A")

        return {
            "status": "success",
            "samples_analyzed": len(readings),
            "latest_state": latest,
            "peak_current_a": max_current,
            "peak_temperature_c": max_temp,
            "diagnostic_warnings": warnings
        }

    except Exception as e:
        return {"status": "error", "message": f"Hardware connection failed on {com_port}: {str(e)}"}
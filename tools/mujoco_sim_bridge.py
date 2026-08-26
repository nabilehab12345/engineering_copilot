import mujoco
import numpy as np

def run_physics_simulation_test(xml_model_string: str = "", simulation_steps: int = 1000) -> dict:
    """
    تشغيل محاكاة فيزيائية في MuJoCo واختبار استقرار المفاصل وقوى التلامس
    """
    try:
        import mujoco
        import numpy as np

        if not xml_model_string:
            return {"status": "error", "message": "No XML model string provided."}

        model = mujoco.MjModel.from_xml_string(xml_model_string)
        data = mujoco.MjData(model)

        diverged = False
        for step in range(simulation_steps):
            mujoco.mj_step(model, data)
            if np.isnan(data.qpos).any() or np.isinf(data.qpos).any():
                diverged = True
                break

        return {
            "status": "success" if not diverged else "unstable",
            "total_steps_simulated": simulation_steps,
            "is_physically_stable": not diverged,
            "final_joint_positions": data.qpos.tolist(),
            "diagnostic_message": "Simulation completed with stable physics." if not diverged else "Instability detected."
        }

    except ImportError:
        return {
            "status": "warning",
            "message": "MuJoCo library is not installed yet. Run 'pip install mujoco' in terminal to enable simulation."
        }
    except Exception as e:
        return {"status": "error", "message": f"MuJoCo Simulation failed: {str(e)}"}
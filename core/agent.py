import json
import ollama
from core.rag_engine import KnowledgeEngine
from core.skill_manager import SkillManager
from tools.mechanics import calculate_shaft_diameter, calculate_gear_ratio_and_teeth
from tools.electrical_panel import design_motor_feeder_circuit
from tools.self_healing_runner import execute_and_auto_debug
from tools.bom_sourcing import calculate_bom_and_weight_budget
from tools.mujoco_sim_bridge import run_physics_simulation_test

class EngineeringAgent:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name
        self.rag = KnowledgeEngine()
        self.skills = SkillManager()
        
        self.tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "calculate_shaft_diameter",
                    "description": "Calculate required shaft diameter from torque, bending moment and yield strength.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "torque_nm": {"type": "number"},
                            "bending_moment_nm": {"type": "number"},
                            "yield_strength_mpa": {"type": "number"},
                            "factor_of_safety": {"type": "number", "default": 2.0}
                        },
                        "required": ["torque_nm", "bending_moment_nm", "yield_strength_mpa"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_gear_ratio_and_teeth",
                    "description": "Calculate reduction gear ratio, pinion teeth, and gear teeth.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "torque_input": {"type": "number"},
                            "desired_torque_output": {"type": "number"},
                            "pinion_teeth": {"type": "integer", "default": 14}
                        },
                        "required": ["torque_input", "desired_torque_output"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "design_motor_feeder_circuit",
                    "description": "Design an electrical feeder and protection circuit for 3-phase electric motors according to IEC standards.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "motor_power_kw": {"type": "number", "description": "Motor rated power in kW"},
                            "voltage_v": {"type": "number", "default": 380}
                        },
                        "required": ["motor_power_kw"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_physics_simulation_test",
                    "description": "Run a physical simulation in MuJoCo to test robot kinematics and stability.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "xml_model_string": {"type": "string"},
                            "simulation_steps": {"type": "integer", "default": 1000}
                        },
                        "required": ["xml_model_string"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_and_auto_debug",
                    "description": "Run Python code with automatic debugging feedback.",
                    "parameters": {
                        "type": "object",
                        "properties": {"python_code": {"type": "string"}},
                        "required": ["python_code"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_references",
                    "description": "Search engineering textbooks and reference vault.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            }
        ]

    def execute_tool(self, name: str, args: dict):
        if name == "calculate_shaft_diameter":
            return calculate_shaft_diameter(**args)
        elif name == "calculate_gear_ratio_and_teeth":
            return calculate_gear_ratio_and_teeth(**args)
        elif name == "design_motor_feeder_circuit":
            return design_motor_feeder_circuit(**args)
        elif name == "run_physics_simulation_test":
            return run_physics_simulation_test(**args)
        elif name == "execute_and_auto_debug":
            return execute_and_auto_debug(args.get("python_code", ""))
        elif name == "save_new_skill":
            return self.skills.save_skill(**args)
        elif name == "calculate_bom_and_weight_budget":
            return calculate_bom_and_weight_budget(args.get("components_list", []))
        elif name == "search_references":
            return self.rag.search_knowledge(args.get("query", ""))
        return {"error": f"Tool {name} not found"}

    def chat(self, user_prompt: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Elite Senior Principal Robotics, Mechanical, and Electrical Engineer. "
                    "Always communicate in fluent, professional English. "
                    "When calculation tools are executed, provide a structured, step-by-step "
                    "engineering explanation of the results."
                )
            },
            {"role": "user", "content": user_prompt}
        ]

        response = ollama.chat(model=self.model_name, messages=messages, tools=self.tools_schema)
        message = response.get("message", {})
        tool_calls = message.get("tool_calls", [])
        content = message.get("content", "").strip()

        if tool_calls:
            messages.append(message)
            for tool in tool_calls:
                fn_name = tool["function"]["name"]
                fn_args = tool["function"]["arguments"]
                result = self.execute_tool(fn_name, fn_args)
                messages.append({"role": "tool", "content": json.dumps(result, ensure_ascii=False)})

            final_response = ollama.chat(model=self.model_name, messages=messages)
            return final_response["message"]["content"]

        if content.startswith("{") and ("design_" in content or "calculate_" in content or "run_" in content or "name" in content):
            try:
                parsed = json.loads(content)
                fn_name = parsed.get("name")
                fn_args = parsed.get("arguments", {})
                if fn_name:
                    result = self.execute_tool(fn_name, fn_args)
                    messages.append({"role": "assistant", "content": content})
                    messages.append({
                        "role": "user",
                        "content": f"Calculation Result: {json.dumps(result)}. Now explain the full engineering solution and breakdown clearly in English."
                    })
                    final_response = ollama.chat(model=self.model_name, messages=messages)
                    return final_response["message"]["content"]
            except Exception:
                pass

        return content
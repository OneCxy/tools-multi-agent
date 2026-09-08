import json
import math

import stun
from agents import function_tool

from infrastructure.logging.logger import logger
from infrastructure.tools.mcp.mcp_servers import baidu_mcp_client


def bd09mc_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    """将百度墨卡托坐标转换为百度经纬度坐标。"""
    if abs(lat) < 1e-6 or abs(lng) < 1e-6:
        return 0.0, 0.0

    converted_lng = lng / 20037508.34 * 180
    converted_lat = lat / 20037508.34 * 180
    converted_lat = 180 / math.pi * (
        2 * math.atan(math.exp(converted_lat * math.pi / 180)) - math.pi / 2
    )
    return converted_lng, converted_lat


def get_ip_via_stun() -> str | None:
    """获取当前运行环境的公网出口 IP。"""
    try:
        _, external_ip, _ = stun.get_ip_info()
        return external_ip
    except Exception as exc:
        logger.warning(f"STUN 获取公网 IP 失败: {exc}")
        return None


@function_tool
async def resolve_user_location_from_text(user_input: str) -> str:
    """将用户提供的起点地名解析为 BD09LL 坐标。

    Args:
        user_input: 用户明确提供的城市、区县或详细地址。用户只说“附近”
            “这里”或“我的位置”时传入空字符串。
    """
    relative_locations = {
        "附近", "这", "这里", "这儿", "周围", "周边",
        "我的位置", "当前位置", "所在位置", "nearby", "here",
    }
    user_input = user_input.strip() if user_input else ""
    if user_input in relative_locations:
        user_input = ""

    if user_input:
        try:
            geo_result = await baidu_mcp_client.call_tool(
                tool_name="map_geocode",
                arguments={"address": user_input},
            )
            data = json.loads(geo_result.content[0].text)
            location = data.get("result", {}).get("location", {})
            if "lat" in location and "lng" in location:
                return json.dumps(
                    {
                        "ok": True,
                        "lat": float(location["lat"]),
                        "lng": float(location["lng"]),
                        "source": "geocode",
                        "original_input": user_input,
                    },
                    ensure_ascii=False,
                )
        except Exception as exc:
            logger.warning(f"地址解析失败 '{user_input}': {exc}")

    user_ip = get_ip_via_stun()
    if user_ip and user_ip not in {"127.0.0.1", "localhost", "::1"}:
        try:
            ip_result = await baidu_mcp_client.call_tool(
                "map_ip_location",
                {"ip": user_ip},
            )
            data = json.loads(ip_result.content[0].text)
            if data.get("status") == 0:
                point = data.get("content", {}).get("point", {})
                if point.get("x") and point.get("y"):
                    lng, lat = bd09mc_to_bd09(float(point["x"]), float(point["y"]))
                    return json.dumps(
                        {"ok": True, "lat": lat, "lng": lng, "source": "ip"},
                        ensure_ascii=False,
                    )
        except Exception as exc:
            logger.warning(f"IP 定位失败 {user_ip}: {exc}")

    return json.dumps(
        {
            "ok": False,
            "error": "无法可靠获取当前位置，请提供城市、区县或详细地址",
            "source": "unresolved",
        },
        ensure_ascii=False,
    )

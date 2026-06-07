"""
Vedic Rectifier — Time Scanner
===============================
扫描出生时间±N分钟范围，输出每分钟的Lagna/D9/D10变化。

用法 (v3.2 起 --tz 必填):
  python time_scan.py --date 2000-01-01 --time 10:30 --lat 28.61 --lon 77.21 --tz Asia/Kolkata
  python time_scan.py --date 2000-01-01 --time 10:30 --lat 28.61 --lon 77.21 --tz Asia/Kolkata --range 60
  python time_scan.py --date 2000-01-01 --time 05:00 --lat 28.61 --lon 77.21 --tz UTC  # 已转好 UTC

依赖: pip install -r ../requirements.txt
      (核心是 ephem；时区用 Python 3.9+ 内置 zoneinfo)
"""

import math
import os
import argparse
import sys

try:
    import ephem
except ModuleNotFoundError:
    _here = os.path.dirname(os.path.abspath(__file__))
    _req = os.path.normpath(os.path.join(_here, "..", "requirements.txt"))
    print(
        "❌ 缺少依赖 ephem。\n"
        f"   请先运行: pip install -r {_req}\n"
        "   或:       pip install ephem>=4.1",
        file=sys.stderr,
    )
    sys.exit(1)

SIGNS = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
SIGNS_CN = ['白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶', '双鱼']


def get_ayanamsa(year):
    """
    Lahiri Ayanamsa 简化公式

    基于 2000年 = 23.86°, 每年增加约 0.0139°
    精度 ±0.1°（对应 Lagna 移动 ±0.4 分钟）

    ⚠️ 边界精度警告：
    本系统目标精度 ±5 分钟，本简化公式在大多数情况下足够。
    但在以下场景容差紧：
      - Lagna 度数距离星座边界 < 0.5°
      - 出生时间距 D9 换座点 < 1 分钟
      - 出生时间距 D10 换座点 < 1 分钟
    
    遇到边界案例时（rectifier Step 3c 会标记），
    应人工核对 ephemeris 软件（JHora / Swiss Ephemeris）的 Ayanamsa 值，
    或考虑升级为完整 Lahiri 公式（含章动项 ±10″）。

    本公式不考虑：
      - 章动项（精度损失 < 10″）
      - 非线性项（高精度 Lahiri 公式中存在的二阶项）
    
    对绝大多数 ±5 分钟目标，简化公式足够；
    对 ±1 分钟级目标（D60 应用），必须升级。
    """
    return 23.86 + (year - 2000) * 0.0139


def calc_sidereal_asc(obs):
    """
    计算恒星(sidereal)上升点度数。
    
    参数: ephem.Observer 对象（已设置 lat/lon/date）
    返回: 恒星Lagna绝对度数 (0-360)
    """
    lst = float(obs.sidereal_time())  # Local Sidereal Time (radians)
    lat_r = float(obs.lat)            # 纬度 (radians)
    
    # 黄赤交角
    obliquity = math.radians(23.4393)
    
    # ASC公式
    asc_rad = math.atan2(
        math.cos(lst),
        -(math.sin(lst) * math.cos(obliquity) +
          math.tan(lat_r) * math.sin(obliquity))
    )
    asc_tropical = math.degrees(asc_rad) % 360
    
    # 转恒星坐标
    year = ephem.Date(obs.date).tuple()[0]
    ayanamsa = get_ayanamsa(year)
    
    return (asc_tropical - ayanamsa) % 360


def deg_to_sign(deg):
    """绝对度数 → (星座缩写, 星座中文, 度数在星座内)"""
    sign_idx = int(deg / 30) % 12
    deg_in_sign = deg % 30
    return SIGNS[sign_idx], SIGNS_CN[sign_idx], deg_in_sign


def calc_d9(asc_deg):
    """
    Lagna绝对度数 → D9(Navamsa)星座
    
    Navamsa规则：每个星座30°分为9等份(3°20')
    起点取决于元素：
      火象(Ar/Le/Sg) → 从Aries(0)开始
      土象(Ta/Vi/Cp) → 从Capricorn(9)开始
      风象(Ge/Li/Aq) → 从Libra(6)开始
      水象(Cn/Sc/Pi) → 从Cancer(3)开始
    """
    sign = int(asc_deg / 30) % 12
    deg_in_sign = asc_deg % 30
    nav_part = int(deg_in_sign / (30.0 / 9))  # 0-8
    
    element = sign % 4  # 0=火, 1=土, 2=风, 3=水
    start_signs = [0, 9, 6, 3]  # Ar, Cp, Li, Cn
    d9_sign = (start_signs[element] + nav_part) % 12
    return SIGNS[d9_sign], SIGNS_CN[d9_sign]


def calc_d10(asc_deg):
    """
    Lagna绝对度数 → D10(Dashamsha)星座
    
    Dashamsha规则：每个星座30°分为10等份(3°)
    起点取决于奇偶：
      奇数星座(Ar/Ge/Le/Li/Sg/Aq) → 从本星座开始
      偶数星座(Ta/Cn/Vi/Sc/Cp/Pi) → 从本星座+9开始
    """
    sign = int(asc_deg / 30) % 12
    deg_in_sign = asc_deg % 30
    das_part = int(deg_in_sign / 3.0)  # 0-9
    if das_part > 9:
        das_part = 9
    
    is_odd = (sign % 2 == 0)  # Ar=0(奇), Ta=1(偶)...
    # ⚠️ v3.2 修订：偶数星座起点是"该星座的第 9 个"，0-index 下是 +8 不是 +9
    # 旧代码 +9 会让所有偶数星座（Ta/Cn/Vi/Sc/Cp/Pi）的 D10 整体错后一宫
    # 验证：Sun in Taurus 2° → D10 应为 Capricorn (公开标准例)
    start = sign if is_odd else (sign + 8) % 12
    d10_sign = (start + das_part) % 12
    return SIGNS[d10_sign], SIGNS_CN[d10_sign]


def scan(date_str, time_str, lat, lon, range_min=30):
    """
    扫描时间范围，输出每分钟的Lagna变化。
    
    参数:
        date_str: "YYYY-MM-DD"
        time_str: "HH:MM"
        lat, lon: 出生地纬度/经度
        range_min: 扫描范围（±分钟）
    
    返回: list of dict
    """
    # 转换日期格式 YYYY-MM-DD → YYYY/MM/DD
    date_ephem = date_str.replace('-', '/')
    
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    
    results = []
    prev_sign = None
    prev_d9 = None
    prev_d10 = None
    
    for delta in range(-range_min, range_min + 1):
        obs.date = f"{date_ephem} {time_str}:00"
        obs.date += delta * ephem.minute
        
        asc_deg = calc_sidereal_asc(obs)
        sign, sign_cn, deg_in_sign = deg_to_sign(asc_deg)
        d9, d9_cn = calc_d9(asc_deg)
        d10, d10_cn = calc_d10(asc_deg)
        
        # 标记变化点
        markers = []
        if prev_sign and sign != prev_sign:
            markers.append(f"★ LAGNA换座→{sign_cn}")
        if prev_d9 and d9 != prev_d9:
            markers.append(f"◆ D9换座→{d9_cn}")
        if prev_d10 and d10 != prev_d10:
            markers.append(f"◇ D10换座→{d10_cn}")
        
        results.append({
            'delta': delta,
            'asc_deg': asc_deg,
            'sign': sign,
            'sign_cn': sign_cn,
            'deg_in_sign': deg_in_sign,
            'd9': d9,
            'd9_cn': d9_cn,
            'd10': d10,
            'd10_cn': d10_cn,
            'markers': ' '.join(markers),
        })
        
        prev_sign = sign
        prev_d9 = d9
        prev_d10 = d10
    
    return results


def print_results(results, date_str, time_str, lat, lon):
    """格式化输出扫描结果"""
    print(f"# 时间扫描结果")
    print(f"# 基准: {date_str} {time_str} UTC | 坐标: ({lat}, {lon})")
    print(f"# 范围: {results[0]['delta']:+d} ~ {results[-1]['delta']:+d} 分钟")
    print()
    print(f"{'偏移':>6} | {'Lagna度数':>10} | {'星座':>6} | {'座内度数':>8} | {'D9':>4} | {'D10':>4} | 标记")
    print("-" * 75)
    
    for r in results:
        marker_str = f"  {r['markers']}" if r['markers'] else ""
        is_base = " ← 原始" if r['delta'] == 0 else ""
        print(f"{r['delta']:+4d}min | {r['asc_deg']:8.2f}° | {r['sign']:>4}{r['sign_cn']} | {r['deg_in_sign']:6.2f}° | {r['d9']:>4} | {r['d10']:>4} |{marker_str}{is_base}")


def save_results(results, date_str, time_str, lat, lon, filepath, time_note=""):
    """保存为Markdown表格"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 时间扫描结果\n\n")
        f.write(f"> 基准 (UTC): {date_str} {time_str}\n")
        if time_note:
            f.write(f"> {time_note}\n")
        f.write(f"> 坐标: ({lat}, {lon})\n\n")
        f.write(f"| 偏移 | Lagna度数 | 星座 | D9 | D10 | 标记 |\n")
        f.write(f"|------|----------|------|-----|------|------|\n")
        
        for r in results:
            base = " ← 原始" if r['delta'] == 0 else ""
            marker = r['markers'] + base
            f.write(f"| {r['delta']:+4d}min | {r['asc_deg']:.2f}° | "
                    f"{r['sign']} {r['deg_in_sign']:.1f}° | "
                    f"{r['d9']} | {r['d10']} | {marker} |\n")
    
    print(f"\n已保存: {filepath}")


# 时区处理 v3.2 修订：用 Python 标准库 zoneinfo（Python 3.9+ 标配）
# 处理夏令时和历史时区变更，比手维护静态表准确
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    HAS_ZONEINFO = True
except ImportError:
    HAS_ZONEINFO = False


def parse_local_to_utc(date_str, time_str, tz_str):
    """本地时间 + 时区 → UTC 日期和时间
    
    用 zoneinfo 处理 IANA 时区（含夏令时、历史时区变更）
    """
    if tz_str == 'UTC':
        return date_str, time_str
    
    if not HAS_ZONEINFO:
        raise RuntimeError(
            "zoneinfo 不可用（需要 Python 3.9+）。请升级 Python 或先把时间手动转 UTC 后传 --tz UTC"
        )
    
    try:
        tz = ZoneInfo(tz_str)
    except ZoneInfoNotFoundError:
        raise ValueError(
            f"未知 IANA 时区: {tz_str}\n"
            f"常见值: Asia/Shanghai, Asia/Kolkata, Europe/Berlin, "
            f"America/New_York, America/Los_Angeles, Australia/Sydney 等\n"
            f"完整列表见 https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        )
    
    from datetime import datetime, timezone
    dt_local = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt_local = dt_local.replace(tzinfo=tz)
    dt_utc = dt_local.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%d"), dt_utc.strftime("%H:%M")


def main():
    parser = argparse.ArgumentParser(
        description='Vedic Rectifier Time Scanner',
        epilog=(
            '⚠️ v3.2 修订: --tz 必填，用 zoneinfo 处理夏令时和历史时区变更。\n'
            '示例:\n'
            '  python time_scan.py --date 1990-05-21 --time 14:23 --lat 31.23 --lon 121.47 --tz Asia/Shanghai\n'
            '  python time_scan.py --date 1990-05-21 --time 06:23 --lat 31.23 --lon 121.47 --tz UTC'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--date', required=True, help='出生日期 YYYY-MM-DD (本地日期)')
    parser.add_argument('--time', required=True, help='预估出生时间 HH:MM (按 --tz 解释)')
    parser.add_argument('--lat', required=True, type=float, help='出生地纬度')
    parser.add_argument('--lon', required=True, type=float, help='出生地经度')
    parser.add_argument('--tz', required=True, type=str,
                        help='⚠️ 必填: 时区 IANA 字符串。中国大陆=Asia/Shanghai, '
                             '印度=Asia/Kolkata, 美东=America/New_York, 已转 UTC=UTC。'
                             '用 zoneinfo 处理夏令时和历史时区变更。')
    parser.add_argument('--range', type=int, default=30, help='扫描范围±分钟 (默认30)')
    parser.add_argument('--save', type=str, help='保存结果到文件路径')
    
    args = parser.parse_args()

    # 时区转换
    if args.tz != 'UTC':
        try:
            utc_date, utc_time = parse_local_to_utc(args.date, args.time, args.tz)
            time_note = f"输入: {args.date} {args.time} ({args.tz}) → UTC: {utc_date} {utc_time}"
            print(f"⏰ 时区转换 (zoneinfo): {args.time} ({args.tz}) → UTC {utc_time}")
            args.date, args.time = utc_date, utc_time
        except (ValueError, RuntimeError) as e:
            parser.error(str(e))
    else:
        time_note = f"输入: {args.date} {args.time} UTC"
    
    results = scan(args.date, args.time, args.lat, args.lon, args.range)
    print_results(results, args.date, args.time, args.lat, args.lon)
    
    if args.save:
        save_results(results, args.date, args.time, args.lat, args.lon, args.save, time_note)
    
    # 输出变化点摘要
    print("\n## 关键变化点")
    for r in results:
        if r['markers']:
            print(f"  {r['delta']:+4d}min: {r['markers']}")


if __name__ == '__main__':
    main()

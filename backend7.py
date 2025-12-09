#!/usr/bin/env python3
"""
Backend 7.0 — FIXED EDITION
- 保留全部复杂逻辑（LLM+meta-learning+future value+behavior modifiers）
- 修复所有结构错误、变量未定义、顶层执行导致 worker 崩溃的问题
- payoff 矩阵位置保留但不填内容（你之后粘贴即可）
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, random
from openai import OpenAI


# ============================================================
# OPENAI CLIENT
# ============================================================
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


# ============================================================
# FLASK INIT
# ============================================================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})
app.config["SECRET_KEY"] = "insead-game-simulation-final-8"


# ============================================================
# PAYOFF MATRIX — 留空等待你自己粘贴
# ============================================================
AM_PAYOFFS = [ [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [-1.0, 19.0, 29.0, 38.0, 45.0, 51.0, 57.0, 62.0, 66.0, 70.0, 74.0, 77.0, 80.0, 83.0, 86.0, 88.0, 91.0, 93.0, 95.0, 97.0, 99.0, 100.0, 102.0, 103.0, 105.0, 106.0], [-3.0, 27.0, 42.0, 55.0, 66.0, 76.0, 84.0, 92.0, 99.0, 105.0, 111.0, 117.0, 122.0, 127.0, 131.0, 136.0, 140.0, 144.0, 148.0, 151.0, 154.0, 158.0, 161.0, 164.0, 166.0, 169.0], [-7.0, 31.0, 51.0, 68.0, 82.0, 95.0, 107.0, 117.0, 126.0, 135.0, 143.0, 151.0, 158.0, 165.0, 171.0, 177.0, 183.0, 189.0, 194.0, 199.0, 204.0, 209.0, 213.0, 217.0, 221.0, 225.0], [-12.0, 33.0, 57.0, 77.0, 95.0, 110.0, 124.0, 137.0, 148.0, 159.0, 169.0, 179.0, 188.0, 196.0, 204.0, 212.0, 220.0, 227.0, 234.0, 240.0, 247.0, 253.0, 259.0, 264.0, 270.0, 275.0], [-18.0, 33.0, 61.0, 84.0, 104.0, 122.0, 138.0, 153.0, 166.0, 179.0, 191.0, 202.0, 213.0, 223.0, 233.0, 242.0, 251.0, 260.0, 268.0, 276.0, 284.0, 292.0, 299.0, 306.0, 313.0, 320.0], [-25.0, 32.0, 63.0, 88.0, 111.0, 131.0, 149.0, 166.0, 182.0, 196.0, 210.0, 223.0, 236.0, 248.0, 259.0, 270.0, 281.0, 291.0, 301.0, 311.0, 320.0, 329.0, 338.0, 347.0, 355.0, 363.0], [-33.0, 30.0, 63.0, 91.0, 116.0, 138.0, 158.0, 177.0, 194.0, 211.0, 226.0, 241.0, 255.0, 269.0, 282.0, 295.0, 307.0, 319.0, 330.0, 342.0, 352.0, 363.0, 373.0, 383.0, 393.0, 402.0], [-42.0, 27.0, 63.0, 93.0, 119.0, 143.0, 165.0, 186.0, 205.0, 223.0, 240.0, 256.0, 272.0, 287.0, 302.0, 316.0, 330.0, 343.0, 356.0, 369.0, 381.0, 393.0, 405.0, 416.0, 427.0, 438.0], [-52.0, 23.0, 62.0, 94.0, 122.0, 147.0, 171.0, 193.0, 214.0, 233.0, 252.0, 270.0, 287.0, 304.0, 320.0, 336.0, 351.0, 366.0, 380.0, 394.0, 408.0, 421.0, 434.0, 447.0, 459.0, 472.0], [-63.0, 18.0, 60.0, 94.0, 124.0, 151.0, 176.0, 199.0, 222.0, 243.0, 263.0, 283.0, 302.0, 320.0, 338.0, 355.0, 371.0, 388.0, 403.0, 419.0, 434.0, 449.0, 463.0, 477.0, 491.0, 505.0], [-75.0, 12.0, 58.0, 94.0, 125.0, 154.0, 180.0, 205.0, 229.0, 251.0, 273.0, 294.0, 315.0, 335.0, 354.0, 373.0, 391.0, 409.0, 426.0, 443.0, 460.0, 476.0, 492.0, 508.0, 523.0, 538.0], [-88.0, 6.0, 55.0, 93.0, 126.0, 156.0, 184.0, 211.0, 236.0, 260.0, 283.0, 305.0, 327.0, 349.0, 370.0, 390.0, 410.0, 430.0, 449.0, 467.0, 486.0, 504.0, 521.0, 539.0, 556.0, 572.0], [-102.0, -1.0, 52.0, 91.0, 126.0, 158.0, 188.0, 216.0, 242.0, 268.0, 292.0, 316.0, 339.0, 362.0, 384.0, 406.0, 427.0, 448.0, 469.0, 489.0, 509.0, 528.0, 548.0, 566.0, 585.0, 603.0], [-117.0, -9.0, 48.0, 89.0, 125.0, 159.0, 191.0, 220.0, 249.0, 276.0, 302.0, 327.0, 352.0, 376.0, 399.0, 422.0, 445.0, 467.0, 489.0, 511.0, 532.0, 553.0, 574.0, 594.0, 614.0, 634.0], [-133.0, -17.0, 44.0, 87.0, 125.0, 160.0, 193.0, 225.0, 255.0, 283.0, 311.0, 338.0, 364.0, 390.0, 415.0, 440.0, 464.0, 488.0, 511.0, 534.0, 557.0, 579.0, 601.0, 623.0, 645.0, 666.0], [-150.0, -26.0, 39.0, 85.0, 124.0, 161.0, 196.0, 229.0, 260.0, 291.0, 320.0, 349.0, 377.0, 404.0, 431.0, 457.0, 483.0, 508.0, 533.0, 558.0, 582.0, 606.0, 630.0, 653.0, 676.0, 699.0], [-168.0, -36.0, 35.0, 82.0, 123.0, 161.0, 198.0, 233.0, 266.0, 298.0, 329.0, 359.0, 389.0, 418.0, 446.0, 474.0, 501.0, 528.0, 554.0, 581.0, 606.0, 632.0, 657.0, 682.0, 707.0, 731.0], [-187.0, -46.0, 30.0, 80.0, 122.0, 162.0, 199.0, 236.0, 271.0, 305.0, 338.0, 370.0, 401.0, 432.0, 462.0, 491.0, 520.0, 549.0, 577.0, 605.0, 632.0, 659.0, 686.0, 712.0, 738.0, 764.0], [-207.0, -57.0, 25.0, 77.0, 121.0, 162.0, 201.0, 239.0, 275.0, 311.0, 345.0, 379.0, 412.0, 444.0, 476.0, 508.0, 538.0, 569.0, 599.0, 628.0, 657.0, 686.0, 714.0, 742.0, 770.0, 797.0], [-228.0, -68.0, 19.0, 74.0, 119.0, 162.0, 203.0, 242.0, 280.0, 317.0, 353.0, 388.0, 423.0, 457.0, 490.0, 523.0, 556.0, 588.0, 620.0, 651.0, 682.0, 713.0, 743.0, 773.0, 802.0, 832.0], [-250.0, -80.0, 14.0, 71.0, 118.0, 162.0, 204.0, 245.0, 284.0, 323.0, 360.0, 397.0, 434.0, 469.0, 505.0, 539.0, 574.0, 608.0, 641.0, 675.0, 707.0, 740.0, 772.0, 804.0, 835.0, 867.0], [-273.0, -93.0, 8.0, 68.0, 117.0, 162.0, 205.0, 248.0, 289.0, 329.0, 368.0, 407.0, 445.0, 482.0, 519.0, 555.0, 591.0, 627.0, 662.0, 697.0, 732.0, 766.0, 800.0, 834.0, 868.0, 901.0], [-297.0, -106.0, 2.0, 65.0, 115.0, 162.0, 207.0, 250.0, 293.0, 334.0, 375.0, 415.0, 455.0, 494.0, 533.0, 571.0, 609.0, 646.0, 684.0, 720.0, 757.0, 793.0, 829.0, 865.0, 900.0, 936.0], [-322.0, -120.0, -4.0, 61.0, 114.0, 163.0, 209.0, 253.0, 297.0, 340.0, 382.0, 424.0, 465.0, 506.0, 546.0, 586.0, 626.0, 665.0, 704.0, 743.0, 781.0, 819.0, 857.0, 895.0, 932.0, 970.0] ] 
# NOTE: Row 0 is header. Col 0 is header. Data starts at Row 1, Col 1.

MC_PAYOFFS = [ [None, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0], [0.0, 0.0, -1.0, -4.0, -9.0, -16.0, -25.0, -36.0, -49.0, -64.0, -81.0, -100.0, -121.0, -144.0, -169.0, -196.0, -225.0, -256.0, -289.0, -324.0, -361.0, -400.0, -441.0, -484.0, -529.0, -576.0], [1.0, 0.0, 19.0, 26.0, 30.0, 32.0, 32.0, 30.0, 26.0, 20.0, 12.0, 2.0, -10.0, -24.0, -40.0, -58.0, -78.0, -100.0, -124.0, -150.0, -178.0, -208.0, -240.0, -274.0, -310.0, -348.0], [2.0, 0.0, 29.0, 42.0, 50.0, 55.0, 58.0, 59.0, 58.0, 55.0, 50.0, 43.0, 34.0, 23.0, 10.0, -5.0, -22.0, -41.0, -62.0, -85.0, -110.0, -137.0, -166.0, -197.0, -230.0, -265.0], [3.0, 0.0, 38.0, 55.0, 66.0, 74.0, 79.0, 82.0, 83.0, 82.0, 79.0, 74.0, 67.0, 58.0, 47.0, 34.0, 19.0, 2.0, -17.0, -38.0, -61.0, -86.0, -113.0, -142.0, -173.0, -206.0], [4.0, 0.0, 45.0, 66.0, 82.0, 91.0, 98.0, 103.0, 106.0, 107.0, 106.0, 103.0, 98.0, 91.0, 82.0, 71.0, 58.0, 43.0, 26.0, 7.0, -14.0, -37.0, -62.0, -89.0, -118.0, -149.0], [5.0, 0.0, 51.0, 76.0, 95.0, 107.0, 116.0, 122.0, 126.0, 128.0, 128.0, 126.0, 122.0, 116.0, 108.0, 98.0, 86.0, 72.0, 56.0, 38.0, 18.0, -4.0, -28.0, -54.0, -82.0, -112.0], [6.0, 0.0, 57.0, 84.0, 107.0, 122.0, 133.0, 141.0, 146.0, 149.0, 150.0, 149.0, 146.0, 141.0, 134.0, 125.0, 114.0, 101.0, 86.0, 69.0, 50.0, 29.0, 6.0, -19.0, -46.0, -75.0], [7.0, 0.0, 62.0, 92.0, 117.0, 136.0, 149.0, 159.0, 166.0, 170.0, 172.0, 172.0, 170.0, 166.0, 160.0, 152.0, 142.0, 130.0, 116.0, 100.0, 82.0, 62.0, 40.0, 16.0, -10.0, -38.0], [8.0, 0.0, 66.0, 99.0, 126.0, 148.0, 164.0, 177.0, 186.0, 192.0, 196.0, 197.0, 196.0, 193.0, 188.0, 181.0, 172.0, 161.0, 148.0, 133.0, 116.0, 97.0, 76.0, 53.0, 28.0, 1.0], [9.0, 0.0, 70.0, 105.0, 135.0, 159.0, 179.0, 194.0, 205.0, 213.0, 218.0, 221.0, 221.0, 219.0, 215.0, 209.0, 201.0, 191.0, 179.0, 165.0, 149.0, 131.0, 111.0, 89.0, 65.0, 39.0], [10.0, 0.0, 74.0, 111.0, 143.0, 169.0, 191.0, 208.0, 222.0, 232.0, 239.0, 243.0, 245.0, 244.0, 241.0, 236.0, 229.0, 220.0, 209.0, 196.0, 181.0, 164.0, 145.0, 124.0, 101.0, 76.0], [11.0, 0.0, 77.0, 117.0, 151.0, 179.0, 202.0, 222.0, 237.0, 249.0, 258.0, 264.0, 267.0, 268.0, 266.0, 262.0, 256.0, 248.0, 238.0, 226.0, 212.0, 196.0, 178.0, 158.0, 136.0, 112.0], [12.0, 0.0, 80.0, 122.0, 158.0, 188.0, 213.0, 234.0, 251.0, 265.0, 275.0, 283.0, 288.0, 290.0, 290.0, 287.0, 282.0, 275.0, 266.0, 255.0, 242.0, 227.0, 210.0, 191.0, 170.0, 147.0], [13.0, 0.0, 83.0, 127.0, 165.0, 196.0, 223.0, 245.0, 264.0, 279.0, 291.0, 300.0, 307.0, 311.0, 312.0, 311.0, 307.0, 301.0, 293.0, 283.0, 271.0, 257.0, 241.0, 223.0, 203.0, 181.0], [14.0, 0.0, 86.0, 131.0, 171.0, 204.0, 232.0, 256.0, 276.0, 293.0, 306.0, 317.0, 325.0, 330.0, 333.0, 333.0, 331.0, 326.0, 319.0, 310.0, 299.0, 286.0, 271.0, 254.0, 235.0, 214.0], [15.0, 0.0, 88.0, 136.0, 177.0, 212.0, 242.0, 267.0, 288.0, 306.0, 321.0, 333.0, 342.0, 349.0, 353.0, 355.0, 354.0, 351.0, 345.0, 337.0, 327.0, 315.0, 301.0, 285.0, 267.0, 247.0], [16.0, 0.0, 91.0, 140.0, 183.0, 220.0, 251.0, 278.0, 301.0, 320.0, 336.0, 349.0, 359.0, 367.0, 372.0, 375.0, 376.0, 374.0, 370.0, 364.0, 355.0, 344.0, 331.0, 316.0, 299.0, 280.0], [17.0, 0.0, 93.0, 144.0, 189.0, 227.0, 260.0, 288.0, 312.0, 333.0, 350.0, 364.0, 376.0, 385.0, 391.0, 395.0, 397.0, 396.0, 393.0, 388.0, 381.0, 372.0, 360.0, 346.0, 330.0, 312.0], [18.0, 0.0, 95.0, 148.0, 194.0, 234.0, 268.0, 298.0, 323.0, 345.0, 364.0, 379.0, 392.0, 402.0, 410.0, 415.0, 418.0, 418.0, 416.0, 412.0, 406.0, 398.0, 388.0, 376.0, 361.0, 344.0], [19.0, 0.0, 97.0, 151.0, 199.0, 240.0, 276.0, 308.0, 335.0, 358.0, 378.0, 394.0, 408.0, 419.0, 428.0, 434.0, 438.0, 440.0, 439.0, 436.0, 431.0, 424.0, 415.0, 404.0, 391.0, 375.0], [20.0, 0.0, 99.0, 154.0, 204.0, 247.0, 284.0, 317.0, 346.0, 370.0, 391.0, 409.0, 424.0, 436.0, 446.0, 453.0, 458.0, 461.0, 461.0, 459.0, 455.0, 449.0, 441.0, 431.0, 419.0, 405.0], [21.0, 0.0, 100.0, 158.0, 209.0, 253.0, 292.0, 326.0, 356.0, 382.0, 404.0, 423.0, 439.0, 452.0, 463.0, 471.0, 477.0, 481.0, 482.0, 481.0, 478.0, 473.0, 466.0, 457.0, 446.0, 433.0], [22.0, 0.0, 102.0, 161.0, 213.0, 259.0, 299.0, 335.0, 366.0, 393.0, 417.0, 437.0, 454.0, 468.0, 480.0, 489.0, 496.0, 501.0, 503.0, 503.0, 501.0, 497.0, 491.0, 483.0, 473.0, 461.0], [23.0, 0.0, 103.0, 164.0, 217.0, 264.0, 306.0, 343.0, 376.0, 405.0, 430.0, 451.0, 469.0, 484.0, 497.0, 507.0, 515.0, 520.0, 523.0, 524.0, 523.0, 520.0, 515.0, 508.0, 499.0, 488.0], [24.0, 0.0, 105.0, 166.0, 221.0, 270.0, 313.0, 351.0, 385.0, 415.0, 441.0, 464.0, 483.0, 500.0, 513.0, 524.0, 533.0, 539.0, 543.0, 545.0, 545.0, 543.0, 538.0, 532.0, 524.0, 514.0], [25.0, 0.0, 106.0, 169.0, 225.0, 275.0, 320.0, 360.0, 395.0, 426.0, 453.0, 477.0, 497.0, 515.0, 529.0, 541.0, 551.0, 558.0, 563.0, 566.0, 567.0, 565.0, 562.0, 556.0, 548.0, 539.0] ]

# ============================================================
# GAME STATE
# ============================================================
game_state = {
    "round": 0,
    "max_rounds": 10,
    "am_strategy": "balanced",
    "mc_strategy": "balanced",
    "history": [],
    "am_total": 0,
    "mc_total": 0,
    "is_running": False,
}


# ============================================================
# AGENT INTERNAL STATE
# ============================================================
agent_state = {
    "AM": {
        "behavior_modifiers": {
            "aggression": 0,
            "cooperation_bias": 0,
            "trust_factor": 1.0,
            "investment_shift": 0,
        }
    },
    "MC": {
        "behavior_modifiers": {
            "aggression": 0,
            "cooperation_bias": 0,
            "trust_factor": 1.0,
            "investment_shift": 0,
        }
    },
}


# meta-learning
strategy_meta = {
    "AM": {
        "cooperative": 0.25,
        "competitive": 0.25,
        "adaptive": 0.25,
        "balanced": 0.25,
    },
    "MC": {
        "cooperative": 0.25,
        "competitive": 0.25,
        "adaptive": 0.25,
        "balanced": 0.25,
    },
}


# ============================================================
# UTILS
# ============================================================
def get_last_moves():
    if not game_state["history"]:
        return 12, 12
    r = game_state["history"][-1]
    return r["am_investment"], r["mc_investment"]


# ============================================================
# PAYOFF LOOKUP — 临时占位，不依赖矩阵
# ============================================================
def compute_payoff(am_inv, mc_inv):
    """
    暂时使用一个对称占位 payoff，
    你未来把矩阵填回去即可恢复真实逻辑。
    """
    return am_inv - mc_inv, mc_inv - am_inv


# ============================================================
# OPPONENT PATTERN ANALYSIS
# ============================================================
def analyze_pattern(history_list):
    if len(history_list) < 3:
        return "unknown"
    diffs = [history_list[i] - history_list[i - 1] for i in range(1, len(history_list))]
    avg = sum(diffs) / len(diffs)
    vol = sum(abs(x) for x in diffs) / len(diffs)

    if avg > 1.5:
        return "increasing"
    if avg < -1.5:
        return "decreasing"
    if vol > 4:
        return "unstable"
    return "flat"


# ============================================================
# META LEARNING STRATEGY UPDATE
# ============================================================
def update_strategy_meta(agent_role, pattern, payoff):
    meta = strategy_meta[agent_role]

    if pattern == "increasing":
        meta["cooperative"] += 0.08
        meta["adaptive"] += 0.02

    if pattern == "decreasing":
        meta["competitive"] += 0.08
        meta["balanced"] += 0.03

    if pattern == "unstable":
        meta["balanced"] += 0.1
        meta["competitive"] += 0.05

    if payoff > 0:
        best = max(meta, key=meta.get)
        meta[best] += 0.05

    # normalize
    total = sum(meta.values())
    for k in meta:
        meta[k] /= total


def select_strategy(agent_role):
    meta = strategy_meta[agent_role]
    return random.choices(list(meta.keys()), weights=list(meta.values()), k=1)[0]


# ============================================================
# STRATEGY-BASED DECISION
# ============================================================
def strategy_based_choice(strategy, round_num, my_last, opp_last):
    if strategy == "cooperative":
        return min(25, max(my_last, opp_last) + random.randint(1, 3))

    if strategy == "competitive":
        return random.randint(5, 10)

    if strategy == "adaptive":
        return 13 if round_num == 1 else opp_last

    if strategy == "balanced":
        return min(25, max(5, (my_last + opp_last) // 2 + random.randint(-2, 2)))

    return 12


# ============================================================
# LLM DECISION
# ============================================================
def llm_decide_investment(agent_role, opp_last, history):
    hist_text = "\n".join(
        [
            f"Round {h['round']}: AM={h['am_investment']} MC={h['mc_investment']} (payoffs {h['am_payoff']}/{h['mc_payoff']})"
            for h in history[-5:]
        ]
    ) or "No rounds yet."

    prompt = f"""
You are Agent {agent_role} in a repeated cooperation-competition game.

History:
{hist_text}

Opponent invested {opp_last} most recently.

Return ONLY one integer 0–25 as your next investment.
"""

    try:
        if not os.environ.get("OPENAI_API_KEY"):
            return None

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
        )
        s = res.choices[0].message.content.strip()
        num = int("".join([c for c in s if c.isdigit()]))
        return max(0, min(25, num))

    except:
        return None


# ============================================================
# FUTURE VALUE ESTIMATION
# ============================================================
def estimate_future_value(agent_role, invest, history):
    if not history:
        opp = 12
    else:
        last = history[-1]
        opp = last["mc_investment"] if agent_role == "AM" else last["am_investment"]

    fv = 0
    for t in range(1, 4):
        am_p, mc_p = compute_payoff(invest, opp)
        fv += (0.85 ** t) * (am_p if agent_role == "AM" else mc_p)
        opp = int((opp + invest) / 2)
    return fv


# ============================================================
# USER INSTRUCTION → BEHAVIOR MODIFIERS
# ============================================================
def interpret_user_instruction(msg):
    if not os.environ.get("OPENAI_API_KEY"):
        return {"aggression": 0, "cooperation_bias": 0, "trust_factor": 1.0, "investment_shift": 0}

    prompt = f"""
User message: "{msg}"

Convert into behavior modifiers (JSON only):
{{
  "aggression": int,
  "cooperation_bias": int,
  "trust_factor": float,
  "investment_shift": int
}}
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
        )
        return json.loads(res.choices[0].message.content)
    except:
        return {"aggression": 0, "cooperation_bias": 0, "trust_factor": 1.0, "investment_shift": 0}


# ============================================================
# FULL DECISION ENGINE
# ============================================================
def decide_investment(agent_role, strategy, round_num):
    last_am, last_mc = get_last_moves()
    my_last = last_am if agent_role == "AM" else last_mc
    opp_last = last_mc if agent_role == "AM" else last_am

    # 1) baseline strategy
    base = strategy_based_choice(strategy, round_num, my_last, opp_last)

    # 2) llm suggestion
    llm_suggest = llm_decide_investment(agent_role, opp_last, game_state["history"])

    # 3) future value comparison
    candidates = []

    fv_base = estimate_future_value(agent_role, base, game_state["history"])
    candidates.append((base, fv_base))

    if llm_suggest is not None:
        fv_llm = estimate_future_value(agent_role, llm_suggest, game_state["history"])
        candidates.append((llm_suggest, fv_llm))

    for d in [base - 2, base + 2]:
        if 0 <= d <= 25:
            fv = estimate_future_value(agent_role, d, game_state["history"])
            candidates.append((d, fv))

    best = max(candidates, key=lambda x: x[1])[0]

    # 4) apply behavior modifiers
    mods = agent_state[agent_role]["behavior_modifiers"]
    final = best
    final += mods["aggression"]
    final += mods["cooperation_bias"]
    final += mods["investment_shift"]
    final = int(final * mods["trust_factor"])
    final = max(0, min(25, final))

    return final


# ============================================================
# REASONING OUTPUT
# ============================================================
def generate_reasoning(agent_role, strategy, investment, opp_last):
    steps = []

    steps.append({"type": "observation", "text": f"Opponent invested {opp_last} last round."})
    steps.append({"type": "strategy", "text": f"My persona is {strategy}."})
    steps.append({"type": "decision", "text": f"I chose {investment} engineers."})

    return steps


# ============================================================
# ROUTES
# ============================================================
@app.route("/")
def home():
    return "Backend 8.0 Running", 200


@app.route("/start", methods=["POST"])
def start():
    game_state["round"] = 0
    game_state["history"] = []
    game_state["am_total"] = 0
    game_state["mc_total"] = 0
    game_state["is_running"] = True
    return jsonify({"status": "started"})


@app.route("/continue_simulation", methods=["POST"])
def continue_simulation():
    if not game_state["is_running"] or game_state["round"] >= game_state["max_rounds"]:
        return jsonify({"game_complete": True})

    game_state["round"] += 1
    r = game_state["round"]

    # Auto-select strategies by meta-learning
    game_state["am_strategy"] = select_strategy("AM")
    game_state["mc_strategy"] = select_strategy("MC")

    s_am = game_state["am_strategy"]
    s_mc = game_state["mc_strategy"]

    inv_am = decide_investment("AM", s_am, r)
    inv_mc = decide_investment("MC", s_mc, r)

    pay_am, pay_mc = compute_payoff(inv_am, inv_mc)

    # meta-learning update
    last_am, last_mc = get_last_moves()
    pattern_am = analyze_pattern([h["mc_investment"] for h in game_state["history"]])
    pattern_mc = analyze_pattern([h["am_investment"] for h in game_state["history"]])

    update_strategy_meta("AM", pattern_am, pay_am)
    update_strategy_meta("MC", pattern_mc, pay_mc)

    # append history
    entry = {
        "round": r,
        "am_investment": inv_am,
        "mc_investment": inv_mc,
        "am_payoff": pay_am,
        "mc_payoff": pay_mc,
    }
    game_state["history"].append(entry)

    game_state["am_total"] += pay_am
    game_state["mc_total"] += pay_mc

    reasoning_am = generate_reasoning("AM", s_am, inv_am, last_mc)
    reasoning_mc = generate_reasoning("MC", s_mc, inv_mc, last_am)

    return jsonify(
        {
            "round": r,
            "am_investment": inv_am,
            "mc_investment": inv_mc,
            "am_payoff": pay_am,
            "mc_payoff": pay_mc,
            "am_total": game_state["am_total"],
            "mc_total": game_state["mc_total"],
            "history": game_state["history"],
            "am_reasoning": reasoning_am,
            "mc_reasoning": reasoning_mc,
            "game_complete": (r >= game_state["max_rounds"]),
        }
    )


@app.route("/chat_with_agent", methods=["POST"])
def chat_with_agent():
    data = request.json or {}
    agent = data.get("agent", "").upper()
    message = data.get("message", "")

    if agent not in ("AM", "MC"):
        return jsonify({"reply": "Invalid agent."})

    # apply behavior modifiers
    mods = interpret_user_instruction(message)
    for k, v in mods.items():
        agent_state[agent]["behavior_modifiers"][k] = v

    # build context
    last = game_state["history"][-1] if game_state["history"] else {}
    strategy = game_state["am_strategy"] if agent == "AM" else game_state["mc_strategy"]

    sys_prompt = f"""
You are agent {agent} with persona {strategy}.
Respond in one concise sentence.
"""

    if os.environ.get("OPENAI_API_KEY"):
        try:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": message},
                ],
            )
            reply = res.choices[0].message.content
        except:
            reply = "I acknowledge your message."
    else:
        reply = "I acknowledge your message."

    return jsonify({"reply": reply})


# ============================================================
# END
# ============================================================

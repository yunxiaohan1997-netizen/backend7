# ============================================================
#  CLEAN BACKEND — 4 STRATEGIES + LLM + COMPLEX REASONING + PERSONA
#  Compatible with OLD front-end endpoints:
#    /start_simulation
#    /continue_simulation
#    /chat_with_agent
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import random

app = Flask(__name__)
CORS(app)

client = OpenAI()

# ============================================================
# GLOBALS
# ============================================================

MAX_ROUNDS = 10

# payoff matrices (占位)
AM_PAYOFFS = [ [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [-1.0, 19.0, 29.0, 38.0, 45.0, 51.0, 57.0, 62.0, 66.0, 70.0, 74.0, 77.0, 80.0, 83.0, 86.0, 88.0, 91.0, 93.0, 95.0, 97.0, 99.0, 100.0, 102.0, 103.0, 105.0, 106.0], [-3.0, 27.0, 42.0, 55.0, 66.0, 76.0, 84.0, 92.0, 99.0, 105.0, 111.0, 117.0, 122.0, 127.0, 131.0, 136.0, 140.0, 144.0, 148.0, 151.0, 154.0, 158.0, 161.0, 164.0, 166.0, 169.0], [-7.0, 31.0, 51.0, 68.0, 82.0, 95.0, 107.0, 117.0, 126.0, 135.0, 143.0, 151.0, 158.0, 165.0, 171.0, 177.0, 183.0, 189.0, 194.0, 199.0, 204.0, 209.0, 213.0, 217.0, 221.0, 225.0], [-12.0, 33.0, 57.0, 77.0, 95.0, 110.0, 124.0, 137.0, 148.0, 159.0, 169.0, 179.0, 188.0, 196.0, 204.0, 212.0, 220.0, 227.0, 234.0, 240.0, 247.0, 253.0, 259.0, 264.0, 270.0, 275.0], [-18.0, 33.0, 61.0, 84.0, 104.0, 122.0, 138.0, 153.0, 166.0, 179.0, 191.0, 202.0, 213.0, 223.0, 233.0, 242.0, 251.0, 260.0, 268.0, 276.0, 284.0, 292.0, 299.0, 306.0, 313.0, 320.0], [-25.0, 32.0, 63.0, 88.0, 111.0, 131.0, 149.0, 166.0, 182.0, 196.0, 210.0, 223.0, 236.0, 248.0, 259.0, 270.0, 281.0, 291.0, 301.0, 311.0, 320.0, 329.0, 338.0, 347.0, 355.0, 363.0], [-33.0, 30.0, 63.0, 91.0, 116.0, 138.0, 158.0, 177.0, 194.0, 211.0, 226.0, 241.0, 255.0, 269.0, 282.0, 295.0, 307.0, 319.0, 330.0, 342.0, 352.0, 363.0, 373.0, 383.0, 393.0, 402.0], [-42.0, 27.0, 63.0, 93.0, 119.0, 143.0, 165.0, 186.0, 205.0, 223.0, 240.0, 256.0, 272.0, 287.0, 302.0, 316.0, 330.0, 343.0, 356.0, 369.0, 381.0, 393.0, 405.0, 416.0, 427.0, 438.0], [-52.0, 23.0, 62.0, 94.0, 122.0, 147.0, 171.0, 193.0, 214.0, 233.0, 252.0, 270.0, 287.0, 304.0, 320.0, 336.0, 351.0, 366.0, 380.0, 394.0, 408.0, 421.0, 434.0, 447.0, 459.0, 472.0], [-63.0, 18.0, 60.0, 94.0, 124.0, 151.0, 176.0, 199.0, 222.0, 243.0, 263.0, 283.0, 302.0, 320.0, 338.0, 355.0, 371.0, 388.0, 403.0, 419.0, 434.0, 449.0, 463.0, 477.0, 491.0, 505.0], [-75.0, 12.0, 58.0, 94.0, 125.0, 154.0, 180.0, 205.0, 229.0, 251.0, 273.0, 294.0, 315.0, 335.0, 354.0, 373.0, 391.0, 409.0, 426.0, 443.0, 460.0, 476.0, 492.0, 508.0, 523.0, 538.0], [-88.0, 6.0, 55.0, 93.0, 126.0, 156.0, 184.0, 211.0, 236.0, 260.0, 283.0, 305.0, 327.0, 349.0, 370.0, 390.0, 410.0, 430.0, 449.0, 467.0, 486.0, 504.0, 521.0, 539.0, 556.0, 572.0], [-102.0, -1.0, 52.0, 91.0, 126.0, 158.0, 188.0, 216.0, 242.0, 268.0, 292.0, 316.0, 339.0, 362.0, 384.0, 406.0, 427.0, 448.0, 469.0, 489.0, 509.0, 528.0, 548.0, 566.0, 585.0, 603.0], [-117.0, -9.0, 48.0, 89.0, 125.0, 159.0, 191.0, 220.0, 249.0, 276.0, 302.0, 327.0, 352.0, 376.0, 399.0, 422.0, 445.0, 467.0, 489.0, 511.0, 532.0, 553.0, 574.0, 594.0, 614.0, 634.0], [-133.0, -17.0, 44.0, 87.0, 125.0, 160.0, 193.0, 225.0, 255.0, 283.0, 311.0, 338.0, 364.0, 390.0, 415.0, 440.0, 464.0, 488.0, 511.0, 534.0, 557.0, 579.0, 601.0, 623.0, 645.0, 666.0], [-150.0, -26.0, 39.0, 85.0, 124.0, 161.0, 196.0, 229.0, 260.0, 291.0, 320.0, 349.0, 377.0, 404.0, 431.0, 457.0, 483.0, 508.0, 533.0, 558.0, 582.0, 606.0, 630.0, 653.0, 676.0, 699.0], [-168.0, -36.0, 35.0, 82.0, 123.0, 161.0, 198.0, 233.0, 266.0, 298.0, 329.0, 359.0, 389.0, 418.0, 446.0, 474.0, 501.0, 528.0, 554.0, 581.0, 606.0, 632.0, 657.0, 682.0, 707.0, 731.0], [-187.0, -46.0, 30.0, 80.0, 122.0, 162.0, 199.0, 236.0, 271.0, 305.0, 338.0, 370.0, 401.0, 432.0, 462.0, 491.0, 520.0, 549.0, 577.0, 605.0, 632.0, 659.0, 686.0, 712.0, 738.0, 764.0], [-207.0, -57.0, 25.0, 77.0, 121.0, 162.0, 201.0, 239.0, 275.0, 311.0, 345.0, 379.0, 412.0, 444.0, 476.0, 508.0, 538.0, 569.0, 599.0, 628.0, 657.0, 686.0, 714.0, 742.0, 770.0, 797.0], [-228.0, -68.0, 19.0, 74.0, 119.0, 162.0, 203.0, 242.0, 280.0, 317.0, 353.0, 388.0, 423.0, 457.0, 490.0, 523.0, 556.0, 588.0, 620.0, 651.0, 682.0, 713.0, 743.0, 773.0, 802.0, 832.0], [-250.0, -80.0, 14.0, 71.0, 118.0, 162.0, 204.0, 245.0, 284.0, 323.0, 360.0, 397.0, 434.0, 469.0, 505.0, 539.0, 574.0, 608.0, 641.0, 675.0, 707.0, 740.0, 772.0, 804.0, 835.0, 867.0], [-273.0, -93.0, 8.0, 68.0, 117.0, 162.0, 205.0, 248.0, 289.0, 329.0, 368.0, 407.0, 445.0, 482.0, 519.0, 555.0, 591.0, 627.0, 662.0, 697.0, 732.0, 766.0, 800.0, 834.0, 868.0, 901.0], [-297.0, -106.0, 2.0, 65.0, 115.0, 162.0, 207.0, 250.0, 293.0, 334.0, 375.0, 415.0, 455.0, 494.0, 533.0, 571.0, 609.0, 646.0, 684.0, 720.0, 757.0, 793.0, 829.0, 865.0, 900.0, 936.0], [-322.0, -120.0, -4.0, 61.0, 114.0, 163.0, 209.0, 253.0, 297.0, 340.0, 382.0, 424.0, 465.0, 506.0, 546.0, 586.0, 626.0, 665.0, 704.0, 743.0, 781.0, 819.0, 857.0, 895.0, 932.0, 970.0] ] 
# NOTE: Row 0 is header. Col 0 is header. Data starts at Row 1, Col 1.

MC_PAYOFFS = [ [None, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0], [0.0, 0.0, -1.0, -4.0, -9.0, -16.0, -25.0, -36.0, -49.0, -64.0, -81.0, -100.0, -121.0, -144.0, -169.0, -196.0, -225.0, -256.0, -289.0, -324.0, -361.0, -400.0, -441.0, -484.0, -529.0, -576.0], [1.0, 0.0, 19.0, 26.0, 30.0, 32.0, 32.0, 30.0, 26.0, 20.0, 12.0, 2.0, -10.0, -24.0, -40.0, -58.0, -78.0, -100.0, -124.0, -150.0, -178.0, -208.0, -240.0, -274.0, -310.0, -348.0], [2.0, 0.0, 29.0, 42.0, 50.0, 55.0, 58.0, 59.0, 58.0, 55.0, 50.0, 43.0, 34.0, 23.0, 10.0, -5.0, -22.0, -41.0, -62.0, -85.0, -110.0, -137.0, -166.0, -197.0, -230.0, -265.0], [3.0, 0.0, 38.0, 55.0, 66.0, 74.0, 79.0, 82.0, 83.0, 82.0, 79.0, 74.0, 67.0, 58.0, 47.0, 34.0, 19.0, 2.0, -17.0, -38.0, -61.0, -86.0, -113.0, -142.0, -173.0, -206.0], [4.0, 0.0, 45.0, 66.0, 82.0, 91.0, 98.0, 103.0, 106.0, 107.0, 106.0, 103.0, 98.0, 91.0, 82.0, 71.0, 58.0, 43.0, 26.0, 7.0, -14.0, -37.0, -62.0, -89.0, -118.0, -149.0], [5.0, 0.0, 51.0, 76.0, 95.0, 107.0, 116.0, 122.0, 126.0, 128.0, 128.0, 126.0, 122.0, 116.0, 108.0, 98.0, 86.0, 72.0, 56.0, 38.0, 18.0, -4.0, -28.0, -54.0, -82.0, -112.0], [6.0, 0.0, 57.0, 84.0, 107.0, 122.0, 133.0, 141.0, 146.0, 149.0, 150.0, 149.0, 146.0, 141.0, 134.0, 125.0, 114.0, 101.0, 86.0, 69.0, 50.0, 29.0, 6.0, -19.0, -46.0, -75.0], [7.0, 0.0, 62.0, 92.0, 117.0, 136.0, 149.0, 159.0, 166.0, 170.0, 172.0, 172.0, 170.0, 166.0, 160.0, 152.0, 142.0, 130.0, 116.0, 100.0, 82.0, 62.0, 40.0, 16.0, -10.0, -38.0], [8.0, 0.0, 66.0, 99.0, 126.0, 148.0, 164.0, 177.0, 186.0, 192.0, 196.0, 197.0, 196.0, 193.0, 188.0, 181.0, 172.0, 161.0, 148.0, 133.0, 116.0, 97.0, 76.0, 53.0, 28.0, 1.0], [9.0, 0.0, 70.0, 105.0, 135.0, 159.0, 179.0, 194.0, 205.0, 213.0, 218.0, 221.0, 221.0, 219.0, 215.0, 209.0, 201.0, 191.0, 179.0, 165.0, 149.0, 131.0, 111.0, 89.0, 65.0, 39.0], [10.0, 0.0, 74.0, 111.0, 143.0, 169.0, 191.0, 208.0, 222.0, 232.0, 239.0, 243.0, 245.0, 244.0, 241.0, 236.0, 229.0, 220.0, 209.0, 196.0, 181.0, 164.0, 145.0, 124.0, 101.0, 76.0], [11.0, 0.0, 77.0, 117.0, 151.0, 179.0, 202.0, 222.0, 237.0, 249.0, 258.0, 264.0, 267.0, 268.0, 266.0, 262.0, 256.0, 248.0, 238.0, 226.0, 212.0, 196.0, 178.0, 158.0, 136.0, 112.0], [12.0, 0.0, 80.0, 122.0, 158.0, 188.0, 213.0, 234.0, 251.0, 265.0, 275.0, 283.0, 288.0, 290.0, 290.0, 287.0, 282.0, 275.0, 266.0, 255.0, 242.0, 227.0, 210.0, 191.0, 170.0, 147.0], [13.0, 0.0, 83.0, 127.0, 165.0, 196.0, 223.0, 245.0, 264.0, 279.0, 291.0, 300.0, 307.0, 311.0, 312.0, 311.0, 307.0, 301.0, 293.0, 283.0, 271.0, 257.0, 241.0, 223.0, 203.0, 181.0], [14.0, 0.0, 86.0, 131.0, 171.0, 204.0, 232.0, 256.0, 276.0, 293.0, 306.0, 317.0, 325.0, 330.0, 333.0, 333.0, 331.0, 326.0, 319.0, 310.0, 299.0, 286.0, 271.0, 254.0, 235.0, 214.0], [15.0, 0.0, 88.0, 136.0, 177.0, 212.0, 242.0, 267.0, 288.0, 306.0, 321.0, 333.0, 342.0, 349.0, 353.0, 355.0, 354.0, 351.0, 345.0, 337.0, 327.0, 315.0, 301.0, 285.0, 267.0, 247.0], [16.0, 0.0, 91.0, 140.0, 183.0, 220.0, 251.0, 278.0, 301.0, 320.0, 336.0, 349.0, 359.0, 367.0, 372.0, 375.0, 376.0, 374.0, 370.0, 364.0, 355.0, 344.0, 331.0, 316.0, 299.0, 280.0], [17.0, 0.0, 93.0, 144.0, 189.0, 227.0, 260.0, 288.0, 312.0, 333.0, 350.0, 364.0, 376.0, 385.0, 391.0, 395.0, 397.0, 396.0, 393.0, 388.0, 381.0, 372.0, 360.0, 346.0, 330.0, 312.0], [18.0, 0.0, 95.0, 148.0, 194.0, 234.0, 268.0, 298.0, 323.0, 345.0, 364.0, 379.0, 392.0, 402.0, 410.0, 415.0, 418.0, 418.0, 416.0, 412.0, 406.0, 398.0, 388.0, 376.0, 361.0, 344.0], [19.0, 0.0, 97.0, 151.0, 199.0, 240.0, 276.0, 308.0, 335.0, 358.0, 378.0, 394.0, 408.0, 419.0, 428.0, 434.0, 438.0, 440.0, 439.0, 436.0, 431.0, 424.0, 415.0, 404.0, 391.0, 375.0], [20.0, 0.0, 99.0, 154.0, 204.0, 247.0, 284.0, 317.0, 346.0, 370.0, 391.0, 409.0, 424.0, 436.0, 446.0, 453.0, 458.0, 461.0, 461.0, 459.0, 455.0, 449.0, 441.0, 431.0, 419.0, 405.0], [21.0, 0.0, 100.0, 158.0, 209.0, 253.0, 292.0, 326.0, 356.0, 382.0, 404.0, 423.0, 439.0, 452.0, 463.0, 471.0, 477.0, 481.0, 482.0, 481.0, 478.0, 473.0, 466.0, 457.0, 446.0, 433.0], [22.0, 0.0, 102.0, 161.0, 213.0, 259.0, 299.0, 335.0, 366.0, 393.0, 417.0, 437.0, 454.0, 468.0, 480.0, 489.0, 496.0, 501.0, 503.0, 503.0, 501.0, 497.0, 491.0, 483.0, 473.0, 461.0], [23.0, 0.0, 103.0, 164.0, 217.0, 264.0, 306.0, 343.0, 376.0, 405.0, 430.0, 451.0, 469.0, 484.0, 497.0, 507.0, 515.0, 520.0, 523.0, 524.0, 523.0, 520.0, 515.0, 508.0, 499.0, 488.0], [24.0, 0.0, 105.0, 166.0, 221.0, 270.0, 313.0, 351.0, 385.0, 415.0, 441.0, 464.0, 483.0, 500.0, 513.0, 524.0, 533.0, 539.0, 543.0, 545.0, 545.0, 543.0, 538.0, 532.0, 524.0, 514.0], [25.0, 0.0, 106.0, 169.0, 225.0, 275.0, 320.0, 360.0, 395.0, 426.0, 453.0, 477.0, 497.0, 515.0, 529.0, 541.0, 551.0, 558.0, 563.0, 566.0, 567.0, 565.0, 562.0, 556.0, 548.0, 539.0] ]

# player states
game_state = {
    "round": 0,
    "history": [],
    "am_total": 0,
    "mc_total": 0,
    "last_am": None,
    "last_mc": None,
}

# === PERSONA & STRATEGY 配置 =================================

# 每种 strategy 对应一个 persona + 风格标签
PERSONA_PROFILES = {
    "cooperative": {
        "name": "Visionary Builder",
        "style": "long-term partnership, high trust, willing to invest ahead",
    },
    "competitive": {
        "name": "Hard-nosed Fighter",
        "style": "short-term payoff, defensive, protects downside first",
    },
    "balanced": {
        "name": "Pragmatic Optimizer",
        "style": "weighs both upside and risk, stays in the middle lane",
    },
    "adaptive": {
        "name": "Opportunistic Learner",
        "style": "reads opponent signals and tweaks investment dynamically",
    },
}


# ============================================================
# PAYOFF FALLBACK
# ============================================================

def compute_payoff(am_inv, mc_inv):
    """
    If AM_PAYOFFS/MC_PAYOFFS are empty, fallback to a simple payoff.
    """
    if AM_PAYOFFS and MC_PAYOFFS:
        try:
            return AM_PAYOFFS[am_inv][mc_inv], MC_PAYOFFS[am_inv][mc_inv]
        except:
            pass
    # fallback: 简单差额结构
    return (am_inv - mc_inv, mc_inv - am_inv)


# ============================================================
# STRATEGIES
# ============================================================

def cooperative_strategy(state):
    """More likely to invest higher."""
    base = 18 + random.randint(-2, 2)
    return max(0, min(25, base))

def competitive_strategy(state):
    """More likely to invest minimal."""
    base = 3 + random.randint(-1, 1)
    return max(0, min(25, base))

def balanced_strategy(state):
    """Middle point."""
    base = 12 + random.randint(-3, 3)
    return max(0, min(25, base))

def adaptive_strategy(state):
    """
    If AM was losing last round, invest more.
    If winning, invest less.
    """
    last_am = state["last_am"]
    last_mc = state["last_mc"]
    if last_am is None or last_mc is None:
        return balanced_strategy(state)

    # 简单：如果当前累计 am_total < mc_total，偏向加码
    if state["am_total"] < state["mc_total"]:
        base = last_am + 3
    else:
        base = last_am - 2

    return max(0, min(25, base + random.randint(-1, 1)))


# ============================================================
# STRATEGY WRAPPER
# ============================================================

def strategy_pick(strategy_name, state):
    if strategy_name == "cooperative":
        return cooperative_strategy(state)
    elif strategy_name == "competitive":
        return competitive_strategy(state)
    elif strategy_name == "balanced":
        return balanced_strategy(state)
    elif strategy_name == "adaptive":
        return adaptive_strategy(state)
    else:
        return balanced_strategy(state)


# ============================================================
# LLM DECISION (GPT-4o-mini)
# ============================================================

def llm_decide_investment(state):
    """
    Produces an investment guess (0–25).
    """
    if not game_state["history"]:
        history_text = "(no previous rounds)"
    else:
        history_text = "\n".join(
            [
                f"Round {i+1}: AM={h['am']}, MC={h['mc']}, AM_pay={h['am_pay']}, MC_pay={h['mc_pay']}"
                for i, h in enumerate(state["history"])
            ]
        )

    prompt = f"""
You are the AM agent in a repeated investment game.
Each round both sides choose an investment between 0 and 25.
Higher investment can help long-term competitiveness but also costs more.
The opponent is 'MC'.

History so far:
{history_text}

Now we are entering round {state["round"]+1}.
Given this context, choose ONE integer between 0 and 25 as your next AM investment.
Return ONLY the number, no explanation.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        content = resp.choices[0].message.content.strip()
        digits = "".join([c for c in content if c.isdigit()])
        val = int(digits) if digits else 12
        return max(0, min(25, val))
    except Exception:
        # fallback
        return balanced_strategy(state)


# ============================================================
# COMPLEX REASONING + PERSONA
# ============================================================

def generate_reasoning(am_choice, strategy_name, llm_used, state):
    """
    更复杂的推理链 + persona 风格。
    输出为 list[str]，兼容现有前端。
    """
    persona_info = PERSONA_PROFILES.get(strategy_name, PERSONA_PROFILES["balanced"])
    persona_name = persona_info["name"]
    persona_style = persona_info["style"]

    round_idx = state["round"] + 1
    am_total = state["am_total"]
    mc_total = state["mc_total"]
    last_am = state["last_am"]
    last_mc = state["last_mc"]

    if last_am is None or last_mc is None:
        last_am_str = "no previous AM move"
        last_mc_str = "no previous MC move"
    else:
        last_am_str = str(last_am)
        last_mc_str = str(last_mc)

    lead_status = "behind"
    if am_total > mc_total:
        lead_status = "ahead"
    elif am_total == mc_total:
        lead_status = "tied"

    steps = []

    # 1. 角色自我定位
    steps.append(
        f"1. As **{persona_name}**, I lean into a {persona_style} approach."
    )

    # 2. 局势盘点
    steps.append(
        f"2. We are entering **round {round_idx}**, with cumulative payoff AM={am_total}, MC={mc_total} — AM is currently **{lead_status}**."
    )

    # 3. 回顾上一轮
    steps.append(
        f"3. In the previous round, AM invested **{last_am_str}**, MC invested **{last_mc_str}**, which shapes my sense of how aggressive MC is."
    )

    # 4. 解析当前 strategy
    if strategy_name == "cooperative":
        steps.append(
            "4. Under the *cooperative* strategy, I am willing to invest more now to build future advantage, assuming MC will not fully exploit me."
        )
    elif strategy_name == "competitive":
        steps.append(
            "4. Under the *competitive* strategy, I prioritize protecting my downside and will keep my investment relatively lean unless forced to respond."
        )
    elif strategy_name == "balanced":
        steps.append(
            "4. Under the *balanced* strategy, I try to stay near the middle, adjusting slightly up or down based on the score and MC's last move."
        )
    else:  # adaptive
        steps.append(
            "4. Under the *adaptive* strategy, I read both the score gap and MC's last decision, adjusting my level dynamically."
        )

    # 5. 引入 LLM 建议
    steps.append(
        f"5. I asked an internal 'advisor' model for a suggestion; it proposed an investment of **{llm_used}**."
    )

    # 6. 内部权衡
    steps.append(
        f"6. I combine my persona's bias with the model's suggestion, weighing how far I can push investment without over-committing in this round."
    )

    # 7. 对对手行为的预判
    steps.append(
        "7. I also anticipate that MC may slightly adjust around its recent behavior rather than making a radical jump."
    )

    # 8. 最终决策
    steps.append(
        f"8. Putting all this together, my final decision for this round is to invest **{am_choice}** engineers."
    )

    return steps


# ============================================================
# ONE-ROUND DECISION
# ============================================================

def decide_am_investment(state, strategy_name):
    # strategy suggestion
    strat_choice = strategy_pick(strategy_name, state)
    # llm suggestion
    llm_choice = llm_decide_investment(state)

    # 简单线性融合（你之后可以改更复杂的权重机制）
    final = round((strat_choice * 0.6) + (llm_choice * 0.4))
    final = max(0, min(25, final))

    reasoning = generate_reasoning(final, strategy_name, llm_choice, state)
    return final, reasoning


def decide_mc_investment(state):
    # MC 简单 policy：12 左右波动
    base = 12 + random.randint(-4, 4)
    return max(0, min(25, base))


# ============================================================
# ENDPOINTS
# ============================================================

@app.route("/start_simulation", methods=["POST"])
def start_sim():
    global game_state
    game_state = {
        "round": 0,
        "history": [],
        "am_total": 0,
        "mc_total": 0,
        "last_am": None,
        "last_mc": None,
    }
    return jsonify({"message": "Simulation started", "round": 0})


@app.route("/continue_simulation", methods=["POST"])
def continue_sim():
    global game_state

    if game_state["round"] >= MAX_ROUNDS:
        return jsonify({"finished": True, "history": game_state["history"]})

    data = request.json or {}
    strategy_name = data.get("strategy", "balanced")

    am_inv, reasoning = decide_am_investment(game_state, strategy_name)
    mc_inv = decide_mc_investment(game_state)

    am_pay, mc_pay = compute_payoff(am_inv, mc_inv)

    game_state["am_total"] += am_pay
    game_state["mc_total"] += mc_pay
    game_state["last_am"] = am_inv
    game_state["last_mc"] = mc_inv

    game_state["history"].append({
        "round": game_state["round"] + 1,
        "am": am_inv,
        "mc": mc_inv,
        "am_pay": am_pay,
        "mc_pay": mc_pay,
        "am_reasoning": reasoning,  # list[str] with persona reasoning
    })

    game_state["round"] += 1

    return jsonify({
        "finished": game_state["round"] >= MAX_ROUNDS,
        "round": game_state["round"],
        "history": game_state["history"],
        "am_total": game_state["am_total"],
        "mc_total": game_state["mc_total"]
    })


@app.route("/chat_with_agent", methods=["POST"])
def chat_with_agent():
    data = request.json or {}
    user_msg = data.get("message", "")

    # 根据当前 strategy 输出对应 persona 语气
    if game_state["history"]:
        last_round = game_state["history"][-1]
        # 简单：从最后一次的 reasoning 不能直接反推策略，就假定 balanced
        current_strategy = "balanced"
    else:
        current_strategy = "balanced"

    persona_info = PERSONA_PROFILES.get(current_strategy, PERSONA_PROFILES["balanced"])
    persona_name = persona_info["name"]

    prompt = f"""
You are the AM agent in a repeated investment game.
Your persona is **{persona_name}**.
User says: {user_msg}

Reply in 1–2 sentences, staying in character as {persona_name}.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = resp.choices[0].message.content
    except Exception:
        reply = f"As {persona_name}, I hear you. Let's see how the next round plays out."

    return jsonify({"reply": reply})


# ============================================================
# RUN
# ============================================================

@app.route("/")
def home():
    return "Backend with persona reasoning running."

# ============================================================
# END
# ============================================================

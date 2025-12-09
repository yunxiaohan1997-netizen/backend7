#!/usr/bin/env python3
"""
Backend 7.0 — Reasoning + Persona + True Payoff Edition
Author: ChatGPT
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, random, math
from datetime import datetime
from openai import OpenAI

# --------------------------
# OpenAI Client
# --------------------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# --------------------------
# Flask App Init
# --------------------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})
app.config['SECRET_KEY'] = 'insead-game-simulation-final-8'

# --------------------------
# Health Route
# --------------------------
@app.route("/")
def home():
    return "Backend 8.0 Running", 200


# ----------------------------------------------------------------------
# REAL PAYOFF MATRIX (Your original 11.29 Excel data — unchanged)
# ----------------------------------------------------------------------
# NOTE: I keep exactly your matrices — no modifications.
# ----------------------------------------------------------------------

AM_PAYOFFS = [ [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [-1.0, 19.0, 29.0, 38.0, 45.0, 51.0, 57.0, 62.0, 66.0, 70.0, 74.0, 77.0, 80.0, 83.0, 86.0, 88.0, 91.0, 93.0, 95.0, 97.0, 99.0, 100.0, 102.0, 103.0, 105.0, 106.0], [-3.0, 27.0, 42.0, 55.0, 66.0, 76.0, 84.0, 92.0, 99.0, 105.0, 111.0, 117.0, 122.0, 127.0, 131.0, 136.0, 140.0, 144.0, 148.0, 151.0, 154.0, 158.0, 161.0, 164.0, 166.0, 169.0], [-7.0, 31.0, 51.0, 68.0, 82.0, 95.0, 107.0, 117.0, 126.0, 135.0, 143.0, 151.0, 158.0, 165.0, 171.0, 177.0, 183.0, 189.0, 194.0, 199.0, 204.0, 209.0, 213.0, 217.0, 221.0, 225.0], [-12.0, 33.0, 57.0, 77.0, 95.0, 110.0, 124.0, 137.0, 148.0, 159.0, 169.0, 179.0, 188.0, 196.0, 204.0, 212.0, 220.0, 227.0, 234.0, 240.0, 247.0, 253.0, 259.0, 264.0, 270.0, 275.0], [-18.0, 33.0, 61.0, 84.0, 104.0, 122.0, 138.0, 153.0, 166.0, 179.0, 191.0, 202.0, 213.0, 223.0, 233.0, 242.0, 251.0, 260.0, 268.0, 276.0, 284.0, 292.0, 299.0, 306.0, 313.0, 320.0], [-25.0, 32.0, 63.0, 88.0, 111.0, 131.0, 149.0, 166.0, 182.0, 196.0, 210.0, 223.0, 236.0, 248.0, 259.0, 270.0, 281.0, 291.0, 301.0, 311.0, 320.0, 329.0, 338.0, 347.0, 355.0, 363.0], [-33.0, 30.0, 63.0, 91.0, 116.0, 138.0, 158.0, 177.0, 194.0, 211.0, 226.0, 241.0, 255.0, 269.0, 282.0, 295.0, 307.0, 319.0, 330.0, 342.0, 352.0, 363.0, 373.0, 383.0, 393.0, 402.0], [-42.0, 27.0, 63.0, 93.0, 119.0, 143.0, 165.0, 186.0, 205.0, 223.0, 240.0, 256.0, 272.0, 287.0, 302.0, 316.0, 330.0, 343.0, 356.0, 369.0, 381.0, 393.0, 405.0, 416.0, 427.0, 438.0], [-52.0, 23.0, 62.0, 94.0, 122.0, 147.0, 171.0, 193.0, 214.0, 233.0, 252.0, 270.0, 287.0, 304.0, 320.0, 336.0, 351.0, 366.0, 380.0, 394.0, 408.0, 421.0, 434.0, 447.0, 459.0, 472.0], [-63.0, 18.0, 60.0, 94.0, 124.0, 151.0, 176.0, 199.0, 222.0, 243.0, 263.0, 283.0, 302.0, 320.0, 338.0, 355.0, 371.0, 388.0, 403.0, 419.0, 434.0, 449.0, 463.0, 477.0, 491.0, 505.0], [-75.0, 12.0, 58.0, 94.0, 125.0, 154.0, 180.0, 205.0, 229.0, 251.0, 273.0, 294.0, 315.0, 335.0, 354.0, 373.0, 391.0, 409.0, 426.0, 443.0, 460.0, 476.0, 492.0, 508.0, 523.0, 538.0], [-88.0, 6.0, 55.0, 93.0, 126.0, 156.0, 184.0, 211.0, 236.0, 260.0, 283.0, 305.0, 327.0, 349.0, 370.0, 390.0, 410.0, 430.0, 449.0, 467.0, 486.0, 504.0, 521.0, 539.0, 556.0, 572.0], [-102.0, -1.0, 52.0, 91.0, 126.0, 158.0, 188.0, 216.0, 242.0, 268.0, 292.0, 316.0, 339.0, 362.0, 384.0, 406.0, 427.0, 448.0, 469.0, 489.0, 509.0, 528.0, 548.0, 566.0, 585.0, 603.0], [-117.0, -9.0, 48.0, 89.0, 125.0, 159.0, 191.0, 220.0, 249.0, 276.0, 302.0, 327.0, 352.0, 376.0, 399.0, 422.0, 445.0, 467.0, 489.0, 511.0, 532.0, 553.0, 574.0, 594.0, 614.0, 634.0], [-133.0, -17.0, 44.0, 87.0, 125.0, 160.0, 193.0, 225.0, 255.0, 283.0, 311.0, 338.0, 364.0, 390.0, 415.0, 440.0, 464.0, 488.0, 511.0, 534.0, 557.0, 579.0, 601.0, 623.0, 645.0, 666.0], [-150.0, -26.0, 39.0, 85.0, 124.0, 161.0, 196.0, 229.0, 260.0, 291.0, 320.0, 349.0, 377.0, 404.0, 431.0, 457.0, 483.0, 508.0, 533.0, 558.0, 582.0, 606.0, 630.0, 653.0, 676.0, 699.0], [-168.0, -36.0, 35.0, 82.0, 123.0, 161.0, 198.0, 233.0, 266.0, 298.0, 329.0, 359.0, 389.0, 418.0, 446.0, 474.0, 501.0, 528.0, 554.0, 581.0, 606.0, 632.0, 657.0, 682.0, 707.0, 731.0], [-187.0, -46.0, 30.0, 80.0, 122.0, 162.0, 199.0, 236.0, 271.0, 305.0, 338.0, 370.0, 401.0, 432.0, 462.0, 491.0, 520.0, 549.0, 577.0, 605.0, 632.0, 659.0, 686.0, 712.0, 738.0, 764.0], [-207.0, -57.0, 25.0, 77.0, 121.0, 162.0, 201.0, 239.0, 275.0, 311.0, 345.0, 379.0, 412.0, 444.0, 476.0, 508.0, 538.0, 569.0, 599.0, 628.0, 657.0, 686.0, 714.0, 742.0, 770.0, 797.0], [-228.0, -68.0, 19.0, 74.0, 119.0, 162.0, 203.0, 242.0, 280.0, 317.0, 353.0, 388.0, 423.0, 457.0, 490.0, 523.0, 556.0, 588.0, 620.0, 651.0, 682.0, 713.0, 743.0, 773.0, 802.0, 832.0], [-250.0, -80.0, 14.0, 71.0, 118.0, 162.0, 204.0, 245.0, 284.0, 323.0, 360.0, 397.0, 434.0, 469.0, 505.0, 539.0, 574.0, 608.0, 641.0, 675.0, 707.0, 740.0, 772.0, 804.0, 835.0, 867.0], [-273.0, -93.0, 8.0, 68.0, 117.0, 162.0, 205.0, 248.0, 289.0, 329.0, 368.0, 407.0, 445.0, 482.0, 519.0, 555.0, 591.0, 627.0, 662.0, 697.0, 732.0, 766.0, 800.0, 834.0, 868.0, 901.0], [-297.0, -106.0, 2.0, 65.0, 115.0, 162.0, 207.0, 250.0, 293.0, 334.0, 375.0, 415.0, 455.0, 494.0, 533.0, 571.0, 609.0, 646.0, 684.0, 720.0, 757.0, 793.0, 829.0, 865.0, 900.0, 936.0], [-322.0, -120.0, -4.0, 61.0, 114.0, 163.0, 209.0, 253.0, 297.0, 340.0, 382.0, 424.0, 465.0, 506.0, 546.0, 586.0, 626.0, 665.0, 704.0, 743.0, 781.0, 819.0, 857.0, 895.0, 932.0, 970.0] ] 
# NOTE: Row 0 is header. Col 0 is header. Data starts at Row 1, Col 1.

MC_PAYOFFS = [ [None, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0], [0.0, 0.0, -1.0, -4.0, -9.0, -16.0, -25.0, -36.0, -49.0, -64.0, -81.0, -100.0, -121.0, -144.0, -169.0, -196.0, -225.0, -256.0, -289.0, -324.0, -361.0, -400.0, -441.0, -484.0, -529.0, -576.0], [1.0, 0.0, 19.0, 26.0, 30.0, 32.0, 32.0, 30.0, 26.0, 20.0, 12.0, 2.0, -10.0, -24.0, -40.0, -58.0, -78.0, -100.0, -124.0, -150.0, -178.0, -208.0, -240.0, -274.0, -310.0, -348.0], [2.0, 0.0, 29.0, 42.0, 50.0, 55.0, 58.0, 59.0, 58.0, 55.0, 50.0, 43.0, 34.0, 23.0, 10.0, -5.0, -22.0, -41.0, -62.0, -85.0, -110.0, -137.0, -166.0, -197.0, -230.0, -265.0], [3.0, 0.0, 38.0, 55.0, 66.0, 74.0, 79.0, 82.0, 83.0, 82.0, 79.0, 74.0, 67.0, 58.0, 47.0, 34.0, 19.0, 2.0, -17.0, -38.0, -61.0, -86.0, -113.0, -142.0, -173.0, -206.0], [4.0, 0.0, 45.0, 66.0, 82.0, 91.0, 98.0, 103.0, 106.0, 107.0, 106.0, 103.0, 98.0, 91.0, 82.0, 71.0, 58.0, 43.0, 26.0, 7.0, -14.0, -37.0, -62.0, -89.0, -118.0, -149.0], [5.0, 0.0, 51.0, 76.0, 95.0, 107.0, 116.0, 122.0, 126.0, 128.0, 128.0, 126.0, 122.0, 116.0, 108.0, 98.0, 86.0, 72.0, 56.0, 38.0, 18.0, -4.0, -28.0, -54.0, -82.0, -112.0], [6.0, 0.0, 57.0, 84.0, 107.0, 122.0, 133.0, 141.0, 146.0, 149.0, 150.0, 149.0, 146.0, 141.0, 134.0, 125.0, 114.0, 101.0, 86.0, 69.0, 50.0, 29.0, 6.0, -19.0, -46.0, -75.0], [7.0, 0.0, 62.0, 92.0, 117.0, 136.0, 149.0, 159.0, 166.0, 170.0, 172.0, 172.0, 170.0, 166.0, 160.0, 152.0, 142.0, 130.0, 116.0, 100.0, 82.0, 62.0, 40.0, 16.0, -10.0, -38.0], [8.0, 0.0, 66.0, 99.0, 126.0, 148.0, 164.0, 177.0, 186.0, 192.0, 196.0, 197.0, 196.0, 193.0, 188.0, 181.0, 172.0, 161.0, 148.0, 133.0, 116.0, 97.0, 76.0, 53.0, 28.0, 1.0], [9.0, 0.0, 70.0, 105.0, 135.0, 159.0, 179.0, 194.0, 205.0, 213.0, 218.0, 221.0, 221.0, 219.0, 215.0, 209.0, 201.0, 191.0, 179.0, 165.0, 149.0, 131.0, 111.0, 89.0, 65.0, 39.0], [10.0, 0.0, 74.0, 111.0, 143.0, 169.0, 191.0, 208.0, 222.0, 232.0, 239.0, 243.0, 245.0, 244.0, 241.0, 236.0, 229.0, 220.0, 209.0, 196.0, 181.0, 164.0, 145.0, 124.0, 101.0, 76.0], [11.0, 0.0, 77.0, 117.0, 151.0, 179.0, 202.0, 222.0, 237.0, 249.0, 258.0, 264.0, 267.0, 268.0, 266.0, 262.0, 256.0, 248.0, 238.0, 226.0, 212.0, 196.0, 178.0, 158.0, 136.0, 112.0], [12.0, 0.0, 80.0, 122.0, 158.0, 188.0, 213.0, 234.0, 251.0, 265.0, 275.0, 283.0, 288.0, 290.0, 290.0, 287.0, 282.0, 275.0, 266.0, 255.0, 242.0, 227.0, 210.0, 191.0, 170.0, 147.0], [13.0, 0.0, 83.0, 127.0, 165.0, 196.0, 223.0, 245.0, 264.0, 279.0, 291.0, 300.0, 307.0, 311.0, 312.0, 311.0, 307.0, 301.0, 293.0, 283.0, 271.0, 257.0, 241.0, 223.0, 203.0, 181.0], [14.0, 0.0, 86.0, 131.0, 171.0, 204.0, 232.0, 256.0, 276.0, 293.0, 306.0, 317.0, 325.0, 330.0, 333.0, 333.0, 331.0, 326.0, 319.0, 310.0, 299.0, 286.0, 271.0, 254.0, 235.0, 214.0], [15.0, 0.0, 88.0, 136.0, 177.0, 212.0, 242.0, 267.0, 288.0, 306.0, 321.0, 333.0, 342.0, 349.0, 353.0, 355.0, 354.0, 351.0, 345.0, 337.0, 327.0, 315.0, 301.0, 285.0, 267.0, 247.0], [16.0, 0.0, 91.0, 140.0, 183.0, 220.0, 251.0, 278.0, 301.0, 320.0, 336.0, 349.0, 359.0, 367.0, 372.0, 375.0, 376.0, 374.0, 370.0, 364.0, 355.0, 344.0, 331.0, 316.0, 299.0, 280.0], [17.0, 0.0, 93.0, 144.0, 189.0, 227.0, 260.0, 288.0, 312.0, 333.0, 350.0, 364.0, 376.0, 385.0, 391.0, 395.0, 397.0, 396.0, 393.0, 388.0, 381.0, 372.0, 360.0, 346.0, 330.0, 312.0], [18.0, 0.0, 95.0, 148.0, 194.0, 234.0, 268.0, 298.0, 323.0, 345.0, 364.0, 379.0, 392.0, 402.0, 410.0, 415.0, 418.0, 418.0, 416.0, 412.0, 406.0, 398.0, 388.0, 376.0, 361.0, 344.0], [19.0, 0.0, 97.0, 151.0, 199.0, 240.0, 276.0, 308.0, 335.0, 358.0, 378.0, 394.0, 408.0, 419.0, 428.0, 434.0, 438.0, 440.0, 439.0, 436.0, 431.0, 424.0, 415.0, 404.0, 391.0, 375.0], [20.0, 0.0, 99.0, 154.0, 204.0, 247.0, 284.0, 317.0, 346.0, 370.0, 391.0, 409.0, 424.0, 436.0, 446.0, 453.0, 458.0, 461.0, 461.0, 459.0, 455.0, 449.0, 441.0, 431.0, 419.0, 405.0], [21.0, 0.0, 100.0, 158.0, 209.0, 253.0, 292.0, 326.0, 356.0, 382.0, 404.0, 423.0, 439.0, 452.0, 463.0, 471.0, 477.0, 481.0, 482.0, 481.0, 478.0, 473.0, 466.0, 457.0, 446.0, 433.0], [22.0, 0.0, 102.0, 161.0, 213.0, 259.0, 299.0, 335.0, 366.0, 393.0, 417.0, 437.0, 454.0, 468.0, 480.0, 489.0, 496.0, 501.0, 503.0, 503.0, 501.0, 497.0, 491.0, 483.0, 473.0, 461.0], [23.0, 0.0, 103.0, 164.0, 217.0, 264.0, 306.0, 343.0, 376.0, 405.0, 430.0, 451.0, 469.0, 484.0, 497.0, 507.0, 515.0, 520.0, 523.0, 524.0, 523.0, 520.0, 515.0, 508.0, 499.0, 488.0], [24.0, 0.0, 105.0, 166.0, 221.0, 270.0, 313.0, 351.0, 385.0, 415.0, 441.0, 464.0, 483.0, 500.0, 513.0, 524.0, 533.0, 539.0, 543.0, 545.0, 545.0, 543.0, 538.0, 532.0, 524.0, 514.0], [25.0, 0.0, 106.0, 169.0, 225.0, 275.0, 320.0, 360.0, 395.0, 426.0, 453.0, 477.0, 497.0, 515.0, 529.0, 541.0, 551.0, 558.0, 563.0, 566.0, 567.0, 565.0, 562.0, 556.0, 548.0, 539.0] ]


# --------------------------
# Global Game State
# --------------------------
game_state = {
    "round": 0,
    "max_rounds": 10,
    "am_strategy": "balanced",
    "mc_strategy": "balanced",
    "history": [],
    "am_total": 0,
    "mc_total": 0,
    "is_running": False,

    # NEW: 给 reasoning 用
    "last_reasoning_am": [],
    "last_reasoning_mc": []
}


# --------------------------
# Payoff Lookup Function
# --------------------------
def compute_payoff(am_inv, mc_inv):
    """Use exact lookup in your matrix."""
    am_i = min(max(0, am_inv), 25)
    mc_i = min(max(0, mc_inv), 25)

    try:
        am_p = float(AM_PAYOFFS[am_i + 1][mc_i])
        mc_p = float(MC_PAYOFFS[am_i + 1][mc_i + 1])
    except:
        am_p = mc_p = (am_i + mc_i) * 2

    return int(am_p), int(mc_p)
# ============================================================================
#  DECISION ENGINE — Core behavioral logic for AM/MC agents
# ============================================================================

def get_last_moves():
    """Return last round's investment moves. Defaults to moderate values."""
    if not game_state["history"]:
        return 12, 12
    last_round = game_state["history"][-1]
    return last_round["am_investment"], last_round["mc_investment"]


def best_response_to_opponent(opp_invest):
    """
    Compute the best-response investment for AM and MC respectively,
    given the opponent's previous investment, using the actual payoff matrices.
    """
    opp_i = min(max(0, opp_invest), 25)

    # Best response for AM
    best_am = 0
    best_am_pay = -1e9
    for am_i in range(26):
        p, _ = compute_payoff(am_i, opp_i)
        if p > best_am_pay:
            best_am_pay = p
            best_am = am_i

    # Best response for MC
    best_mc = 0
    best_mc_pay = -1e9
    for mc_i in range(26):
        _, p = compute_payoff(opp_i, mc_i)
        if p > best_mc_pay:
            best_mc_pay = p
            best_mc = mc_i

    return best_am, best_mc


def decide_investment(agent, strategy, round_num):
    """
    Determine the agent's investment for the current round.
    Behaviors are tied to personas (cooperative, competitive, balanced, adaptive).
    """
    last_am, last_mc = get_last_moves()

    if agent == "AM":
        my_last = last_am
        opp_last = last_mc
    else:
        my_last = last_mc
        opp_last = last_am

    # -------------------------------------------------------------
    # Cooperative Strategy
    # -------------------------------------------------------------
    if strategy == "cooperative":
        # Increase trust and push synergy
        target = max(opp_last + 2, 15)
        return min(target + random.randint(0, 2), 25)

    # -------------------------------------------------------------
    # Competitive Strategy
    # -------------------------------------------------------------
    if strategy == "competitive":
        # True game-theoretic best-response based on payoff matrix
        br_am, br_mc = best_response_to_opponent(opp_last)
        return br_am if agent == "AM" else br_mc

    # -------------------------------------------------------------
    # Adaptive (Tit-for-Tat)
    # -------------------------------------------------------------
    if strategy == "adaptive":
        if round_num == 1:
            return 13
        return opp_last

    # -------------------------------------------------------------
    # Balanced (fair moderate reasoning)
    # -------------------------------------------------------------
    if strategy == "balanced":
        avg = (my_last + opp_last) // 2
        noise = random.randint(-2, 2)
        return min(max(5, avg + noise), 25)

    # Default fallback
    return 12
# ============================================================================
#  REASONING ENGINE — Structured explanation for frontend visualization
# ============================================================================

def generate_reasoning(agent, strategy, investment, opp_last):
    """
    Produce a structured reasoning array that the frontend animates step-by-step.
    """
    steps = []

    # Step 1: Observation
    steps.append({
        "type": "observation",
        "text": f"I observed that my partner invested {opp_last} in the previous round."
    })

    # Step 2: Strategy Explanation
    if strategy == "cooperative":
        strategy_text = (
            "I aim to maximize joint welfare and strengthen mutual trust."
        )
    elif strategy == "competitive":
        strategy_text = (
            "I aim to maximize my own payoff based on the payoff matrix incentives."
        )
    elif strategy == "adaptive":
        strategy_text = (
            "I follow a Tit-for-Tat strategy, mirroring my partner’s previous action."
        )
    elif strategy == "balanced":
        strategy_text = (
            "I balance individual and joint outcomes, adjusting moderately each round."
        )
    else:
        strategy_text = "I make decisions based on general payoff considerations."

    steps.append({
        "type": "strategy",
        "text": strategy_text
    })

    # Step 3: Final Decision
    steps.append({
        "type": "decision",
        "text": f"Therefore, I chose to invest {investment} engineers this round."
    })

    return steps
# ============================================================================
#  REASONING ENGINE — Structured explanation for frontend visualization
# ============================================================================

def generate_reasoning(agent, strategy, investment, opp_last):
    """
    Produce a structured reasoning array that the frontend animates step-by-step.
    """
    steps = []

    # Step 1: Observation
    steps.append({
        "type": "observation",
        "text": f"I observed that my partner invested {opp_last} in the previous round."
    })

    # Step 2: Strategy Explanation
    if strategy == "cooperative":
        strategy_text = (
            "I aim to maximize joint welfare and strengthen mutual trust."
        )
    elif strategy == "competitive":
        strategy_text = (
            "I aim to maximize my own payoff based on the payoff matrix incentives."
        )
    elif strategy == "adaptive":
        strategy_text = (
            "I follow a Tit-for-Tat strategy, mirroring my partner’s previous action."
        )
    elif strategy == "balanced":
        strategy_text = (
            "I balance individual and joint outcomes, adjusting moderately each round."
        )
    else:
        strategy_text = "I make decisions based on general payoff considerations."

    steps.append({
        "type": "strategy",
        "text": strategy_text
    })

    # Step 3: Final Decision
    steps.append({
        "type": "decision",
        "text": f"Therefore, I chose to invest {investment} engineers this round."
    })

    return steps
    
    # Global structured state for reasoning + chat context
    simulation_state = {
        "last_round": {},
        "am_reasoning": [],
        "mc_reasoning": [],
    }
@app.route('/continue_simulation', methods=['POST'])
def continue_simulation():
    # Stop if already done
    if not game_state["is_running"] or game_state["round"] >= game_state["max_rounds"]:
        return jsonify({"game_complete": True})

    # Advance round
    game_state["round"] += 1
    round_number = game_state["round"]

    # Current strategies
    strat_am = game_state["am_strategy"]
    strat_mc = game_state["mc_strategy"]

    # Agent decisions
    am_inv = decide_investment("AM", strat_am, round_number)
    mc_inv = decide_investment("MC", strat_mc, round_number)

    # Matrix payoffs
    am_pay, mc_pay = compute_payoff(am_inv, mc_inv)

    # Update totals
    game_state["am_total"] += am_pay
    game_state["mc_total"] += mc_pay

    # Generate reasoning
    last_am, last_mc = get_last_moves()

    am_reasoning = generate_reasoning("AM", strat_am, am_inv, last_mc)
    mc_reasoning = generate_reasoning("MC", strat_mc, mc_inv, last_am)

    # Save simulation_state for chat
    simulation_state["last_round"] = {
        "round": round_number,
        "am_investment": am_inv,
        "mc_investment": mc_inv,
        "am_payoff": am_pay,
        "mc_payoff": mc_pay
    }
    simulation_state["am_reasoning"] = am_reasoning
    simulation_state["mc_reasoning"] = mc_reasoning

    # Save round history
    game_state["history"].append(simulation_state["last_round"])

    # Logging
    print(f"[Round {round_number}] AM={am_inv} MC={mc_inv} → Payoffs {am_pay}/{mc_pay}")

    # Return JSON for frontend
    return jsonify({
        "round": round_number,
        "am_investment": am_inv,
        "mc_investment": mc_inv,
        "am_payoff": am_pay,
        "mc_payoff": mc_pay,
        "am_total": game_state["am_total"],
        "mc_total": game_state["mc_total"],
        "am_reasoning": am_reasoning,
        "mc_reasoning": mc_reasoning,
        "history": game_state["history"],
        "game_complete": (round_number >= game_state["max_rounds"])
    })
@app.route("/chat_with_agent", methods=["POST"])
def chat_with_agent():
    data = request.json or {}
    agent = data.get("agent", "").upper()
    user_message = data.get("message", "")

    # Which agent?
    if agent not in ("AM", "MC"):
        return jsonify({"reply": "Invalid agent."})

    # Strategy and context
    strategy = game_state["am_strategy"] if agent == "AM" else game_state["mc_strategy"]
    last = simulation_state.get("last_round", {})
    reasoning = (
        simulation_state.get("am_reasoning", [])
        if agent == "AM"
        else simulation_state.get("mc_reasoning", [])
    )

    # Prepare reasoning text block
    reasoning_text = "\n".join([f"- {step['text']}" for step in reasoning])

    system_prompt = f"""
    You are Agent {agent} in a repeated engineering investment game.
    Your persona (strategy) is: **{strategy}**.

    Latest round:
    - AM invested: {last.get('am_investment')}
    - MC invested: {last.get('mc_investment')}
    - AM payoff: {last.get('am_payoff')}
    - MC payoff: {last.get('mc_payoff')}

    Your reasoning from that round:
    {reasoning_text}

    RULES:
    - Respond in one short, concise sentence.
    - Stay in character according to your persona.
    - Use ONLY the data above; do NOT invent numbers.
    """

    # ---------------- OpenAI Call -------------------
    reply = None

    if os.environ.get("OPENAI_API_KEY"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4
            )
            reply = response.choices[0].message.content

        except Exception as e:
            print("🔥 OpenAI Error:", e)

    # Fallback reply
    if reply is None:
        reply = f"As a {strategy} agent, my last decision was based on maintaining consistent incentives."

    # OPTIONAL: let user influence persona dynamically
    if "be more competitive" in user_message.lower():
        if agent == "AM":
            game_state["am_strategy"] = "competitive"
        else:
            game_state["mc_strategy"] = "competitive"
        reply += " (Persona updated to competitive.)"

    if "be more cooperative" in user_message.lower():
        if agent == "AM":
            game_state["am_strategy"] = "cooperative"
        else:
            game_state["mc_strategy"] = "cooperative"
        reply += " (Persona updated to cooperative.)"

    print(f"Chat Reply[{agent}]: {reply}")
    return jsonify({"reply": reply})
# Enhanced internal cognitive states for AM and MC
agent_state = {
    "AM": {
        "trust": 0.5,     # confidence opponent is cooperative
        "risk": 0.5,      # perceived risk of exploitation
        "volatility": 0,  # how unstable opponent appears
        "history": []     # sequence of opponent's past investments
    },
    "MC": {
        "trust": 0.5,
        "risk": 0.5,
        "volatility": 0,
        "history": []
    }
}
def analyze_opponent(agent_role, opp_last_moves):
    """Analyze opponent pattern based on past N investments."""
    N = min(5, len(opp_last_moves))
    if N < 2:
        return "unknown"

    recent = opp_last_moves[-N:]
    diffs = [recent[i] - recent[i-1] for i in range(1, N)]
    
    avg_change = sum(diffs) / len(diffs)
    volatility = sum(abs(x) for x in diffs) / len(diffs)

    # Update volatility
    agent_state[agent_role]["volatility"] = volatility

    if avg_change > 1.5:
        return "increasing"
    elif avg_change < -1.5:
        return "decreasing"
    elif volatility > 5:
        return "unstable"
    else:
        return "flat"
def decide_investment(agent_role, strategy, round_num):
    """
    Version 4.0 — True intelligent decision engine.
    Persona + opponent pattern + internal memory.
    """
    my_state = agent_state[agent_role]
    opponent = "MC" if agent_role == "AM" else "AM"

    # Pull last opponent moves
    opp_history = my_state["history"]

    # Get last investments
    last_am, last_mc = get_last_moves()
    my_last = last_am if agent_role == "AM" else last_mc
    opp_last = last_mc if agent_role == "AM" else last_am

    # Analyze opponent pattern
    pattern = analyze_opponent(agent_role, opp_history)

    # Baseline investment
    invest = my_last

    # --------------------------
    # STRATEGY-DRIVEN ADJUSTMENTS
    # --------------------------

    if strategy == "cooperative":
        invest += 2
        if pattern == "increasing":
            invest += 2
            my_state["trust"] += 0.1
        if pattern == "decreasing":
            invest -= 2
            my_state["risk"] += 0.1
    
    elif strategy == "competitive":
        invest -= 3
        if pattern == "unstable":
            invest -= 2
        if opp_last > my_last + 5:
            invest = max(3, invest - 2)
    
    elif strategy == "balanced":
        invest = (my_last + opp_last) // 2
        if pattern == "increasing":
            invest += 1
        if pattern == "decreasing":
            invest -= 1
    
    elif strategy == "adaptive":
        # weighted tit-for-tat
        invest = int(0.7 * opp_last + 0.3 * my_last)
        if pattern == "unstable":
            invest -= 2

    # Update internal memory
    my_state["history"].append(opp_last)

    # Clamp
    invest = max(0, min(25, invest))
    return invest
def generate_reasoning(agent_role, strategy, investment, opp_last):
    """Produce more intelligent reasoning steps."""
    my_state = agent_state[agent_role]
    pattern = analyze_opponent(agent_role, my_state["history"])

    steps = []

    steps.append({
        "type": "observation",
        "text": f"I observed the opponent invested {opp_last} engineers last round. Pattern appears: {pattern}."
    })

    steps.append({
        "type": "strategy",
        "text": f"My persona is {strategy}, influencing my risk ({my_state['risk']:.2f}) and trust ({my_state['trust']:.2f})."
    })

    steps.append({
        "type": "reasoning",
        "text": f"Given their pattern ({pattern}), I adjust expectations of future cooperation."
    })

    steps.append({
        "type": "decision",
        "text": f"I therefore choose to invest **{investment} engineers** this round."
    })

    return steps
strategy_meta = {
    "AM": {
        "cooperative": 0.25,
        "competitive": 0.25,
        "adaptive": 0.25,
        "balanced": 0.25
    },
    "MC": {
        "cooperative": 0.25,
        "competitive": 0.25,
        "adaptive": 0.25,
        "balanced": 0.25
    }
}
def update_strategy_meta(agent_role, pattern, payoff, opp_last):
    meta = strategy_meta[agent_role]

    # --- reward cooperative if pattern suggests trust ---
    if pattern == "increasing":
        meta["cooperative"] += 0.08
        meta["adaptive"] += 0.02

    # --- punish cooperation if opponent betrays or lowers investment ---
    if pattern == "decreasing":
        meta["competitive"] += 0.08
        meta["balanced"] += 0.03

    # --- unstable opponent: prefer safe balanced ---
    if pattern == "unstable":
        meta["balanced"] += 0.10
        meta["competitive"] += 0.05

    # --- if payoff is high, reinforce current dominant strategy ---
    if payoff > 0:
        best = max(meta, key=meta.get)
        meta[best] += 0.05

    # normalize to keep sum = 1
    total = sum(meta.values())
    for k in meta:
        meta[k] /= total
def select_strategy(agent_role):
    """Choose strategy based on learned probabilities (soft choice)."""
    meta = strategy_meta[agent_role]

    strategies = list(meta.keys())
    weights = list(meta.values())

    # random weighted selection
    import random
    choice = random.choices(strategies, weights=weights, k=1)[0]
    return choice
# Update strategy meta-learning
update_strategy_meta("AM", analyze_opponent("AM", agent_state["AM"]["history"]),
                     am_pay, last_mc)

update_strategy_meta("MC", analyze_opponent("MC", agent_state["MC"]["history"]),
                     mc_pay, last_am)
game_state['am_strategy'] = select_strategy("AM")
game_state['mc_strategy'] = select_strategy("MC")
steps.append({
    "type": "strategy",
    "text": f"My current strategy is **{strategy}**, derived from evolving probabilities: {strategy_meta[agent_role]}"
})
def llm_decide_investment(agent_role, opp_last, history):
    """
    Ask LLM to propose an investment based on payoff structure, history, and prediction.
    """

    # Convert history to readable format
    hist_text = "\n".join([
        f"Round {h['round']}: AM={h['am_investment']} / MC={h['mc_investment']} (payoffs {h['am_payoff']}/{h['mc_payoff']})"
        for h in history[-5:]  # limit to last 5
    ]) or "No previous rounds."

    prompt = f"""
    You are Agent {agent_role} in a repeated cooperation-competition game.

    Here are the last rounds:
    {hist_text}

    Your opponent invested {opp_last} most recently.

    Your goal is to maximize your cumulative payoff over the next rounds.
    Investments range from 0 to 25.

    Provide ONLY a single integer from 0–25 as your next recommended investment.
    Do NOT explain, do NOT add words.
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "What is my next investment?"}
            ]
        )

        raw = res.choices[0].message.content.strip()
        print(f"🔮 LLM proposed: {raw}")

        # Extract integer safely
        num = int("".join([c for c in raw if c.isdigit()]))
        return max(0, min(25, num))

    except Exception as e:
        print("🔥 LLM Decision Error:", e)
        return None
def decide_investment(agent_role, strategy, round_num):
    last_am, last_mc = get_last_moves()
    my_last, opp_last = (last_am, last_mc) if agent_role == "AM" else (last_mc, last_am)

    # 1. Get strategy-based decision
    base_decision = strategy_based_choice(agent_role, strategy, round_num, my_last, opp_last)

    # 2. Try LLM recommendation
    llm_choice = None
    if os.environ.get("OPENAI_API_KEY"):
        llm_choice = llm_decide_investment(agent_role, opp_last, game_state["history"])

    # 3. Blend results
    if llm_choice is not None:
        return int((base_decision + llm_choice) / 2)

    return base_decision
def strategy_based_choice(agent_role, strategy, round_num, my_last, opp_last):
    if strategy == 'cooperative':
        return min(25, max(15, max(my_last, opp_last) + random.randint(1, 3)))

    if strategy == 'competitive':
        return random.randint(5, 10)

    if strategy == 'adaptive':
        return 13 if round_num == 1 else opp_last

    if strategy == 'balanced':
        t = (my_last + opp_last) // 2
        return min(25, max(5, t + random.randint(-2, 2)))

    return 12
steps.append({
    "type": "decision",
    "text": f"My strategy-based choice was {base_decision}, LLM suggested {llm_choice}, so I invested {investment}."
})
def estimate_future_value(agent_role, current_inv, history, horizon=3):
    """
    Estimate the expected future payoff over next few rounds (discounted).
    Very rough but gives agent long-term awareness.
    """

    if not history:
        opp_last = 12
    else:
        last = history[-1]
        opp_last = last["mc_investment"] if agent_role == "AM" else last["am_investment"]

    future_value = 0.0
    discount = 0.85  # future discount factor

    # very rough projection: assume opponent continues near its last level
    predicted_opp = opp_last

    for t in range(1, horizon + 1):
        # If I keep same move, what do I get?
        am_pay, mc_pay = compute_payoff(
            current_inv if agent_role == "AM" else predicted_opp,
            predicted_opp if agent_role == "AM" else current_inv
        )
        immediate = am_pay if agent_role == "AM" else mc_pay

        future_value += (discount ** t) * immediate

        # update predicted opponent (simple reversion)
        predicted_opp = int((predicted_opp + current_inv) / 2)

    return future_value
# 1. Strategy-based choice
base_decision = strategy_based_choice(agent_role, strategy, round_num, my_last, opp_last)

# 2. LLM recommendation
llm_choice = llm_decide_investment(agent_role, opp_last, game_state["history"]) if has_key else None

# 3. Future value estimation
fv_base = estimate_future_value(agent_role, base_decision, game_state["history"])
fv_llm = estimate_future_value(agent_role, llm_choice, game_state["history"]) if llm_choice else None

# 4. Decision ranking
candidates = []

# base
candidates.append((base_decision, fv_base))

# LLM option
if llm_choice:
    candidates.append((llm_choice, fv_llm))

# explore: +2 and -2 around base
for d in [base_decision - 2, base_decision + 2]:
    if 0 <= d <= 25:
        fv = estimate_future_value(agent_role, d, game_state["history"])
        candidates.append((d, fv))

# sort by future value
best = max(candidates, key=lambda x: x[1])[0]


steps.append({
    "type": "calculation",
    "text": f"I estimated future value for {investment} as {fv_invest:.1f}, which guided my long-term decision."
})
agent_state = {
    "AM": {
        "behavior_modifiers": {
            "aggression": 0,
            "cooperation_bias": 0,
            "trust_factor": 1.0,
            "investment_shift": 0
        }
    },
    "MC": {
        "behavior_modifiers": {
            "aggression": 0,
            "cooperation_bias": 0,
            "trust_factor": 1.0,
            "investment_shift": 0
        }
    }
}
def interpret_user_instruction(message):
    """
    Use LLM to convert user message into a structured behavioral modification.
    Example: "be more cooperative" -> {"cooperation_bias": +2}
    """
    client = OpenAI()

    prompt = f"""
    The user said: "{message}"

    Interpret this as behavioral modification instructions
    for a repeated-game strategy agent (AM or MC).
    
    Respond ONLY in pure JSON with keys like:
    {{
        "aggression": +1 or -1,
        "cooperation_bias": +1 or -1,
        "trust_factor": +0.1 or -0.1,
        "investment_shift": integer from -5 to +5
    }}

    If no behavioral meaning, return:
    {{
        "aggression": 0,
        "cooperation_bias": 0,
        "trust_factor": 0,
        "investment_shift": 0
    }}
    """

    try:
        result = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(result.choices[0].message["content"])
    except:
        return {"aggression": 0, "cooperation_bias": 0, "trust_factor": 0, "investment_shift": 0}
mods = interpret_user_instruction(user_message)

agent_state[target_agent]["behavior_modifiers"]["aggression"] += mods["aggression"]
agent_state[target_agent]["behavior_modifiers"]["cooperation_bias"] += mods["cooperation_bias"]
agent_state[target_agent]["behavior_modifiers"]["trust_factor"] += mods["trust_factor"]
agent_state[target_agent]["behavior_modifiers"]["investment_shift"] += mods["investment_shift"]
mods = agent_state[agent_role]["behavior_modifiers"]

# modify by aggression
final_value = int(best + mods["aggression"] * 1)

# modify by cooperation bias
final_value += mods["cooperation_bias"]

# modify by trust
final_value = int(final_value * mods["trust_factor"])

# modify investment shift
final_value += mods["investment_shift"]

# Clamp
final_value = max(0, min(25, final_value))
if mods["cooperation_bias"] != 0:
    steps.append({"type": "modifier", "text": f"User instructions increased my cooperation tendency by {mods['cooperation_bias']}."})

if mods["aggression"] != 0:
    steps.append({"type": "modifier", "text": f"My aggression level changed by {mods['aggression']} due to user guidance."})



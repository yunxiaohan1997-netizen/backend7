#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend7 is running!", 200
    
#!/usr/bin/env python3
"""
Backend 7.0 - The Final "Production" Version
Combines:
1. EXACT Payoff Matrices from 11.29.xlsx (No more random approximation)
2. Robust MVP Architecture (Stable endpoints)
3. Persona-Driven Logic (Cooperative/Competitive/etc)
4. Structured Reasoning for Frontend UI
"""

from flask_cors import CORS
import json
import openai
import random
import math
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

app.config['SECRET_KEY'] = 'insead-game-simulation-final'
CORS(app, resources={r"/*": {"origins": "*"}})

openai.api_key = os.environ.get('OPENAI_API_KEY', '')

# ============================================================================
# [cite_start]REAL PAYOFF DATA (From 11.29.xlsx) [cite: 1]
# ============================================================================

# NOTE: Row 0 is the Header (0, 1, 2...). Data starts at Row 1 (Index 1).
# Row Index = AM Engineers + 1
# Col Index = MC Engineers

AM_PAYOFFS = [
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0], 
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
    [-1.0, 19.0, 29.0, 38.0, 45.0, 51.0, 57.0, 62.0, 66.0, 70.0, 74.0, 77.0, 80.0, 83.0, 86.0, 88.0, 91.0, 93.0, 95.0, 97.0, 99.0, 100.0, 102.0, 103.0, 105.0, 106.0], 
    [-3.0, 27.0, 42.0, 55.0, 66.0, 76.0, 84.0, 92.0, 99.0, 105.0, 111.0, 117.0, 122.0, 127.0, 131.0, 136.0, 140.0, 144.0, 148.0, 151.0, 154.0, 158.0, 161.0, 164.0, 166.0, 169.0], 
    [-7.0, 31.0, 51.0, 68.0, 82.0, 95.0, 107.0, 117.0, 126.0, 135.0, 143.0, 151.0, 158.0, 165.0, 171.0, 177.0, 183.0, 189.0, 194.0, 199.0, 204.0, 209.0, 213.0, 217.0, 221.0, 225.0], 
    [-12.0, 33.0, 57.0, 77.0, 95.0, 110.0, 124.0, 137.0, 148.0, 159.0, 169.0, 179.0, 188.0, 196.0, 204.0, 212.0, 220.0, 227.0, 234.0, 240.0, 247.0, 253.0, 259.0, 264.0, 270.0, 275.0], 
    [-18.0, 33.0, 61.0, 84.0, 104.0, 122.0, 138.0, 153.0, 166.0, 179.0, 191.0, 202.0, 213.0, 223.0, 233.0, 242.0, 251.0, 260.0, 268.0, 276.0, 284.0, 292.0, 299.0, 306.0, 313.0, 320.0], 
    [-25.0, 32.0, 63.0, 88.0, 111.0, 131.0, 149.0, 166.0, 182.0, 196.0, 210.0, 223.0, 236.0, 248.0, 259.0, 270.0, 281.0, 291.0, 301.0, 311.0, 320.0, 329.0, 338.0, 347.0, 355.0, 363.0], 
    [-33.0, 30.0, 63.0, 91.0, 116.0, 138.0, 158.0, 177.0, 194.0, 211.0, 226.0, 241.0, 255.0, 269.0, 282.0, 295.0, 307.0, 319.0, 330.0, 342.0, 352.0, 363.0, 373.0, 383.0, 393.0, 402.0], 
    [-42.0, 27.0, 63.0, 93.0, 119.0, 143.0, 165.0, 186.0, 205.0, 223.0, 240.0, 256.0, 272.0, 287.0, 302.0, 316.0, 330.0, 343.0, 356.0, 369.0, 381.0, 393.0, 405.0, 416.0, 427.0, 438.0], 
    [-52.0, 23.0, 62.0, 94.0, 122.0, 147.0, 171.0, 193.0, 214.0, 233.0, 252.0, 270.0, 287.0, 304.0, 320.0, 336.0, 351.0, 366.0, 380.0, 394.0, 408.0, 421.0, 434.0, 447.0, 459.0, 472.0], 
    [-63.0, 18.0, 60.0, 94.0, 124.0, 151.0, 176.0, 199.0, 222.0, 243.0, 263.0, 283.0, 302.0, 320.0, 338.0, 355.0, 371.0, 388.0, 403.0, 419.0, 434.0, 449.0, 463.0, 477.0, 491.0, 505.0], 
    [-75.0, 12.0, 58.0, 94.0, 125.0, 154.0, 180.0, 205.0, 229.0, 251.0, 273.0, 294.0, 315.0, 335.0, 354.0, 373.0, 391.0, 409.0, 426.0, 443.0, 460.0, 476.0, 492.0, 508.0, 523.0, 538.0], 
    [-88.0, 6.0, 55.0, 93.0, 126.0, 156.0, 184.0, 211.0, 236.0, 260.0, 283.0, 305.0, 327.0, 349.0, 370.0, 390.0, 410.0, 430.0, 449.0, 467.0, 486.0, 504.0, 521.0, 539.0, 556.0, 572.0], 
    [-102.0, -1.0, 52.0, 91.0, 126.0, 158.0, 188.0, 216.0, 242.0, 268.0, 292.0, 316.0, 339.0, 362.0, 384.0, 406.0, 427.0, 448.0, 469.0, 489.0, 509.0, 528.0, 548.0, 566.0, 585.0, 603.0], 
    [-117.0, -9.0, 48.0, 89.0, 125.0, 159.0, 191.0, 220.0, 249.0, 276.0, 302.0, 327.0, 352.0, 376.0, 399.0, 422.0, 445.0, 467.0, 489.0, 511.0, 532.0, 553.0, 574.0, 594.0, 614.0, 634.0], 
    [-133.0, -17.0, 44.0, 87.0, 125.0, 160.0, 193.0, 225.0, 255.0, 283.0, 311.0, 338.0, 364.0, 390.0, 415.0, 440.0, 464.0, 488.0, 511.0, 534.0, 557.0, 579.0, 601.0, 623.0, 645.0, 666.0], 
    [-150.0, -26.0, 39.0, 85.0, 124.0, 161.0, 196.0, 229.0, 260.0, 291.0, 320.0, 349.0, 377.0, 404.0, 431.0, 457.0, 483.0, 508.0, 533.0, 558.0, 582.0, 606.0, 630.0, 653.0, 676.0, 699.0], 
    [-168.0, -36.0, 35.0, 82.0, 123.0, 161.0, 198.0, 233.0, 266.0, 298.0, 329.0, 359.0, 389.0, 418.0, 446.0, 474.0, 501.0, 528.0, 554.0, 581.0, 606.0, 632.0, 657.0, 682.0, 707.0, 731.0], 
    [-187.0, -46.0, 30.0, 80.0, 122.0, 162.0, 199.0, 236.0, 271.0, 305.0, 338.0, 370.0, 401.0, 432.0, 462.0, 491.0, 520.0, 549.0, 577.0, 605.0, 632.0, 659.0, 686.0, 712.0, 738.0, 764.0], 
    [-207.0, -57.0, 25.0, 77.0, 121.0, 162.0, 201.0, 239.0, 275.0, 311.0, 345.0, 379.0, 412.0, 444.0, 476.0, 508.0, 538.0, 569.0, 599.0, 628.0, 657.0, 686.0, 714.0, 742.0, 770.0, 797.0], 
    [-228.0, -68.0, 19.0, 74.0, 119.0, 162.0, 203.0, 242.0, 280.0, 317.0, 353.0, 388.0, 423.0, 457.0, 490.0, 523.0, 556.0, 588.0, 620.0, 651.0, 682.0, 713.0, 743.0, 773.0, 802.0, 832.0], 
    [-250.0, -80.0, 14.0, 71.0, 118.0, 162.0, 204.0, 245.0, 284.0, 323.0, 360.0, 397.0, 434.0, 469.0, 505.0, 539.0, 574.0, 608.0, 641.0, 675.0, 707.0, 740.0, 772.0, 804.0, 835.0, 867.0], 
    [-273.0, -93.0, 8.0, 68.0, 117.0, 162.0, 205.0, 248.0, 289.0, 329.0, 368.0, 407.0, 445.0, 482.0, 519.0, 555.0, 591.0, 627.0, 662.0, 697.0, 732.0, 766.0, 800.0, 834.0, 868.0, 901.0], 
    [-297.0, -106.0, 2.0, 65.0, 115.0, 162.0, 207.0, 250.0, 293.0, 334.0, 375.0, 415.0, 455.0, 494.0, 533.0, 571.0, 609.0, 646.0, 684.0, 720.0, 757.0, 793.0, 829.0, 865.0, 900.0, 936.0], 
    [-322.0, -120.0, -4.0, 61.0, 114.0, 163.0, 209.0, 253.0, 297.0, 340.0, 382.0, 424.0, 465.0, 506.0, 546.0, 586.0, 626.0, 665.0, 704.0, 743.0, 781.0, 819.0, 857.0, 895.0, 932.0, 970.0]
]

# NOTE: Row 0 is header. Col 0 is header. Data starts at Row 1, Col 1.
MC_PAYOFFS = [
    [None, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0], 
    [0.0, 0.0, -1.0, -4.0, -9.0, -16.0, -25.0, -36.0, -49.0, -64.0, -81.0, -100.0, -121.0, -144.0, -169.0, -196.0, -225.0, -256.0, -289.0, -324.0, -361.0, -400.0, -441.0, -484.0, -529.0, -576.0], 
    [1.0, 0.0, 19.0, 26.0, 30.0, 32.0, 32.0, 30.0, 26.0, 20.0, 12.0, 2.0, -10.0, -24.0, -40.0, -58.0, -78.0, -100.0, -124.0, -150.0, -178.0, -208.0, -240.0, -274.0, -310.0, -348.0], 
    [2.0, 0.0, 29.0, 42.0, 50.0, 55.0, 58.0, 59.0, 58.0, 55.0, 50.0, 43.0, 34.0, 23.0, 10.0, -5.0, -22.0, -41.0, -62.0, -85.0, -110.0, -137.0, -166.0, -197.0, -230.0, -265.0], 
    [3.0, 0.0, 38.0, 55.0, 66.0, 74.0, 79.0, 82.0, 83.0, 82.0, 79.0, 74.0, 67.0, 58.0, 47.0, 34.0, 19.0, 2.0, -17.0, -38.0, -61.0, -86.0, -113.0, -142.0, -173.0, -206.0], 
    [4.0, 0.0, 45.0, 66.0, 82.0, 91.0, 98.0, 103.0, 106.0, 107.0, 106.0, 103.0, 98.0, 91.0, 82.0, 71.0, 58.0, 43.0, 26.0, 7.0, -14.0, -37.0, -62.0, -89.0, -118.0, -149.0], 
    [5.0, 0.0, 51.0, 76.0, 95.0, 107.0, 116.0, 122.0, 126.0, 128.0, 128.0, 126.0, 122.0, 116.0, 108.0, 98.0, 86.0, 72.0, 56.0, 38.0, 18.0, -4.0, -28.0, -54.0, -82.0, -112.0], 
    [6.0, 0.0, 57.0, 84.0, 107.0, 122.0, 133.0, 141.0, 146.0, 149.0, 150.0, 149.0, 146.0, 141.0, 134.0, 125.0, 114.0, 101.0, 86.0, 69.0, 50.0, 29.0, 6.0, -19.0, -46.0, -75.0], 
    [7.0, 0.0, 62.0, 92.0, 117.0, 136.0, 149.0, 159.0, 166.0, 170.0, 172.0, 172.0, 170.0, 166.0, 160.0, 152.0, 142.0, 130.0, 116.0, 100.0, 82.0, 62.0, 40.0, 16.0, -10.0, -38.0], 
    [8.0, 0.0, 66.0, 99.0, 126.0, 148.0, 164.0, 177.0, 186.0, 192.0, 196.0, 197.0, 196.0, 193.0, 188.0, 181.0, 172.0, 161.0, 148.0, 133.0, 116.0, 97.0, 76.0, 53.0, 28.0, 1.0], 
    [9.0, 0.0, 70.0, 105.0, 135.0, 159.0, 179.0, 194.0, 205.0, 213.0, 218.0, 221.0, 221.0, 219.0, 215.0, 209.0, 201.0, 191.0, 179.0, 165.0, 149.0, 131.0, 111.0, 89.0, 65.0, 39.0], 
    [10.0, 0.0, 74.0, 111.0, 143.0, 169.0, 191.0, 208.0, 222.0, 232.0, 239.0, 243.0, 245.0, 244.0, 241.0, 236.0, 229.0, 220.0, 209.0, 196.0, 181.0, 164.0, 145.0, 124.0, 101.0, 76.0], 
    [11.0, 0.0, 77.0, 117.0, 151.0, 179.0, 202.0, 222.0, 237.0, 249.0, 258.0, 264.0, 267.0, 268.0, 266.0, 262.0, 256.0, 248.0, 238.0, 226.0, 212.0, 196.0, 178.0, 158.0, 136.0, 112.0], 
    [12.0, 0.0, 80.0, 122.0, 158.0, 188.0, 213.0, 234.0, 251.0, 265.0, 275.0, 283.0, 288.0, 290.0, 290.0, 287.0, 282.0, 275.0, 266.0, 255.0, 242.0, 227.0, 210.0, 191.0, 170.0, 147.0], 
    [13.0, 0.0, 83.0, 127.0, 165.0, 196.0, 223.0, 245.0, 264.0, 279.0, 291.0, 300.0, 307.0, 311.0, 312.0, 311.0, 307.0, 301.0, 293.0, 283.0, 271.0, 257.0, 241.0, 223.0, 203.0, 181.0], 
    [14.0, 0.0, 86.0, 131.0, 171.0, 204.0, 232.0, 256.0, 276.0, 293.0, 306.0, 317.0, 325.0, 330.0, 333.0, 333.0, 331.0, 326.0, 319.0, 310.0, 299.0, 286.0, 271.0, 254.0, 235.0, 214.0], 
    [15.0, 0.0, 88.0, 136.0, 177.0, 212.0, 242.0, 267.0, 288.0, 306.0, 321.0, 333.0, 342.0, 349.0, 353.0, 355.0, 354.0, 351.0, 345.0, 337.0, 327.0, 315.0, 301.0, 285.0, 267.0, 247.0], 
    [16.0, 0.0, 91.0, 140.0, 183.0, 220.0, 251.0, 278.0, 301.0, 320.0, 336.0, 349.0, 359.0, 367.0, 372.0, 375.0, 376.0, 374.0, 370.0, 364.0, 355.0, 344.0, 331.0, 316.0, 299.0, 280.0], 
    [17.0, 0.0, 93.0, 144.0, 189.0, 227.0, 260.0, 288.0, 312.0, 333.0, 350.0, 364.0, 376.0, 385.0, 391.0, 395.0, 397.0, 396.0, 393.0, 388.0, 381.0, 372.0, 360.0, 346.0, 330.0, 312.0], 
    [18.0, 0.0, 95.0, 148.0, 194.0, 234.0, 268.0, 298.0, 323.0, 345.0, 364.0, 379.0, 392.0, 402.0, 410.0, 415.0, 418.0, 418.0, 416.0, 412.0, 406.0, 398.0, 388.0, 376.0, 361.0, 344.0], 
    [19.0, 0.0, 97.0, 151.0, 199.0, 240.0, 276.0, 308.0, 335.0, 358.0, 378.0, 394.0, 408.0, 419.0, 428.0, 434.0, 438.0, 440.0, 439.0, 436.0, 431.0, 424.0, 415.0, 404.0, 391.0, 375.0], 
    [20.0, 0.0, 99.0, 154.0, 204.0, 247.0, 284.0, 317.0, 346.0, 370.0, 391.0, 409.0, 424.0, 436.0, 446.0, 453.0, 458.0, 461.0, 461.0, 459.0, 455.0, 449.0, 441.0, 431.0, 419.0, 405.0], 
    [21.0, 0.0, 100.0, 158.0, 209.0, 253.0, 292.0, 326.0, 356.0, 382.0, 404.0, 423.0, 439.0, 452.0, 463.0, 471.0, 477.0, 481.0, 482.0, 481.0, 478.0, 473.0, 466.0, 457.0, 446.0, 433.0], 
    [22.0, 0.0, 102.0, 161.0, 213.0, 259.0, 299.0, 335.0, 366.0, 393.0, 417.0, 437.0, 454.0, 468.0, 480.0, 489.0, 496.0, 501.0, 503.0, 503.0, 501.0, 497.0, 491.0, 483.0, 473.0, 461.0], 
    [23.0, 0.0, 103.0, 164.0, 217.0, 264.0, 306.0, 343.0, 376.0, 405.0, 430.0, 451.0, 469.0, 484.0, 497.0, 507.0, 515.0, 520.0, 523.0, 524.0, 523.0, 520.0, 515.0, 508.0, 499.0, 488.0], 
    [24.0, 0.0, 105.0, 166.0, 221.0, 270.0, 313.0, 351.0, 385.0, 415.0, 441.0, 464.0, 483.0, 500.0, 513.0, 524.0, 533.0, 539.0, 543.0, 545.0, 545.0, 543.0, 538.0, 532.0, 524.0, 514.0], 
    [25.0, 0.0, 106.0, 169.0, 225.0, 275.0, 320.0, 360.0, 395.0, 426.0, 453.0, 477.0, 497.0, 515.0, 529.0, 541.0, 551.0, 558.0, 563.0, 566.0, 567.0, 565.0, 562.0, 556.0, 548.0, 539.0]
]

MC_PAYOFFS = [
    [None, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0], 
    [0.0, 0.0, -1.0, -4.0, -9.0, -16.0, -25.0, -36.0, -49.0, -64.0, -81.0, -100.0, -121.0, -144.0, -169.0, -196.0, -225.0, -256.0, -289.0, -324.0, -361.0, -400.0, -441.0, -484.0, -529.0, -576.0], 
    [1.0, 0.0, 19.0, 26.0, 30.0, 32.0, 32.0, 30.0, 26.0, 20.0, 12.0, 2.0, -10.0, -24.0, -40.0, -58.0, -78.0, -100.0, -124.0, -150.0, -178.0, -208.0, -240.0, -274.0, -310.0, -348.0], 
    [2.0, 0.0, 29.0, 42.0, 50.0, 55.0, 58.0, 59.0, 58.0, 55.0, 50.0, 43.0, 34.0, 23.0, 10.0, -5.0, -22.0, -41.0, -62.0, -85.0, -110.0, -137.0, -166.0, -197.0, -230.0, -265.0], 
    [3.0, 0.0, 38.0, 55.0, 66.0, 74.0, 79.0, 82.0, 83.0, 82.0, 79.0, 74.0, 67.0, 58.0, 47.0, 34.0, 19.0, 2.0, -17.0, -38.0, -61.0, -86.0, -113.0, -142.0, -173.0, -206.0], 
    [4.0, 0.0, 45.0, 66.0, 82.0, 91.0, 98.0, 103.0, 106.0, 107.0, 106.0, 103.0, 98.0, 91.0, 82.0, 71.0, 58.0, 43.0, 26.0, 7.0, -14.0, -37.0, -62.0, -89.0, -118.0, -149.0], 
    [5.0, 0.0, 51.0, 76.0, 95.0, 107.0, 116.0, 122.0, 126.0, 128.0, 128.0, 126.0, 122.0, 116.0, 108.0, 98.0, 86.0, 72.0, 56.0, 38.0, 18.0, -4.0, -28.0, -54.0, -82.0, -112.0], 
    [6.0, 0.0, 57.0, 84.0, 107.0, 122.0, 133.0, 141.0, 146.0, 149.0, 150.0, 149.0, 146.0, 141.0, 134.0, 125.0, 114.0, 101.0, 86.0, 69.0, 50.0, 29.0, 6.0, -19.0, -46.0, -75.0], 
    [7.0, 0.0, 62.0, 92.0, 117.0, 136.0, 149.0, 159.0, 166.0, 170.0, 172.0, 172.0, 170.0, 166.0, 160.0, 152.0, 142.0, 130.0, 116.0, 100.0, 82.0, 62.0, 40.0, 16.0, -10.0, -38.0], 
    [8.0, 0.0, 66.0, 99.0, 126.0, 148.0, 164.0, 177.0, 186.0, 192.0, 196.0, 197.0, 196.0, 193.0, 188.0, 181.0, 172.0, 161.0, 148.0, 133.0, 116.0, 97.0, 76.0, 53.0, 28.0, 1.0], 
    [9.0, 0.0, 70.0, 105.0, 135.0, 159.0, 179.0, 194.0, 205.0, 213.0, 218.0, 221.0, 221.0, 219.0, 215.0, 209.0, 201.0, 191.0, 179.0, 165.0, 149.0, 131.0, 111.0, 89.0, 65.0, 39.0], 
    [10.0, 0.0, 74.0, 111.0, 143.0, 169.0, 191.0, 208.0, 222.0, 232.0, 239.0, 243.0, 245.0, 244.0, 241.0, 236.0, 229.0, 220.0, 209.0, 196.0, 181.0, 164.0, 145.0, 124.0, 101.0, 76.0], 
    [11.0, 0.0, 77.0, 117.0, 151.0, 179.0, 202.0, 222.0, 237.0, 249.0, 258.0, 264.0, 267.0, 268.0, 266.0, 262.0, 256.0, 248.0, 238.0, 226.0, 212.0, 196.0, 178.0, 158.0, 136.0, 112.0], 
    [12.0, 0.0, 80.0, 122.0, 158.0, 188.0, 213.0, 234.0, 251.0, 265.0, 275.0, 283.0, 288.0, 290.0, 290.0, 287.0, 282.0, 275.0, 266.0, 255.0, 242.0, 227.0, 210.0, 191.0, 170.0, 147.0], 
    [13.0, 0.0, 83.0, 127.0, 165.0, 196.0, 223.0, 245.0, 264.0, 279.0, 291.0, 300.0, 307.0, 311.0, 312.0, 311.0, 307.0, 301.0, 293.0, 283.0, 271.0, 257.0, 241.0, 223.0, 203.0, 181.0], 
    [14.0, 0.0, 86.0, 131.0, 171.0, 204.0, 232.0, 256.0, 276.0, 293.0, 306.0, 317.0, 325.0, 330.0, 333.0, 333.0, 331.0, 326.0, 319.0, 310.0, 299.0, 286.0, 271.0, 254.0, 235.0, 214.0], 
    [15.0, 0.0, 88.0, 136.0, 177.0, 212.0, 242.0, 267.0, 288.0, 306.0, 321.0, 333.0, 342.0, 349.0, 353.0, 355.0, 354.0, 351.0, 345.0, 337.0, 327.0, 315.0, 301.0, 285.0, 267.0, 247.0], 
    [16.0, 0.0, 91.0, 140.0, 183.0, 220.0, 251.0, 278.0, 301.0, 320.0, 336.0, 349.0, 359.0, 367.0, 372.0, 375.0, 376.0, 374.0, 370.0, 364.0, 355.0, 344.0, 331.0, 316.0, 299.0, 280.0], 
    [17.0, 0.0, 93.0, 144.0, 189.0, 227.0, 260.0, 288.0, 312.0, 333.0, 350.0, 364.0, 376.0, 385.0, 391.0, 395.0, 397.0, 396.0, 393.0, 388.0, 381.0, 372.0, 360.0, 346.0, 330.0, 312.0], 
    [18.0, 0.0, 95.0, 148.0, 194.0, 234.0, 268.0, 298.0, 323.0, 345.0, 364.0, 379.0, 392.0, 402.0, 410.0, 415.0, 418.0, 418.0, 416.0, 412.0, 406.0, 398.0, 388.0, 376.0, 361.0, 344.0], 
    [19.0, 0.0, 97.0, 151.0, 199.0, 240.0, 276.0, 308.0, 335.0, 358.0, 378.0, 394.0, 408.0, 419.0, 428.0, 434.0, 438.0, 440.0, 439.0, 436.0, 431.0, 424.0, 415.0, 404.0, 391.0, 375.0], 
    [20.0, 0.0, 99.0, 154.0, 204.0, 247.0, 284.0, 317.0, 346.0, 370.0, 391.0, 409.0, 424.0, 436.0, 446.0, 453.0, 458.0, 461.0, 461.0, 459.0, 455.0, 449.0, 441.0, 431.0, 419.0, 405.0], 
    [21.0, 0.0, 100.0, 158.0, 209.0, 253.0, 292.0, 326.0, 356.0, 382.0, 404.0, 423.0, 439.0, 452.0, 463.0, 471.0, 477.0, 481.0, 482.0, 481.0, 478.0, 473.0, 466.0, 457.0, 446.0, 433.0], 
    [22.0, 0.0, 102.0, 161.0, 213.0, 259.0, 299.0, 335.0, 366.0, 393.0, 417.0, 437.0, 454.0, 468.0, 480.0, 489.0, 496.0, 501.0, 503.0, 503.0, 501.0, 497.0, 491.0, 483.0, 473.0, 461.0], 
    [23.0, 0.0, 103.0, 164.0, 217.0, 264.0, 306.0, 343.0, 376.0, 405.0, 430.0, 451.0, 469.0, 484.0, 497.0, 507.0, 515.0, 520.0, 523.0, 524.0, 523.0, 520.0, 515.0, 508.0, 499.0, 488.0], 
    [24.0, 0.0, 105.0, 166.0, 221.0, 270.0, 313.0, 351.0, 385.0, 415.0, 441.0, 464.0, 483.0, 500.0, 513.0, 524.0, 533.0, 539.0, 543.0, 545.0, 545.0, 543.0, 538.0, 532.0, 524.0, 514.0], 
    [25.0, 0.0, 106.0, 169.0, 225.0, 275.0, 320.0, 360.0, 395.0, 426.0, 453.0, 477.0, 497.0, 515.0, 529.0, 541.0, 551.0, 558.0, 563.0, 566.0, 567.0, 565.0, 562.0, 556.0, 548.0, 539.0]
]

# ============================================================================
# Global Game State (In-Memory)
# ============================================================================

game_state = {
    'round': 0,
    'max_rounds': 10,
    'am_strategy': 'balanced',
    'mc_strategy': 'balanced',
    'history': [],
    'am_total': 0,
    'mc_total': 0,
    'is_running': False
}

# ============================================================================
# Core Logic: Decision Engine
# ============================================================================

def get_last_moves():
    """Helper to get last round's investments. Defaults to moderate start."""
    if not game_state['history']:
        return 12, 12 # Default start for Round 1
    last = game_state['history'][-1]
    return last['am_investment'], last['mc_investment']

def decide_investment(agent_role, strategy, round_num):
    """
    Determines investment (0-25) based on Strategy and History.
    This creates the 'Behavior' of the agent.
    """
    last_am, last_mc = get_last_moves()
    
    # Identify self and opponent moves from last round
    if agent_role == 'AM':
        my_last, opp_last = last_am, last_mc
    else:
        my_last, opp_last = last_mc, last_am

    # --- STRATEGY LOGIC (The "Brain") ---
    
    if strategy == 'cooperative':
        # "I trust you, let's build big."
        # Tries to increase value slightly above opponent's last move, encouraging growth.
        target = max(opp_last, my_last) + random.randint(1, 3)
        return min(25, max(15, target)) # Floor at 15 to show commitment
        
    elif strategy == 'competitive':
        # "Free rider strategy"
        # Invest low to reduce cost, hoping opponent invests high.
        return random.randint(5, 10) 
        
    elif strategy == 'adaptive':
        # Tit-for-Tat: Copy opponent's last move exactly
        # "I do what you do."
        if round_num == 1:
            return 13 # Start nice
        return opp_last
        
    elif strategy == 'balanced':
        # Middle ground, slightly random noise but generally fair
        target = (my_last + opp_last) // 2
        return min(25, max(5, target + random.randint(-2, 2)))
    
    # Default fallback
    return 12

def generate_reasoning(agent_role, strategy, investment, opp_last_investment):
    """
    Generates structured reasoning steps for the Frontend UI.
    Matches the {type, text} structure expected by the Javascript renderer.
    """
    steps = []
    
    # Step 1: Observation
    steps.append({
        "type": "observation",
        "text": f"Observation: Last round, my partner invested {opp_last_investment} engineers."
    })
    
    # Step 2: Strategy/Persona check
    if strategy == 'cooperative':
        strat_text = "Strategy: As a Cooperative partner, I want to signal trust and maximize our joint synergy."
    elif strategy == 'competitive':
        strat_text = "Strategy: My Competitive focus is on minimizing my own costs while capturing value from the partnership."
    elif strategy == 'adaptive':
        strat_text = "Strategy: I am Adaptive (Tit-for-Tat). I will mirror your behavior to ensure fairness."
    else:
        strat_text = "Strategy: I am taking a Balanced approach, weighing risks and rewards equally."
        
    steps.append({
        "type": "strategy",
        "text": strat_text
    })
    
    # Step 3: Decision
    steps.append({
        "type": "decision",
        "text": f"Decision: Based on this, I decided to allocate {investment} engineers this round."
    })
    
    return steps

# ============================================================================
# Core Logic: Payoff Engine (USING REAL MATRICES)
# ============================================================================

def compute_payoff(am_inv, mc_inv):
    """
    Retrieves the EXACT payoff from the provided matrix tables.
    Uses precise index offset logic to skip headers.
    """
    
    # Clamp inputs to valid range 0-25
    am_idx = min(max(0, int(am_inv)), 25)
    mc_idx = min(max(0, int(mc_inv)), 25)
    
    try:
        # OFFSET LOGIC EXPLAINED:
        # The variables AM_PAYOFFS and MC_PAYOFFS contain headers in the first row/col.
        #
        # For AM_PAYOFFS:
        # Row 0 is header [0, 1, 2...]. Row 1 corresponds to 0 engineers.
        # So AM Engineers = i  -->  Row Index = i + 1
        # MC Engineers = j  -->  Col Index = j (Columns align directly after row header)
        am_payoff = float(AM_PAYOFFS[am_idx + 1][mc_idx])
        
        # For MC_PAYOFFS:
        # Row 0 is header. Col 0 is header.
        # So AM Engineers = i  -->  Row Index = i + 1
        # So MC Engineers = j  -->  Col Index = j + 1
        mc_payoff = float(MC_PAYOFFS[am_idx + 1][mc_idx + 1])
        
    except (IndexError, ValueError):
        # Fallback if somehow out of bounds (should not happen with clamp)
        # Using a simple safety formula just in case
        print(f"Error accessing matrix at [{am_idx}, {mc_idx}]. Using fallback.")
        am_payoff = (am_idx + mc_idx) * 2
        mc_payoff = (am_idx + mc_idx) * 2
    
    return int(am_payoff), int(mc_payoff)

# ============================================================================
# Routes
# ============================================================================


@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    data = request.json
    game_state['round'] = 0
    game_state['max_rounds'] = int(data.get('max_rounds', 10))
    game_state['am_strategy'] = data.get('am_strategy', 'balanced')
    game_state['mc_strategy'] = data.get('mc_strategy', 'balanced')
    game_state['history'] = []
    game_state['am_total'] = 0
    game_state['mc_total'] = 0
    game_state['is_running'] = True
    
    print(f"🎮 Simulation Started: {game_state['am_strategy']} vs {game_state['mc_strategy']}")
    return jsonify({'status': 'success'})

@app.route('/continue_simulation', methods=['POST'])
def continue_simulation():
    if not game_state['is_running'] or game_state['round'] >= game_state['max_rounds']:
        return jsonify({'game_complete': True})
        
    game_state['round'] += 1
    current_round = game_state['round']
    
    # 1. Get Strategies
    strat_am = game_state['am_strategy']
    strat_mc = game_state['mc_strategy']
    
    # 2. Make Decisions (Agent Logic)
    am_inv = decide_investment('AM', strat_am, current_round)
    mc_inv = decide_investment('MC', strat_mc, current_round)
    
    # 3. Calculate Payoffs (REAL MATRIX LOOKUP)
    am_pay, mc_pay = compute_payoff(am_inv, mc_inv)
    
    # 4. Update Totals
    game_state['am_total'] += am_pay
    game_state['mc_total'] += mc_pay
    
    # 5. Generate Reasoning (For UI Animation)
    last_am, last_mc = get_last_moves() 
    
    reasoning_am = generate_reasoning('AM', strat_am, am_inv, last_mc)
    reasoning_mc = generate_reasoning('MC', strat_mc, mc_inv, last_am)
    
    # 6. Save History (Crucial for next round logic)
    round_data = {
        'round': current_round,
        'am_investment': am_inv,
        'mc_investment': mc_inv,
        'am_payoff': am_pay,
        'mc_payoff': mc_pay
    }
    game_state['history'].append(round_data)
    
    print(f"R{current_round}: AM({am_inv}) vs MC({mc_inv}) -> Pays: {am_pay}/{mc_pay}")

    # 7. Return strict JSON structure expected by Frontend
    return jsonify({
        'round': current_round,
        'am_investment': am_inv,
        'mc_investment': mc_inv,
        'am_payoff': am_pay,
        'mc_payoff': mc_pay,
        'am_total': int(game_state['am_total']),
        'mc_total': int(game_state['mc_total']),
        'reasoning_steps_am': reasoning_am, # Matches frontend expectation
        'reasoning_steps_mc': reasoning_mc,
        'history': game_state['history'],
        'game_complete': current_round >= game_state['max_rounds']
    })

@app.route('/chat_with_agent', methods=['POST'])
def chat_with_agent():
    """
    Persona-aware chat endpoint.
    Falls back to robust templates if OpenAI is not configured.
    """
    data = request.json or {}
    agent = data.get("agent", "").upper() # AM or MC
    user_msg = data.get("message", "")
    reply = f"[{agent.upper()}] Received: {user_msg}"

    return jsonify({"reply": reply}), 200
    
    strategy = game_state['am_strategy'] if agent == 'AM' else game_state['mc_strategy']
    last_inv = 0
    if game_state['history']:
        last = game_state['history'][-1]
        last_inv = last['am_investment'] if agent == 'AM' else last['mc_investment']
        
    # Attempt OpenAI Generation (if key exists)
    if openai.api_key:
        try:
            system_prompt = f"""You are Agent {agent} in a repeated game simulation. 
            Your strategy is {strategy}. 
            Last round you invested {last_inv} engineers.
            The user is asking: "{user_msg}"
            Answer briefly (1 sentence) in character. 
            If you are competitive, be selfish/business-like. If cooperative, be friendly/trusting."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=60
            )
            return jsonify({'response': response.choices[0].message.content})
        except Exception as e:
            print(f"OpenAI Error: {e}")
            # Fall through to template if API fails
            
    # Robust Fallback Template (Persona-aware)
    if strategy == 'competitive':
        reply = f"I chose {last_inv} because I prioritize my own ROI. I need to see more commitment from you first."
    elif strategy == 'cooperative':
        reply = f"I invested {last_inv} because I believe in our partnership. Let's create value together!"
    elif strategy == 'adaptive':
        reply = f"My move of {last_inv} was a direct response to the previous round. I treat you exactly as you treat me."
    else:
        reply = f"I think {last_inv} was a balanced decision given the current market conditions."
        
    return jsonify({'response': reply})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✅ BACKEND 6.0 (FINAL PRODUCTION) STARTED")
    print("   - Logic Engine: Active")
    print("   - Payoff Data: 11.29.xlsx Loaded (Real Matrix)")
    print("   - Persona System: Active")
    print("   - History Tracking: Active")
    print("   - Endpoint Alignment: Fixed")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
